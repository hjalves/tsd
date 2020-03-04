import asyncio
from asyncio import create_task
from functools import partial
from time import time, strftime

import urwid
from emoji import emojize
from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_1

_ = partial(emojize, use_aliases=True)


class Clock(urwid.WidgetWrap):
    signals = ["title_changed"]

    def __init__(self):
        self._title = _(f"Clock :clock3: {time()}")
        self.time = urwid.BigText("Clock", urwid.HalfBlock7x7Font())
        self.temp = urwid.BigText("-'C", urwid.HalfBlock5x4Font())
        self.root_widget = urwid.Filler(
            urwid.Pile(
                [
                    urwid.Padding(self.time, width=urwid.CLIP, align=urwid.CENTER),
                    urwid.Divider(),
                    urwid.Padding(
                        urwid.AttrMap(self.temp, "temp"),
                        width=urwid.CLIP,
                        align=urwid.CENTER,
                    ),
                ]
            )
        )
        super().__init__(self.root_widget)

    def get_title(self):
        return self._title

    def set_title(self, title):
        self._title = title
        self._emit("title_changed", self._title)

    title = property(get_title, set_title)

    def setup(self, loop):
        self.update_time(loop)
        create_task(self.get_temperature())

    async def get_temperature(self):
        client = MQTTClient()
        await client.connect("mqtt://192.168.10.254")
        topics = [
            ("sensors/temper", QOS_1),
        ]
        await client.subscribe(topics)
        while True:
            try:
                message = await client.deliver_message(30)
            except asyncio.TimeoutError:
                self.temp.set_text("-'C")
            else:
                temperature = float(message.data)
                self.temp.set_text(f"{temperature:.1f}'C")

    def update_time(self, loop, user_data=None):
        self.title = _("Clock :clock3: ") + strftime("%H:%M")

        at = int(time()) + 1.01
        loop.set_alarm_at(at, self.update_time, user_data)
        self.time.set_text(
            [
                strftime("%H"),
                ("blink", ":"),
                strftime("%M"),
                ("blink", ":"),
                strftime("%S"),
            ]
        )
