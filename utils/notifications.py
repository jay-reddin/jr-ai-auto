#!/usr/bin/env python3
"""
JR AI Control - Notification System
Handles system notifications for task completion and progress updates
"""

import threading
import time
import queue
from datetime import datetime
from typing import Optional, Dict, List
import json
import os

try:
    from plyer import notification
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False

try:
    from win10toast import ToastNotifier
    WIN10TOAST_AVAILABLE = True
except ImportError:
    WIN10TOAST_AVAILABLE = False

class NotificationManager:
    """Manages system notifications for JR AI Control"""
    
    def __init__(self):
        self.enabled = True
        self.notification_queue = queue.Queue()
        self.notification_history = []
        self.max_history = 100
        
        # Initialize notification system
        self.toaster = None
        if WIN10TOAST_AVAILABLE:
            try:
                self.toaster = ToastNotifier()
            except Exception as e:
                print(f"Error initializing Windows toast notifications: {e}")
        
        # Notification worker thread
        self.worker_thread = None
        self.worker_running = False
        
        # Load settings
        self.load_notification_settings()
        
        # Start worker thread
        self.start_worker()
    
    def start_worker(self):
        """Start the notification worker thread"""
        if self.worker_thread and self.worker_thread.is_alive():
            return
        
        self.worker_running = True
        self.worker_thread = threading.Thread(target=self._notification_worker, daemon=True)
        self.worker_thread.start()
    
    def _notification_worker(self):
        """Worker thread to process notification queue"""
        while self.worker_running:
            try:
                # Get notification from queue with timeout
                notification_data = self.notification_queue.get(timeout=1)
                
                if notification_data and self.enabled:
                    self._show_system_notification(notification_data)
                
                self.notification_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Notification worker error: {e}")
    
    def _show_system_notification(self, notification_data: Dict):
        """Show system notification using available method"""
        title = notification_data.get('title', 'JR AI Control')
        message = notification_data.get('message', '')
        duration = notification_data.get('duration', 5)
        icon = notification_data.get('icon', None)
        
        try:
            # Try Windows 10 toast notification first
            if self.toaster and WIN10TOAST_AVAILABLE:
                self.toaster.show_toast(
                    title=title,
                    msg=message,
                    duration=duration,
                    icon_path=icon,
                    threaded=True
                )
            
            # Fallback to plyer notification
            elif PLYER_AVAILABLE:
                notification.notify(
                    title=title,
                    message=message,
                    timeout=duration,
                    app_icon=icon
                )
            
            # Fallback to console output
            else:
                print(f"NOTIFICATION: {title} - {message}")
            
            # Add to history
            self._add_to_history(notification_data)
            
        except Exception as e:
            print(f"Error showing notification: {e}")
            # Fallback to console
            print(f"NOTIFICATION: {title} - {message}")
    
    def _add_to_history(self, notification_data: Dict):
        """Add notification to history"""
        notification_data['timestamp'] = datetime.now().isoformat()
        self.notification_history.append(notification_data)
        
        # Limit history size
        if len(self.notification_history) > self.max_history:
            self.notification_history = self.notification_history[-self.max_history:]
    
    def show_task_completion(self, task_name: str, details: str = "", 
                           duration: int = 5, priority: bool = False):
        """Show task completion notification"""
        notification_data = {
            'type': 'task_completion',
            'title': 'Task Completed',
            'message': f"{task_name}\n{details}" if details else task_name,
            'duration': duration,
            'priority': priority
        }
        
        self.queue_notification(notification_data, priority)
    
    def show_progress_update(self, progress: int, message: str, 
                           duration: int = 3, priority: bool = False):
        """Show progress update notification"""
        notification_data = {
            'type': 'progress_update',
            'title': f'Progress: {progress}%',
            'message': message,
            'duration': duration,
            'priority': priority
        }
        
        self.queue_notification(notification_data, priority)
    
    def show_error_notification(self, error_message: str, 
                              duration: int = 8, priority: bool = True):
        """Show error notification"""
        notification_data = {
            'type': 'error',
            'title': 'Error - JR AI Control',
            'message': error_message,
            'duration': duration,
            'priority': priority
        }
        
        self.queue_notification(notification_data, priority)
    
    def show_info_notification(self, title: str, message: str, 
                             duration: int = 5, priority: bool = False):
        """Show general information notification"""
        notification_data = {
            'type': 'info',
            'title': title,
            'message': message,
            'duration': duration,
            'priority': priority
        }
        
        self.queue_notification(notification_data, priority)
    
    def show_voice_status(self, status: str, duration: int = 3):
        """Show voice system status notification"""
        notification_data = {
            'type': 'voice_status',
            'title': 'Voice System',
            'message': status,
            'duration': duration,
            'priority': False
        }
        
        self.queue_notification(notification_data)
    
    def show_token_usage_alert(self, tokens_used: int, total_tokens: int, 
                             threshold: int = 10000):
        """Show token usage alert when threshold is reached"""
        if total_tokens >= threshold:
            notification_data = {
                'type': 'token_alert',
                'title': 'Token Usage Alert',
                'message': f'Total tokens used: {total_tokens:,}\nSession: {tokens_used:,}',
                'duration': 6,
                'priority': False
            }
            
            self.queue_notification(notification_data)
    
    def queue_notification(self, notification_data: Dict, priority: bool = False):
        """Add notification to queue"""
        if not self.enabled:
            return
        
        if priority:
            # For priority notifications, clear non-priority items from queue
            temp_queue = queue.Queue()
            while not self.notification_queue.empty():
                try:
                    item = self.notification_queue.get_nowait()
                    if item.get('priority', False):
                        temp_queue.put(item)
                except queue.Empty:
                    break
            
            # Put priority items back
            while not temp_queue.empty():
                try:
                    self.notification_queue.put(temp_queue.get_nowait())
                except queue.Empty:
                    break
        
        # Add new notification
        self.notification_queue.put(notification_data)
    
    def clear_queue(self):
        """Clear all pending notifications"""
        while not self.notification_queue.empty():
            try:
                self.notification_queue.get_nowait()
            except queue.Empty:
                break
    
    def toggle_notifications(self, enabled: bool):
        """Enable or disable notifications"""
        self.enabled = enabled
        
        if not enabled:
            self.clear_queue()
        
        self.save_notification_settings()
    
    def get_notification_history(self, limit: int = 20) -> List[Dict]:
        """Get recent notification history"""
        return self.notification_history[-limit:] if limit > 0 else self.notification_history
    
    def clear_history(self):
        """Clear notification history"""
        self.notification_history = []
    
    def get_statistics(self) -> Dict:
        """Get notification statistics"""
        if not self.notification_history:
            return {
                'total_notifications': 0,
                'by_type': {},
                'recent_count': 0
            }
        
        # Count by type
        type_counts = {}
        recent_count = 0
        recent_cutoff = datetime.now().timestamp() - (24 * 3600)  # Last 24 hours
        
        for notification in self.notification_history:
            notif_type = notification.get('type', 'unknown')
            type_counts[notif_type] = type_counts.get(notif_type, 0) + 1
            
            # Count recent notifications
            try:
                notif_time = datetime.fromisoformat(notification['timestamp']).timestamp()
                if notif_time >= recent_cutoff:
                    recent_count += 1
            except (KeyError, ValueError):
                pass
        
        return {
            'total_notifications': len(self.notification_history),
            'by_type': type_counts,
            'recent_count': recent_count
        }
    
    def test_notification(self):
        """Test the notification system"""
        test_notification = {
            'type': 'test',
            'title': 'JR AI Control - Test',
            'message': 'Notification system is working correctly!',
            'duration': 5,
            'priority': True
        }
        
        self.queue_notification(test_notification, priority=True)
        return "Test notification queued"
    
    def load_notification_settings(self):
        """Load notification settings from config"""
        try:
            config_path = 'config.json'
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                notification_config = config.get('notification_settings', {})
                self.enabled = notification_config.get('enabled', True)
                
        except Exception as e:
            print(f"Error loading notification settings: {e}")
    
    def save_notification_settings(self):
        """Save notification settings to config"""
        try:
            config_path = 'config.json'
            config = {}
            
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
            
            config['notification_settings'] = {
                'enabled': self.enabled
            }
            
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
                
        except Exception as e:
            print(f"Error saving notification settings: {e}")
    
    def cleanup(self):
        """Cleanup notification resources"""
        self.worker_running = False
        self.clear_queue()
        
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=2)

# Global notification manager instance
_notification_manager = None

def get_notification_manager() -> NotificationManager:
    """Get the global notification manager instance"""
    global _notification_manager
    if _notification_manager is None:
        _notification_manager = NotificationManager()
    return _notification_manager