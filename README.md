# UAC-Bypass-ComputerDefaults

This script is a proof-of-concept demonstrating a registry hijacking technique to bypass UAC on Windows. It targets ComputerDefaults.exe, a high-integrity binary that auto-elevates, to execute a command with Administrator privileges without a prompt.

Mechanism
The bypass works by exploiting a search order vulnerability in the Windows Registry:

Payload Prep: The script copies cmd.exe to a temporary directory. This is a simple evasion tactic, as some security monitors flag system shells spawned directly by auto-elevating binaries.

Registry Hijack: It modifies HKCU\Software\Classes\ms-settings\Shell\Open\command. When ComputerDefaults.exe starts, it checks this user-controlled registry key to launch its interface.

Execution: By setting the default value to our payload and including a DelegateExecute string, the system executes our command at a high integrity level.

Cleanup: The script deletes the registry keys and the temporary file immediately after execution to minimize the footprint.

Instructions
Run the script from a standard terminal. Note that the user account must belong to the local Administrators group for the bypass to function.

Defensive Note
To prevent this type of hijack, set the Windows User Account Control (UAC) setting to Always Notify. This forces a prompt for all elevation requests, including those from built-in Windows binaries.

Disclaimer
This project is for educational purposes and authorized security auditing only. Using this against systems without prior consent is illegal.