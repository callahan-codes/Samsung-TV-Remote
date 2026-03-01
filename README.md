To generate a single executable on your Windows machine, run the command below in the /src directory:

    python -m PyInstaller --onefile --name "TV_Remote" src/main.py

Make sure to replace the following variables found in main.py with the correct information:

    TV_IP = "127.0.0.1" # replace with your TV's IP address
    TV_MAC = "A0:B1:C2:D3:67:67" # replace with your TV's MAC address