import socket
import asyncio
import prompt_toolkit as ptk
from prompt_toolkit import widgets
from prompt_toolkit.eventloop import use_asyncio_event_loop
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import VSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from datetime import datetime


HOST = '127.0.0.1'
PORT = 2018

kb = KeyBindings()
buffer1 = Buffer()
root_container = widgets.MenuContainer(
    VSplit([
        Window(content=BufferControl(buffer=buffer1)),
        widgets.Shadow(
            widgets.Frame(
            Window(content=FormattedTextControl(text='System Logs')),
            title='System logs')
        )
    ]),
    menu_items=[widgets.menus.MenuItem(text='Menu')],
)
layout = Layout(root_container)

reader, writer = None, None
use_asyncio_event_loop()


def main():
    app = ptk.Application(layout=layout, key_bindings=kb, full_screen=True)
    app.run()
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
def exit(event):
    event.app.exit()


if __name__ == '__main__':
    main()

