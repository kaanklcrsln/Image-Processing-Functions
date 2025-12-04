import numpy as np
import rasterio
from scipy.ndimage import convolve

def bilateral_filter(infile='Image_HW2.tif', sigma_spatial=1.5, sigma_intensity=0.1, window_size=5, outfile=None):
    """
    Bilateral filter for edge-preserving smoothing
    """
    if outfile is None:
        outfile = f'Image_HW2_bilateral_ss{sigma_spatial}_si{sigma_intensity}.tif'
    
    with rasterio.open(infile) as src:
        profile = src.profile.copy()
        data = src.read().astype(np.float32)
    
    def bilateral_filter_band(band, sigma_s, sigma_i, size):
        # Normalize band to 0-1 range
        band_min, band_max = band.min(), band.max()
        if band_max == band_min:
            return band
        normalized = (band - band_min) / (band_max - band_min)
        
        # Pad image
        pad_size = size // 2
        padded = np.pad(normalized, pad_size, mode='reflect')
        filtered = np.zeros_like(normalized)
        
        # Create spatial weight matrix
        y, x = np.mgrid[-pad_size:pad_size+1, -pad_size:pad_size+1]
        spatial_weights = np.exp(-(x**2 + y**2) / (2 * sigma_s**2))
        
        for i in range(normalized.shape[0]):
            for j in range(normalized.shape[1]):
                # Get neighborhood
                neighborhood = padded[i:i+size, j:j+size]
                center_val = normalized[i, j]
                
                # Calculate intensity weights
                intensity_weights = np.exp(-((neighborhood - center_val)**2) / (2 * sigma_i**2))
                
                # Combined weights
                weights = spatial_weights * intensity_weights
                weights_sum = np.sum(weights)
                
                if weights_sum > 0:
                    filtered[i, j] = np.sum(neighborhood * weights) / weights_sum
                else:
                    filtered[i, j] = center_val
        
        # Scale back to original range
        return filtered * (band_max - band_min) + band_min
    
    enhanced = np.empty_like(data)
    for b in range(data.shape[0]):
        print(f"Processing band {b+1}/{data.shape[0]}")
        enhanced[b] = bilateral_filter_band(data[b], sigma_spatial, sigma_intensity, window_size)
    
    profile.update(dtype=rasterio.float32)
    with rasterio.open(outfile, 'w', **profile) as dst:
        dst.write(enhanced.astype(np.float32))
    
    print(f"Bilateral filter applied, saved as {outfile}")
    return outfile

def main():
    # Test with different parameters
    params = [
        (1.0, 0.1, 5),
        (1.5, 0.1, 5),
        (2.0, 0.2, 5)
    ]
    for sigma_s, sigma_i, size in params:
        bilateral_filter(sigma_spatial=sigma_s, sigma_intensity=sigma_i, window_size=size)

if __name__ == '__main__':
    main()