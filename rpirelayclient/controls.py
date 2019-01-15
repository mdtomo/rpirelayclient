from prompt_toolkit.widgets import Button
from prompt_toolkit.layout.containers import Window, WindowAlign
from prompt_toolkit.application import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl


class ChannelSwitch(Button):

    instances = []
    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status
        if status:
            self.text = 'Enabled'
            self.current_style = '#5faf00'
        else:
            self.text = 'Disabled'
            self.current_style = '#ff5f5f'

    def __init__(self, status, handler, handler_args):
        super().__init__('text', handler)
        self.current_style = None
        self.status = status
        self.control = FormattedTextControl(
            self._get_text_fragments,
            key_bindings=self._get_key_bindings(),
            focusable=True)
        self.control.show_cursor = False
        self.handler_args = handler_args

        def get_style():
            if get_app().layout.has_focus(self):
                return f'{self.current_style} bold reverse'
            else:
                return self.current_style

        self.window = Window(
            self.control,
            align=WindowAlign.CENTER,
            height=1,
            width=12,
            style=get_style,
            dont_extend_width=True,
            dont_extend_height=True)
        
        ChannelSwitch.instances.append(self)

    def _get_text_fragments(self):
        text = ('{:^%s}' % (self.width - 2)).format(self.text)

        def handler(mouse_event):
            if mouse_event.event_type == MouseEventType.MOUSE_UP:
                self.handler(self.handleqr_args)

        return [
            ('class:button.arrow', '<', handler),
            ('[SetCursorPosition]', ''),
            ('class:button.text', text, handler),
            ('class:button.arrow', '>', handler),
        ]

    def _get_key_bindings(self):
        " Key bindings for the Button. "
        kb = KeyBindings()

        @kb.add(' ')
        @kb.add('enter')
        def _(event):
            if self.handler is not None:
                self.handler(self.handler_args)

        return kb