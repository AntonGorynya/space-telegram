import requests
import json
import os


def download_image(url, path):
    folder, img_name = os.path.split(path)
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)


def read_db():
    os.makedirs('./images', exist_ok=True)
    if os.path.exists('./images/db.txt'):
        with open('./images/db.txt', 'r') as f:
            img_descriptions = f.read()
        return json.loads(img_descriptions)
    else:
        return {}
