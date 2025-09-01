"""
Screenshot thumbnail management system for JR AI Control.
Handles thumbnail generation, storage, and retrieval.
"""

import os
import uuid
import time
import threading
from datetime import datetime
from PIL import Image
from typing import Dict, Tuple, Optional, Any
import json

class ScreenshotManager:
    """Manages screenshot thumbnails with configurable sizes and efficient storage."""
    
    # Thumbnail size configurations
    THUMBNAIL_SIZES = {
        'small': (100, 75),
        'medium': (150, 112),
        'large': (200, 150)
    }
    
    def __init__(self, screenshots_dir: str = "screenshots", default_size: str = "medium"):
        """
        Initialize the screenshot manager with enhanced performance optimization.
        
        Args:
            screenshots_dir: Directory to store screenshots and thumbnails
            default_size: Default thumbnail size ('small', 'medium', 'large')
        """
        self.screenshots_dir = screenshots_dir
        self.thumbnails_dir = os.path.join(screenshots_dir, "thumbnails")
        self.default_size = default_size
        self.metadata_file = os.path.join(screenshots_dir, "metadata.json")
        
        # Enhanced performance optimization: multi-level caches
        self.image_cache = {}  # Cache for loaded PIL images
        self.thumbnail_cache = {}  # Cache for thumbnail paths
        self.thumbnail_image_cache = {}  # Cache for loaded thumbnail images
        self.max_cache_size = 30  # Reduced for better memory management
        self.max_thumbnail_cache_size = 50  # Separate limit for thumbnails
        
        # Lazy loading support
        self.lazy_loading_enabled = True
        self.preload_queue = []
        self.preload_thread = None
        
        # Performance monitoring
        self.cache_hits = 0
        self.cache_misses = 0
        self.generation_times = []
        
        # Thread safety
        self._cache_lock = threading.Lock()
        
        # Create directories if they don't exist
        os.makedirs(self.screenshots_dir, exist_ok=True)
        os.makedirs(self.thumbnails_dir, exist_ok=True)
        
        # Load existing metadata
        self.metadata = self._load_metadata()
        
        # Start background preloading thread
        if self.lazy_loading_enabled:
            self._start_preload_thread()
    
    def _load_metadata(self) -> Dict:
        """Load screenshot metadata from JSON file."""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_metadata(self):
        """Save screenshot metadata to JSON file."""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save metadata: {e}")
    
    def generate_thumbnail(self, image_path: str, size: str = None) -> Optional[str]:
        """
        Generate a thumbnail from a screenshot image with enhanced performance optimization.
        
        Args:
            image_path: Path to the original screenshot
            size: Thumbnail size ('small', 'medium', 'large')
            
        Returns:
            Path to the generated thumbnail or None if failed
        """
        generation_start = time.time()
        
        if size is None:
            size = self.default_size
            
        if size not in self.THUMBNAIL_SIZES:
            print(f"Warning: Invalid thumbnail size '{size}', using '{self.default_size}'")
            size = self.default_size
        
        # Check cache first with thread safety
        cache_key = f"{image_path}_{size}"
        with self._cache_lock:
            if cache_key in self.thumbnail_cache:
                self.cache_hits += 1
                return self.thumbnail_cache[cache_key]
            self.cache_misses += 1
        
        try:
            # Load image with caching
            img = self._load_image_cached(image_path)
            if img is None:
                return None
            
            # Create thumbnail with optimized processing
            thumbnail_size = self.THUMBNAIL_SIZES[size]
            
            # Optimize thumbnail generation based on original image size and system performance
            original_size = img.size
            scale_factor = min(thumbnail_size[0] / original_size[0], 
                             thumbnail_size[1] / original_size[1])
            
            # Performance optimization: check system resources
            try:
                import psutil
                cpu_percent = psutil.cpu_percent(interval=None)
                memory_percent = psutil.virtual_memory().percent
                
                # Adjust processing based on system load
                if cpu_percent > 80 or memory_percent > 80:
                    # Use faster but lower quality processing under high load
                    resampling_method = Image.Resampling.BILINEAR
                    save_quality = 70 if size == 'small' else 80
                else:
                    # Use higher quality processing when system is not busy
                    resampling_method = Image.Resampling.LANCZOS
                    save_quality = 75 if size == 'small' else 85
            except ImportError:
                # Fallback if psutil not available
                resampling_method = Image.Resampling.LANCZOS
                save_quality = 75 if size == 'small' else 85
            
            # Skip processing if image is already small enough
            if scale_factor >= 0.9:
                thumbnail_img = img.copy()
            else:
                # Use optimized resampling for better performance
                new_size = (int(original_size[0] * scale_factor), 
                           int(original_size[1] * scale_factor))
                thumbnail_img = img.resize(new_size, resampling_method)
            
            # Generate unique filename for thumbnail
            screenshot_id = str(uuid.uuid4())
            thumbnail_filename = f"{screenshot_id}_{size}.jpg"
            thumbnail_path = os.path.join(self.thumbnails_dir, thumbnail_filename)
            
            # Save thumbnail with adaptive compression settings
            save_kwargs = {
                'format': 'JPEG',
                'quality': save_quality,
                'optimize': True,
                'progressive': True
            }
            
            # Additional quality adjustments based on size
            if size == 'large':
                save_kwargs['quality'] = min(90, save_quality + 10)
            
            thumbnail_img.save(thumbnail_path, **save_kwargs)
            
            # Store metadata with additional performance info
            generation_time = time.time() - generation_start
            self.metadata[screenshot_id] = {
                'original_path': image_path,
                'thumbnail_path': thumbnail_path,
                'thumbnail_size': size,
                'dimensions': thumbnail_img.size,
                'created_at': datetime.now().isoformat(),
                'file_size': os.path.getsize(thumbnail_path),
                'generation_time': generation_time,
                'scale_factor': scale_factor,
                'resampling_method': str(resampling_method),
                'save_quality': save_quality
            }
            self._save_metadata()
            
            # Cache the result with thread safety
            with self._cache_lock:
                self.thumbnail_cache[cache_key] = screenshot_id
                # Also cache the thumbnail image for immediate use
                self.thumbnail_image_cache[screenshot_id] = thumbnail_img.copy()
                self._cleanup_cache()
            
            # Record generation time for performance monitoring
            self.generation_times.append(generation_time)
            if len(self.generation_times) > 100:
                self.generation_times.pop(0)
            
            # Adaptive cache size based on performance
            if generation_time > 1.0:  # Slow generation
                self.max_cache_size = min(50, self.max_cache_size + 5)  # Increase cache
            elif generation_time < 0.2:  # Fast generation
                self.max_cache_size = max(20, self.max_cache_size - 2)  # Decrease cache
            
            return screenshot_id
                
        except Exception as e:
            print(f"Error generating thumbnail: {e}")
            return None
    
    def _load_image_cached(self, image_path: str) -> Optional[Image.Image]:
        """Load image with caching for better performance"""
        # Check cache first
        if image_path in self.image_cache:
            return self.image_cache[image_path].copy()
        
        try:
            # Load and process the image
            with Image.open(image_path) as img:
                # Convert to RGB if necessary (removes alpha channel)
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'RGBA':
                        background.paste(img, mask=img.split()[-1])
                    else:
                        background.paste(img, mask=img.split()[-1])
                    processed_img = background
                elif img.mode != 'RGB':
                    processed_img = img.convert('RGB')
                else:
                    processed_img = img.copy()
                
                # Cache the processed image
                self.image_cache[image_path] = processed_img.copy()
                self._cleanup_cache()
                
                return processed_img
                
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return None
    
    def _cleanup_cache(self):
        """Clean up caches to prevent memory bloat with enhanced optimization"""
        # Clean up image cache
        if len(self.image_cache) > self.max_cache_size:
            # Remove oldest entries (FIFO)
            items_to_remove = len(self.image_cache) - self.max_cache_size
            keys_to_remove = list(self.image_cache.keys())[:items_to_remove]
            for key in keys_to_remove:
                del self.image_cache[key]
        
        # Clean up thumbnail cache
        if len(self.thumbnail_cache) > self.max_cache_size:
            items_to_remove = len(self.thumbnail_cache) - self.max_cache_size
            keys_to_remove = list(self.thumbnail_cache.keys())[:items_to_remove]
            for key in keys_to_remove:
                del self.thumbnail_cache[key]
        
        # Clean up thumbnail image cache
        if len(self.thumbnail_image_cache) > self.max_thumbnail_cache_size:
            items_to_remove = len(self.thumbnail_image_cache) - self.max_thumbnail_cache_size
            keys_to_remove = list(self.thumbnail_image_cache.keys())[:items_to_remove]
            for key in keys_to_remove:
                del self.thumbnail_image_cache[key]
    
    def _start_preload_thread(self):
        """Start background thread for preloading thumbnails"""
        if self.preload_thread is None or not self.preload_thread.is_alive():
            self.preload_thread = threading.Thread(target=self._preload_worker, daemon=True)
            self.preload_thread.start()
    
    def _preload_worker(self):
        """Background worker for preloading thumbnails"""
        while True:
            try:
                if self.preload_queue:
                    screenshot_id = self.preload_queue.pop(0)
                    self._preload_thumbnail(screenshot_id)
                else:
                    time.sleep(0.1)  # Wait for new items
            except Exception as e:
                print(f"Error in preload worker: {e}")
                time.sleep(1)
    
    def _preload_thumbnail(self, screenshot_id: str):
        """Preload a thumbnail image into cache"""
        if screenshot_id in self.thumbnail_image_cache:
            return  # Already cached
        
        try:
            thumbnail_path = self.get_thumbnail_path(screenshot_id)
            if thumbnail_path and os.path.exists(thumbnail_path):
                with Image.open(thumbnail_path) as img:
                    with self._cache_lock:
                        self.thumbnail_image_cache[screenshot_id] = img.copy()
                        self._cleanup_cache()
        except Exception as e:
            print(f"Error preloading thumbnail {screenshot_id}: {e}")
    
    def get_cached_thumbnail_image(self, screenshot_id: str) -> Optional[Image.Image]:
        """Get cached thumbnail image for immediate display"""
        with self._cache_lock:
            if screenshot_id in self.thumbnail_image_cache:
                return self.thumbnail_image_cache[screenshot_id].copy()
        
        # Add to preload queue if not cached
        if screenshot_id not in self.preload_queue:
            self.preload_queue.append(screenshot_id)
        
        return None
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics for the screenshot manager"""
        cache_hit_rate = 0.0
        if self.cache_hits + self.cache_misses > 0:
            cache_hit_rate = self.cache_hits / (self.cache_hits + self.cache_misses)
        
        avg_generation_time = 0.0
        if self.generation_times:
            avg_generation_time = sum(self.generation_times) / len(self.generation_times)
        
        return {
            'cache_hit_rate': cache_hit_rate,
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'average_generation_time': avg_generation_time,
            'image_cache_size': len(self.image_cache),
            'thumbnail_cache_size': len(self.thumbnail_cache),
            'thumbnail_image_cache_size': len(self.thumbnail_image_cache),
            'preload_queue_size': len(self.preload_queue),
            'total_thumbnails': len(self.metadata)
        }
    
    def get_thumbnail_path(self, screenshot_id: str) -> Optional[str]:
        """
        Get the file path for a thumbnail.
        
        Args:
            screenshot_id: Unique identifier for the screenshot
            
        Returns:
            Path to thumbnail file or None if not found
        """
        if screenshot_id in self.metadata:
            thumbnail_path = self.metadata[screenshot_id]['thumbnail_path']
            if os.path.exists(thumbnail_path):
                return thumbnail_path
        return None
    
    def get_thumbnail_info(self, screenshot_id: str) -> Optional[Dict]:
        """
        Get metadata information for a thumbnail.
        
        Args:
            screenshot_id: Unique identifier for the screenshot
            
        Returns:
            Dictionary with thumbnail metadata or None if not found
        """
        return self.metadata.get(screenshot_id)
    
    def create_screenshot_with_thumbnail(self, screenshot_path: str, size: str = None) -> Optional[str]:
        """
        Create a thumbnail from an existing screenshot file.
        
        Args:
            screenshot_path: Path to the screenshot file
            size: Thumbnail size ('small', 'medium', 'large')
            
        Returns:
            Screenshot ID for the generated thumbnail or None if failed
        """
        if not os.path.exists(screenshot_path):
            print(f"Screenshot file not found: {screenshot_path}")
            return None
        
        return self.generate_thumbnail(screenshot_path, size)
    
    def cleanup_old_thumbnails(self, max_age_days: int = 30):
        """
        Clean up old thumbnails to save disk space.
        
        Args:
            max_age_days: Maximum age in days for thumbnails to keep
        """
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(days=max_age_days)
        to_remove = []
        
        for screenshot_id, metadata in self.metadata.items():
            try:
                created_at = datetime.fromisoformat(metadata['created_at'])
                if created_at < cutoff_date:
                    # Remove thumbnail file
                    thumbnail_path = metadata['thumbnail_path']
                    if os.path.exists(thumbnail_path):
                        os.remove(thumbnail_path)
                    to_remove.append(screenshot_id)
            except (ValueError, KeyError):
                # Invalid metadata, mark for removal
                to_remove.append(screenshot_id)
        
        # Remove from metadata
        for screenshot_id in to_remove:
            del self.metadata[screenshot_id]
        
        if to_remove:
            self._save_metadata()
            print(f"Cleaned up {len(to_remove)} old thumbnails")
    
    def get_all_thumbnails(self) -> Dict[str, Dict]:
        """
        Get all thumbnail metadata.
        
        Returns:
            Dictionary of all thumbnail metadata
        """
        return self.metadata.copy()
    
    def set_default_size(self, size: str):
        """
        Set the default thumbnail size.
        
        Args:
            size: New default size ('small', 'medium', 'large')
        """
        if size in self.THUMBNAIL_SIZES:
            self.default_size = size
        else:
            print(f"Warning: Invalid size '{size}', keeping current default '{self.default_size}'")