#!/usr/bin/env python3
from tkinter import Toplevel
from .ui import MyUI
from os import name

if name == 'nt':
    import ctypes
    from multiprocessing.dummy import freeze_support

    freeze_support()


class Main(Toplevel):
    def __init__(self):
        super().__init__()
        self.title("MTK Port Tool")
        self.resizable(False, False)
        self.gui()
        self.mainloop()

    def gui(self):
        myapp = MyUI(self)
        myapp.pack(side='top', fill='both', padx=5, pady=5, expand=True)
        # Fix high dpi
        if name == 'nt':
            # SetProcessDpiAwareness is only available on Windows 8.1+
            # For Windows 7 compatibility, we need to check the version
            try:
                # Try Windows 8.1+ API
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
                # Get screen resize scale factor
                self.tk.call('tk', 'scaling', ctypes.windll.shcore.GetScaleFactorForDevice(0) / 75)
            except (OSError, AttributeError):
                # Fallback for Windows 7 - use older API
                try:
                    ctypes.windll.user32.SetProcessDPIAware()
                except (OSError, AttributeError):
                    pass  # DPI awareness not available, continue without it
        self.update()

