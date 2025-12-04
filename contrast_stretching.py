import numpy as np
import rasterio

def contrast_stretching(infile='Image_HW2.tif', percentile_range=(2, 98), outfile=None):
    """
    Linear contrast stretching using percentile clipping
    """
    if outfile is None:
        outfile = f'Image_HW2_contrast_stretch_{percentile_range[0]}_{percentile_range[1]}.tif'
    
    with rasterio.open(infile) as src:
        profile = src.profile.copy()
        data = src.read().astype(np.float32)
    
    def stretch_band(band, pmin, pmax):
        # Calculate percentiles
        low_val = np.percentile(band, pmin)
        high_val = np.percentile(band, pmax)
        
        if high_val == low_val:
            return band
        
        # Linear stretch
        stretched = (band - low_val) / (high_val - low_val)
        
        # Scale to original range
        original_min, original_max = band.min(), band.max()
        stretched = stretched * (original_max - original_min) + original_min
        
        # Clip to original range
        return np.clip(stretched, original_min, original_max)
    
    enhanced = np.empty_like(data)
    for b in range(data.shape[0]):
        enhanced[b] = stretch_band(data[b], percentile_range[0], percentile_range[1])
    
    profile.update(dtype=rasterio.float32)
    with rasterio.open(outfile, 'w', **profile) as dst:
        dst.write(enhanced.astype(np.float32))
    
    print(f"Contrast stretching applied with percentiles {percentile_range}, saved as {outfile}")
    return outfile

def main():
    # Test different percentile ranges
    ranges = [(1, 99), (2, 98), (5, 95)]
    for prange in ranges:
        contrast_stretching(percentile_range=prange)

if __name__ == '__main__':
    main()