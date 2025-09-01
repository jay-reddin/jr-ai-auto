"""
Advanced memory management and optimization system for JR AI Control.
Handles memory pressure, garbage collection optimization, and long-running session management.
"""

import gc
import threading
import time
import weakref
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable, Set
from collections import deque
import os

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

class MemoryPressureMonitor:
    """Monitor system memory pressure and trigger optimizations"""
    
    def __init__(self):
        self.monitoring_active = False
        self.monitoring_thread = None
        self.callbacks = []
        
        # Memory thresholds (in MB)
        self.warning_threshold = 400
        self.critical_threshold = 600
        self.emergency_threshold = 800
        
        # Monitoring interval
        self.check_interval = 5.0  # seconds
        
        # Memory history for trend analysis
        self.memory_history = deque(maxlen=60)  # 5 minutes of history
        
        # Pressure levels
        self.current_pressure = 'normal'
        self.pressure_history = deque(maxlen=20)
    
    def start_monitoring(self):
        """Start memory pressure monitoring"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            daemon=True
        )
        self.monitoring_thread.start()
    
    def stop_monitoring(self):
        """Stop memory pressure monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=2.0)
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Get current memory usage
                memory_mb = self._get_memory_usage()
                
                if memory_mb is not None:
                    # Store in history
                    self.memory_history.append({
                        'timestamp': datetime.now(),
                        'memory_mb': memory_mb
                    })
                    
                    # Determine pressure level
                    pressure_level = self._calculate_pressure_level(memory_mb)
                    
                    # Check for pressure level change
                    if pressure_level != self.current_pressure:
                        self._handle_pressure_change(self.current_pressure, pressure_level, memory_mb)
                        self.current_pressure = pressure_level
                    
                    # Store pressure history
                    self.pressure_history.append({
                        'timestamp': datetime.now(),
                        'pressure': pressure_level,
                        'memory_mb': memory_mb
                    })
                
                time.sleep(self.check_interval)
                
            except Exception as e:
                print(f"Error in memory pressure monitoring: {e}")
                time.sleep(self.check_interval * 2)
    
    def _get_memory_usage(self) -> Optional[float]:
        """Get current memory usage in MB"""
        if PSUTIL_AVAILABLE:
            try:
                process = psutil.Process()
                return process.memory_info().rss / 1024 / 1024
            except:
                pass
        return None
    
    def _calculate_pressure_level(self, memory_mb: float) -> str:
        """Calculate memory pressure level"""
        if memory_mb >= self.emergency_threshold:
            return 'emergency'
        elif memory_mb >= self.critical_threshold:
            return 'critical'
        elif memory_mb >= self.warning_threshold:
            return 'warning'
        else:
            return 'normal'
    
    def _handle_pressure_change(self, old_level: str, new_level: str, memory_mb: float):
        """Handle memory pressure level change"""
        print(f"Memory pressure changed: {old_level} -> {new_level} ({memory_mb:.1f}MB)")
        
        # Notify callbacks
        for callback in self.callbacks:
            try:
                callback('pressure_change', {
                    'old_level': old_level,
                    'new_level': new_level,
                    'memory_mb': memory_mb
                })
            except Exception as e:
                print(f"Error in memory pressure callback: {e}")
    
    def add_callback(self, callback: Callable):
        """Add callback for memory pressure events"""
        if callback not in self.callbacks:
            self.callbacks.append(callback)
    
    def get_memory_trend(self) -> str:
        """Get memory usage trend"""
        if len(self.memory_history) < 10:
            return 'stable'
        
        recent = list(self.memory_history)[-10:]
        older = list(self.memory_history)[-20:-10] if len(self.memory_history) >= 20 else recent[:5]
        
        recent_avg = sum(entry['memory_mb'] for entry in recent) / len(recent)
        older_avg = sum(entry['memory_mb'] for entry in older) / len(older)
        
        diff_percent = ((recent_avg - older_avg) / older_avg) * 100
        
        if diff_percent > 10:
            return 'increasing'
        elif diff_percent < -10:
            return 'decreasing'
        else:
            return 'stable'
    
    def get_pressure_stats(self) -> Dict[str, Any]:
        """Get memory pressure statistics"""
        return {
            'current_pressure': self.current_pressure,
            'current_memory_mb': self._get_memory_usage(),
            'memory_trend': self.get_memory_trend(),
            'warning_threshold': self.warning_threshold,
            'critical_threshold': self.critical_threshold,
            'emergency_threshold': self.emergency_threshold,
            'history_length': len(self.memory_history)
        }

