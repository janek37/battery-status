#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import os
gtk.gdk.threads_init()
import gobject
import battery

#ICON_DIR = '/usr/share/icons/ubuntu-mono-dark/status/24/'
ICON_DIR = ''

ICON_NAMES = {
    'discharging': 'battery-%03d.svg',
    'charging': 'battery-%03d-charging.svg',
    'charged': 'battery-charged.svg',
}
ICON_STEP = 20

TOOLTIP_TEMPLATE = '%d%% %d:%02d left'

SHOW_CHARGED = False

class BatteryStatus:
    def __init__(self):
        self.icon = gtk.StatusIcon()
        self.tick_interval = 10000 # number of miliseconds between each poll
        self.icon.connect('popup-menu', self.right_click)
        self.update()
        self.icon.set_visible(True)
        self.menu_init()
    def menu_init(self):
        self.menu = gtk.Menu()
        about = gtk.MenuItem()
        about.set_label("About")
        about.connect("activate", self.show_about_dialog)
        quit = gtk.MenuItem()
        quit.set_label("Quit")
        quit.connect("activate", gtk.main_quit)
        self.menu.attach(about, 0, 1, 0, 1)
        self.menu.attach(quit, 0, 1, 1, 2)
        self.menu.show_all()
    def right_click(self, icon, button, time):
        def pos(menu):
            return (gtk.status_icon_position_menu(menu, icon))
        self.menu.popup(None, None, pos, button, time)
    def icon_directory(self):
        return os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'icons')
    def update(self):
        """This method is called everytime a tick interval occurs"""
        state = battery.state()
        if state == 'charged' and not SHOW_CHARGED:
            self.icon.set_visible(False)
        else:
            hours, minutes = battery.time_left_hm()
            percent = battery.percent_full()
            icon_name = ICON_NAMES[state]
            if ICON_DIR:
                icon_dir = ICON_DIR
            else:
                icon_dir = self.icon_directory()
            if state != 'charged':
                icon_name %= ICON_STEP * round(percent/ICON_STEP)
            self.icon.set_visible(True)
            tooltip_text = TOOLTIP_TEMPLATE % (int(percent), hours, minutes)
            self.icon.set_from_file(os.path.join(icon_dir, icon_name))
            self.icon.set_tooltip(tooltip_text)
        source_id = gobject.timeout_add(self.tick_interval, self.update)
    def show_about_dialog(self, widget):
        about_dialog = gtk.AboutDialog()
        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_name("Battery Status Icon")
        about_dialog.set_version("1.0")
        about_dialog.set_authors(["Jan Szejko"])
        about_dialog.run()
        about_dialog.destroy()
    def main(self):
        gtk.main()

if __name__ == "__main__":
    app = BatteryStatus()
    app.main()
