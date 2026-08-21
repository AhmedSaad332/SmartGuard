# start_backend_single_terminal.py
import threading
from run_stream import process_video_stream_debug

import uvicorn
import time
import asyncio

import shared_state

# RTSP Stream Configuration
VIDEO_SOURCE = "rtsp://admin:CJNAKZ@192.168.1.5:554/h264/ch1/main/av_stream"
VIDEO_ID = "rtsp_cam1"

def run_backend():
    shared_state.loop = asyncio.new_event_loop()
    asyncio.set_event_loop(shared_state.loop)
    config = uvicorn.Config("main:app", host="127.0.0.1", port=8001, loop="asyncio")
    server = uvicorn.Server(config)
    shared_state.loop.run_until_complete(server.serve())

def run_stream():
    time.sleep(3)  # Increased wait time for backend and event loop to initialize
    print("Starting RTSP stream processor with live detection...")
    try:
        process_video_stream_debug(video_source=VIDEO_SOURCE, video_id=VIDEO_ID, show_window=False)
    except Exception as e:
        print("Error in RTSP video stream:", e)

if __name__ == "__main__":
    # Run backend in a daemon thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()

    # Run video stream in main thread
    stream_thread = threading.Thread(target=run_stream)
    stream_thread.start()

    # Wait for threads
    backend_thread.join()
    stream_thread.join()
