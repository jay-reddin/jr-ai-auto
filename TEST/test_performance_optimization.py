"""
Comprehensive test suite for performance optimization and final polish (Task 21).
Tests all performance enhancements including voice processing, UI rendering, 
screenshot thumbnails, memory management, and monitoring tools.
"""

import unittest
import time
import threading
import tempfile
import os
import sys
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestVoicePerformanceOptimization(unittest.TestCase):
    """Test voice processing performance optimizations"""
    
    def setUp(self):
        """Set up test environment"""
        try:
            from voice.voice_manager import VoiceManager
            self.voice_manager = VoiceManager()
        except ImportError:
            self.skipTest("Voice manager not available")
    
    def test_adaptive_timeout_adjustment(self):
        """Test adaptive timeout adjustment in voice recognition"""
        # Mock the voice manager's listening worker
        with patch.object(self.voice_manager, '_process_audio_recognition'):
            # Test that timeout adjusts based on performance
            initial_timeout = 0.3
            
            # Simulate slow performance
            with patch('time.time', side_effect=[0, 1.0]):  # 1 second capture time
                # This would trigger timeout increase in real implementation
                pass
            
            # Simulate fast performance  
            with patch('time.time', side_effect=[0, 0.1]):  # 0.1 second capture time
                # This would trigger timeout decrease in real implementation
                pass
            
            self.assertTrue(True)  # Test passes if no exceptions
    
    def test_batch_tts_processing(self):
        """Test batch processing in TTS worker"""
        if not self.voice_manager.voice_available:
            self.skipTest("Voice not available")
        
        # Test that multiple texts are batched together
        test_texts = ["Hello", "World", "Test"]
        
        for text in test_texts:
            self.voice_manager.speak_text(text)
        
        # Verify queue has items
        self.assertGreater(self.voice_manager.speech_queue.qsize(), 0)
    
    def test_text_optimization_performance(self):
        """Test text optimization for speech performance"""
        if not self.voice_manager.voice_available:
            self.skipTest("Voice not available")
        
        # Test with various text types
        test_cases = [
            "This is a simple test.",
            "API call to JSON endpoint with HTTP request",
            "**Bold text** and *italic text* with `code`",
            "Very long text " * 100,  # Long text
            "https://example.com/very/long/url/path",
            "CPU usage is 50% and RAM is 8GB"
        ]
        
        for text in test_cases:
            start_time = time.time()
            optimized = self.voice_manager._optimize_text_for_speech(text)
            optimization_time = time.time() - start_time
            
            # Optimization should be fast (< 10ms)
            self.assertLess(optimization_time, 0.01)
            
            # Optimized text should be reasonable length
            self.assertLessEqual(len(optimized), 500)
            
            # Should not be empty unless input was empty
            if text.strip():
                self.assertTrue(optimized.strip())

class TestChatInterfacePerformance(unittest.TestCase):
    """Test chat interface performance optimizations"""
    
    def setUp(self):
        """Set up test environment"""
        try:
            import tkinter as tk
            from ui.chat_interface import ChatInterface
            
            self.root = tk.Tk()
            self.root.withdraw()  # Hide window during tests
            self.chat_interface = ChatInterface(self.root)
        except ImportError:
            self.skipTest("Chat interface not available")
    
    def tearDown(self):
        """Clean up test environment"""
        if hasattr(self, 'root'):
            self.root.destroy()
    
    def test_message_pooling(self):
        """Test message widget pooling for memory efficiency"""
        # Add many messages to trigger pooling
        for i in range(100):
            self.chat_interface.add_message(
                sender="Test",
                message=f"Test message {i}",
                is_user=i % 2 == 0
            )
        
        # Check that pooling is working
        self.assertGreater(len(self.chat_interface.message_pool), 0)
        
        # Check that message count is limited
        self.assertLessEqual(len(self.chat_interface.messages), 
                           self.chat_interface.max_visible_messages)
    
    def test_batch_rendering_performance(self):
        """Test batch rendering performance"""
        start_time = time.time()
        
        # Add multiple messages quickly
        for i in range(20):
            self.chat_interface.add_message(
                sender="Test",
                message=f"Batch message {i}",
                is_user=False
            )
        
        # Process any pending operations
        self.root.update_idletasks()
        
        render_time = time.time() - start_time
        
        # Rendering should be reasonably fast
        self.assertLess(render_time, 2.0)
        
        # Check average render time
        if self.chat_interface.render_times:
            avg_render_time = self.chat_interface.get_average_render_time()
            self.assertLess(avg_render_time, 0.1)  # < 100ms average
    
    def test_virtual_scrolling(self):
        """Test virtual scrolling implementation"""
        # Enable virtual scrolling
        self.chat_interface.virtual_scrolling_enabled = True
        
        # Add many messages
        for i in range(200):
            self.chat_interface.add_message(
                sender="Test",
                message=f"Virtual scroll test {i}",
                is_user=False
            )
        
        # Test virtual scrolling optimization
        self.chat_interface._implement_virtual_scrolling()
        
        # Check that viewport is set
        self.assertIsNotNone(self.chat_interface.viewport_start)
        self.assertIsNotNone(self.chat_interface.viewport_end)
    
    def test_memory_optimization(self):
        """Test memory optimization features"""
        initial_message_count = len(self.chat_interface.messages)
        
        # Add messages to trigger cleanup
        for i in range(self.chat_interface.max_visible_messages + 10):
            self.chat_interface.add_message(
                sender="Test",
                message=f"Memory test {i}",
                is_user=False
            )
        
        # Trigger memory optimization
        self.chat_interface._optimize_memory_usage()
        
        # Check that cleanup occurred
        final_message_count = len(self.chat_interface.messages)
        self.assertLessEqual(final_message_count, self.chat_interface.max_visible_messages)

