from functools import partial

import urwid
from emoji import emojize
from urwid import connect_signal

from tsd.clock import Clock
from tsd.nop_app import Nop

_ = partial(emojize, use_aliases=True)


class TabButton(urwid.Button):
    button_left = urwid.Text("[",)
    button_right = urwid.Text("]")

    def __init__(self, parent, tab_app, pos):
        self._tab_app = tab_app
        self._parent = parent
        self._pos = pos
        title = tab_app.title
        super().__init__(title, self.on_press)
        connect_signal(tab_app, "title_changed", self.title_changed)

    def on_press(self, a):
        self._parent.change_tab_pos(self._pos)

    def title_changed(self, widget, title):
        self._label.set_text(title)


class TabHeader(urwid.Columns):
    def keypress(self, size, key):
        if self._command_map[key] == "activate":
            pos = self.focus_position + 1
            self.focus_position = pos % len(self.contents)
        else:
            key = super().keypress(size, key)
        self.focus.original_widget._emit("click")
        return key


class TabbedApplication(urwid.Frame):
    def __init__(self):
        self.loop = None
        self._sub_apps = [Clock()]
        self._header = TabHeader(self._get_tab_buttons())
        super().__init__(self._sub_apps[0], header=self._header)
        self.focus_position = "header"

    def setup(self, loop):
        self.loop = loop
        self.body.setup(loop)
        self.add_sub_app(Nop("/", title="Nop1"))
        self.add_sub_app(Nop("x", title="Nop2"))

    def _get_tab_buttons(self):
        return [
            urwid.AttrMap(TabButton(self, subapp, pos), "tab", focus_map="selected")
            for pos, subapp in enumerate(self._sub_apps)
        ]

    def add_sub_app(self, tab_app, switch=False):
        self._sub_apps.append(tab_app)
        self._header.widget_list = self._get_tab_buttons()
        if switch:
            self.change_tab_pos(len(self._sub_apps) - 1)

    def change_tab_pos(self, pos):
        sub_app = self._sub_apps[pos]
        self.set_body(sub_app)
        self._header.focus_position = pos
