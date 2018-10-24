import socket
import asyncio
from prompt_toolkit import print_formatted_text, HTML


HOST = '127.0.0.1'
PORT = 2018

reader, writer = None, None


def main():
    asyncio.run(create_connection())


async def create_connection():
    global reader, writer
    reader, writer = await asyncio.open_connection(HOST, PORT)
    print('Sending message..')
    await send_data('Hello')
    print('Closing connection.')
    writer.close()


async def send_data(data):
    global writer
    writer.write(data.encode())


if __name__ == '__main__':
    main()

