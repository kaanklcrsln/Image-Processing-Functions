import numpy as np
import rasterio
from scipy.ndimage import gaussian_filter

def gaussian_blur_filter(infile='Image_HW2.tif', sigma=1.0, outfile=None):
    """
    Gaussian blur filter for noise reduction and smoothing
    """
    if outfile is None:
        outfile = f'Image_HW2_gaussian_blur_sigma{sigma:.1f}.tif'
    
    with rasterio.open(infile) as src:
        profile = src.profile.copy()
        data = src.read().astype(np.float32)
    
    # Apply Gaussian blur to each band
    filtered = np.empty_like(data)
    for b in range(data.shape[0]):
        filtered[b] = gaussian_filter(data[b], sigma=sigma, mode='reflect')
    
    # Maintain original data type
    profile.update(dtype=rasterio.float32)
    with rasterio.open(outfile, 'w', **profile) as dst:
        dst.write(filtered.astype(np.float32))
    
    print(f"Gaussian blur filter applied with sigma={sigma}, saved as {outfile}")
    return outfile

def main():
    # Test different sigma values
    sigmas = [0.5, 1.0, 1.5, 2.0]
    for sigma in sigmas:
        gaussian_blur_filter(sigma=sigma)

if __name__ == '__main__':
    main()