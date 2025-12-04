import numpy as np
import rasterio
from scipy.ndimage import convolve, gaussian_filter

def canny_edge_enhancement(infile='Image_HW2.tif', sigma=1.0, low_threshold=0.1, high_threshold=0.2, alpha=0.5, outfile=None):
    """
    Canny edge detection and enhancement
    """
    if outfile is None:
        outfile = f'Image_HW2_canny_sigma{sigma}_alpha{alpha:.1f}.tif'
    
    with rasterio.open(infile) as src:
        profile = src.profile.copy()
        data = src.read().astype(np.float32)
    
    def canny_enhance_band(band, sigma, low_thresh, high_thresh, alpha):
        # Step 1: Gaussian smoothing
        smoothed = gaussian_filter(band, sigma=sigma)
        
        # Step 2: Gradient calculation
        sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
        sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)
        
        grad_x = convolve(smoothed, sobel_x, mode='reflect')
        grad_y = convolve(smoothed, sobel_y, mode='reflect')
        
        magnitude = np.sqrt(grad_x**2 + grad_y**2)
        
        # Normalize magnitude
        mag_max = magnitude.max()
        if mag_max > 0:
            magnitude = magnitude / mag_max
        
        # Step 3: Non-maximum suppression (simplified)
        angle = np.arctan2(grad_y, grad_x)
        
        # Step 4: Double thresholding
        strong_edges = magnitude > high_thresh
        weak_edges = (magnitude >= low_thresh) & (magnitude <= high_thresh)
        
        # Combine edges
        edges = strong_edges.astype(np.float32) + 0.5 * weak_edges.astype(np.float32)
        
        # Enhance original image with edges
        return band + alpha * edges * magnitude
    
    enhanced = np.empty_like(data)
    for b in range(data.shape[0]):
        enhanced[b] = canny_enhance_band(data[b], sigma, low_threshold, high_threshold, alpha)
    
    profile.update(dtype=rasterio.float32)
    with rasterio.open(outfile, 'w', **profile) as dst:
        dst.write(enhanced.astype(np.float32))
    
    print(f"Canny edge enhancement applied, saved as {outfile}")
    return outfile

def prewitt_edge_enhancement(infile='Image_HW2.tif', alpha=0.5, outfile=None):
    """
    Prewitt edge enhancement filter
    """
    if outfile is None:
        outfile = f'Image_HW2_prewitt_alpha{alpha:.1f}.tif'
    
    with rasterio.open(infile) as src:
        profile = src.profile.copy()
        data = src.read().astype(np.float32)
    
    # Prewitt kernels
    prewitt_x = np.array([
        [-1, 0, 1],
        [-1, 0, 1],
        [-1, 0, 1]
    ], dtype=np.float32)
    
    prewitt_y = np.array([
        [-1, -1, -1],
        [0, 0, 0],
        [1, 1, 1]
    ], dtype=np.float32)
    
    enhanced = np.empty_like(data)
    for b in range(data.shape[0]):
        grad_x = convolve(data[b], prewitt_x, mode='reflect')
        grad_y = convolve(data[b], prewitt_y, mode='reflect')
        gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        enhanced[b] = data[b] + alpha * gradient_magnitude
    
    profile.update(dtype=rasterio.float32)
    with rasterio.open(outfile, 'w', **profile) as dst:
        dst.write(enhanced.astype(np.float32))
    
    print(f"Prewitt enhancement applied with alpha={alpha}, saved as {outfile}")
    return outfile

def roberts_cross_enhancement(infile='Image_HW2.tif', alpha=0.5, outfile=None):
    """
    Roberts cross-gradient edge enhancement
    """
    if outfile is None:
        outfile = f'Image_HW2_roberts_alpha{alpha:.1f}.tif'
    
    with rasterio.open(infile) as src:
        profile = src.profile.copy()
        data = src.read().astype(np.float32)
    
    # Roberts cross kernels
    roberts_x = np.array([
        [1, 0],
        [0, -1]
    ], dtype=np.float32)
    
    roberts_y = np.array([
        [0, 1],
        [-1, 0]
    ], dtype=np.float32)
    
    enhanced = np.empty_like(data)
    for b in range(data.shape[0]):
        grad_x = convolve(data[b], roberts_x, mode='reflect')
        grad_y = convolve(data[b], roberts_y, mode='reflect')
        gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        enhanced[b] = data[b] + alpha * gradient_magnitude
    
    profile.update(dtype=rasterio.float32)
    with rasterio.open(outfile, 'w', **profile) as dst:
        dst.write(enhanced.astype(np.float32))
    
    print(f"Roberts cross enhancement applied with alpha={alpha}, saved as {outfile}")
    return outfile

def main():
    # Test Canny edge enhancement
    canny_edge_enhancement()
    
    # Test Prewitt enhancement
    alphas = [0.3, 0.5, 0.8]
    for alpha in alphas:
        prewitt_edge_enhancement(alpha=alpha)
        roberts_cross_enhancement(alpha=alpha)

if __name__ == '__main__':
    main()