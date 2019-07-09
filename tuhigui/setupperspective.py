#!/usr/bin/env python3
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#

from gi.repository import GObject, Gtk

import gi
gi.require_version("Gtk", "3.0")


@Gtk.Template(resource_path="/org/freedesktop/TuhiGui/ui/SetupPerspective.ui")
class SetupPerspective(Gtk.Stack):
    __gtype_name__ = "SetupPerspective"
    __gsignals__ = {
        'new-device':
            (GObject.SignalFlags.RUN_FIRST, None, (GObject.TYPE_PYOBJECT,)),
    }

    device_name_p1 = Gtk.Template.Child()
    device_name_p3 = Gtk.Template.Child()
    label_size = Gtk.Template.Child()
    label_btaddr = Gtk.Template.Child()
    label_battery = Gtk.Template.Child()

    def __init__(self, tuhi, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tuhi = tuhi
        self._sig = tuhi.connect('unregistered-device', self._on_unregistered_device)
        tuhi.start_search()

    def _on_unregistered_device(self, tuhi, device):
        tuhi.disconnect(self._sig)

        self.device_name_p1.set_text(device.name)
        self.set_visible_child_name('page1')
        self._sig = device.connect('button-press-required', self._on_button_press_required)
        device.register()

    def _on_button_press_required(self, tuhi, device):
        tuhi.disconnect(self._sig)

        self.set_visible_child_name('page2')
        self._sig = device.connect('registered', self._on_registered)

    def _on_registered(self, tuhi, device):
        tuhi.disconnect(self._sig)

        self.device_name_p3.set_text(device.name)
        self.set_visible_child_name('page3')
        self.label_size.set_text(f'not implemented')
        self.label_btaddr.set_text(device.address)
        self.label_battery.set_text(f'{device.battery_percent}%')
        self.device = device

    @GObject.Property
    def name(self):
        return "setup_perspective"

    @Gtk.Template.Callback("_on_go_button_clicked")
    def _on_go_button_clicked(self, button):
        self.emit('new-device', self.device)
