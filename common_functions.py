import requests
import os


def download_pick(url, path):
    folder, img_name = os.path.split(path)
    if not os.path.exists(folder):
        os.makedirs(folder)
    response = requests.get(url)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)
