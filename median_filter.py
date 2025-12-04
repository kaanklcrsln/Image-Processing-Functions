import numpy as np
import rasterio
from scipy.ndimage import median_filter

def median_filter_enhancement(infile='Image_HW2.tif', size=3, outfile=None):
    """
    Median filter for noise reduction while preserving edges
    """
    if outfile is None:
        outfile = f'Image_HW2_median_size{size}.tif'
    
    with rasterio.open(infile) as src:
        profile = src.profile.copy()
        data = src.read().astype(np.float32)
    
    # Apply median filter to each band
    filtered = np.empty_like(data)
    for b in range(data.shape[0]):
        filtered[b] = median_filter(data[b], size=size, mode='reflect')
    
    profile.update(dtype=rasterio.float32)
    with rasterio.open(outfile, 'w', **profile) as dst:
        dst.write(filtered.astype(np.float32))
    
    print(f"Median filter applied with size={size}, saved as {outfile}")
    return outfile

def main():
    # Test different kernel sizes
    sizes = [3, 5, 7]
    for size in sizes:
        median_filter_enhancement(size=size)

if __name__ == '__main__':
    main()