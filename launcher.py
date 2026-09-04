import threading
import time
import sys
import os
import uvicorn
import webbrowser
import pystray
from PIL import Image, ImageDraw

def create_icon_image():
    # Generate a simple icon if we don't have one
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), color=(11, 17, 32))
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 4, height // 4, width * 3 // 4, height * 3 // 4),
        fill=(34, 211, 238) # aria-cyan
    )
    return image

class AriaLauncher:
    def __init__(self):
        self.server = None
        self.server_thread = None

    def start_server(self):
        # We run uvicorn programmatically
        from app.main import app
        config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="error")
        self.server = uvicorn.Server(config)
        self.server.run()

    def on_open(self, icon, item):
        webbrowser.open('http://127.0.0.1:8000')

    def on_exit(self, icon, item):
        icon.stop()
        if self.server:
            self.server.should_exit = True

    def run(self):
        # Start server in thread
        self.server_thread = threading.Thread(target=self.start_server, daemon=True)
        self.server_thread.start()

        # Wait for server to bind
        time.sleep(2)

        # Setup System Tray
        image = create_icon_image()
        menu = pystray.Menu(
            pystray.MenuItem('Open ARIA Dashboard', self.on_open, default=True),
            pystray.MenuItem('Exit', self.on_exit)
        )
        icon = pystray.Icon("ARIA_QUANT", image, "ARIA QUANT Lab", menu)
        
        # This blocks until exit
        icon.run()

if __name__ == '__main__':
    launcher = AriaLauncher()
    launcher.run()