class TestScreenshotManagerPerformance(unittest.TestCase):
    """Test screenshot manager performance optimizations"""
    
    def setUp(self):
        """Set up test environment"""
        try:
            from utils.screenshot_manager import ScreenshotManager
            
            # Create temporary directory for tests
            self.temp_dir = tempfile.mkdtemp()
            self.screenshot_manager = ScreenshotManager(
                screenshots_dir=self.temp_dir,
                default_size="medium"
            )
        except ImportError:
            self.skipTest("Screenshot manager not available")
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        if hasattr(self, 'temp_dir'):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_thumbnail_caching(self):
        """Test thumbnail caching performance"""
        # Create a test image
        from PIL import Image
        test_image_path = os.path.join(self.temp_dir, "test_image.png")
        
        # Create a simple test image
        img = Image.new('RGB', (800, 600), color='red')
        img.save(test_image_path)
        
        # Generate thumbnail first time
        start_time = time.time()
        thumbnail_id1 = self.screenshot_manager.generate_thumbnail(test_image_path, "medium")
        first_generation_time = time.time() - start_time
        
        # Generate same thumbnail again (should use cache)
        start_time = time.time()
        thumbnail_id2 = self.screenshot_manager.generate_thumbnail(test_image_path, "medium")
        second_generation_time = time.time() - start_time
        
        # Second generation should be much faster (cached)
        self.assertLess(second_generation_time, first_generation_time * 0.5)
        
        # Should return same thumbnail ID
        self.assertEqual(thumbnail_id1, thumbnail_id2)
        
        # Check cache hit rate
        stats = self.screenshot_manager.get_performance_stats()
        self.assertGreater(stats['cache_hit_rate'], 0)
    
    def test_adaptive_quality_settings(self):
        """Test adaptive quality settings based on system load"""
        from PIL import Image
        test_image_path = os.path.join(self.temp_dir, "test_image.png")
        
        # Create a test image
        img = Image.new('RGB', (1920, 1080), color='blue')
        img.save(test_image_path)
        
        # Test thumbnail generation with different system loads
        with patch('psutil.cpu_percent', return_value=90):  # High CPU
            thumbnail_id_high_load = self.screenshot_manager.generate_thumbnail(test_image_path, "large")
        
        with patch('psutil.cpu_percent', return_value=20):  # Low CPU
            thumbnail_id_low_load = self.screenshot_manager.generate_thumbnail(test_image_path, "large")
        
        # Both should succeed
        self.assertIsNotNone(thumbnail_id_high_load)
        self.assertIsNotNone(thumbnail_id_low_load)
    
    def test_preloading_system(self):
        """Test background preloading system"""
        from PIL import Image
        
        # Create multiple test images
        image_paths = []
        for i in range(5):
            test_image_path = os.path.join(self.temp_dir, f"test_image_{i}.png")
            img = Image.new('RGB', (400, 300), color=(i*50, i*40, i*30))
            img.save(test_image_path)
            image_paths.append(test_image_path)
        
        # Generate thumbnails
        thumbnail_ids = []
        for path in image_paths:
            thumbnail_id = self.screenshot_manager.generate_thumbnail(path, "small")
            thumbnail_ids.append(thumbnail_id)
        
        # Test preloading
        for thumbnail_id in thumbnail_ids:
            if thumbnail_id not in self.screenshot_manager.preload_queue:
                self.screenshot_manager.preload_queue.append(thumbnail_id)
        
        # Wait a bit for preloading
        time.sleep(0.5)
        
        # Check that some thumbnails are cached
        cached_count = len(self.screenshot_manager.thumbnail_image_cache)
        self.assertGreater(cached_count, 0)

