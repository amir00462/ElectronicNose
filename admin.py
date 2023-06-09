import ctypes
import sys

def run_as_admin():
    if sys.platform.startswith('win'):
        try:
            # Windows-specific code
            path_to_script = sys.argv[0]
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, path_to_script, None, 1)
            sys.exit()
        except:
            # Handle error when user cancels the elevation prompt
            print("Script execution cancelled.")
            sys.exit(0)
    else:
        # Non-Windows platform
        print("Administrator privilege is required to run this script on your platform.")
        sys.exit(0)

# Call the function to run main.py as an administrator
if __name__ == '__main__':
    run_as_admin()