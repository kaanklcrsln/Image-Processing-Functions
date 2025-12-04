import numpy as np
import rasterio
from scipy.ndimage import convolve

def sobel_edge_enhancement(infile='Image_HW2.tif', alpha=0.5, outfile=None):
    """
    Sobel edge enhancement filter combining horizontal and vertical gradients
    """
    if outfile is None:
        outfile = f'Image_HW2_sobel_alpha{alpha:.1f}.tif'
    
    with rasterio.open(infile) as src:
        profile = src.profile.copy()
        data = src.read().astype(np.float32)
    
    # Sobel kernels
    sobel_x = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ], dtype=np.float32)
    
    sobel_y = np.array([
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1]
    ], dtype=np.float32)
    
    enhanced = np.empty_like(data)
    for b in range(data.shape[0]):
        grad_x = convolve(data[b], sobel_x, mode='reflect')
        grad_y = convolve(data[b], sobel_y, mode='reflect')
        gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        enhanced[b] = data[b] + alpha * gradient_magnitude
    
    profile.update(dtype=rasterio.float32)
    with rasterio.open(outfile, 'w', **profile) as dst:
        dst.write(enhanced.astype(np.float32))
    
    print(f"Sobel enhancement applied with alpha={alpha}, saved as {outfile}")
    return outfile

def main():
    # Test different alpha values
    alphas = [0.2, 0.5, 0.8, 1.0]
    for alpha in alphas:
        sobel_edge_enhancement(alpha=alpha)

if __name__ == '__main__':
    main()