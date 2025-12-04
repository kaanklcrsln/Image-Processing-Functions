import numpy as np
import rasterio
from scipy.ndimage import convolve

def laplacian_edge_enhancement(infile='Image_HW2.tif', alpha=0.5, outfile=None):
    """
    Laplacian edge enhancement filter
    Enhanced = Original + alpha * Laplacian(Original)
    """
    if outfile is None:
        outfile = f'Image_HW2_laplacian_alpha{alpha:.1f}.tif'
    
    with rasterio.open(infile) as src:
        profile = src.profile.copy()
        data = src.read().astype(np.float32)
    
    # Standard Laplacian kernel
    laplacian_kernel = np.array([
        [0, -1, 0],
        [-1, 4, -1],
        [0, -1, 0]
    ], dtype=np.float32)
    
    enhanced = np.empty_like(data)
    for b in range(data.shape[0]):
        laplacian = convolve(data[b], laplacian_kernel, mode='reflect')
        enhanced[b] = data[b] + alpha * laplacian
    
    profile.update(dtype=rasterio.float32)
    with rasterio.open(outfile, 'w', **profile) as dst:
        dst.write(enhanced.astype(np.float32))
    
    print(f"Laplacian enhancement applied with alpha={alpha}, saved as {outfile}")
    return outfile

def main():
    # Test different alpha values
    alphas = [0.2, 0.5, 0.8, 1.0]
    for alpha in alphas:
        laplacian_edge_enhancement(alpha=alpha)

if __name__ == '__main__':
    main()