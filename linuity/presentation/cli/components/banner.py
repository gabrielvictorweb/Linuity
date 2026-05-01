def show(version: str):
    SOFT_RED = "\033[38;5;203m"
    GREEN = "\033[1;32m"
    GRAY = "\033[1;30m"
    CYAN = "\033[1;36m"
    RESET = "\033[0m"

    print(f"""{SOFT_RED}
██╗     ██╗███╗   ██╗██╗   ██╗██╗████████╗██╗   ██╗
██║     ██║████╗  ██║██║   ██║██║╚══██╔══╝╚██╗ ██╔╝
██║     ██║██╔██╗ ██║██║   ██║██║   ██║    ╚████╔╝ 
██║     ██║██║╚██╗██║██║   ██║██║   ██║     ╚██╔╝  
███████╗██║██║ ╚████║╚██████╔╝██║   ██║      ██║   
╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝   ╚═╝      ╚═╝   
{RESET}
{GRAY}──────────────────────────────────────────────{RESET}
  HyperX LED Controller for Linux

  {CYAN}> Version:{RESET}  {version}
  {GREEN}> Author:{RESET}   Gabriel Victor
  {GREEN}> GitHub:{RESET}   https://github.com/gabrielvictorweb/linuity
{GRAY}──────────────────────────────────────────────{RESET}
""")