class ObjectTracker:
    """Track and manage object lifecycle for memory optimization"""
    
    def __init__(self):
        # Weak references to tracked objects
        self.tracked_objects = weakref.WeakSet()
        
        # Object type counters
        self.object_counts = {}
        
        # Large object tracking (objects > 1MB)
        self.large_objects = weakref.WeakKeyDictionary()
        
        # Cleanup callbacks
        self.cleanup_callbacks = {}
    
    def track_object(self, obj, object_type: str = None, size_hint: int = 0):
        """Track an object for memory management"""
        try:
            self.tracked_objects.add(obj)
            
            # Update type counter
            if object_type:
                self.object_counts[object_type] = self.object_counts.get(object_type, 0) + 1
            
            # Track large objects
            if size_hint > 1024 * 1024:  # > 1MB
                self.large_objects[obj] = {
                    'type': object_type or type(obj).__name__,
                    'size_hint': size_hint,
                    'created_at': datetime.now()
                }
            
        except TypeError:
            # Object doesn't support weak references
            pass
    
    def register_cleanup_callback(self, object_type: str, callback: Callable):
        """Register cleanup callback for specific object type"""
        if object_type not in self.cleanup_callbacks:
            self.cleanup_callbacks[object_type] = []
        self.cleanup_callbacks[object_type].append(callback)
    
    def cleanup_objects(self, object_type: str = None) -> int:
        """Cleanup objects of specific type or all objects"""
        cleaned_count = 0
        
        if object_type and object_type in self.cleanup_callbacks:
            # Call specific cleanup callbacks
            for callback in self.cleanup_callbacks[object_type]:
                try:
                    result = callback()
                    if isinstance(result, int):
                        cleaned_count += result
                except Exception as e:
                    print(f"Error in cleanup callback for {object_type}: {e}")
        else:
            # General cleanup - call all callbacks
            for obj_type, callbacks in self.cleanup_callbacks.items():
                for callback in callbacks:
                    try:
                        result = callback()
                        if isinstance(result, int):
                            cleaned_count += result
                    except Exception as e:
                        print(f"Error in cleanup callback for {obj_type}: {e}")
        
        return cleaned_count
    
    def get_object_stats(self) -> Dict[str, Any]:
        """Get object tracking statistics"""
        return {
            'tracked_objects': len(self.tracked_objects),
            'object_counts': self.object_counts.copy(),
            'large_objects': len(self.large_objects),
            'cleanup_callbacks': {k: len(v) for k, v in self.cleanup_callbacks.items()}
        }

