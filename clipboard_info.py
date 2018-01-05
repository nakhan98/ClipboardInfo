#!/usr/bin/env python
"""
Simple app to show and clear current clipboard contents on GNU/Linux

Requires xsel and python-notify

Adapted from: https://github.com/majorsilence/pygtknotebook
Also see: http://pygtk.org/pygtk2tutorial/examples/clipboard.py

License: GPLv3
"""


import gtk
import subprocess
import pynotify
import logging


logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


class ClearClipboard(object):
    APP_NAME = "ClipboardInfo"
    ABOUT_MSG = __doc__
    CLEAR_CLIPBOARD_COMMAND = ("xsel", "-b", "-c")

    def __init__(self):
        icon = gtk.status_icon_new_from_stock(gtk.STOCK_PASTE)
        icon.connect('popup-menu', self.on_right_click)
        icon.connect('activate', self.on_left_click)
        pynotify.init(self.APP_NAME)

    def run(self):
        gtk.main()

    def message(self, data=None):
        "Function to display messages to the user."
        msg = gtk.MessageDialog(None, gtk.DIALOG_MODAL,
                                gtk.MESSAGE_INFO, gtk.BUTTONS_OK, data)
        msg.run()
        msg.destroy()

    def send_notification(self, msg):
        notice = pynotify.Notification(self.APP_NAME, msg)
        notice.show()

    def open_app(self, data):
        self.message(self.ABOUT_MSG.strip())

    def close_app(self, data):
        gtk.main_quit()

    def make_menu(self, event_button, event_time, data=None):
        menu = gtk.Menu()
        open_item = gtk.MenuItem("Open")
        clear_clipboard_item = gtk.MenuItem("Clear Clipboard")
        about_item = gtk.MenuItem("About")
        close_item = gtk.MenuItem("Close")

        # Append the menu items
        menu.append(open_item)
        menu.append(clear_clipboard_item)
        menu.append(about_item)
        menu.append(close_item)

        # add callbacks
        open_item.connect_object("activate", self.open_app, "Open App")
        clear_clipboard_item.connect_object("activate", self.clear_clipboard, None)
        about_item.connect_object("activate", self.clear_clipboard, None)
        close_item.connect_object("activate", self.close_app, None)

        # Show the menu items
        open_item.show()
        clear_clipboard_item.show()
        about_item.show()
        close_item.show()

        # Popup the menu
        menu.popup(None, None, None, event_button, event_time)

    def on_right_click(self, data, event_button, event_time):
        self.make_menu(event_button, event_time)

    def on_left_click(self, event):
        self.clear_clipboard()

    def clear_clipboard(self, data=None):
        subprocess.check_call(self.CLEAR_CLIPBOARD_COMMAND)
        logging.info("Cleared clipboard")
        self.send_notification("Cleared clipboard")

    def about_app(self, data):
        self.message(self.ABOUT_MSG.strip())


if __name__ == '__main__':
    ClearClipboard().run()
