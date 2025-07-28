import os
import numpy as np
import tifffile
import cohere_core.utilities as ut

def preprocess(experiment_dir):
    config_prep = ut.read_config(ut.join(experiment_dir, 'conf', 'config_prep'))
    data_dir = config_prep['data_dir']

    tiff_files = [f for f in os.listdir(data_dir) if f.endswith('.tiff') or f.endswith('.tif')]

    if not tiff_files:
        raise ValueError("No TIFF files found in the specified directory.")

    # Read the first image to get the shape
    first_image = tifffile.imread(os.path.join(data_dir, tiff_files[0]))
    sum_image = np.zeros_like(first_image, dtype=np.float64)

    for tiff_file in tiff_files:
        image = tifffile.imread(os.path.join(data_dir, tiff_file))
        sum_image += image

    average_image = sum_image / len(tiff_files)

    ut.save_tif(average_image, ut.join(experiment_dir, 'prep_data.tif'))