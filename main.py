import subprocess
import os

def runPowerShell(cmd):
    try:
        result = subprocess.run(
            ["powershell", "-Command", cmd],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("PowerShell Error:", e)
        return ""

def writeToFile(path, data):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            '''
                # If write all to one file
                with open(path, 'a', encoding='utf-8') as f:
                    f.write(f"--------------------------------------\n")
                    f.write(data)
                    f.write("\n\n\n\n")
            '''
            
            f.write(data)
        print(f"Written OK: {path}")
    except Exception as e:
        print(f"Write error: {e}")

def readFromFile(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def createFolderIfNotExists(folder_path):
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Created folder: {folder_path}")
        else:
            print(f"Folder exists: {folder_path}")
    except Exception as e:
        print(f"Error creating folder: {e}")

if __name__ == "__main__":
    
    # --- Get username from whoami ---
    whoami_output = runPowerShell("whoami")  # example: desktop-12345\huy
    user_folder_name = whoami_output.replace("\\", "_")
    
    baseFolder = r"\\QH-DESKTOP\CheckDeviceInfo"
    userFolder = os.path.join(baseFolder, user_folder_name)

    # --- Create folder for this user ---
    createFolderIfNotExists(userFolder)

    # PowerShell commands
    command_powershell = {
        "cpu": "Get-CimInstance Win32_Processor | Select-Object Name",
        "mainboard": "Get-CimInstance Win32_BaseBoard | Select-Object Product, Manufacturer",
        "ram": "Get-WmiObject Win32_PhysicalMemory | Select-Object Manufacturer, @{Name='GB';Expression={$_.Capacity/1GB}}, Speed, SerialNumber",
        "disk": "Get-PhysicalDisk | Select-Object DeviceId, Model, MediaType, @{Name='GB';Expression={$_.Size/1GB}}, HealthStatus, SerialNumber",
        "gpu": "Get-CimInstance Win32_VideoController | Select-Object Name, Description, @{Name='VRAM';Expression={$_.AdapterRAM/1GB}}",
    }

    # --- Write each component's info ---
    for component, command in command_powershell.items():
        
        result = runPowerShell(command)

        # If write all to one file
        # filepath = os.path.join(userFolder, f"device_info.txt")
        filepath = os.path.join(userFolder, f"{component}_info.txt")

        writeToFile(filepath, result)

        print("----- File Content -----")
        print(readFromFile(filepath))
        print("------------------------")
