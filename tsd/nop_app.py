import urwid


class Nop(urwid.WidgetWrap):
    signals = ["title_changed"]

    def __init__(self, fill="/", title="Nop"):
        self.title = title
        self.root_widget = urwid.SolidFill(fill)
        super().__init__(self.root_widget)

    def setup(self, loop):
        pass

    def get_title(self):
        return self.title
