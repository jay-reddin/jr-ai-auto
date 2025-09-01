"""
Real-time performance dashboard and monitoring tools for JR AI Control.
Provides comprehensive performance metrics, optimization recommendations, and system health monitoring.
"""

import tkinter as tk
from tkinter import ttk
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
import json
import os
from collections import deque

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

from ui.material_design import get_theme, apply_md3_theme
from ui.enhanced_components import MD3Frame, MD3Card, MD3Button
from utils.performance_monitor import get_performance_optimizer
from utils.performance_optimizer import get_performance_manager

class PerformanceMetricsWidget(MD3Frame):
    """Widget for displaying real-time performance metrics"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.theme = get_theme()
        self.configure(bg=self.theme.colors['surface'])
        
        # Performance data
        self.metrics_history = {
            'cpu': deque(maxlen=60),
            'memory': deque(maxlen=60),
            'response_time': deque(maxlen=60),
            'ui_render_time': deque(maxlen=60)
        }
        
        # Update interval
        self.update_interval = 1000  # 1 second
        self.update_job = None
        
        # Create UI
        self.create_metrics_ui()
        
        # Start updates
        self.start_updates()
    
    def create_metrics_ui(self):
        """Create the metrics display UI"""
        # Title
        title_label = tk.Label(self, text="Performance Metrics", 
                              font=self.theme.typography['title_large'],
                              fg=self.theme.colors['on_surface'],
                              bg=self.theme.colors['surface'])
        title_label.pack(pady=(0, 10))
        
        # Metrics grid
        metrics_frame = MD3Frame(self)
        metrics_frame.pack(fill=tk.BOTH, expand=True)
        
        # CPU Usage
        self.cpu_card = self.create_metric_card(metrics_frame, "CPU Usage", "0%", self.theme.colors['primary'])
        self.cpu_card.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        # Memory Usage
        self.memory_card = self.create_metric_card(metrics_frame, "Memory", "0 MB", self.theme.colors['secondary'])
        self.memory_card.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Response Time
        self.response_card = self.create_metric_card(metrics_frame, "Avg Response", "0.0s", self.theme.colors['tertiary'])
        self.response_card.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        # UI Render Time
        self.render_card = self.create_metric_card(metrics_frame, "UI Render", "0.0ms", self.theme.colors['error'])
        self.render_card.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # Configure grid weights
        metrics_frame.grid_columnconfigure(0, weight=1)
        metrics_frame.grid_columnconfigure(1, weight=1)
    
    def create_metric_card(self, parent, title: str, value: str, color: str) -> MD3Card:
        """Create a metric display card"""
        card = MD3Card(parent)
        card.configure(bg=self.theme.colors['surface_variant'])
        
        # Card content
        content = MD3Frame(card)
        content.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)
        content.configure(bg=card['bg'])
        
        # Title
        title_label = tk.Label(content, text=title,
                              font=self.theme.typography['body_small'],
                              fg=self.theme.colors['on_surface_variant'],
                              bg=card['bg'])
        title_label.pack(anchor='w')
        
        # Value
        value_label = tk.Label(content, text=value,
                              font=self.theme.typography['headline_small'],
                              fg=color,
                              bg=card['bg'])
        value_label.pack(anchor='w')
        
        # Store reference to value label
        card.value_label = value_label
        
        return card
    
    def start_updates(self):
        """Start periodic updates"""
        self.update_metrics()
    
    def stop_updates(self):
        """Stop periodic updates"""
        if self.update_job:
            self.after_cancel(self.update_job)
            self.update_job = None
    
    def update_metrics(self):
        """Update performance metrics"""
        try:
            # Get performance data
            optimizer = get_performance_optimizer()
            current_metrics = optimizer.metrics.get_current_metrics()
            
            # Update CPU
            cpu_usage = current_metrics.get('cpu_usage', 0)
            self.cpu_card.value_label.configure(text=f"{cpu_usage:.1f}%")
            self.metrics_history['cpu'].append(cpu_usage)
            
            # Update Memory
            memory_mb = current_metrics.get('memory_usage_mb', 0)
            self.memory_card.value_label.configure(text=f"{memory_mb:.0f} MB")
            self.metrics_history['memory'].append(memory_mb)
            
            # Update Response Time
            avg_response = optimizer.metrics.get_average_metrics(1).get('response_times', 0)
            self.response_card.value_label.configure(text=f"{avg_response:.2f}s")
            self.metrics_history['response_time'].append(avg_response)
            
            # Update UI Render Time
            avg_render = optimizer.metrics.get_average_metrics(1).get('ui_render_times', 0) * 1000
            self.render_card.value_label.configure(text=f"{avg_render:.1f}ms")
            self.metrics_history['ui_render_time'].append(avg_render)
            
            # Update colors based on thresholds
            self.update_metric_colors(cpu_usage, memory_mb, avg_response, avg_render)
            
        except Exception as e:
            print(f"Error updating metrics: {e}")
        
        # Schedule next update
        self.update_job = self.after(self.update_interval, self.update_metrics)
    
    def update_metric_colors(self, cpu: float, memory: float, response: float, render: float):
        """Update metric colors based on performance thresholds"""
        # CPU color
        if cpu > 80:
            cpu_color = self.theme.colors['error']
        elif cpu > 60:
            cpu_color = self.theme.colors['tertiary']
        else:
            cpu_color = self.theme.colors['primary']
        self.cpu_card.value_label.configure(fg=cpu_color)
        
        # Memory color
        if memory > 500:
            memory_color = self.theme.colors['error']
        elif memory > 300:
            memory_color = self.theme.colors['tertiary']
        else:
            memory_color = self.theme.colors['secondary']
        self.memory_card.value_label.configure(fg=memory_color)
        
        # Response time color
        if response > 3.0:
            response_color = self.theme.colors['error']
        elif response > 1.5:
            response_color = self.theme.colors['tertiary']
        else:
            response_color = self.theme.colors['primary']
        self.response_card.value_label.configure(fg=response_color)
        
        # Render time color
        if render > 100:
            render_color = self.theme.colors['error']
        elif render > 50:
            render_color = self.theme.colors['tertiary']
        else:
            render_color = self.theme.colors['primary']
        self.render_card.value_label.configure(fg=render_color)

class OptimizationRecommendationsWidget(MD3Frame):
    """Widget for displaying optimization recommendations"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.theme = get_theme()
        self.configure(bg=self.theme.colors['surface'])
        
        # Recommendations data
        self.recommendations = []
        
        # Create UI
        self.create_recommendations_ui()
        
        # Update recommendations
        self.update_recommendations()
    
    def create_recommendations_ui(self):
        """Create the recommendations display UI"""
        # Title
        title_label = tk.Label(self, text="Optimization Recommendations", 
                              font=self.theme.typography['title_large'],
                              fg=self.theme.colors['on_surface'],
                              bg=self.theme.colors['surface'])
        title_label.pack(pady=(0, 10))
        
        # Recommendations list
        self.recommendations_frame = MD3Frame(self)
        self.recommendations_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollable area for recommendations
        self.canvas = tk.Canvas(self.recommendations_frame, 
                               bg=self.theme.colors['surface'],
                               highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.recommendations_frame, 
                                     orient=tk.VERTICAL,
                                     command=self.canvas.yview)
        self.scrollable_frame = MD3Frame(self.canvas)
        
        self.scrollable_frame.bind('<Configure>', 
                                  lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def update_recommendations(self):
        """Update optimization recommendations"""
        try:
            # Clear existing recommendations
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            
            # Get performance data
            optimizer = get_performance_optimizer()
            manager = get_performance_manager()
            
            current_metrics = optimizer.metrics.get_current_metrics()
            performance_report = manager.get_performance_report()
            
            # Generate recommendations
            recommendations = self.generate_recommendations(current_metrics, performance_report)
            
            # Display recommendations
            for i, recommendation in enumerate(recommendations):
                self.create_recommendation_card(self.scrollable_frame, recommendation, i)
            
            # Schedule next update
            self.after(5000, self.update_recommendations)  # Update every 5 seconds
            
        except Exception as e:
            print(f"Error updating recommendations: {e}")
    
    def generate_recommendations(self, metrics: Dict[str, Any], report: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate optimization recommendations based on current metrics"""
        recommendations = []
        
        # CPU recommendations
        cpu_usage = metrics.get('cpu_usage', 0)
        if cpu_usage > 80:
            recommendations.append({
                'title': 'High CPU Usage Detected',
                'description': f'CPU usage is at {cpu_usage:.1f}%. Consider reducing voice processing quality or closing other applications.',
                'priority': 'high',
                'action': 'Optimize voice processing settings'
            })
        elif cpu_usage > 60:
            recommendations.append({
                'title': 'Moderate CPU Usage',
                'description': f'CPU usage is at {cpu_usage:.1f}%. Monitor for performance impact.',
                'priority': 'medium',
                'action': 'Monitor CPU usage'
            })
        
        # Memory recommendations
        memory_mb = metrics.get('memory_usage_mb', 0)
        if memory_mb > 500:
            recommendations.append({
                'title': 'High Memory Usage',
                'description': f'Memory usage is at {memory_mb:.0f}MB. Consider clearing chat history or optimizing caches.',
                'priority': 'high',
                'action': 'Clear old messages and optimize caches'
            })
        elif memory_mb > 300:
            recommendations.append({
                'title': 'Moderate Memory Usage',
                'description': f'Memory usage is at {memory_mb:.0f}MB. Regular cleanup recommended.',
                'priority': 'medium',
                'action': 'Schedule regular cleanup'
            })
        
        # Component-specific recommendations
        component_stats = report.get('component_stats', {})
        
        # Chat interface recommendations
        if 'ChatInterface' in component_stats:
            chat_stats = component_stats['ChatInterface']
            if 'add_message' in chat_stats:
                avg_render_time = chat_stats['add_message'].get('average', 0)
                if avg_render_time > 0.1:
                    recommendations.append({
                        'title': 'Slow Chat Rendering',
                        'description': f'Chat messages are taking {avg_render_time:.3f}s to render. Consider enabling virtual scrolling.',
                        'priority': 'medium',
                        'action': 'Enable virtual scrolling for chat'
                    })
        
        # Voice system recommendations
        if 'VoiceManager' in component_stats:
            voice_stats = component_stats['VoiceManager']
            if 'speech_synthesis' in voice_stats:
                avg_synthesis_time = voice_stats['speech_synthesis'].get('average', 0)
                if avg_synthesis_time > 2.0:
                    recommendations.append({
                        'title': 'Slow Speech Synthesis',
                        'description': f'Speech synthesis is taking {avg_synthesis_time:.2f}s. Consider reducing text length or adjusting quality.',
                        'priority': 'medium',
                        'action': 'Optimize speech synthesis settings'
                    })
        
        # General recommendations
        if not recommendations:
            recommendations.append({
                'title': 'System Running Optimally',
                'description': 'All performance metrics are within acceptable ranges.',
                'priority': 'low',
                'action': 'Continue monitoring'
            })
        
        return recommendations
    
    def create_recommendation_card(self, parent, recommendation: Dict[str, str], index: int):
        """Create a recommendation display card"""
        card = MD3Card(parent)
        card.pack(fill=tk.X, pady=5)
        
        # Priority color
        priority_colors = {
            'high': self.theme.colors['error'],
            'medium': self.theme.colors['tertiary'],
            'low': self.theme.colors['primary']
        }
        priority_color = priority_colors.get(recommendation['priority'], self.theme.colors['primary'])
        
        # Card content
        content = MD3Frame(card)
        content.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)
        content.configure(bg=card['bg'])
        
        # Priority indicator
        priority_frame = MD3Frame(content)
        priority_frame.pack(fill=tk.X, pady=(0, 5))
        priority_frame.configure(bg=card['bg'])
        
        priority_label = tk.Label(priority_frame, 
                                 text=f"● {recommendation['priority'].upper()}",
                                 font=self.theme.typography['label_small'],
                                 fg=priority_color,
                                 bg=card['bg'])
        priority_label.pack(side=tk.LEFT)
        
        # Title
        title_label = tk.Label(content, text=recommendation['title'],
                              font=self.theme.typography['title_medium'],
                              fg=self.theme.colors['on_surface'],
                              bg=card['bg'])
        title_label.pack(anchor='w', pady=(0, 5))
        
        # Description
        desc_label = tk.Label(content, text=recommendation['description'],
                             font=self.theme.typography['body_medium'],
                             fg=self.theme.colors['on_surface_variant'],
                             bg=card['bg'],
                             wraplength=400,
                             justify=tk.LEFT)
        desc_label.pack(anchor='w', pady=(0, 5))
        
        # Action button
        if recommendation['action']:
            action_btn = MD3Button(content, text=recommendation['action'],
                                  style='secondary',
                                  command=lambda: self.execute_recommendation_action(recommendation))
            action_btn.pack(anchor='w')
    
    def execute_recommendation_action(self, recommendation: Dict[str, str]):
        """Execute a recommendation action"""
        action = recommendation['action']
        
        try:
            if 'clear' in action.lower() or 'cleanup' in action.lower():
                # Trigger cleanup
                manager = get_performance_manager()
                manager.optimize_all_components()
                
            elif 'optimize' in action.lower():
                # Trigger optimization
                optimizer = get_performance_optimizer()
                optimizer.optimize_performance()
                
            elif 'monitor' in action.lower():
                # Just acknowledge - monitoring is already active
                pass
            
            print(f"Executed recommendation action: {action}")
            
        except Exception as e:
            print(f"Error executing recommendation action: {e}")

class PerformanceDashboard(tk.Toplevel):
    """Main performance dashboard window"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("JR AI Control - Performance Dashboard")
        self.geometry("800x600")
        
        # Apply theme
        self.theme = apply_md3_theme(self, get_theme().theme_mode)
        
        # Make window resizable
        self.resizable(True, True)
        
        # Create UI
        self.create_dashboard_ui()
        
        # Center window
        self.center_window()
    
    def create_dashboard_ui(self):
        """Create the dashboard UI"""
        # Main container
        main_frame = MD3Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)
        
        # Title
        title_label = tk.Label(main_frame, text="Performance Dashboard",
                              font=self.theme.typography['headline_large'],
                              fg=self.theme.colors['on_surface'],
                              bg=self.theme.colors['surface'])
        title_label.pack(pady=(0, 20))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Metrics tab
        metrics_frame = MD3Frame(notebook)
        self.metrics_widget = PerformanceMetricsWidget(metrics_frame)
        self.metrics_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        notebook.add(metrics_frame, text="Metrics")
        
        # Recommendations tab
        recommendations_frame = MD3Frame(notebook)
        self.recommendations_widget = OptimizationRecommendationsWidget(recommendations_frame)
        self.recommendations_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        notebook.add(recommendations_frame, text="Recommendations")
        
        # Control buttons
        button_frame = MD3Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Optimize button
        optimize_btn = MD3Button(button_frame, text="Optimize Now", style='primary',
                                command=self.optimize_now)
        optimize_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Export button
        export_btn = MD3Button(button_frame, text="Export Report", style='secondary',
                              command=self.export_report)
        export_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Close button
        close_btn = MD3Button(button_frame, text="Close", style='secondary',
                             command=self.destroy)
        close_btn.pack(side=tk.RIGHT)
    
    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def optimize_now(self):
        """Trigger immediate optimization"""
        try:
            manager = get_performance_manager()
            results = manager.optimize_all_components()
            
            # Show results in a simple message
            optimizations = results.get('system_optimization', {}).get('optimizations_performed', [])
            if optimizations:
                message = "Optimization completed:\n" + "\n".join(optimizations)
            else:
                message = "System is already optimized."
            
            # Create simple message dialog
            msg_window = tk.Toplevel(self)
            msg_window.title("Optimization Results")
            msg_window.geometry("400x200")
            
            msg_label = tk.Label(msg_window, text=message, 
                               font=self.theme.typography['body_medium'],
                               justify=tk.LEFT, wraplength=350)
            msg_label.pack(padx=20, pady=20)
            
            ok_btn = MD3Button(msg_window, text="OK", command=msg_window.destroy)
            ok_btn.pack(pady=10)
            
        except Exception as e:
            print(f"Error during optimization: {e}")
    
    def export_report(self):
        """Export performance report to file"""
        try:
            # Get comprehensive report
            optimizer = get_performance_optimizer()
            manager = get_performance_manager()
            
            report = {
                'timestamp': datetime.now().isoformat(),
                'performance_metrics': optimizer.get_performance_report(),
                'optimization_report': manager.get_performance_report(),
                'system_info': self.get_system_info()
            }
            
            # Save to file
            filename = f"performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            
            print(f"Performance report exported to {filename}")
            
        except Exception as e:
            print(f"Error exporting report: {e}")
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        info = {
            'platform': os.name,
            'python_version': f"{__import__('sys').version_info.major}.{__import__('sys').version_info.minor}"
        }
        
        if PSUTIL_AVAILABLE:
            try:
                info.update({
                    'cpu_count': psutil.cpu_count(),
                    'total_memory_gb': psutil.virtual_memory().total / (1024**3),
                    'disk_usage_gb': psutil.disk_usage('/').total / (1024**3) if os.name != 'nt' else psutil.disk_usage('C:').total / (1024**3)
                })
            except:
                pass
        
        return info
    
    def destroy(self):
        """Clean up when closing"""
        # Stop metrics updates
        if hasattr(self, 'metrics_widget'):
            self.metrics_widget.stop_updates()
        
        super().destroy()

def show_performance_dashboard(parent=None):
    """Show the performance dashboard"""
    dashboard = PerformanceDashboard(parent)
    return dashboard