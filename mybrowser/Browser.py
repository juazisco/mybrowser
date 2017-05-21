# Browser.py
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
gi.require_version('WebKit', '3.0')
from os.path import join, dirname
from gi.repository import GLib, Gio, Gtk, WebKit, GObject,Gdk
from mybrowser.Util import Util

class Browser(object):
    def __init__(self, application):
        try:
            builder = Gtk.Builder.new_from_file(dirname(sys.argv[0])+"/../share/data/my_browser.ui")
            builder.connect_signals(self)
        except GObject.GError:
            print("Error en el archivito xml")
            raise
        self.mainWindow = builder.get_object("mainBrowser")
        self.mainWindow.set_default_size(800, 600)
        self.mainWindow.set_application(application)

        max_action = Gio.SimpleAction.new_stateful("maximize", None,
                                           GLib.Variant.new_boolean(False))
        max_action.connect("change-state", self.on_maximize_toggle)
        self.mainWindow.add_action(max_action)
        self.mainWindow.connect("key-press-event", self._key_pressed)
        self.mainWindow.connect("notify::is-maximized",
                            lambda obj, pspec: max_action.set_state(
                                               GLib.Variant.new_boolean(obj.props.is_maximized)))
        self.webView = WebKit.WebView()
        self.webView.load_uri("https://planet.gnome.org")
        self.webView.set_editable(False)
        self.urlentry = builder.get_object("txtURI")
        self.urlentry.set_text("https://planet.gnome.org")
        self.popMenuZoom = builder.get_object("popMenuZoom")
        self.btnZoomNormal = builder.get_object("btnZoomNormal")
        self.btnZoomNormal.set_property("width-request", 70)
        scrolled_window = builder.get_object("scrContent")
        scrolled_window.add(self.webView)
        self.webView.show()
        self.mainWindow.show()

    def close(self, *args):
        self.mainWindow.destroy()

    def on_maximize_toggle(self, action, value):
        action.set_state(value)
        if value.get_boolean():
            self.mainWindow.maximize()
        else:
            self.mainWindow.unmaximize()

    def on_btnBack_clicked(self, button):
        self.webView.go_back()

    def on_btnForward_clicked(self, button):
        #print(help(self.webView))
        self.webView.go_forward()

    def on_btnGo_clicked(self, button):
        self.webView.reload()

    def on_txtURI_activate(self, button):
        newUrl=Util.get_valid_url(str(self.urlentry.get_text()))
        self.webView.load_uri(newUrl)
        self.urlentry.set_text(newUrl)

    def on_btnPopMenu_clicked(self,button):
        self.popMenuZoom.set_relative_to(button)
        if self.popMenuZoom.get_visible():
            self.popMenuZoom.hide()
        else:
            self.popMenuZoom.show_all()

    def _change_zoom_in(self,button=None):
        self.webView.zoom_in()
        self._change_zoom_update()

    def _change_zoom_out(self,button=None):
        self.webView.zoom_out()
        self._change_zoom_update()

    def _change_zoom_normal(self,button=None):
        self.webView.set_zoom_level(1)
        self._change_zoom_update()

    def _change_zoom_update(self):
        zoomValue = int(round(self.webView.get_zoom_level()*100))
        self.btnZoomNormal.set_label(str(zoomValue)+'%')
        if zoomValue == 100:
            self.btnZoomNormal.set_sensitive(False)
        else:
            self.btnZoomNormal.set_sensitive(True)

    def _key_pressed(self, widget, event):
        modifiers = Gtk.accelerator_get_default_mod_mask()
        mapping = {Gdk.KEY_r: self.on_btnGo_clicked,
                   Gdk.KEY_plus: self._change_zoom_in,
                   Gdk.KEY_minus: self._change_zoom_out,
                   Gdk.KEY_0: self._change_zoom_normal,
                   Gdk.KEY_q: Gtk.main_quit}

        if event.state & modifiers == Gdk.ModifierType.CONTROL_MASK \
          and event.keyval in mapping:
            mapping[event.keyval]()
