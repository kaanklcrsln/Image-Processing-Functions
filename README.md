<<<<<<< HEAD
## Image Processing Filters Collection

This repository contains a collection of Python scripts for popular image enhancement and pansharpening filters, tested on `Image_HW2.tif`.

### Main Filters
- Edge Enhancement: `laplacian_enhancement.py`, `sobel_enhancement.py`, `advanced_edge_filters.py`, `highpass_filter.py`
- Noise Reduction: `gaussian_blur_filter.py`, `median_filter.py`, `bilateral_filter.py`
- Contrast Enhancement: `histogram_equalization.py`, `adaptive_histogram_equalization.py`, `contrast_stretching.py`
- Brightness: `gamma_log_transforms.py`
- Sharpening: `highboost_unsharp.py`, `highpass_filter.py`
- Pansharpening: `pansharpening_methods.py`

### Usage

Run all filters:
```bash
python run_all_filters.py
```
Run a single filter:
```bash
python gaussian_blur_filter.py
python laplacian_enhancement.py
# ...
```

### Requirements
```
numpy
rasterio
scipy
```
Install:
```bash
pip install numpy rasterio scipy
```

### Notes
- All scripts use `Image_HW2.tif` as input.
- Output files: `Image_HW2_[filter]_[params].tif`
- See each script for parameter options.
- `run_all_filters.py` runs all and summarizes results.
