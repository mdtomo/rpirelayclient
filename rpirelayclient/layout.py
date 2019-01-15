from prompt_toolkit.layout.containers import VSplit, HSplit, Window
from prompt_toolkit.widgets import MenuItem
from prompt_toolkit import widgets
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout import Float, FloatContainer
from config import Config as config
from controls import ChannelSwitch
import utils


info_bar = FormattedTextControl('Press TAB to toggle channels.', style='#ffffff')
style_warning = '#800000 bg:#a8a8a8 bold reverse'
style_ok = '#005f00 bg:#a8a8a8 bold'
status_bar = FormattedTextControl('text', style=style_ok)
channel_status = [True,True,False,True,False,False,False,False]
channel_status_labels = [ChannelSwitch(status, handler=utils.toggle_channel, handler_args=i) for i, status in enumerate(channel_status)]
root_container = HSplit([
    widgets.MenuContainer(
        VSplit([
            widgets.Shadow(
                widgets.Frame(
                    VSplit([
                        HSplit([widgets.Label('Channel ' + str(i)) for i in range(1,9)]),
                        HSplit([widgets.Label(label, style=u'#ffaf00') for label in config.RELAY_LABELS]),
                        HSplit([status for status in channel_status_labels]),
                    ]),
                    title='Relay Status')
            ),
            widgets.Shadow(
                widgets.Frame(
                    Window(content=FormattedTextControl('Log Stream')),
                    title='Log Stream')
            )
        ]),
        menu_items=[MenuItem('Status'), MenuItem('Logs')],
        floats=[Float(Window(status_bar), right=1, top=0)]
    ),
    Window(info_bar),
])