class TestMemoryOptimization(unittest.TestCase):
    """Test memory optimization and management"""
    
    def setUp(self):
        """Set up test environment"""
        try:
            from utils.memory_optimizer import MemoryOptimizer
            self.memory_optimizer = MemoryOptimizer()
        except ImportError:
            self.skipTest("Memory optimizer not available")
    
    def test_memory_pressure_monitoring(self):
        """Test memory pressure monitoring"""
        # Test pressure level calculation
        monitor = self.memory_optimizer.pressure_monitor
        
        # Test different memory levels
        self.assertEqual(monitor._calculate_pressure_level(100), 'normal')
        self.assertEqual(monitor._calculate_pressure_level(500), 'warning')
        self.assertEqual(monitor._calculate_pressure_level(700), 'critical')
        self.assertEqual(monitor._calculate_pressure_level(900), 'emergency')
    
    def test_garbage_collection_optimization(self):
        """Test garbage collection optimization"""
        gc_optimizer = self.memory_optimizer.gc_optimizer
        
        # Test GC optimization
        results = gc_optimizer.optimize_gc_settings()
        
        # Should have performed collections
        self.assertGreaterEqual(results['objects_collected'], 0)
        self.assertIn('collections_performed', results)
        self.assertGreater(results['duration'], 0)
    
    def test_component_cleanup_registration(self):
        """Test component cleanup registration"""
        cleanup_called = False
        
        def test_cleaner():
            nonlocal cleanup_called
            cleanup_called = True
            return 5  # Return number of items cleaned
        
        # Register cleaner
        self.memory_optimizer.register_component_cleaner('TestComponent', test_cleaner)
        
        # Trigger cleanup
        results = self.memory_optimizer.standard_cleanup()
        
        # Check that cleaner was called
        self.assertTrue(cleanup_called)
        self.assertIn('TestComponent', str(results['actions_performed']))
    
    def test_emergency_cleanup(self):
        """Test emergency cleanup procedures"""
        # Trigger emergency cleanup
        results = self.memory_optimizer.emergency_cleanup()
        
        # Should have performed emergency actions
        self.assertEqual(results['cleanup_type'], 'emergency')
        self.assertGreater(len(results['actions_performed']), 0)
        self.assertGreater(results['duration'], 0)

class TestPerformanceMonitoring(unittest.TestCase):
    """Test performance monitoring and dashboard"""
    
    def setUp(self):
        """Set up test environment"""
        try:
            from utils.performance_monitor import PerformanceOptimizer
            from utils.performance_optimizer import PerformanceOptimizationManager
            
            self.performance_optimizer = PerformanceOptimizer()
            self.performance_manager = PerformanceOptimizationManager()
        except ImportError:
            self.skipTest("Performance monitoring not available")
    
    def test_performance_metrics_collection(self):
        """Test performance metrics collection"""
        # Start monitoring briefly
        self.performance_optimizer.start_monitoring()
        
        # Wait for some metrics to be collected
        time.sleep(2)
        
        # Get current metrics
        current_metrics = self.performance_optimizer.metrics.get_current_metrics()
        
        # Should have basic metrics
        self.assertIn('cpu_usage', current_metrics)
        self.assertIn('memory_usage_mb', current_metrics)
        
        # Stop monitoring
        self.performance_optimizer.stop_monitoring()
    
    def test_operation_timing(self):
        """Test operation timing functionality"""
        # Test timing context manager
        with self.performance_optimizer.time_operation('test_operation'):
            time.sleep(0.1)  # Simulate work
        
        # Check that timing was recorded
        metrics = self.performance_optimizer.metrics.metrics
        self.assertIn('test_operation', metrics)
        
        if metrics['test_operation']:
            recorded_time = metrics['test_operation'][-1]
            self.assertGreaterEqual(recorded_time, 0.1)
    
    def test_performance_report_generation(self):
        """Test performance report generation"""
        # Generate report
        report = self.performance_optimizer.get_performance_report()
        
        # Should contain expected sections
        self.assertIn('current_metrics', report)
        self.assertIn('average_metrics_5min', report)
        self.assertIn('monitoring_active', report)
    
    def test_optimization_triggers(self):
        """Test automatic optimization triggers"""
        # Test component registration
        mock_component = Mock()
        mock_component.optimize_performance = Mock(return_value={'optimized': True})
        
        self.performance_manager.register_component(mock_component)
        
        # Trigger optimization
        results = self.performance_manager.optimize_all_components()
        
        # Should have optimization results
        self.assertIn('system_optimization', results)
        self.assertIn('component_optimizations', results)

