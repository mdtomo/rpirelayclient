import socket
import asyncio
import json
import prompt_toolkit as ptk
from prompt_toolkit.application import get_app
#from prompt_toolkit import widgets
from prompt_toolkit.eventloop import use_asyncio_event_loop
from prompt_toolkit.buffer import Buffer
#from prompt_toolkit.layout.containers import VSplit, HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
#from prompt_toolkit.layout import Float, FloatContainer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
#from prompt_toolkit.widgets import MenuItem, Button
from datetime import datetime
from config import Config as config
#from controls import ChannelSwitch
from layout import root_container, status_bar, info_bar, style_warning
import utils


program_quitting = False
use_asyncio_event_loop()
global_kb = KeyBindings()
channel_kb = KeyBindings()
reader, writer, app = None, None, None


def main():
    global app
    loop = asyncio.get_event_loop()

    app = ptk.Application(layout=Layout(root_container), key_bindings=global_kb, full_screen=True)

    connection_task = loop.create_task(create_connection())
    message_queue_task = loop.create_task(message_queue_processor(utils.message_queue))
    final_task = asyncio.gather(connection_task, message_queue_task, app.run_async().to_asyncio_future())
    loop.run_until_complete(final_task)
    # asyncio.run(create_connection())


async def create_connection():
    global reader, writer
    try:
        reader, writer = await asyncio.open_connection(config.HOST, config.PORT)
        addr = writer.get_extra_info('peername')
        status_bar.text = f'Connected to {addr[0]}:{addr[1]}'
        app.invalidate()

        data = None
        while data is not b'':
            data = await reader.read(200)
            status_bar.text = f'Received: {data.decode()}'
            app.invalidate()
        
        status_bar.text = 'Server closed the connection.'
        status_bar.style = style_warning
        app.invalidate()
    except OSError as e:
        status_bar.text = str(e.strerror)
        status_bar.style = style_warning
        app.invalidate()

    

    #print('Sending message..')
    #await send_data(str(datetime.now()))
    #await asyncio.sleep(15)
    #print('Closing connection.')
    #writer.close()
    #await writer.wait_closed()
    #print('Waited to close.')


async def message_queue_processor(queue):
    while True:
        if utils.message_queue:
            if utils.message_queue[0] == 'quit':
                break
            info_bar.text = 'Sending command.'
            json_msg = json.dumps(utils.message_queue[0])
            writer.write(json_msg.encode())
            await writer.drain()
            utils.message_queue.pop()
        else:
            await asyncio.sleep(0.5)
    print('Program quitting. Closing connection.')
    writer.close()


@global_kb.add('q')
def quit(event):
    global program_quitting
    program_quitting = True
    utils.message_queue.append('quit')
    #print('Program quitting. Closing connection.')
    # if writer is not None:
    #     writer.close()
    event.app.exit()


@global_kb.add('c-i')
def tab(event):
    current_control = get_app().layout.current_control
    get_app().layout.focus_next()


@global_kb.add('down')
def down(event):
    get_app().layout.focus_next()
    current_control = get_app().layout.current_control
    if isinstance(current_control, FormattedTextControl):
        info_bar.text = 'Space/Enter to enable/disable.'


@global_kb.add('up')
def up(event):
    get_app().layout.focus_last()


if __name__ == '__main__':
    main()

