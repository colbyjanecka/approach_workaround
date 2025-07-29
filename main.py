import serial
import serial.tools.list_ports
import subprocess
import shlex
import time

alt_browser = "Safari"
url = "https://benchmark.kiosk.approach.app/barcode-checkin"

def find_scanner_port():
    """Auto-detect USB serial scanner port."""
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if 'usb' in port.device.lower() or 'tty.' in port.device.lower():
            print(f"found scanner port {port.device}")
            return port.device
    print("could not auto-detect scanner port")
    return None

def get_front_app_name():
    result = subprocess.run([
        "osascript", "-e",
        'tell application "System Events" to get name of first application process whose frontmost is true'
    ], capture_output=True, text=True)
    return result.stdout.strip()

def switch_to_app(app_name):
    script = f'''
    tell application "System Events"
        set frontmost of application process "{app_name}" to true
    end tell
    '''
    subprocess.run(['osascript', '-e', script])

def send_string_applescript(text):
    safe_text = text.replace('"', '\\"')
    script = f'''
    tell application "System Events"
        keystroke "{safe_text}"
        key code 36 -- press Enter
    end tell
    '''
    subprocess.run(["osascript", "-e", script])

def handle_scan(scan_text):
    previous_app = get_front_app_name()
    print(f"switching from '{previous_app}' to {alt_browser}...")
    switch_to_app(alt_browser)
    time.sleep(0.5)
    send_string_applescript(scan_text)
    time.sleep(0.2)
    print(f"returning to '{previous_app}'...")
    switch_to_app(previous_app)

def main():
    port = find_scanner_port()
    if not port:
        print("please plug in your scanner in USB Serial mode, and relaunch.")
        return

    print("Scanner Detected.  Opening Approach Checkin Page")
    cmd = f"open -a Safari {url}"
    cmd_parts = shlex.split(cmd)

    subprocess.run(cmd_parts)

    try:
        with serial.Serial(port, baudrate=9600, timeout=1) as ser:
            print(f"listening on {port}...")
            while True:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    print(f"scanned: {line}")
                    handle_scan(line)
    except serial.SerialException as e:
        print(f"serial error: {e}")

if __name__ == "__main__":
    main()
