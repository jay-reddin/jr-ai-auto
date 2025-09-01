#!/usr/bin/env python3
"""
Performance benchmark test to measure improvements from the migration
"""

import sys
import os
import time
import psutil
import subprocess

def measure_import_time():
    """Measure time to import all modules"""
    print("Measuring import performance...")
    
    start_time = time.time()
    
    # Import all main modules
    from utils.contants import MODELS
    from utils.agent import create_clevrr_agent
    from utils.tools import get_screen_info
    from utils.prompt import prompt
    import pyautogui
    import main
    
    end_time = time.time()
    import_time = end_time - start_time
    
    print(f"✓ Total import time: {import_time:.3f} seconds")
    return import_time

def measure_agent_creation_time():
    """Measure time to create agent"""
    print("Measuring agent creation performance...")
    
    from utils.contants import MODELS
    from utils.agent import create_clevrr_agent
    from utils.prompt import prompt
    
    start_time = time.time()
    agent = create_clevrr_agent(MODELS['gemini'], prompt)
    end_time = time.time()
    
    creation_time = end_time - start_time
    print(f"✓ Agent creation time: {creation_time:.3f} seconds")
    return creation_time

def measure_memory_efficiency():
    """Measure memory efficiency"""
    print("Measuring memory efficiency...")
    
    process = psutil.Process()
    
    # Baseline memory
    baseline = process.memory_info().rss / 1024 / 1024
    
    # Import modules
    from utils.contants import MODELS
    from utils.agent import create_clevrr_agent
    from utils.tools import get_screen_info
    
    after_imports = process.memory_info().rss / 1024 / 1024
    
    # Create agent
    from utils.prompt import prompt
    agent = create_clevrr_agent(MODELS['gemini'], prompt)
    
    after_agent = process.memory_info().rss / 1024 / 1024
    
    print(f"✓ Baseline memory: {baseline:.2f} MB")
    print(f"✓ After imports: {after_imports:.2f} MB (+{after_imports-baseline:.2f} MB)")
    print(f"✓ After agent creation: {after_agent:.2f} MB (+{after_agent-baseline:.2f} MB)")
    
    return {
        'baseline': baseline,
        'after_imports': after_imports,
        'after_agent': after_agent,
        'total_increase': after_agent - baseline
    }

def test_windows_font_performance():
    """Test Windows font loading performance"""
    print("Testing Windows font loading performance...")
    
    from utils.tools import _load_windows_font
    
    start_time = time.time()
    font = _load_windows_font(25)
    end_time = time.time()
    
    font_time = end_time - start_time
    print(f"✓ Font loading time: {font_time:.3f} seconds")
    
    if font:
        print("✓ Font loaded successfully")
        return font_time
    else:
        print("✗ Font loading failed")
        return None

def count_dependencies():
    """Count and analyze dependencies"""
    print("Analyzing dependencies...")
    
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.readlines()
        
        # Count total dependencies
        total_deps = len([line for line in requirements if line.strip() and not line.startswith('#')])
        
        # Count by category
        langchain_deps = len([line for line in requirements if 'langchain' in line.lower()])
        google_deps = len([line for line in requirements if 'google' in line.lower()])
        automation_deps = len([line for line in requirements if any(pkg in line.lower() for pkg in ['pyautogui', 'pillow'])])
        
        print(f"✓ Total dependencies: {total_deps}")
        print(f"✓ LangChain dependencies: {langchain_deps}")
        print(f"✓ Google dependencies: {google_deps}")
        print(f"✓ Automation dependencies: {automation_deps}")
        
        return {
            'total': total_deps,
            'langchain': langchain_deps,
            'google': google_deps,
            'automation': automation_deps
        }
        
    except Exception as e:
        print(f"✗ Failed to analyze dependencies: {e}")
        return None

def main():
    """Run performance benchmark"""
    print("Clevrr Computer Performance Benchmark")
    print("=" * 45)
    
    results = {}
    
    # Measure import performance
    results['import_time'] = measure_import_time()
    
    print()
    
    # Measure agent creation performance
    results['agent_creation_time'] = measure_agent_creation_time()
    
    print()
    
    # Measure memory efficiency
    results['memory'] = measure_memory_efficiency()
    
    print()
    
    # Test Windows font performance
    results['font_time'] = test_windows_font_performance()
    
    print()
    
    # Analyze dependencies
    results['dependencies'] = count_dependencies()
    
    # Generate performance report
    print("\n" + "=" * 45)
    print("PERFORMANCE BENCHMARK REPORT")
    print("=" * 45)
    
    print(f"Import Performance: {results['import_time']:.3f}s")
    print(f"Agent Creation: {results['agent_creation_time']:.3f}s")
    print(f"Font Loading: {results['font_time']:.3f}s" if results['font_time'] else "Font Loading: FAILED")
    
    if results['memory']:
        print(f"Memory Usage: {results['memory']['baseline']:.1f} MB → {results['memory']['after_agent']:.1f} MB")
        print(f"Memory Overhead: {results['memory']['total_increase']:.1f} MB")
    
    if results['dependencies']:
        print(f"Dependencies: {results['dependencies']['total']} total")
    
    # Performance assessment
    print("\nPerformance Assessment:")
    
    # Import time assessment
    if results['import_time'] < 2.0:
        print("✓ Import time: Excellent")
    elif results['import_time'] < 5.0:
        print("✓ Import time: Good")
    else:
        print("⚠ Import time: Could be improved")
    
    # Memory assessment
    if results['memory'] and results['memory']['total_increase'] < 100:
        print("✓ Memory usage: Efficient")
    elif results['memory'] and results['memory']['total_increase'] < 200:
        print("✓ Memory usage: Reasonable")
    else:
        print("⚠ Memory usage: High")
    
    # Dependencies assessment
    if results['dependencies'] and results['dependencies']['total'] < 30:
        print("✓ Dependencies: Minimal")
    elif results['dependencies'] and results['dependencies']['total'] < 50:
        print("✓ Dependencies: Reasonable")
    else:
        print("⚠ Dependencies: Many")
    
    print("\n🎯 Benchmark completed successfully!")

if __name__ == "__main__":
    main()