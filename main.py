import serial
import serial.tools.list_ports
import subprocess

def find_scanner_port():
    """Auto-detect USB serial scanner port."""
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if 'usb' in port.device.lower() or 'tty.' in port.device.lower():
            print(f"Found scanner port: {port.device}")
            return port.device
    print("❌ Could not auto-detect scanner port.")
    return None

def send_keys_to_safari(text):
    # Escape quotes if needed
    text = text.replace('"', '\\"')

    applescript = f'''
    tell application "Safari"
        activate
        delay 0.2
        tell application "System Events"
            keystroke "{text}"
            key code 36 -- press Enter
        end tell
    end tell
    '''
    subprocess.run(['osascript', '-e', applescript])

def main():
    port = find_scanner_port()
    if not port:
        print("Please plug in your scanner in USB Serial mode.")
        return

    try:
        with serial.Serial(port, baudrate=9600, timeout=1) as ser:
            print(f"📡 Listening on {port}...")
            while True:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    print(f"Scanned: {line}")
                    send_keys_to_safari(line)
    except serial.SerialException as e:
        print(f"⚠️ Serial error: {e}")

if __name__ == "__main__":
    main()