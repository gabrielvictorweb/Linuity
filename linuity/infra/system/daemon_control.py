import subprocess


class DaemonControl:
    @staticmethod
    def restart():
        print("[ + ] Applying configuration to device...")

        subprocess.run(["sudo", "systemctl", "restart", "linuity.service"])

        print("[ ✔ ] Configuration applied successfully")

    @staticmethod
    def disable():
        print("[ + ] Disabling daemon service...")

        subprocess.run(["sudo", "systemctl", "disable", "--now", "linuity.service"])

        print("[ ✔ ] Daemon service disabled")
