import numpy as np
import rasterio
from scipy.ndimage import uniform_filter, convolve

def adaptive_histogram_equalization(infile='Image_HW2.tif', clip_limit=2.0, tile_size=8, outfile=None):
    """
    Contrast Limited Adaptive Histogram Equalization (CLAHE)
    """
    if outfile is None:
        outfile = f'Image_HW2_clahe_clip{clip_limit}_tile{tile_size}.tif'
    
    with rasterio.open(infile) as src:
        profile = src.profile.copy()
        data = src.read().astype(np.float32)
    
    def clahe_band(band, clip_limit, tile_size):
        rows, cols = band.shape
        
        # Normalize to 0-1 range
        band_min, band_max = band.min(), band.max()
        if band_max == band_min:
            return band
        normalized = (band - band_min) / (band_max - band_min)
        
        # Calculate tile dimensions
        tile_rows = rows // tile_size
        tile_cols = cols // tile_size
        
        # Create output array
        output = np.zeros_like(normalized)
        
        for i in range(tile_rows):
            for j in range(tile_cols):
                # Define tile boundaries
                row_start = i * tile_size
                row_end = min((i + 1) * tile_size, rows)
                col_start = j * tile_size
                col_end = min((j + 1) * tile_size, cols)
                
                # Extract tile
                tile = normalized[row_start:row_end, col_start:col_end]
                
                # Calculate histogram
                hist, bins = np.histogram(tile.flatten(), bins=256, range=[0, 1])
                
                # Apply clip limit
                excess = np.maximum(hist - clip_limit * tile.size / 256, 0)
                hist = np.minimum(hist, clip_limit * tile.size / 256)
                redistribution = excess.sum() / 256
                hist += redistribution
                
                # Calculate CDF
                cdf = hist.cumsum()
                cdf_normalized = cdf / cdf[-1]
                
                # Apply equalization to tile
                equalized_tile = np.interp(tile.flatten(), bins[:-1], cdf_normalized)
                output[row_start:row_end, col_start:col_end] = equalized_tile.reshape(tile.shape)
        
        # Scale back to original range
        return output * (band_max - band_min) + band_min
    
    enhanced = np.empty_like(data)
    for b in range(data.shape[0]):
        print(f"Processing band {b+1}/{data.shape[0]} with CLAHE")
        enhanced[b] = clahe_band(data[b], clip_limit, tile_size)
    
    profile.update(dtype=rasterio.float32)
    with rasterio.open(outfile, 'w', **profile) as dst:
        dst.write(enhanced.astype(np.float32))
    
    print(f"CLAHE applied with clip_limit={clip_limit}, tile_size={tile_size}, saved as {outfile}")
    return outfile

def main():
    # Test different CLAHE parameters
    params = [
        (2.0, 8),
        (3.0, 8),
        (2.0, 16)
    ]
    for clip_limit, tile_size in params:
        adaptive_histogram_equalization(clip_limit=clip_limit, tile_size=tile_size)

if __name__ == '__main__':
    main()