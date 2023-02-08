import requests
import os


def download_image(url, path):
    folder, img_name = os.path.split(path)
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)