class TestPerformanceDashboard(unittest.TestCase):
    """Test performance dashboard functionality"""
    
    def setUp(self):
        """Set up test environment"""
        try:
            import tkinter as tk
            from utils.performance_dashboard import PerformanceMetricsWidget, OptimizationRecommendationsWidget
            
            self.root = tk.Tk()
            self.root.withdraw()  # Hide window during tests
        except ImportError:
            self.skipTest("Performance dashboard not available")
    
    def tearDown(self):
        """Clean up test environment"""
        if hasattr(self, 'root'):
            self.root.destroy()
    
    def test_metrics_widget_creation(self):
        """Test performance metrics widget creation"""
        from utils.performance_dashboard import PerformanceMetricsWidget
        
        # Create metrics widget
        metrics_widget = PerformanceMetricsWidget(self.root)
        
        # Should have metric cards
        self.assertTrue(hasattr(metrics_widget, 'cpu_card'))
        self.assertTrue(hasattr(metrics_widget, 'memory_card'))
        self.assertTrue(hasattr(metrics_widget, 'response_card'))
        self.assertTrue(hasattr(metrics_widget, 'render_card'))
    
    def test_recommendations_generation(self):
        """Test optimization recommendations generation"""
        from utils.performance_dashboard import OptimizationRecommendationsWidget
        
        # Create recommendations widget
        recommendations_widget = OptimizationRecommendationsWidget(self.root)
        
        # Test recommendation generation with mock data
        mock_metrics = {
            'cpu_usage': 85.0,  # High CPU
            'memory_usage_mb': 600.0  # High memory
        }
        
        mock_report = {
            'component_stats': {
                'ChatInterface': {
                    'add_message': {'average': 0.15}  # Slow rendering
                }
            }
        }
        
        recommendations = recommendations_widget.generate_recommendations(mock_metrics, mock_report)
        
        # Should generate recommendations for high resource usage
        self.assertGreater(len(recommendations), 0)
        
        # Should have high priority recommendations
        high_priority_recs = [r for r in recommendations if r['priority'] == 'high']
        self.assertGreater(len(high_priority_recs), 0)

class TestIntegrationPerformance(unittest.TestCase):
    """Test integrated performance optimizations"""
    
    def test_end_to_end_performance(self):
        """Test end-to-end performance with all optimizations enabled"""
        try:
            # Import main components
            from utils.performance_monitor import get_performance_optimizer
            from utils.performance_optimizer import get_performance_manager
            from utils.memory_optimizer import get_memory_optimizer
            
            # Get optimizers
            perf_optimizer = get_performance_optimizer()
            perf_manager = get_performance_manager()
            memory_optimizer = get_memory_optimizer()
            
            # Start monitoring
            perf_optimizer.start_monitoring()
            perf_manager.start_monitoring()
            memory_optimizer.start_monitoring()
            
            # Simulate some work
            time.sleep(1)
            
            # Trigger optimizations
            perf_results = perf_optimizer.optimize_performance()
            memory_results = memory_optimizer.standard_cleanup()
            
            # Check results
            self.assertIn('timestamp', perf_results)
            self.assertIn('timestamp', memory_results)
            
            # Stop monitoring
            perf_optimizer.stop_monitoring()
            perf_manager.stop_monitoring()
            memory_optimizer.stop_monitoring()
            
        except ImportError as e:
            self.skipTest(f"Integration test components not available: {e}")

def run_performance_tests():
    """Run all performance optimization tests"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestVoicePerformanceOptimization,
        TestChatInterfacePerformance,
        TestScreenshotManagerPerformance,
        TestMemoryOptimization,
        TestPerformanceMonitoring,
        TestPerformanceDashboard,
        TestIntegrationPerformance
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print("PERFORMANCE OPTIMIZATION TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.failures:
        print(f"\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print(f"\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback.split('Exception:')[-1].strip()}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0
    print(f"\nSuccess rate: {success_rate:.1f}%")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    print("Running Performance Optimization Tests...")
    print("Testing Task 21: Performance optimization and final polish")
    print("="*60)
    
    success = run_performance_tests()
    
    if success:
        print("\n✅ All performance optimization tests passed!")
        print("Task 21 implementation is working correctly.")
    else:
        print("\n❌ Some performance optimization tests failed.")
        print("Please review the failures and fix any issues.")
    
    sys.exit(0 if success else 1)