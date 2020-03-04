#!/usr/bin/env python3
import argparse
import asyncio

import urwid

from tsd.tabbed import TabbedApplication

palette = [
    ("temp", "dark gray", ""),
    ("tab", "dark gray", ""),
    ("selected", "bold", ""),
    ("blink", "blink", ""),
]


def main(args=None):
    parser = argparse.ArgumentParser(description="tsd - Terminal Smart Display")
    parser.add_argument(
        "-c", "--config", type=argparse.FileType("r"), help="Configuration file"
    )
    args = parser.parse_args(args)
    return App(config_file=args.config).run()


class App:
    def __init__(self, config_file):
        self.config_file = config_file
        self._app = TabbedApplication()

    def run(self):
        urwid.escape.SHOW_CURSOR = ""
        event_loop = urwid.AsyncioEventLoop()
        loop = urwid.MainLoop(self._app, palette, event_loop=event_loop)
        loop.set_alarm_in(0, self.setup)
        loop.run()

    def setup(self, loop, user_data=None):
        self._app.setup(loop)
