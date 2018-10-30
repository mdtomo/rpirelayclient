import socket
import asyncio
import prompt_toolkit as ptk
from prompt_toolkit import widgets
from prompt_toolkit.eventloop import use_asyncio_event_loop
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import VSplit, HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import MenuItem
from datetime import datetime
from config import Config as config


HOST = '127.0.0.1'
PORT = 2018

kb = KeyBindings()
channel_status = [1,1,0,0,0,0,0,0]
channel_status_labels = [FormattedTextControl('Enabled', style=u'#5faf00') if status == 1 else FormattedTextControl('Disabled', style=u'#ff5f5f') for status in channel_status]
log_title = FormattedTextControl('test')
root_container = widgets.MenuContainer(
    VSplit([
        widgets.Shadow(
            widgets.Frame(
                #HSplit([Window(height=2, char=' ')]),
                VSplit([
                    HSplit([widgets.Label('Channel ' + str(i)) for i in range(1,9)]),
                    HSplit([widgets.Label(label, style=u'#ffaf00') for label in config.RELAY_LABELS]),
                    HSplit([Window(status) for status in channel_status_labels]),
                ]),
                title='Relay Status')
        ),
        widgets.Shadow(
            widgets.Frame(
                Window(content=log_title),
                title='Test')
        )
    ]),
    menu_items=[MenuItem('Status', children=[MenuItem('Update')])],
)
layout = Layout(root_container)

reader, writer = None, None
use_asyncio_event_loop()


def main():
    app = ptk.Application(layout=layout, key_bindings=kb, full_screen=True)
    #app.run()
    asyncio.get_event_loop().run_until_complete(app.run_async().to_asyncio_future())
    asyncio.run(create_connection())


async def create_connection():
    global reader, writer
    reader, writer = await asyncio.open_connection(HOST, PORT)
    print('Sending message..')
    await send_data(str(datetime.now()))
    print('Closing connection.')
    writer.close()


async def send_data(data):
    global writer
    writer.write(data.encode())


@kb.add('q')
def quit(event):
    event.app.exit()


@kb.add('1')
def _(event):
    # event.app.reset()
    global channel_status_labels
    channel_status_labels[0].text = 'test'
    global log_title
    log_title.text = 'Logs 123'


if __name__ == '__main__':
    main()

