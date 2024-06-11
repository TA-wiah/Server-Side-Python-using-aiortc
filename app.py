import argparse
import asyncio
import cv2
import numpy as np
import aiortc
from aiortc.contrib.media import MediaPlayer

async def run(pc):
    await pc.setLocalDescription(await pc.createOffer())
    offer = {'sdp': pc.localDescription.sdp, 'type': pc.localDescription.type}
    return offer

class VideoStreamTrack(aiortc.VideoStreamTrack):
    def __init__(self):
        super().__init__()

        self.cap = cv2.VideoCapture(0)

    async def recv(self):
        ret, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pts, time_base = await self.next_timestamp()

        return aiortc.VideoFrame(width=frame.shape[1], height=frame.shape[0], pts=pts, time_base=time_base, data=frame.tobytes())

async def create_server():
    pc = await aiortc.MediaSoupTransport.createProducerTransport('wss://your_server_ip:4443')

    @pc.on("icetransportstatechange")
    async def on_ice(ice):
        if ice == "connected":
            print("Connected!")

    pc.addTrack(VideoStreamTrack())

    await run(pc)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Camera server")
    parser.add_argument("--port", default=4443, type=int, help="Port for the camera server")
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_server())
    loop.run_forever()
