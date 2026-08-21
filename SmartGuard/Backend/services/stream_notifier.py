# services/stream_notifier.py
import time
import json
from datetime import datetime
from typing import Optional, Dict, Any
from services.notifier import Notifier
from config.settings import settings

class StreamNotifier:
    """Enhanced notification system for RTSP stream events"""
    
    def __init__(self, webhook_url: Optional[str] = None):
        self.notifier = Notifier(webhook_url=webhook_url)
        self.last_notifications = {}  # Track last notification times by type
        self.notification_cooldowns = {
            'connection_lost': 300,      # 5 minutes
            'connection_restored': 60,    # 1 minute
            'abnormal_behavior': 60,     # 1 minute
            'inference_error': 180,       # 3 minutes
            'stream_started': 300,        # 5 minutes
            'stream_stopped': 60          # 1 minute
        }
        
    def _should_notify(self, notification_type: str) -> bool:
        """Check if enough time has passed since last notification of this type"""
        current_time = time.time()
        last_time = self.last_notifications.get(notification_type, 0)
        cooldown = self.notification_cooldowns.get(notification_type, 60)
        
        if current_time - last_time > cooldown:
            self.last_notifications[notification_type] = current_time
            return True
        return False
    
    def notify_stream_started(self, stream_url: str, video_id: str):
        """Send notification when stream starts successfully"""
        if self._should_notify('stream_started'):
            message = f"RTSP stream started successfully\nStream: {stream_url}\nCamera ID: {video_id}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            self.notifier.send_alert(message)
            print(f"Stream started notification sent for {video_id}")
    
    def notify_stream_stopped(self, stream_url: str, video_id: str, reason: str = "normal"):
        """Send notification when stream stops"""
        if self._should_notify('stream_stopped'):
            message = f"RTSP stream stopped\nStream: {stream_url}\nCamera ID: {video_id}\nReason: {reason}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            self.notifier.send_alert(message)
            print(f"Stream stopped notification sent for {video_id}")
    
    def notify_connection_lost(self, stream_url: str, video_id: str):
        """Send notification when connection to stream is lost"""
        if self._should_notify('connection_lost'):
            message = f"RTSP stream connection lost\nStream: {stream_url}\nCamera ID: {video_id}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nAction: Attempting to reconnect..."
            self.notifier.send_alert(message)
            print(f"Connection lost notification sent for {video_id}")
    
    def notify_connection_restored(self, stream_url: str, video_id: str):
        """Send notification when connection is restored"""
        if self._should_notify('connection_restored'):
            message = f"RTSP stream connection restored\nStream: {stream_url}\nCamera ID: {video_id}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            self.notifier.send_alert(message)
            print(f"Connection restored notification sent for {video_id}")
    
    def notify_abnormal_behavior(self, stream_url: str, video_id: str, confidence: float, additional_info: Optional[Dict[str, Any]] = None):
        """Send notification for abnormal behavior detection"""
        if self._should_notify('abnormal_behavior'):
            message = f"ABNORMAL BEHAVIOR DETECTED\nStream: {stream_url}\nCamera ID: {video_id}\nConfidence: {confidence:.2f}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            if additional_info:
                message += f"\nAdditional Info: {json.dumps(additional_info, indent=2)}"
            
            self.notifier.send_alert(message)
            print(f"Abnormal behavior notification sent for {video_id} (confidence: {confidence:.2f})")
    
    def notify_inference_error(self, stream_url: str, video_id: str, error_message: str):
        """Send notification for inference errors"""
        if self._should_notify('inference_error'):
            message = f"Inference error occurred\nStream: {stream_url}\nCamera ID: {video_id}\nError: {error_message}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            self.notifier.send_alert(message)
            print(f"Inference error notification sent for {video_id}")
    
    def notify_reconnection_failed(self, stream_url: str, video_id: str, attempt_count: int):
        """Send notification when reconnection attempts fail"""
        message = f"RTSP stream reconnection failed\nStream: {stream_url}\nCamera ID: {video_id}\nReconnection attempts: {attempt_count}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nAction: Manual intervention may be required"
        self.notifier.send_alert(message)
        print(f"Reconnection failed notification sent for {video_id} (attempts: {attempt_count})")
    
    def notify_frame_processing_stats(self, video_id: str, frames_processed: int, abnormal_detections: int, uptime_minutes: int):
        """Send periodic statistics about stream processing"""
        message = f"Stream Processing Statistics\nCamera ID: {video_id}\nFrames processed: {frames_processed}\nAbnormal detections: {abnormal_detections}\nUptime: {uptime_minutes} minutes\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self.notifier.send_alert(message)
        print(f"Statistics notification sent for {video_id}")
    
    def reset_cooldowns(self):
        """Reset all notification cooldowns (useful for testing)"""
        self.last_notifications.clear()
        print("All notification cooldowns reset")
