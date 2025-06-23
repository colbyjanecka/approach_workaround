# Approach Workaround

this fixes an issue (feature) with the approach gym management system where a separate computer has to be set up for the qr code scanner. when the scanner acts as a keyboard in a textbox it cannot detect and scan someone in. unfortunately this solution is pretty invasive - you will be tabbed into another window (safari) every time a user tries to check in with the scanner. made for mosaic boulders

install: download [approach_workaround](approach_workaround). open (right click then select open) - then grant necessary permissions.

in order to work:

1. scanner must be plugged in
2. scanner must be set up in serial usb mode (see your scanner's user guide)
3. safari must be open (not minimized). you must be logged into the approach app and on the dashboard (not in any textboxes)
   a. you can use chrome or another browser to open/use approach as normal

this solution was only made to work for apple devices. if you want to change the browser that the program tabs into, download the repository, create a virtual environment (`python -m venv .env`; `source .env/bin/activate`) and install dependencies (`pip install -r requirements.txt`), change the `alt_browser` variable, then rebuild the app using `pyinstaller --onefile main.py`
