import numpy as np
import rasterio
from scipy.ndimage import gaussian_filter

def pansharpening_brovey(ms_file='Image_HW2.tif', pan_file=None, outfile=None):
    """
    Brovey pansharpening method
    If pan_file is None, uses the first band as panchromatic
    """
    if outfile is None:
        outfile = 'Image_HW2_pansharp_brovey.tif'
    
    with rasterio.open(ms_file) as src:
        profile = src.profile.copy()
        ms_data = src.read().astype(np.float32)
    
    if pan_file is None:
        # Use first band as panchromatic (highest resolution assumed)
        pan_data = ms_data[0]
        ms_bands = ms_data[1:] if ms_data.shape[0] > 1 else ms_data
    else:
        with rasterio.open(pan_file) as pan_src:
            pan_data = pan_src.read(1).astype(np.float32)
        ms_bands = ms_data
    
    # Calculate intensity (mean of all MS bands)
    intensity = np.mean(ms_bands, axis=0)
    
    # Avoid division by zero
    intensity = np.where(intensity == 0, 1e-8, intensity)
    
    # Apply Brovey transform
    sharpened = np.empty_like(ms_bands)
    for i in range(ms_bands.shape[0]):
        sharpened[i] = (ms_bands[i] / intensity) * pan_data
    
    profile.update(count=sharpened.shape[0], dtype=rasterio.float32)
    with rasterio.open(outfile, 'w', **profile) as dst:
        dst.write(sharpened.astype(np.float32))
    
    print(f"Brovey pansharpening applied, saved as {outfile}")
    return outfile

def pansharpening_ihs(ms_file='Image_HW2.tif', pan_file=None, outfile=None):
    """
    IHS (Intensity-Hue-Saturation) pansharpening method
    """
    if outfile is None:
        outfile = 'Image_HW2_pansharp_ihs.tif'
    
    with rasterio.open(ms_file) as src:
        profile = src.profile.copy()
        ms_data = src.read().astype(np.float32)
    
    if pan_file is None:
        # Use first band as panchromatic
        pan_data = ms_data[0]
        ms_bands = ms_data[1:] if ms_data.shape[0] > 1 else ms_data
    else:
        with rasterio.open(pan_file) as pan_src:
            pan_data = pan_src.read(1).astype(np.float32)
        ms_bands = ms_data
    
    # Ensure we have at least 3 bands for RGB
    if ms_bands.shape[0] < 3:
        # Duplicate bands to make RGB
        while ms_bands.shape[0] < 3:
            ms_bands = np.concatenate([ms_bands, ms_bands[:1]], axis=0)
    
    # Take first 3 bands as RGB
    r, g, b = ms_bands[0], ms_bands[1], ms_bands[2]
    
    # RGB to IHS transformation
    intensity = (r + g + b) / 3.0
    
    # Replace intensity with panchromatic
    new_intensity = pan_data
    
    # Calculate the difference
    diff = new_intensity - intensity
    
    # Add the difference to each band
    sharpened = np.empty_like(ms_bands)
    for i in range(ms_bands.shape[0]):
        sharpened[i] = ms_bands[i] + diff
    
    profile.update(count=sharpened.shape[0], dtype=rasterio.float32)
    with rasterio.open(outfile, 'w', **profile) as dst:
        dst.write(sharpened.astype(np.float32))
    
    print(f"IHS pansharpening applied, saved as {outfile}")
    return outfile

def pansharpening_pca(ms_file='Image_HW2.tif', pan_file=None, outfile=None):
    """
    PCA (Principal Component Analysis) pansharpening method
    """
    if outfile is None:
        outfile = 'Image_HW2_pansharp_pca.tif'
    
    with rasterio.open(ms_file) as src:
        profile = src.profile.copy()
        ms_data = src.read().astype(np.float32)
    
    if pan_file is None:
        # Use first band as panchromatic
        pan_data = ms_data[0]
        ms_bands = ms_data[1:] if ms_data.shape[0] > 1 else ms_data
    else:
        with rasterio.open(pan_file) as pan_src:
            pan_data = pan_src.read(1).astype(np.float32)
        ms_bands = ms_data
    
    # Reshape for PCA
    rows, cols = ms_bands.shape[1], ms_bands.shape[2]
    reshaped = ms_bands.reshape(ms_bands.shape[0], -1).T
    
    # Calculate covariance matrix
    cov_matrix = np.cov(reshaped.T)
    
    # Calculate eigenvalues and eigenvectors
    eigenvals, eigenvecs = np.linalg.eigh(cov_matrix)
    
    # Sort by eigenvalues (descending)
    idx = np.argsort(eigenvals)[::-1]
    eigenvecs = eigenvecs[:, idx]
    
    # Transform to PC space
    pc_data = np.dot(reshaped, eigenvecs)
    
    # Replace first PC with panchromatic
    pc_data[:, 0] = pan_data.flatten()
    
    # Transform back
    sharpened_flat = np.dot(pc_data, eigenvecs.T)
    sharpened = sharpened_flat.T.reshape(ms_bands.shape)
    
    profile.update(count=sharpened.shape[0], dtype=rasterio.float32)
    with rasterio.open(outfile, 'w', **profile) as dst:
        dst.write(sharpened.astype(np.float32))
    
    print(f"PCA pansharpening applied, saved as {outfile}")
    return outfile

def main():
    # Apply different pansharpening methods
    pansharpening_brovey()
    pansharpening_ihs()
    pansharpening_pca()

if __name__ == '__main__':
    main()