import numpy as np
import pandas as pd
import config
from utils import create_buffers, crop_to_buffer, apply_cloud_mask, compute_ndvi, remove_builtup
from plot_chart import plot_ndvi_series


def main(data_dir, points_fn, BUFFER_DIST, tif_filenames, NODATA, CLOUD_PROB_THRESHOLD, CLOUD_PROB_IDX, RED_IDX, NIR_IDX, NDVI_STD_THRESH, NDVI_MIN_THRESH):
    """
    Create NDVI time series for each location, computing the mean value of valid pixels for each buffer and date.
    Then, plot a chart of the time series.

    Args:
        data_dir (str) : path to the directory containing the input data.
        points_fn (str) : path to the csv file containing the point location coordinates.
        BUFFER_DIST (int) : buffer distance in meters.
        tif_filenames (list[str]) : list with filenames of each tif (original Sentinel-2 images).
        NODATA (int) : nodata value for the generated raster.
        CLOUD_PROB_THRESHOLD (int) : threshold of cloud probability used to filter clouds.
        CLOUD_PROB_IDX (int)  : index of the band in the numpy array that contains the cloud probability values.
        RED_IDX (int) : index of the red band in the numpy array.
        NIR_IDX (int) : index of the nir band in the numpy array.
        NDVI_STD_THRESH (int) : threshold of standard deviation used to filter builtup land.
        NDVI_MIN_THRESH (int) : threshold of minimum ndvi used to filter builtup land.
    
    Returns:
        None
    """


    # create buffer around locations
    buffers = create_buffers(data_dir, points_fn, BUFFER_DIST)

    # create dictionary to store ndvi arrays for each buffer
    ndvi_buffers = {}
    
    # for each buffer, open images and crop to buffer
    for i, b in enumerate(buffers):

        # create list to store ndvis
        ndvis_temp = []
        img_meta_temp = []

        geom = [b.__geo_interface__]

        for tif_filename in tif_filenames:

            cropped_img, img_meta, out_transform = crop_to_buffer(data_dir, tif_filename, geom, NODATA)

            #mask clouds
            cloudless_img = apply_cloud_mask(cropped_img, CLOUD_PROB_THRESHOLD, CLOUD_PROB_IDX, NODATA)
            #calculate ndvi
            ndvi = compute_ndvi(cloudless_img, RED_IDX, NIR_IDX, NODATA)

            ndvis_temp.append(ndvi)
            img_meta.update({
                    "driver": "GTiff",
                    "dtype": 'int16',
                    "height": ndvi.shape[1],
                    "width": ndvi.shape[2],
                    "transform": out_transform,
                    "count": 1,
                    "nodata": NODATA
                })
            img_meta_temp.append(img_meta)

        #remove builtup areas - keep only areas that are likely to be vegetation
        ndvis_temp = remove_builtup(ndvis_temp, NODATA, NDVI_STD_THRESH, NDVI_MIN_THRESH)
        
        
        ndvi_buffers[i] = np.nanmean(np.stack(ndvis_temp), axis=(1,2))

    df = pd.DataFrame(ndvi_buffers)
    #extract tif dates
    tif_dates = [f.replace('.tiff','') for f in tif_filenames]

    #set dates as df index
    df['dates'] = pd.to_datetime(tif_dates)
    df = df.set_index('dates')


    #plot NDVI time series
    plot_ndvi_series(df)



if __name__ == '__main__':

    main(
        config.data_dir,
        config.points_fn,
        config.BUFFER_DIST,
        config.tif_filenames,
        config.NODATA,
        config.CLOUD_PROB_THRESHOLD,
        config.CLOUD_PROB_IDX,
        config.RED_IDX,
        config.NIR_IDX,
        config.NDVI_STD_THRESH,
        config.NDVI_MIN_THRESH
        )