class GarbageCollectionOptimizer:
    """Optimize garbage collection for better performance"""
    
    def __init__(self):
        # GC statistics
        self.gc_stats = {
            'collections': deque(maxlen=100),
            'collection_times': deque(maxlen=100)
        }
        
        # Optimization settings
        self.auto_optimize = True
        self.optimization_interval = timedelta(minutes=2)
        self.last_optimization = datetime.now()
        
        # Adaptive thresholds
        self.adaptive_thresholds = True
        self.base_thresholds = (700, 10, 10)
        self.current_thresholds = self.base_thresholds
    
    def optimize_gc_settings(self) -> Dict[str, Any]:
        """Optimize garbage collection settings"""
        optimization_start = time.time()
        results = {
            'timestamp': datetime.now().isoformat(),
            'collections_performed': [],
            'threshold_changes': [],
            'objects_collected': 0,
            'duration': 0
        }
        
        try:
            # Get initial GC stats
            initial_counts = gc.get_count()
            
            # Perform garbage collection for all generations
            for generation in range(3):
                collected = gc.collect(generation)
                results['objects_collected'] += collected
                results['collections_performed'].append(f"Gen {generation}: {collected} objects")
            
            # Optimize thresholds if adaptive mode is enabled
            if self.adaptive_thresholds:
                new_thresholds = self._calculate_adaptive_thresholds()
                if new_thresholds != self.current_thresholds:
                    gc.set_threshold(*new_thresholds)
                    results['threshold_changes'].append(f"Updated thresholds: {new_thresholds}")
                    self.current_thresholds = new_thresholds
            
            # Record collection statistics
            collection_time = time.time() - optimization_start
            self.gc_stats['collection_times'].append(collection_time)
            self.gc_stats['collections'].append({
                'timestamp': datetime.now(),
                'objects_collected': results['objects_collected'],
                'duration': collection_time
            })
            
        except Exception as e:
            results['error'] = str(e)
        
        results['duration'] = time.time() - optimization_start
        self.last_optimization = datetime.now()
        
        return results
    
    def _calculate_adaptive_thresholds(self) -> tuple:
        """Calculate adaptive GC thresholds based on collection history"""
        if len(self.gc_stats['collection_times']) < 10:
            return self.base_thresholds
        
        # Analyze recent collection performance
        recent_times = list(self.gc_stats['collection_times'])[-10:]
        avg_time = sum(recent_times) / len(recent_times)
        
        # Adjust thresholds based on collection performance
        gen0_threshold, gen1_threshold, gen2_threshold = self.base_thresholds
        
        if avg_time > 0.1:  # Slow collections
            # Increase thresholds to reduce collection frequency
            gen0_threshold = min(1000, int(gen0_threshold * 1.2))
            gen1_threshold = min(15, int(gen1_threshold * 1.1))
            gen2_threshold = min(15, int(gen2_threshold * 1.1))
        elif avg_time < 0.01:  # Fast collections
            # Decrease thresholds for more frequent cleanup
            gen0_threshold = max(500, int(gen0_threshold * 0.9))
            gen1_threshold = max(5, int(gen1_threshold * 0.9))
            gen2_threshold = max(5, int(gen2_threshold * 0.9))
        
        return (gen0_threshold, gen1_threshold, gen2_threshold)
    
    def should_optimize(self) -> bool:
        """Check if GC optimization should be performed"""
        if not self.auto_optimize:
            return False
        
        time_since_last = datetime.now() - self.last_optimization
        return time_since_last > self.optimization_interval
    
    def get_gc_stats(self) -> Dict[str, Any]:
        """Get garbage collection statistics"""
        current_counts = gc.get_count()
        current_thresholds = gc.get_threshold()
        
        stats = {
            'current_counts': current_counts,
            'current_thresholds': current_thresholds,
            'total_collections': len(self.gc_stats['collections']),
            'last_optimization': self.last_optimization.isoformat(),
            'adaptive_thresholds': self.adaptive_thresholds
        }
        
        if self.gc_stats['collection_times']:
            stats['average_collection_time'] = sum(self.gc_stats['collection_times']) / len(self.gc_stats['collection_times'])
            stats['recent_collections'] = list(self.gc_stats['collections'])[-5:]
        
        return stats

