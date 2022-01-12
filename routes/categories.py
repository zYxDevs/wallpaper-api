import re

import requests
from fastapi import HTTPException, status

from routes import config, router


@router.get(path="/category", tags=['Category'])
async def get_category_list():
    return config.wallpaper_categories


@router.get(path="/category/{name}", tags=['Category'])
async def get_collections_from_category(name: str):
    if name not in config.wallpaper_categories:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'category not found')
    print(config.wallpaper_api_url+config.wallpaper_search_path+name)
    pack_response = requests.get(
        config.wallpaper_api_url+config.wallpaper_search_path+name).text
    extracted_wlprs = re.findall(
        config.wallpaper_collection_regex, pack_response)
    extracted_wlprs = list(set(extracted_wlprs))
    if extracted_wlprs:
        return extracted_wlprs
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'no result found')
