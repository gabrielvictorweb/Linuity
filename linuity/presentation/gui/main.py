import logging
import subprocess
import threading
from importlib import resources
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as pkg_version
from subprocess import CalledProcessError

from linuity.infra.update_checker import check_for_update
from linuity.presentation.gui.gui_controller import (
    MODE_PARAMS,
    MODES,
    PARAM_SPECS,
    GUIController,
    matches_preset,
)

logger = logging.getLogger(__name__)

GITHUB_URL = "https://github.com/gabrielvictorweb/linuity"


def _app_version():
    try:
        return pkg_version("linuity")
    except PackageNotFoundError:
        return "dev"


def launch_gui():
    try:
        import gi

        gi.require_version("Gtk", "4.0")
        from gi.repository import Gtk  # noqa: F401
    except (ImportError, ValueError):
        logger.error(
            "PyGObject/GTK4 not found. Install with: "
            "sudo apt install python3-gi gir1.2-gtk-4.0 "
            "(or: pip install linuity[gui])"
        )
        return 1

    app = _build_app()
    return app.run(None)


def _build_app():
    from gi.repository import Gtk

    class LinuityWindow(Gtk.ApplicationWindow):
        def __init__(self, app):
            super().__init__(application=app, title="Linuity")
            self.controller = GUIController()
            self.set_default_size(420, -1)
            self._log_stop = threading.Event()
            self.connect("destroy", self._stop_log_stream)

            root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            self.set_child(root)

            # header fixed above the stack — visible on all pages
            header_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            header_box.set_margin_top(16)
            header_box.set_margin_start(16)
            header_box.set_margin_end(16)
            header_box.append(self._build_header())
            header_box.append(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))
            root.append(header_box)

            stack = Gtk.Stack()
            stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)

            switcher = Gtk.StackSwitcher()
            switcher.set_stack(stack)
            switcher.set_halign(Gtk.Align.CENTER)
            switcher.set_margin_top(12)
            switcher.set_margin_bottom(12)

            root.append(switcher)
            root.append(stack)

            # --- Controls page ---
            controls = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
            controls.set_margin_top(4)
            controls.set_margin_bottom(16)
            controls.set_margin_start(16)
            controls.set_margin_end(16)
            stack.add_titled(controls, "controls", "Controls")

            self._mode_dropdown = Gtk.DropDown.new_from_strings(MODES)
            self._mode_dropdown.connect("notify::selected", self._on_mode_changed)
            controls.append(self._labeled_row("Mode", self._mode_dropdown))

            self._param_rows = {}
            self._param_widgets = {}
            for param, (label, kind, lo, hi, step, default) in PARAM_SPECS.items():
                widget = self._build_param_widget(kind, lo, hi, step, default)
                row = self._labeled_row(label, widget)
                self._param_rows[param] = row
                self._param_widgets[param] = (kind, widget)
                if kind == "switch":
                    widget.connect("notify::active", self._on_param_changed)
                else:
                    widget.connect("value-changed", self._on_param_changed)
                controls.append(row)

            buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            self._apply_btn = Gtk.Button(label="Apply")
            self._apply_btn.add_css_class("suggested-action")
            self._apply_btn.connect("clicked", self._on_apply)
            self._off_btn = Gtk.Button(label="Turn Off")
            self._off_btn.add_css_class("destructive-action")
            self._off_btn.connect("clicked", self._on_turn_off)
            self._spinner = Gtk.Spinner()
            self._spinner.set_visible(False)
            buttons.append(self._apply_btn)
            buttons.append(self._off_btn)
            buttons.append(self._spinner)
            controls.append(buttons)

            self._status_label = Gtk.Label(label="")
            self._status_label.set_xalign(0)
            controls.append(self._status_label)

            self._update_label = Gtk.Label(label="")
            self._update_label.set_xalign(0)
            self._update_label.set_visible(False)
            controls.append(self._update_label)

            # --- Logs page ---
            logs = self._build_logs_page()
            stack.add_titled(logs, "logs", "Logs")

            self._preset = {}
            self._load_current_preset()
            self._on_mode_changed(self._mode_dropdown, None)
            self._check_for_update_async()
            self._start_log_stream()

        def _check_for_update_async(self):
            from gi.repository import GLib

            def worker():
                latest = check_for_update(_app_version())
                if latest:
                    GLib.idle_add(self._show_update_notice, latest)

            threading.Thread(target=worker, daemon=True).start()

        def _show_update_notice(self, latest):
            self._update_label.set_markup(
                f"⬆ New version <b>v{latest}</b> available — "
                f'<a href="{GITHUB_URL}/releases">update on GitHub</a>'
            )
            self._update_label.set_visible(True)
            return False

        def _build_header(self):
            header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)

            icon_path = resources.files("linuity").joinpath("resources/linuity.png")
            logo = Gtk.Image.new_from_file(str(icon_path))
            logo.set_pixel_size(56)
            header.append(logo)

            titles = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            titles.set_valign(Gtk.Align.CENTER)
            title = Gtk.Label()
            title.set_markup("<b>Linuity</b>")
            title.set_xalign(0)
            subtitle = Gtk.Label(label=f"v{_app_version()} — HyperX LED Controller")
            subtitle.set_xalign(0)
            subtitle.add_css_class("dim-label")
            titles.append(title)
            titles.append(subtitle)
            header.append(titles)

            link = Gtk.LinkButton.new_with_label(GITHUB_URL, "GitHub")
            link.set_halign(Gtk.Align.END)
            link.set_valign(Gtk.Align.CENTER)
            link.set_hexpand(True)
            header.append(link)

            return header

        def _labeled_row(self, text, widget):
            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            label = Gtk.Label(label=text)
            label.set_xalign(0)
            label.set_size_request(120, -1)
            widget.set_hexpand(True)
            row.append(label)
            row.append(widget)
            return row

        def _build_param_widget(self, kind, lo, hi, step, default):
            if kind == "scale":
                widget = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, lo, hi, step)
                widget.set_value(default)
                widget.set_draw_value(True)
                return widget
            if kind == "spin":
                widget = Gtk.SpinButton.new_with_range(lo, hi, step)
                widget.set_digits(2 if isinstance(step, float) else 0)
                widget.set_value(default)
                return widget
            switch = Gtk.Switch()
            switch.set_active(default)
            switch.set_halign(Gtk.Align.START)
            switch.set_hexpand(False)
            return switch

        def _selected_mode(self):
            return MODES[self._mode_dropdown.get_selected()]

        def _on_mode_changed(self, dropdown, _param):
            visible = MODE_PARAMS[self._selected_mode()]
            for param, row in self._param_rows.items():
                row.set_visible(param in visible)
            self._sync_apply_button()

        def _on_param_changed(self, _widget, *_args):
            self._sync_apply_button()

        def _widget_value(self, param):
            kind, widget = self._param_widgets[param]
            if kind == "switch":
                return widget.get_active()
            value = widget.get_value()
            return value if param in ("interval", "speed") else int(value)

        def _collect_values(self):
            visible = MODE_PARAMS[self._selected_mode()]
            return {param: self._widget_value(param) for param in visible}

        def _sync_apply_button(self):
            mode = self._selected_mode()
            if matches_preset(self._preset, mode, self._collect_values()):
                self._apply_btn.set_label("Already applied")
                self._apply_btn.set_sensitive(False)
            else:
                self._apply_btn.set_label("Apply")
                self._apply_btn.set_sensitive(True)

        def _set_busy(self, busy):
            self._apply_btn.set_sensitive(not busy)
            self._off_btn.set_sensitive(not busy)
            self._spinner.set_visible(busy)
            if busy:
                self._spinner.start()
                self._status_label.set_text("Applying…")
            else:
                self._spinner.stop()

        def _on_apply(self, _button):
            mode = self._selected_mode()
            values = self._collect_values()
            kwargs = {
                "min_val" if key == "min" else "max_val" if key == "max" else key: value
                for key, value in values.items()
            }
            self._set_busy(True)
            threading.Thread(target=self._do_apply, args=(mode, kwargs), daemon=True).start()

        def _do_apply(self, mode, kwargs):
            from gi.repository import GLib
            try:
                self.controller.apply(mode, **kwargs)
                GLib.idle_add(self._on_apply_done, mode, None)
            except (ValueError, CalledProcessError) as e:
                GLib.idle_add(self._on_apply_done, mode, str(e))

        def _on_apply_done(self, mode, error):
            self._set_busy(False)
            if error:
                self._show_error(error)
            else:
                self._status_label.set_text(f"Applied: {mode}")
                self._preset = self.controller.load_preset()
                self._sync_apply_button()
            return False

        def _on_turn_off(self, _button):
            self._set_busy(True)
            threading.Thread(target=self._do_turn_off, daemon=True).start()

        def _do_turn_off(self):
            from gi.repository import GLib
            try:
                self.controller.turn_off()
                GLib.idle_add(self._on_turn_off_done, None)
            except CalledProcessError as e:
                GLib.idle_add(self._on_turn_off_done, str(e))

        def _on_turn_off_done(self, error):
            self._set_busy(False)
            if error:
                self._show_error(error)
            else:
                self._status_label.set_text("Daemon disabled")
                # daemon is off — re-applying the same preset is meaningful
                self._preset = {}
                self._sync_apply_button()
            return False

        def _show_error(self, message):
            dialog = Gtk.AlertDialog()
            dialog.set_message("Error")
            dialog.set_detail(message)
            dialog.show(self)

        def _load_current_preset(self):
            self._preset = self.controller.load_preset()
            mode = self._preset.get("mode")
            if mode in MODES:
                self._mode_dropdown.set_selected(MODES.index(mode))
            for param, (kind, widget) in self._param_widgets.items():
                raw = self._preset.get(param)
                if raw is None:
                    continue
                if kind == "switch":
                    widget.set_active(raw == "true")
                else:
                    widget.set_value(float(raw))
            if mode:
                self._status_label.set_text(f"Current preset: {mode}")
            self._sync_apply_button()

        def _build_logs_page(self):
            scroll = Gtk.ScrolledWindow()
            scroll.set_vexpand(True)
            scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

            self._log_view = Gtk.TextView()
            self._log_view.set_editable(False)
            self._log_view.set_cursor_visible(False)
            self._log_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
            self._log_view.add_css_class("monospace")
            self._log_view.set_margin_top(8)
            self._log_view.set_margin_bottom(8)
            self._log_view.set_margin_start(8)
            self._log_view.set_margin_end(8)

            scroll.set_child(self._log_view)
            return scroll

        def _start_log_stream(self):
            try:
                proc = subprocess.Popen(
                    [
                        "journalctl", "-u", "linuity.service",
                        "-f", "-n", "30", "--no-pager", "--output=short",
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                )
            except FileNotFoundError:
                return
            self._log_proc = proc
            threading.Thread(target=self._log_worker, args=(proc,), daemon=True).start()

        def _log_worker(self, proc):
            from gi.repository import GLib
            for line in proc.stdout:
                if self._log_stop.is_set():
                    break
                GLib.idle_add(self._append_log, line.rstrip())
            proc.stdout.close()

        def _append_log(self, line):
            buf = self._log_view.get_buffer()
            buf.insert(buf.get_end_iter(), line + "\n")
            vadj = self._log_view.get_parent().get_vadjustment()
            at_bottom = vadj.get_value() >= vadj.get_upper() - vadj.get_page_size() - 1
            if at_bottom:
                self._log_view.scroll_to_mark(buf.get_insert(), 0, False, 0, 0)
            return False

        def _stop_log_stream(self, *_):
            self._log_stop.set()
            if hasattr(self, "_log_proc"):
                self._log_proc.terminate()

    class LinuityApp(Gtk.Application):
        def __init__(self):
            super().__init__(application_id="dev.linuity.gui")

        def do_activate(self):
            window = self.props.active_window or LinuityWindow(self)
            window.present()

    return LinuityApp()
