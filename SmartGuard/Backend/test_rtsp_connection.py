# test_rtsp_connection.py
import cv2
import time
from services.stream_notifier import StreamNotifier
from config.settings import settings

def test_rtsp_connection():
    """Test basic RTSP connection to verify stream is accessible"""
    
    # RTSP Stream Configuration
    rtsp_url = "rtsp://admin:CJNAKZ@192.168.1.5:554/h264/ch1/main/av_stream"
    video_id = "test_cam1"
    
    print(f"Testing RTSP connection to: {rtsp_url}")
    
    # Initialize notifier
    stream_notifier = StreamNotifier(webhook_url=settings.WEBHOOK_URL)
    
    # Configure RTSP stream with optimal settings
    cap = cv2.VideoCapture(rtsp_url)
    
    # Set RTSP-specific properties for better performance
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer size for lower latency
    cap.set(cv2.CAP_PROP_FPS, 15)        # Set FPS to 15 for RTSP streams
    # cap.set(cv2.CAP_PROP_TIMEOUT, 10000) # 10 second timeout (not supported in all OpenCV versions)
    
    if not cap.isOpened():
        print("Error: Cannot open RTSP video source")
        stream_notifier.notify_connection_lost(rtsp_url, video_id)
        return False
    
    print("RTSP connection successful! Testing frame capture...")
    stream_notifier.notify_connection_restored(rtsp_url, video_id)
    
    # Test capturing a few frames
    frame_count = 0
    max_frames = 10
    
    try:
        for i in range(max_frames):
            ret, frame = cap.read()
            if not ret or frame is None:
                print(f"Failed to capture frame {i+1}")
                break
            
            frame_count += 1
            print(f"Successfully captured frame {frame_count}/{max_frames}")
            
            # Get frame info
            height, width = frame.shape[:2]
            print(f"Frame dimensions: {width}x{height}")
            
            # Small delay between frames
            time.sleep(0.1)
            
    except Exception as e:
        print(f"Error during frame capture: {e}")
        stream_notifier.notify_inference_error(rtsp_url, video_id, str(e))
        return False
    
    finally:
        cap.release()
    
    if frame_count > 0:
        print(f"RTSP connection test successful! Captured {frame_count} frames")
        return True
    else:
        print("RTSP connection test failed - no frames captured")
        return False

if __name__ == "__main__":
    print("Starting RTSP connection test...")
    success = test_rtsp_connection()
    
    if success:
        print("RTSP connection test PASSED")
        print("You can now run the main stream processor with: python run_stream.py")
    else:
        print("RTSP connection test FAILED")
        print("Please check:")
        print("1. Network connectivity to 192.168.1.x")
        print("2. Camera credentials (admin:CJNAKZ)")
        print("3. Camera RTSP configuration")
        print("4. Firewall settings")
