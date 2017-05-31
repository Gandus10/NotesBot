"""Bot exemple qui retourne les moyennes du cours donnés."""

import xml.etree.ElementTree as ET
import asyncio
import json
import zlib

import aiohttp

# Jupyter hack pour recréer une boucle.
# Pas nécessaire hors de Jupyter
loop = asyncio.get_event_loop()
if loop.is_closed():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
# fin du hack

TOKEN = 'MzEyMTcwNTgzMTA0NDIxODkw.C_72kA._bH0bFDqebVIYXyOowS0NPf_S4k'

URL = "https://discordapp.com/api"
HEADERS = {
    "Authorization": f"Bot {TOKEN}",
    "User-Agent": "DiscordBot (http://he-arc.ch/, 0.1)"
}

async def api_call(path, method="GET", **kwargs):
    """Effectue une  requête sur l'API REST de Discord."""
    default = {"headers": HEADERS}
    kwargs = dict(default, **kwargs)
    with aiohttp.ClientSession() as session:
        async with session.request(method, f"{URL}{path}", **kwargs) as response:
            if 200 == response.status:
                return await response.json()
            elif 204 == response.status:
                return {}
            else:
                body = await response.text()
                raise AssertionError(f"{response.status} {response.reason} was unexpected.\n{body}")

async def send_message(recipient_id, content):
    """Envoie un message à l'utilisateur donné."""
    channel = await api_call("/users/@me/channels", "POST", json={"recipient_id": recipient_id})
    return await api_call(f"/channels/{channel['id']}/messages", "POST", json={"content": content})

# Pas très joli, mais ça le fait.
last_sequence = None

async def heartbeat(ws, interval):
    """Tâche qui informe Discord de notre présence."""
    while True:
        await asyncio.sleep(interval / 1000)
        print("> Heartbeat")
        await ws.send_json({'op': 1,  # Heartbeat
                            'd': last_sequence})


async def identify(ws):
    """Tâche qui identifie le bot à la Web Socket (indispensable)."""
    await ws.send_json({'op': 2,  # Identify
                        'd': {'token': TOKEN,
                              'properties': {},
                              'compress': True,  # implique le bout de code lié à zlib, pas nécessaire.
                              'large_threshold': 250}})


#async def writeFile(data, content):


async def start(ws):
    """Lance le bot sur l'adresse Web Socket donnée."""
    global last_sequence  # global est nécessaire pour modifier la variable
    with aiohttp.ClientSession() as session:
        async with session.ws_connect(f"{ws}?v=5&encoding=json") as ws:
            async for msg in ws:
                if msg.tp == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                elif msg.tp == aiohttp.WSMsgType.BINARY:
                    data = json.loads(zlib.decompress(msg.data))
                else:
                    print("?", msg.tp)

                if data['op'] == 10:  # Hello
                    asyncio.ensure_future(heartbeat(ws, data['d']['heartbeat_interval']))
                    await identify(ws)
                elif data['op'] == 11:  # Heartbeat ACK
                    print("< Heartbeat ACK")
                elif data['op'] == 0:  # Dispatch
                    last_sequence = data['s']
                    if data['t'] == "MESSAGE_CREATE":
                        print(data['d'])
                        if data['d']['content'] == 'note':
                            #task = asyncio.ensure_future(send_message(data['d']['author']['id'],'Tu as deux, tu es nul'))

                        if data['d']['content'] == 'quit':
                            task = asyncio.ensure_future(send_message(data['d']['author']['id'],'Bye bye'))
                            # On l'attend l'envoi du message ci-dessus.
                            await asyncio.wait([task])
                            break
                    else:
                        print('Todo?', data['t'])
                else:
                    print("Unknown?", data)




async def main():
    response = await api_call('/gateway')
    await start(response['url'])


# Lancer le programme.
loop = asyncio.get_event_loop()
loop.set_debug(True)
loop.run_until_complete(main())
loop.close()
