import requests
import os

base_url = "https://storage.googleapis.com/geospatial-interview-2025-sept/"

filenames = [
    "2025-02-02.tiff",
    "2025-03-14.tiff",
    "2025-04-25.tiff",
    "2025-05-13.tiff",
    "2025-07-25.tiff"
]


def download_images():

    for filename in filenames:

        #check if the files already exist in the input_data dir
        if filename in os.listdir("input_data"):
            print("File {} already found in input_data folder, skipping download".format(filename))

        else:
            print("Downloading file {}".format(filename))
            response = requests.get(base_url+filename)

            with open("input_data/{}".format(filename), "wb") as f:
                f.write(response.content)
            print("Downloaded sucessfully")


if __name__ == "__main__":
    download_images()