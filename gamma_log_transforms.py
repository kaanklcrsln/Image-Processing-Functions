import numpy as np
import rasterio

def gamma_correction(infile='Image_HW2.tif', gamma=1.2, outfile=None):
    """
    Gamma correction for brightness and contrast adjustment
    """
    if outfile is None:
        outfile = f'Image_HW2_gamma{gamma:.1f}.tif'
    
    with rasterio.open(infile) as src:
        profile = src.profile.copy()
        data = src.read().astype(np.float32)
    
    def gamma_correct_band(band, gamma_val):
        # Normalize to 0-1 range
        band_min, band_max = band.min(), band.max()
        if band_max == band_min:
            return band
        
        normalized = (band - band_min) / (band_max - band_min)
        
        # Apply gamma correction
        corrected = np.power(normalized, gamma_val)
        
        # Scale back to original range
        return corrected * (band_max - band_min) + band_min
    
    enhanced = np.empty_like(data)
    for b in range(data.shape[0]):
        enhanced[b] = gamma_correct_band(data[b], gamma)
    
    profile.update(dtype=rasterio.float32)
    with rasterio.open(outfile, 'w', **profile) as dst:
        dst.write(enhanced.astype(np.float32))
    
    print(f"Gamma correction applied with gamma={gamma}, saved as {outfile}")
    return outfile

def logarithmic_transformation(infile='Image_HW2.tif', c=1.0, outfile=None):
    """
    Logarithmic transformation for dynamic range compression
    """
    if outfile is None:
        outfile = f'Image_HW2_log_c{c:.1f}.tif'
    
    with rasterio.open(infile) as src:
        profile = src.profile.copy()
        data = src.read().astype(np.float32)
    
    def log_transform_band(band, c_val):
        # Ensure positive values
        band_shifted = band - band.min() + 1
        
        # Apply log transformation
        log_transformed = c_val * np.log(1 + band_shifted)
        
        # Normalize to original range
        log_min, log_max = log_transformed.min(), log_transformed.max()
        if log_max != log_min:
            normalized = (log_transformed - log_min) / (log_max - log_min)
            return normalized * (band.max() - band.min()) + band.min()
        return band
    
    enhanced = np.empty_like(data)
    for b in range(data.shape[0]):
        enhanced[b] = log_transform_band(data[b], c)
    
    profile.update(dtype=rasterio.float32)
    with rasterio.open(outfile, 'w', **profile) as dst:
        dst.write(enhanced.astype(np.float32))
    
    print(f"Logarithmic transformation applied with c={c}, saved as {outfile}")
    return outfile

def main():
    # Test different gamma values
    gammas = [0.5, 0.8, 1.2, 1.5, 2.0]
    for gamma in gammas:
        gamma_correction(gamma=gamma)
    
    # Test logarithmic transformation
    c_values = [0.5, 1.0, 2.0]
    for c in c_values:
        logarithmic_transformation(c=c)

if __name__ == '__main__':
    main()