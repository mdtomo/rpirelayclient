import socket
import asyncio
import prompt_toolkit as ptk
from prompt_toolkit.application import get_app
from prompt_toolkit import widgets
from prompt_toolkit.eventloop import use_asyncio_event_loop
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import VSplit, HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout import Float, FloatContainer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import MenuItem, Button
from datetime import datetime
from config import Config as config
from controls import ChannelSwitch


HOST = '127.0.0.1'
PORT = 2018
program_quitting = False
style_warning = '#800000 bg:#a8a8a8 bold reverse'
style_ok = '#005f00 bg:#a8a8a8 bold'
use_asyncio_event_loop()
global_kb = KeyBindings()
channel_kb = KeyBindings()
channel_status = [1,0,1,0,0,0,0,0]
info_bar = FormattedTextControl('Press TAB to toggle channels.', style='#0087d7')

def toggle_channel(number):
    current_window = get_app().layout.current_window
    parent = get_app().layout.get_parent(current_window)
    info_bar.text = str(ChannelSwitch.instances[number].status)
    if isinstance(current_window, ChannelSwitch):
        current_control.status = not current_control.status
        info_bar.text = 'changed'


#channel_status_labels = [FormattedTextControl('Enabled', style=u'#5faf00', focusable=True, show_cursor=True, key_bindings=channel_kb) if status == 1 else FormattedTextControl('Disabled', style=u'#ff5f5f', focusable=True, show_cursor=True, key_bindings=channel_kb) for status in channel_status]
channel_status_labels = [ChannelSwitch(True, handler=toggle_channel, handler_args=i) if status == 1 else  ChannelSwitch(False, handler=toggle_channel, handler_args=i) for i, status in enumerate(channel_status)]
log_title = FormattedTextControl('test')
#log_buffer = Buffer('buffer control', multiline=True)
status_bar = FormattedTextControl('text', style=style_ok)

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
                    Window(content=log_title),
                    title='Test')
            )
        ]),
        menu_items=[MenuItem('Status'), MenuItem('Logs')],
        floats=[Float(Window(status_bar), right=1, top=0)]
    ),
    Window(info_bar),
    #Window('test'),
])
layout = Layout(root_container)

reader, writer, app = None, None, None


def main():
    global app
    loop = asyncio.get_event_loop()

    app = ptk.Application(layout=layout, key_bindings=global_kb, full_screen=True)

    task1 = loop.create_task(create_connection())
    final_task = asyncio.gather(task1, app.run_async().to_asyncio_future())
    loop.run_until_complete(final_task)
    # asyncio.run(create_connection())


async def create_connection():
    global reader, writer, status_bar
    try:
        reader, writer = await asyncio.open_connection(HOST, PORT)
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


def send_data(data):
    global writer
    #print('Sending message..')
    writer.write(data.encode())
    # await writer.drain()
    #print('Closing connection.')
    #writer.close()
    #print(writer.is_closing())


async def wait_out():
    log_title.text = 'Waiting..'
    await asyncio.sleep(3)
    log_title.text = 'OK'


@global_kb.add('q')
def quit(event):
    global program_quitting
    program_quitting = True
    print('Program quitting. Closing connection.')
    if writer is not None:
        writer.close()
    event.app.exit()


@global_kb.add('c-i')
def tab(event):
    current_control = get_app().layout.current_control
    get_app().layout.focus_next()
    info_bar.text = str(type(current_control))
    if isinstance(current_control, FormattedTextControl):
        #current_control.text = f'<{current_control.text}>'
        current_control.style = f'{current_control.style} bold'
        info_bar.text = current_control.text
        app.invalidate()


@global_kb.add('down')
def down(event):
    get_app().layout.focus_next()
    info_bar.text = str(event)


@global_kb.add('up')
def up(event):
    get_app().layout.focus_last()
    info_bar.text = str(event)

if __name__ == '__main__':
    main()

