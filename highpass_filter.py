import numpy as np
import rasterio
from scipy.ndimage import convolve

def main(infile='Image_HW2.tif', outfile='Image_HW2_highpass.tif'):
    with rasterio.open(infile) as src:
        profile = src.profile.copy()
        data = src.read().astype(np.float32)

    kernel = np.array([
        [-1, -1, -1],
        [-1,  8, -1],
        [-1, -1, -1]
    ], dtype=np.float32) / 9.0

    filtered = np.empty_like(data, dtype=np.float32)

    for b in range(data.shape[0]):
        band = data[b]
        filtered[b] = convolve(band, kernel, mode='reflect')

    profile.update(dtype=rasterio.float32)
    with rasterio.open(outfile, 'w', **profile) as dst:
        dst.write(filtered.astype(np.float32))


if __name__ == '__main__':
    main()
