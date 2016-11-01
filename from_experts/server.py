import asyncio
import aioamqp
import websockets

connected = set()

async def hello(websocket, path):
    global connected
    print("WS client connected")
    connected.add(websocket)

    try:
        await asyncio.sleep(30)
    finally:
        # Unregister.
        connected.remove(websocket)

async def callback(channel, body, envelope, properties):
    print(" [x] Received %r from amqp" % body)
    for c in connected:
        await c.send(body)

async def receive_amqp():
    transport, protocol = await aioamqp.connect()
    channel = await protocol.channel()
    await channel.queue_declare(queue_name='hello')
    await channel.basic_consume(callback, queue_name='hello')



start_server = websockets.serve(hello, 'localhost', 8765)
event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(start_server)
event_loop.run_until_complete(receive_amqp())
event_loop.run_forever()
