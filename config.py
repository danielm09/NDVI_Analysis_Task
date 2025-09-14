
#### PATHS AND FILENAMES ####
# define input_data dir
data_dir = "input_data"
# define csv points filename
points_fn = "point_locations.csv"
# define tif filenames
tif_filenames = [
    "2025-02-02.tiff",
    "2025-03-14.tiff",
    "2025-04-25.tiff",
    "2025-05-13.tiff",
    "2025-07-25.tiff"
]
###########################

#### CONSTANTS ####
#define nodata value
NODATA = 32767
#define Red, NIR and Cloud Probability band indices
RED_IDX = 3
NIR_IDX = 7
CLOUD_PROB_IDX = 12
####################

#### VARIABLES ####
#define cloud probability threshold
CLOUD_PROB_THRESHOLD = 50

#define ndvi std threshold
NDVI_STD_THRESH = 1000
NDVI_MIN_THRESH = 2000

#define buffer distance (in meters)
BUFFER_DIST = 1000