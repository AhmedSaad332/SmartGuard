import cv2
import numpy as np
import tempfile
import datetime
import time
import shared_state
import os
from utils.preprocessing import preprocess_video
from shared_state import latest_pred
from services.frame_store import set_jpeg
from models.abnormal_model import AbnormalModel

def process_video_stream_debug(video_source="rtsp://admin:CJNAKZ@192.168.1.5:554/h264/ch1/main/av_stream", video_id=None, show_window=False):
    """Debug version of video stream processor with console output"""
    global latest_pred

    if video_id is None:
        video_id = "rtsp_cam1"

    print(f"🔄 [DEBUG] Starting stream processing for: {video_id}")

    # Initialize model
    model = None
    max_retries = 3

    for attempt in range(max_retries):
        try:
            print(f"[DEBUG] Model loading attempt {attempt + 1}/{max_retries}")
            model = AbnormalModel()

            if model and model.load():
                print(f"[DEBUG] ✅ Model loaded successfully")
                break
            else:
                print(f"[DEBUG] ❌ Model loading failed")
                model = None
        except Exception as e:
            print(f"[DEBUG] Model error: {e}")
            model = None

    if model is None:
        print("[DEBUG] ⚠️  No model available - running in simulation mode")

    cap = None
    frame_count = 0
    frames = []

    print(f"[DEBUG] Attempting to connect to: {video_source}")

    while True:
        try:
            # Try to connect camera
            if cap is None:
                try:
                    cap = cv2.VideoCapture(video_source)
                    if cap.isOpened():
                        print("[DEBUG] ✅ Camera connected")
                        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                        cap.set(cv2.CAP_PROP_FPS, 15)
                    else:
                        print("[DEBUG] ❌ Camera connection failed")
                        cap = None
                        time.sleep(2)
                        continue
                except Exception as e:
                    print(f"[DEBUG] Camera error: {e}")
                    time.sleep(2)
                    continue

            # Read frame
            ret, frame = cap.read()
            if not ret or frame is None:
                print("[DEBUG] Lost frame - reconnecting...")
                cap.release()
                cap = None
                time.sleep(1)
                continue

            # Ensure consistent frame resolution (640x480)
            if frame.shape != (480, 640, 3):
                frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_AREA)

            frame_count += 1

            # Store frame for streaming
            try:
                ok, buf = cv2.imencode(".jpg", frame)
                if ok:
                    set_jpeg(buf.tobytes())
            except Exception as e:
                print(f"[DEBUG] Encoding error: {e}")

            frames.append(frame)

            # Run inference every 35 frames
            if len(frames) >= 35:
                print(f"[DEBUG] Processing 35 frames for inference...")

                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                    tmp_name = tmp.name
                    try:
                        out = cv2.VideoWriter(tmp_name, cv2.VideoWriter_fourcc(*'mp4v'), 10,
                                            (frames[0].shape[1], frames[0].shape[0]))
                        for f in frames:
                            out.write(f)
                        out.release()

                        with open(tmp_name, "rb") as f:
                            video_bytes = f.read()

                        frames_tensor = preprocess_video(video_bytes)

                        if model is not None:
                            confidence = model.predict(frames_tensor)
                            is_abnormal = confidence > model.adaptive_threshold
                            print(f"[DEBUG] Confidence: {confidence:.4f}, Threshold: {model.adaptive_threshold:.3f} → {'🚨 ABNORMAL' if is_abnormal else '✅ NORMAL'}")
                        else:
                            confidence = 0.0
                            is_abnormal = False
                            print(f"[DEBUG] No model - skipping inference")

                        latest_pred = f"{confidence:.3f} ({'ABNORMAL' if is_abnormal else 'NORMAL'})"

                    except Exception as e:
                        print(f"[DEBUG] Inference error: {e}")
                    finally:
                        if os.path.exists(tmp_name):
                            try:
                                os.remove(tmp_name)
                            except:
                                pass

                frames = []

            if show_window and frame is not None:
                cv2.imshow("Stream Debug", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            time.sleep(0.033)

        except KeyboardInterrupt:
            print("[DEBUG] Stream stopped by user")
            break
        except Exception as e:
            print(f"[DEBUG] Unexpected error: {e}")
            time.sleep(1)

    if cap:
        cap.release()
    if show_window:
        cv2.destroyAllWindows()

    print("[DEBUG] Stream processor stopped")
