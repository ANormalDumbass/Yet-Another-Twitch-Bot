import asyncio
import websockets
import re
from datetime import datetime
import os

async def send_message(websocket, channel, msg):
    message_to_send = f'PRIVMSG #{channel} :{msg}'
    await websocket.send(message_to_send)
    print(f"Sent: {message_to_send}")

async def handle_chat(websocket, channel, message_to_send, trigger_messages):
    while True:
        response = await websocket.recv()
        print(f"Received: {response}")

        match = re.search(r":(\w+)!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #{}\s+:(.*)".format(channel), response)
        if match:
            username, msg = match.groups()
            print(f"User: {username}, Message: {msg}")

            if msg.strip() in trigger_messages:
                await send_message(websocket, channel, message_to_send)

async def connect_to_twitch_chat(username, token, channel, message, trigger_messages):
    server = 'ws://irc-ws.chat.twitch.tv'
    port = 80
    try:
        async with websockets.connect(f'{server}:{port}') as websocket:
            await websocket.send(f'PASS oauth:{token}')
            await websocket.send(f'NICK {username}')
            received_ping = False
            if channel:
                await websocket.send(f'JOIN #{channel}')
                print(f"Successfully connected to {channel}")

            while True:
                response = await websocket.recv()
                if response.startswith('PING'):
                    if not received_ping:
                        await websocket.send('PONG :tmi.twitch.tv')
                        received_ping = True
                elif response.startswith('PONG'):
                    received_ping = False
                else:
                    await handle_chat(websocket, channel, message, trigger_messages)
    except websockets.exceptions.ConnectionClosedError:
        print(f'Connection for {username} closed. Reconnecting...')
        await asyncio.sleep(5)

async def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file = os.path.join(script_dir, 'settings.txt')

    with open(settings_file, 'r') as file:
        settings = file.read()

    username = re.search(r"Username:\s*'([^']*)'", settings).group(1)
    token = re.search(r"Token:\s*'([^']*)'", settings).group(1)
    message = re.search(r"Message:\s*'([^']*)'", settings).group(1)
    channel = re.search(r"Channel:\s*'([^']*)'", settings).group(1)
    trigger_messages = re.search(r"Command:\s*'([^']*)'", settings).group(1).split(',')

    await connect_to_twitch_chat(username, token, channel, message, trigger_messages)

if __name__ == "__main__":
    asyncio.run(main())
