import time
import os
import sys
from samsungtvws import SamsungTVWS
from wakeonlan import send_magic_packet
from pynput import keyboard

# configs
TV_IP = "10.0.0.245"
TV_MAC = "B0:F2:F6:C1:82:04"

# token
TOKEN_DIR = os.path.join(os.environ['APPDATA'], 'SamsungTVRemote')
if not os.path.exists(TOKEN_DIR):
    os.makedirs(TOKEN_DIR)
TOKEN_FILE = os.path.join(TOKEN_DIR, "tv_token.txt")

# connection
tv = SamsungTVWS(TV_IP, port=8002, token_file=TOKEN_FILE)

# turn on
def turn_on():
    print("\nTV is unreachable. Sending wake signal...")
    send_magic_packet(TV_MAC)
    print("Remote > ", end="", flush=True)

# remote
def remote(key):

    # combat input lag
    global last_press_time
    current_time = time.time()
    if current_time - last_press_time < 0.2:
        return
    last_press_time = current_time

    # key bindings
    try:
        valid_command = True
        if key == keyboard.Key.up:
            tv.shortcuts().up()
        elif key == keyboard.Key.down:
            tv.shortcuts().down()
        elif key == keyboard.Key.left:
            tv.shortcuts().left()
        elif key == keyboard.Key.right:
            tv.shortcuts().right()
        elif key == keyboard.Key.enter:
            tv.shortcuts().enter()
        elif key == keyboard.Key.backspace:
            tv.shortcuts().back()
        elif hasattr(key, 'char'):
            if key.char == 'h':
                tv.shortcuts().home()
            elif key.char == 'm':
                tv.shortcuts().menu()
            elif key.char == '-':
                tv.shortcuts().volume_down()
            elif key.char == '+':
                tv.shortcuts().volume_up()
            elif key.char == 'o':
                turn_on()
            elif key.char == 'p':
                tv.shortcuts().power()
                print("\nPowering off...")
                return False
            elif key.char == 'q':
                print("\nExiting...")
                return False
            else:
                valid_command = False
        else:
            valid_command = False

        if not valid_command:
            print(f"\rRemote > Invalid operator: {key}    ", end="")
        else:
            print(f"\rRemote > Last Action: {key}        ", end="")
        
        sys.stdout.flush()

    # basic error handle
    except Exception as e:
        # if tv is off but remote used, turn on
        if "10060" in str(e) or "timeout" in str(e).lower():
            turn_on()
        else:
            print(f"\nError: {e}")
            print("Remote > ", end="", flush=True)

# main
if __name__ == "__main__":
    last_press_time = 0
    print("--- Arrow Key Control Active ---")
    print("O: On | P: Off | Arrows: Move | Enter: Select | Backspace: Back | H: Home | M: Menu | Q: Quit")
    print("-" * 40)
    print("Remote > ", end="", flush=True)
    
    with keyboard.Listener(on_press=remote) as listener:
        listener.join()