class MemoryOptimizer:
    """Main memory optimization coordinator"""
    
    def __init__(self):
        self.pressure_monitor = MemoryPressureMonitor()
        self.object_tracker = ObjectTracker()
        self.gc_optimizer = GarbageCollectionOptimizer()
        
        # Optimization callbacks
        self.optimization_callbacks = []
        
        # Session management
        self.session_start = datetime.now()
        self.optimization_history = deque(maxlen=50)
        
        # Setup pressure monitoring callbacks
        self.pressure_monitor.add_callback(self._handle_memory_pressure)
        
        # Component cleanup registry
        self.component_cleaners = {}
    
    def start_monitoring(self):
        """Start comprehensive memory monitoring"""
        self.pressure_monitor.start_monitoring()
    
    def stop_monitoring(self):
        """Stop memory monitoring"""
        self.pressure_monitor.stop_monitoring()
    
    def register_component_cleaner(self, component_name: str, cleaner_func: Callable):
        """Register a component-specific memory cleaner"""
        self.component_cleaners[component_name] = cleaner_func
    
    def _handle_memory_pressure(self, event_type: str, data: Dict[str, Any]):
        """Handle memory pressure events"""
        if event_type == 'pressure_change':
            new_level = data['new_level']
            memory_mb = data['memory_mb']
            
            print(f"Memory pressure: {new_level} ({memory_mb:.1f}MB)")
            
            # Trigger appropriate optimization based on pressure level
            if new_level == 'emergency':
                self.emergency_cleanup()
            elif new_level == 'critical':
                self.aggressive_cleanup()
            elif new_level == 'warning':
                self.standard_cleanup()
    
    def standard_cleanup(self) -> Dict[str, Any]:
        """Perform standard memory cleanup"""
        cleanup_start = time.time()
        results = {
            'timestamp': datetime.now().isoformat(),
            'cleanup_type': 'standard',
            'actions_performed': [],
            'memory_before_mb': 0,
            'memory_after_mb': 0,
            'duration': 0
        }
        
        try:
            # Get initial memory
            if PSUTIL_AVAILABLE:
                results['memory_before_mb'] = psutil.Process().memory_info().rss / 1024 / 1024
            
            # Standard garbage collection
            gc_results = self.gc_optimizer.optimize_gc_settings()
            if gc_results['objects_collected'] > 0:
                results['actions_performed'].append(f"GC collected {gc_results['objects_collected']} objects")
            
            # Component-specific cleanup
            for component_name, cleaner in self.component_cleaners.items():
                try:
                    cleaned = cleaner()
                    if cleaned and cleaned > 0:
                        results['actions_performed'].append(f"{component_name}: cleaned {cleaned} items")
                except Exception as e:
                    print(f"Error in {component_name} cleaner: {e}")
            
            # Get final memory
            if PSUTIL_AVAILABLE:
                results['memory_after_mb'] = psutil.Process().memory_info().rss / 1024 / 1024
            
        except Exception as e:
            results['error'] = str(e)
        
        results['duration'] = time.time() - cleanup_start
        self.optimization_history.append(results)
        
        # Notify callbacks
        for callback in self.optimization_callbacks:
            try:
                callback('cleanup_performed', results)
            except Exception as e:
                print(f"Error in optimization callback: {e}")
        
        return results
    
    def aggressive_cleanup(self) -> Dict[str, Any]:
        """Perform aggressive memory cleanup"""
        cleanup_start = time.time()
        results = {
            'timestamp': datetime.now().isoformat(),
            'cleanup_type': 'aggressive',
            'actions_performed': [],
            'memory_before_mb': 0,
            'memory_after_mb': 0,
            'duration': 0
        }
        
        try:
            # Get initial memory
            if PSUTIL_AVAILABLE:
                results['memory_before_mb'] = psutil.Process().memory_info().rss / 1024 / 1024
            
            # Multiple GC passes
            total_collected = 0
            for _ in range(3):
                gc_results = self.gc_optimizer.optimize_gc_settings()
                total_collected += gc_results['objects_collected']
                time.sleep(0.1)  # Brief pause between collections
            
            if total_collected > 0:
                results['actions_performed'].append(f"Aggressive GC collected {total_collected} objects")
            
            # Aggressive component cleanup
            for component_name, cleaner in self.component_cleaners.items():
                try:
                    cleaned = cleaner()
                    if cleaned and cleaned > 0:
                        results['actions_performed'].append(f"{component_name}: aggressively cleaned {cleaned} items")
                except Exception as e:
                    print(f"Error in aggressive {component_name} cleaner: {e}")
            
            # Object tracker cleanup
            cleaned_objects = self.object_tracker.cleanup_objects()
            if cleaned_objects > 0:
                results['actions_performed'].append(f"Object tracker cleaned {cleaned_objects} objects")
            
            # Get final memory
            if PSUTIL_AVAILABLE:
                results['memory_after_mb'] = psutil.Process().memory_info().rss / 1024 / 1024
            
        except Exception as e:
            results['error'] = str(e)
        
        results['duration'] = time.time() - cleanup_start
        self.optimization_history.append(results)
        
        return results
    
    def emergency_cleanup(self) -> Dict[str, Any]:
        """Perform emergency memory cleanup"""
        print("EMERGENCY MEMORY CLEANUP TRIGGERED")
        
        cleanup_start = time.time()
        results = {
            'timestamp': datetime.now().isoformat(),
            'cleanup_type': 'emergency',
            'actions_performed': [],
            'memory_before_mb': 0,
            'memory_after_mb': 0,
            'duration': 0
        }
        
        try:
            # Get initial memory
            if PSUTIL_AVAILABLE:
                results['memory_before_mb'] = psutil.Process().memory_info().rss / 1024 / 1024
            
            # Emergency GC - multiple aggressive passes
            total_collected = 0
            for generation in range(3):
                for _ in range(5):  # 5 passes per generation
                    collected = gc.collect(generation)
                    total_collected += collected
                    if collected == 0:
                        break  # No more objects to collect
            
            results['actions_performed'].append(f"Emergency GC collected {total_collected} objects")
            
            # Emergency component cleanup - call all cleaners multiple times
            for component_name, cleaner in self.component_cleaners.items():
                total_cleaned = 0
                for _ in range(3):  # Multiple cleanup passes
                    try:
                        cleaned = cleaner()
                        if cleaned and cleaned > 0:
                            total_cleaned += cleaned
                        else:
                            break  # No more to clean
                    except Exception as e:
                        print(f"Error in emergency {component_name} cleaner: {e}")
                        break
                
                if total_cleaned > 0:
                    results['actions_performed'].append(f"{component_name}: emergency cleaned {total_cleaned} items")
            
            # Clear all object tracking
            self.object_tracker = ObjectTracker()  # Reset tracker
            results['actions_performed'].append("Reset object tracker")
            
            # Force Python memory optimization
            try:
                # Try to return memory to OS (Python 3.8+)
                if hasattr(gc, 'collect'):
                    gc.collect()
                    gc.collect()  # Second pass
                results['actions_performed'].append("Forced memory return to OS")
            except:
                pass
            
            # Get final memory
            if PSUTIL_AVAILABLE:
                results['memory_after_mb'] = psutil.Process().memory_info().rss / 1024 / 1024
            
        except Exception as e:
            results['error'] = str(e)
        
        results['duration'] = time.time() - cleanup_start
        self.optimization_history.append(results)
        
        print(f"Emergency cleanup completed in {results['duration']:.2f}s")
        
        return results
    
    def get_memory_report(self) -> Dict[str, Any]:
        """Get comprehensive memory report"""
        session_duration = datetime.now() - self.session_start
        
        return {
            'session_duration_hours': session_duration.total_seconds() / 3600,
            'pressure_stats': self.pressure_monitor.get_pressure_stats(),
            'object_stats': self.object_tracker.get_object_stats(),
            'gc_stats': self.gc_optimizer.get_gc_stats(),
            'optimization_history': list(self.optimization_history)[-10:],  # Last 10 optimizations
            'registered_cleaners': list(self.component_cleaners.keys())
        }
    
    def add_optimization_callback(self, callback: Callable):
        """Add callback for optimization events"""
        if callback not in self.optimization_callbacks:
            self.optimization_callbacks.append(callback)

# Global memory optimizer instance
_memory_optimizer = None

def get_memory_optimizer() -> MemoryOptimizer:
    """Get the global memory optimizer instance"""
    global _memory_optimizer
    if _memory_optimizer is None:
        _memory_optimizer = MemoryOptimizer()
    return _memory_optimizer

def start_memory_monitoring():
    """Start global memory monitoring"""
    optimizer = get_memory_optimizer()
    optimizer.start_monitoring()

def register_component_cleaner(component_name: str, cleaner_func: Callable):
    """Register a component memory cleaner"""
    optimizer = get_memory_optimizer()
    optimizer.register_component_cleaner(component_name, cleaner_func)

def trigger_memory_cleanup(level: str = 'standard') -> Dict[str, Any]:
    """Trigger memory cleanup"""
    optimizer = get_memory_optimizer()
    
    if level == 'emergency':
        return optimizer.emergency_cleanup()
    elif level == 'aggressive':
        return optimizer.aggressive_cleanup()
    else:
        return optimizer.standard_cleanup()