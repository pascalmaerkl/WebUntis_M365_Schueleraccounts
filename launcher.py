import multiprocessing
import os
import sys


def app_path() -> str:
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, "app.py")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")


if __name__ == "__main__":
    multiprocessing.freeze_support()

    from streamlit.web import cli as stcli

    sys.argv = [
        "streamlit",
        "run",
        app_path(),
        "--global.developmentMode",
        "false",
        "--server.headless",
        "true",
        "--browser.gatherUsageStats",
        "false",
    ]
    sys.exit(stcli.main())
