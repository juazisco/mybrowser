# __main__.py
#
# Copyright (C) 2017 juazisco
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib
from os.path import join, dirname
from mybrowser import Browser

class Application(Gtk.Application):
    def __init__(self, application_id, flags):
        Gtk.Application.__init__(self, application_id=application_id, flags=flags)
        self.connect("activate", self.new_window)

    def new_window(self, *args):
        self.browser = Browser.Browser(self)

    def do_startup(self):
        Gtk.Application.do_startup(self)
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

        builder = Gtk.Builder.new_from_file(dirname(sys.argv[0])+"/../share/data/"+"app_menu.xml")
        self.set_app_menu(builder.get_object("app-menu"))

    def on_about(self, action, param):
        about_dialog = Gtk.AboutDialog(transient_for=self.browser.mainWindow, modal=True)
        about_dialog.set_program_name("My Browser")
        about_dialog.set_version("Versión 1.0")
        about_dialog.set_website("https://github.com/juazisco/mybrowser")
        authors = ["Jose Quiñones <joseq@apesol.org.pe>"]
        about_dialog.set_authors(authors)
        about_dialog.set_license("GNU Lesser General Public License\n"
                          "See http://www.gnu.org/copyleft/lesser.html for more details")
        about_dialog.set_icon_name("web")
        about_dialog.set_logo_icon_name("web")
        about_dialog.present()

    def on_quit(self, action, param):
        self.quit()


def main():
    application = Application("org.gnome.mybrowser", Gio.ApplicationFlags.FLAGS_NONE)

    try:
        ret = application.run()
    except SystemExit as e:
        ret = e.code

    sys.exit(ret)

if __name__ == '__main__':
    main()
