#!/usr/bin/env python3
"""
Master script to run all image enhancement filters
Execute all filtering methods with different parameters for comprehensive analysis
"""

import os
import sys
import time

def run_all_filters():
    """
    Execute all image enhancement filters
    """
    print("=== Image Enhancement Filter Comparison ===")
    print("Running comprehensive image enhancement analysis...\n")
    
    scripts = [
        "gaussian_blur_filter.py",
        "median_filter.py", 
        "laplacian_enhancement.py",
        "sobel_enhancement.py",
        "histogram_equalization.py",
        "contrast_stretching.py",
        "bilateral_filter.py",
        "adaptive_histogram_equalization.py",
        "gamma_log_transforms.py",
        "advanced_edge_filters.py",
        "pansharpening_methods.py",
        "highpass_filter.py",
        "highboost_unsharp.py"
    ]
    
    results = {}
    
    for script in scripts:
        if os.path.exists(script):
            print(f"Running {script}...")
            start_time = time.time()
            
            try:
                # Import and run the script
                module_name = script[:-3]  # Remove .py extension
                module = __import__(module_name)
                if hasattr(module, 'main'):
                    module.main()
                    execution_time = time.time() - start_time
                    results[script] = {'status': 'SUCCESS', 'time': execution_time}
                    print(f"✓ {script} completed in {execution_time:.2f} seconds\n")
                else:
                    print(f"✗ {script} has no main() function\n")
                    results[script] = {'status': 'NO_MAIN', 'time': 0}
                    
            except Exception as e:
                execution_time = time.time() - start_time
                print(f"✗ Error in {script}: {str(e)}\n")
                results[script] = {'status': 'ERROR', 'time': execution_time, 'error': str(e)}
        else:
            print(f"✗ {script} not found\n")
            results[script] = {'status': 'NOT_FOUND', 'time': 0}
    
    # Print summary
    print("=== EXECUTION SUMMARY ===")
    total_time = 0
    success_count = 0
    
    for script, result in results.items():
        status = result['status']
        exec_time = result['time']
        total_time += exec_time
        
        if status == 'SUCCESS':
            success_count += 1
            print(f"✓ {script:<35} - {exec_time:>6.2f}s")
        elif status == 'ERROR':
            print(f"✗ {script:<35} - ERROR: {result.get('error', 'Unknown')}")
        elif status == 'NOT_FOUND':
            print(f"✗ {script:<35} - FILE NOT FOUND")
        elif status == 'NO_MAIN':
            print(f"✗ {script:<35} - NO MAIN FUNCTION")
    
    print(f"\nTotal execution time: {total_time:.2f} seconds")
    print(f"Successful scripts: {success_count}/{len(scripts)}")
    
    # List output files
    print("\n=== OUTPUT FILES GENERATED ===")
    output_files = [f for f in os.listdir('.') if f.startswith('Image_HW2_') and f.endswith('.tif')]
    if output_files:
        for i, filename in enumerate(sorted(output_files), 1):
            print(f"{i:2d}. {filename}")
    else:
        print("No output files found.")
    
    return results

def analyze_results():
    """
    Provide recommendations for best enhancement methods
    """
    print("\n=== FILTER RECOMMENDATIONS ===")
    
    recommendations = {
        "Edge Enhancement": [
            "laplacian_enhancement.py - Best for sharp edge definition",
            "sobel_enhancement.py - Good balance of edge detection",
            "advanced_edge_filters.py - Comprehensive edge methods"
        ],
        "Noise Reduction": [
            "gaussian_blur_filter.py - Simple noise reduction",
            "median_filter.py - Salt-and-pepper noise removal", 
            "bilateral_filter.py - Edge-preserving smoothing"
        ],
        "Contrast Enhancement": [
            "histogram_equalization.py - Global contrast improvement",
            "adaptive_histogram_equalization.py - Local contrast enhancement",
            "contrast_stretching.py - Linear contrast adjustment"
        ],
        "Brightness Adjustment": [
            "gamma_log_transforms.py - Non-linear brightness control"
        ],
        "Pansharpening": [
            "pansharpening_methods.py - Multi-spectral enhancement"
        ],
        "Sharpening": [
            "highboost_unsharp.py - Unsharp masking",
            "highpass_filter.py - High-frequency emphasis"
        ]
    }
    
    for category, methods in recommendations.items():
        print(f"\n{category}:")
        for method in methods:
            print(f"  • {method}")
    
    print("\n=== USAGE GUIDELINES ===")
    print("1. For noisy images: Start with median_filter.py or bilateral_filter.py")
    print("2. For low contrast: Try adaptive_histogram_equalization.py")
    print("3. For blurry images: Use highboost_unsharp.py or laplacian_enhancement.py")
    print("4. For multi-spectral data: Apply pansharpening_methods.py")
    print("5. For fine-tuning: Adjust parameters in individual scripts")

if __name__ == '__main__':
    try:
        results = run_all_filters()
        analyze_results()
        
        print(f"\n=== COMPLETED ===")
        print("All available filters have been applied to Image_HW2.tif")
        print("Compare the output images to determine the best enhancement method for your needs.")
        
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        sys.exit(1)