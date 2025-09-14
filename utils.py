import pandas as pd
import geopandas as gpd
import numpy as np
import rasterio
from rasterio.mask import mask
import os


def create_buffers(data_dir, points_fn, buffer_dist):
    """
    Create buffers from point locations.

    Args:
        data_dir (str) : path to the directory containing the input data.
        points_fn (str) : path to the csv file containing the point location coordinates.
        buffer_dist (int) : buffer distance in meters.
    
    Returns:
        pd.Series : buffers
    """

    #open points 
    df = pd.read_csv(os.path.join(data_dir,points_fn))

    #convert to geodataframe
    gdf = gpd.GeoDataFrame(
        df, 
        geometry=gpd.points_from_xy(df.X, df.Y),
        crs="EPSG:4326"  # WGS84 lat/lon
        )

    #reproject to projected crs (UTM 33N - covers Malta)
    gdf_utm = gdf.to_crs("EPSG:32633")

    #reproject back to WGS84 lat/lon
    buffer = gdf_utm.buffer(buffer_dist).to_crs("EPSG:4326")

    return buffer


def crop_to_buffer(data_dir, tif_filename, geom, NODATA):
    """
    Crop raster to buffer extent.

    Args:
        data_dir (str) : path to the directory containing the input data.
        tif_filename (str) : name of the tif file to be cropped.
        geom  : buffer geometry.
        NODATA (int) : nodata value for the generated raster.
    
    Returns:
        tuple(out_image, out_meta, out_transform)
    """

    with rasterio.open(os.path.join(data_dir,tif_filename)) as src:
        out_image, out_transform = mask(src, geom, crop=True, nodata=NODATA)
        out_meta = src.meta.copy()

    return out_image, out_meta, out_transform


def apply_cloud_mask(img_np, cloud_prob, cloud_prob_idx, NODATA):
    """
    Apply cloud mask to image.

    Args:
        img_np (np.ndarray) : image in the form of a numpy array.
        cloud_prob (int) : threshold of cloud probability used to filter clouds.
        cloud_prob_idx (int)  : index of the band in the numpy array that contains the cloud probability values.
        NODATA (int) : nodata value for the generated raster.
    
    Returns:
        np.ndarray : cloud filter image
    """
    

    cloud_prob_arr = img_np[cloud_prob_idx]

    cloud_mask = cloud_prob_arr < cloud_prob

    cloudless_img = np.where(cloud_mask, img_np, NODATA)

    return cloudless_img


def compute_ndvi(img_np, red_idx, nir_idx, NODATA):
    """
    Compute NDVI for image.

    Args:
        img_np (np.ndarray) : image in the form of a numpy array.
        red_idx (int) : index of the red band in the numpy array.
        nir_idx (int) : index of the nir band in the numpy array.
        NODATA (int) : nodata value for the generated raster.
    
    Returns:
        np.ndarray : ndvi image
    """

    mask = (img_np[0] != NODATA)

    ndvi = np.where(mask, 10000*(img_np[nir_idx] - img_np[red_idx])/(img_np[nir_idx] + img_np[red_idx]), NODATA)

    return np.expand_dims(ndvi, axis=0)


def remove_builtup(ndvis, NODATA, NDVI_STD_THRESH, NDVI_MIN_THRESH):
    """
    Remove builtup areas, leaving the image with areas that are more likely to correspond to vegetation.

    Args:
        ndvis (np.ndarray) : image in the form of a numpy array.
        NODATA (int) : nodata value for the generated raster.
        NDVI_STD_THRESH (int) : threshold of standard deviation used to filter builtup land.
        NDVI_MIN_THRESH (int) : threshold of minimum ndvi used to filter builtup land.

    
    Returns:
        np.ndarray : ndvi images
    """

    #stack ndvis
    ndvis_stacked = np.stack(ndvis)

    # replace NODATA with nan
    ndvis_stacked[ndvis_stacked==NODATA] = np.nan

    #compute std per pixel
    ndvis_std = np.nanstd(ndvis_stacked, axis=0)

    #compute max ndvi per pixel
    ndvis_max = np.nanmax(ndvis_stacked, axis=0)

    #create mask to remove builtup areas - if pixel meets one of the conditions, than it is likely to be vegetation
    #compute mask STD
    mask_std = ndvis_std > NDVI_STD_THRESH
    #compute mask MAX
    mask_max = ndvis_max > NDVI_MIN_THRESH
    #compute union
    final_mask = mask_std | mask_max

    #masked ndvis - with builtup removed
    masked_ndvis = []
    for ndvi in ndvis:
        ndvi[ndvi==NODATA] = np.nan
        masked_ndvis.append(np.where(final_mask, ndvi, np.nan).squeeze())

    return masked_ndvis

