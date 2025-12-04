import numpy as np
import rasterio

def histogram_equalization(infile='Image_HW2.tif', outfile=None):
    """
    Histogram equalization for contrast enhancement
    """
    if outfile is None:
        outfile = f'Image_HW2_histogram_equalized.tif'
    
    with rasterio.open(infile) as src:
        profile = src.profile.copy()
        data = src.read().astype(np.float32)
    
    def equalize_band(band):
        # Normalize to 0-1 range
        band_min, band_max = band.min(), band.max()
        if band_max == band_min:
            return band
        
        normalized = (band - band_min) / (band_max - band_min)
        
        # Calculate histogram
        hist, bins = np.histogram(normalized.flatten(), bins=256, range=[0, 1])
        
        # Calculate cumulative distribution function (CDF)
        cdf = hist.cumsum()
        cdf_normalized = cdf / cdf[-1]
        
        # Interpolate to get equalized values
        equalized = np.interp(normalized.flatten(), bins[:-1], cdf_normalized)
        equalized = equalized.reshape(band.shape)
        
        # Scale back to original range
        return equalized * (band_max - band_min) + band_min
    
    enhanced = np.empty_like(data)
    for b in range(data.shape[0]):
        enhanced[b] = equalize_band(data[b])
    
    profile.update(dtype=rasterio.float32)
    with rasterio.open(outfile, 'w', **profile) as dst:
        dst.write(enhanced.astype(np.float32))
    
    print(f"Histogram equalization applied, saved as {outfile}")
    return outfile

def main():
    histogram_equalization()

if __name__ == '__main__':
    main()