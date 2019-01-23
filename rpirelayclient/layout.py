from prompt_toolkit.layout.containers import VSplit, HSplit, Window
from prompt_toolkit.widgets import MenuItem
from prompt_toolkit import widgets
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout import Float, FloatContainer, HorizontalAlign
from config import Config as config
from controls import ChannelSwitch
from utils import ChannelRequest


message_queue = []


def toggle_channel(number):
    '''
    Put this function in here to prevent an import cycle. Layout needs this function when building the UI.
    Layout is imported by main.
    '''
    ChannelSwitch.instances[number].status = not ChannelSwitch.instances[number].status
    channel_request = ChannelRequest(number, ChannelSwitch.instances[number].status)
    message_queue.append(channel_request.payload)


info_bar = FormattedTextControl('Press TAB to toggle channels.', style='#3a3a3a bg:#a8a8a8 bold')
style_warning = '#800000 bg:#a8a8a8 bold reverse'
style_ok = '#005f00 bg:#a8a8a8 bold'
status_bar = FormattedTextControl('text', style=style_ok)
channel_status = [False for i in range(8)]
channel_status_labels = [ChannelSwitch(status, handler=toggle_channel, handler_args=i) for i, status in enumerate(channel_status)]
root_container = HSplit([
            widgets.Frame(
                widgets.Box(
                    VSplit([
                        HSplit([widgets.Label('Relay ' + str(i)) for i in range(1,9)]),
                        HSplit([widgets.Label(label) for label in config.RELAY_LABELS]),
                        HSplit([status for status in channel_status_labels]),
                        ],
                        align = HorizontalAlign.CENTER
                    )
                ),
            title = 'RPi Relay Client'
            ),
            FloatContainer(Window(style=style_ok), floats=[Float(Window(info_bar), left=1), Float(Window(status_bar), right=1)])
    ])