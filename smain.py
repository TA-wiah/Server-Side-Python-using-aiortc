import asyncio
from aiohttp import web
import json
import cv2
import numpy as np
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack

pc = None
pcs = set()

class VideoTrack(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)

    async def recv(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

async def offer(request):
    global pc
    params = await request.json()
    pc = RTCPeerConnection()
    pcs.add(pc)

    @pc.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange():
        if pc.iceConnectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    pc.addTrack(VideoTrack())

    await pc.setRemoteDescription(RTCSessionDescription(sdp=params["sdp"], type=params["type"]))
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.Response(
        content_type="application/json",
        text=json.dumps({"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}),
    )

async def answer(request):
    global pc
    params = await request.json()
    await pc.setRemoteDescription(RTCSessionDescription(sdp=params["sdp"], type=params["type"]))
    return web.Response(text="OK")

app = web.Application()
app.router.add_post("/offer", offer)
app.router.add_post("/answer", answer)

web.run_app(app, port=5000)
