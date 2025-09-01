"""
Performance monitoring and optimization system for JR AI Control.
Provides real-time performance metrics, memory management, and optimization tools.
"""

import time
import threading
import psutil
import gc
import weakref
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime, timedelta
from collections import deque
import json
import os

class PerformanceMetrics:
    """Collects and tracks performance metrics"""
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.metrics = {
            'cpu_usage': deque(maxlen=max_history),
            'memory_usage': deque(maxlen=max_history),
            'response_times': deque(maxlen=max_history),
            'ui_render_times': deque(maxlen=max_history),
            'voice_processing_times': deque(maxlen=max_history),
            'screenshot_processing_times': deque(maxlen=max_history),
            'token_processing_times': deque(maxlen=max_history)
        }
        self.timestamps = {
            'cpu_usage': deque(maxlen=max_history),
            'memory_usage': deque(maxlen=max_history),
            'response_times': deque(maxlen=max_history),
            'ui_render_times': deque(maxlen=max_history),
            'voice_processing_times': deque(maxlen=max_history),
            'screenshot_processing_times': deque(maxlen=max_history),
            'token_processing_times': deque(maxlen=max_history)
        }
        
        # Performance thresholds
        self.thresholds = {
            'cpu_usage': 80.0,  # %
            'memory_usage': 500.0,  # MB
            'response_time': 5.0,  # seconds
            'ui_render_time': 0.1,  # seconds
            'voice_processing_time': 0.5,  # seconds
            'screenshot_processing_time': 2.0,  # seconds
        }
        
        # Monitoring state
        self.monitoring_active = False
        self.monitoring_thread = None
        self.callbacks = []
        
        # Process reference
        self.process = psutil.Process()
    
    def start_monitoring(self, interval: float = 1.0):
        """Start continuous performance monitoring"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(interval,),
            daemon=True
        )
        self.monitoring_thread.start()
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=2.0)
    
    def _monitoring_loop(self, interval: float):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Collect system metrics
                cpu_percent = self.process.cpu_percent()
                memory_mb = self.process.memory_info().rss / 1024 / 1024
                
                # Store metrics with timestamps
                now = datetime.now()
                self.metrics['cpu_usage'].append(cpu_percent)
                self.timestamps['cpu_usage'].append(now)
                
                self.metrics['memory_usage'].append(memory_mb)
                self.timestamps['memory_usage'].append(now)
                
                # Check thresholds and trigger callbacks
                self._check_thresholds(cpu_percent, memory_mb)
                
                time.sleep(interval)
                
            except Exception as e:
                print(f"Error in performance monitoring: {e}")
                time.sleep(interval)
    
    def _check_thresholds(self, cpu_percent: float, memory_mb: float):
        """Check if performance thresholds are exceeded"""
        alerts = []
        
        if cpu_percent > self.thresholds['cpu_usage']:
            alerts.append(('cpu_usage', cpu_percent, self.thresholds['cpu_usage']))
        
        if memory_mb > self.thresholds['memory_usage']:
            alerts.append(('memory_usage', memory_mb, self.thresholds['memory_usage']))
        
        # Notify callbacks of alerts
        for alert in alerts:
            for callback in self.callbacks:
                try:
                    callback('threshold_exceeded', alert)
                except Exception as e:
                    print(f"Error in performance callback: {e}")
    
    def record_timing(self, metric_name: str, duration: float):
        """Record a timing metric"""
        if metric_name in self.metrics:
            self.metrics[metric_name].append(duration)
            self.timestamps[metric_name].append(datetime.now())
            
            # Check timing thresholds
            threshold_key = metric_name.replace('_times', '_time')
            if threshold_key in self.thresholds:
                if duration > self.thresholds[threshold_key]:
                    for callback in self.callbacks:
                        try:
                            callback('timing_threshold_exceeded', 
                                   (metric_name, duration, self.thresholds[threshold_key]))
                        except Exception as e:
                            print(f"Error in timing callback: {e}")
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        try:
            return {
                'cpu_usage': self.process.cpu_percent(),
                'memory_usage_mb': self.process.memory_info().rss / 1024 / 1024,
                'memory_usage_percent': self.process.memory_percent(),
                'thread_count': self.process.num_threads(),
                'open_files': len(self.process.open_files()),
                'connections': len(self.process.connections()),
            }
        except Exception as e:
            print(f"Error getting current metrics: {e}")
            return {}
    
    def get_average_metrics(self, minutes: int = 5) -> Dict[str, float]:
        """Get average metrics for the last N minutes"""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        averages = {}
        
        for metric_name, values in self.metrics.items():
            timestamps = self.timestamps[metric_name]
            
            # Filter values within time window
            recent_values = [
                value for value, timestamp in zip(values, timestamps)
                if timestamp >= cutoff_time
            ]
            
            if recent_values:
                averages[metric_name] = sum(recent_values) / len(recent_values)
            else:
                averages[metric_name] = 0.0
        
        return averages
    
    def add_callback(self, callback: Callable):
        """Add performance monitoring callback"""
        if callback not in self.callbacks:
            self.callbacks.append(callback)
    
    def remove_callback(self, callback: Callable):
        """Remove performance monitoring callback"""
        if callback in self.callbacks:
            self.callbacks.remove(callback)
    
    def export_metrics(self, filepath: str):
        """Export metrics to JSON file"""
        try:
            export_data = {
                'timestamp': datetime.now().isoformat(),
                'current_metrics': self.get_current_metrics(),
                'average_metrics_5min': self.get_average_metrics(5),
                'thresholds': self.thresholds,
                'history_length': {name: len(values) for name, values in self.metrics.items()}
            }
            
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error exporting metrics: {e}")
            return False

class MemoryManager:
    """Advanced memory management and optimization"""
    
    def __init__(self):
        self.weak_references = weakref.WeakSet()
        self.cleanup_callbacks = []
        self.last_cleanup = datetime.now()
        self.cleanup_interval = timedelta(minutes=5)
        
        # Memory thresholds
        self.memory_warning_threshold = 400  # MB
        self.memory_critical_threshold = 600  # MB
        
        # Cache management
        self.caches = {}
        self.cache_limits = {}
    
    def register_object(self, obj):
        """Register an object for memory tracking"""
        try:
            self.weak_references.add(obj)
        except TypeError:
            # Object doesn't support weak references
            pass
    
    def register_cache(self, name: str, cache_dict: dict, max_size: int = 100):
        """Register a cache for automatic management"""
        self.caches[name] = cache_dict
        self.cache_limits[name] = max_size
    
    def cleanup_caches(self):
        """Clean up registered caches"""
        cleaned_items = 0
        
        for name, cache in self.caches.items():
            max_size = self.cache_limits.get(name, 100)
            
            if len(cache) > max_size:
                # Remove oldest items (assuming dict maintains insertion order)
                items_to_remove = len(cache) - max_size
                keys_to_remove = list(cache.keys())[:items_to_remove]
                
                for key in keys_to_remove:
                    cache.pop(key, None)
                    cleaned_items += 1
        
        return cleaned_items
    
    def force_garbage_collection(self):
        """Force garbage collection and return collected objects"""
        collected = gc.collect()
        return collected
    
    def get_memory_usage(self) -> Dict[str, float]:
        """Get detailed memory usage information"""
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            
            return {
                'rss_mb': memory_info.rss / 1024 / 1024,
                'vms_mb': memory_info.vms / 1024 / 1024,
                'percent': process.memory_percent(),
                'available_mb': psutil.virtual_memory().available / 1024 / 1024,
                'total_mb': psutil.virtual_memory().total / 1024 / 1024
            }
        except Exception as e:
            print(f"Error getting memory usage: {e}")
            return {}
    
    def check_memory_pressure(self) -> str:
        """Check current memory pressure level"""
        memory_usage = self.get_memory_usage()
        rss_mb = memory_usage.get('rss_mb', 0)
        
        if rss_mb > self.memory_critical_threshold:
            return 'critical'
        elif rss_mb > self.memory_warning_threshold:
            return 'warning'
        else:
            return 'normal'
    
    def optimize_memory(self) -> Dict[str, int]:
        """Perform comprehensive memory optimization"""
        results = {
            'caches_cleaned': 0,
            'objects_collected': 0,
            'memory_freed_mb': 0
        }
        
        # Get initial memory usage
        initial_memory = self.get_memory_usage().get('rss_mb', 0)
        
        # Clean up caches
        results['caches_cleaned'] = self.cleanup_caches()
        
        # Force garbage collection
        results['objects_collected'] = self.force_garbage_collection()
        
        # Get final memory usage
        final_memory = self.get_memory_usage().get('rss_mb', 0)
        results['memory_freed_mb'] = max(0, initial_memory - final_memory)
        
        # Update last cleanup time
        self.last_cleanup = datetime.now()
        
        # Notify cleanup callbacks
        for callback in self.cleanup_callbacks:
            try:
                callback(results)
            except Exception as e:
                print(f"Error in cleanup callback: {e}")
        
        return results
    
    def should_cleanup(self) -> bool:
        """Check if automatic cleanup should be performed"""
        time_since_cleanup = datetime.now() - self.last_cleanup
        memory_pressure = self.check_memory_pressure()
        
        return (time_since_cleanup > self.cleanup_interval or 
                memory_pressure in ['warning', 'critical'])
    
    def add_cleanup_callback(self, callback: Callable):
        """Add callback for cleanup events"""
        if callback not in self.cleanup_callbacks:
            self.cleanup_callbacks.append(callback)

class PerformanceOptimizer:
    """Main performance optimization coordinator"""
    
    def __init__(self):
        self.metrics = PerformanceMetrics()
        self.memory_manager = MemoryManager()
        self.optimization_callbacks = []
        
        # Optimization settings
        self.auto_optimize = True
        self.optimization_interval = timedelta(minutes=10)
        self.last_optimization = datetime.now()
        
        # Performance tracking
        self.optimization_history = deque(maxlen=50)
        
        # Setup monitoring callbacks
        self.metrics.add_callback(self._handle_performance_alert)
        self.memory_manager.add_cleanup_callback(self._handle_memory_cleanup)
    
    def start_monitoring(self):
        """Start comprehensive performance monitoring"""
        self.metrics.start_monitoring()
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.metrics.stop_monitoring()
    
    def _handle_performance_alert(self, alert_type: str, data: Any):
        """Handle performance alerts"""
        if alert_type == 'threshold_exceeded':
            metric_name, value, threshold = data
            print(f"Performance alert: {metric_name} = {value:.2f} (threshold: {threshold:.2f})")
            
            # Trigger optimization if needed
            if self.auto_optimize:
                self.optimize_performance()
        
        elif alert_type == 'timing_threshold_exceeded':
            metric_name, duration, threshold = data
            print(f"Timing alert: {metric_name} = {duration:.3f}s (threshold: {threshold:.3f}s)")
    
    def _handle_memory_cleanup(self, results: Dict[str, int]):
        """Handle memory cleanup results"""
        print(f"Memory cleanup: {results['caches_cleaned']} caches cleaned, "
              f"{results['objects_collected']} objects collected, "
              f"{results['memory_freed_mb']:.1f}MB freed")
    
    def optimize_performance(self) -> Dict[str, Any]:
        """Perform comprehensive performance optimization"""
        optimization_start = time.time()
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'memory_optimization': {},
            'performance_improvements': [],
            'duration': 0
        }
        
        # Memory optimization
        if self.memory_manager.should_cleanup():
            results['memory_optimization'] = self.memory_manager.optimize_memory()
        
        # Additional optimizations can be added here
        # - UI component cleanup
        # - Cache optimization
        # - Thread pool management
        
        # Record optimization duration
        results['duration'] = time.time() - optimization_start
        
        # Store in history
        self.optimization_history.append(results)
        self.last_optimization = datetime.now()
        
        # Notify callbacks
        for callback in self.optimization_callbacks:
            try:
                callback(results)
            except Exception as e:
                print(f"Error in optimization callback: {e}")
        
        return results
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        return {
            'current_metrics': self.metrics.get_current_metrics(),
            'average_metrics_5min': self.metrics.get_average_metrics(5),
            'memory_usage': self.memory_manager.get_memory_usage(),
            'memory_pressure': self.memory_manager.check_memory_pressure(),
            'optimization_history': list(self.optimization_history)[-10:],  # Last 10 optimizations
            'monitoring_active': self.metrics.monitoring_active,
            'last_optimization': self.last_optimization.isoformat()
        }
    
    def add_optimization_callback(self, callback: Callable):
        """Add callback for optimization events"""
        if callback not in self.optimization_callbacks:
            self.optimization_callbacks.append(callback)
    
    def time_operation(self, operation_name: str):
        """Context manager for timing operations"""
        return TimingContext(self.metrics, operation_name)

class TimingContext:
    """Context manager for timing operations"""
    
    def __init__(self, metrics: PerformanceMetrics, operation_name: str):
        self.metrics = metrics
        self.operation_name = operation_name
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration = time.time() - self.start_time
            self.metrics.record_timing(self.operation_name, duration)

# Global performance optimizer instance
_performance_optimizer = None

def get_performance_optimizer() -> PerformanceOptimizer:
    """Get the global performance optimizer instance"""
    global _performance_optimizer
    if _performance_optimizer is None:
        _performance_optimizer = PerformanceOptimizer()
    return _performance_optimizer

def start_performance_monitoring():
    """Start global performance monitoring"""
    optimizer = get_performance_optimizer()
    optimizer.start_monitoring()

def stop_performance_monitoring():
    """Stop global performance monitoring"""
    optimizer = get_performance_optimizer()
    optimizer.stop_monitoring()

def optimize_performance() -> Dict[str, Any]:
    """Trigger global performance optimization"""
    optimizer = get_performance_optimizer()
    return optimizer.optimize_performance()

def get_performance_report() -> Dict[str, Any]:
    """Get global performance report"""
    optimizer = get_performance_optimizer()
    return optimizer.get_performance_report()