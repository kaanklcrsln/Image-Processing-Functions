import argparse
import numpy as np
import rasterio
from scipy.ndimage import uniform_filter


def highboost_band(band, k=1.5):
    blurred = uniform_filter(band, size=3, mode='reflect')
    mask = band - blurred
    return band + k * mask


def main(infile='Image_HW2.tif', k=1.5):
    with rasterio.open(infile) as src:
        profile = src.profile.copy()
        band1 = src.read(1).astype(np.float32)
        orig_dtype = src.dtypes[0]

    boosted = highboost_band(band1, k=k)

    try:
        npdtype = np.dtype(orig_dtype)
        if np.issubdtype(npdtype, np.integer):
            info = np.iinfo(npdtype)
            min_val, max_val = info.min, info.max
        else:
            info = np.finfo(npdtype)
            min_val, max_val = info.min, info.max
    except Exception:
        min_val, max_val = 0, 65535

    boosted_clipped = np.clip(boosted, min_val, max_val).astype(npdtype)

    outfile = f"Image_HW2_B1_highboost_k{float(k):.2f}.tif"

    profile.update(count=1, dtype=orig_dtype)

    with rasterio.open(outfile, 'w', **profile) as dst:
        dst.write(boosted_clipped, 1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='High-boost filtering on B1 (NIR)')
    parser.add_argument('--k', type=float, default=1.5, help='boost factor (k > 1)')
    parser.add_argument('--infile', type=str, default='Image_HW2.tif', help='input GeoTIFF')
    args = parser.parse_args()
    main(infile=args.infile, k=args.k)
