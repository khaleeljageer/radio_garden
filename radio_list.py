import json
import logging
import os
from datetime import datetime

import requests
import yaml
from github import Github

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

THIS_DIR: str = os.path.dirname(os.path.abspath(__file__))


def connect(config: dict) -> dict:
    try:
        respone = requests.get(config["RADIO_URL"])
        if respone.ok:
            data = respone.json()
            return data["data"]
        else:
            return {"list": []}
    except:
        return {"list": []}


def get_india(list_array: list) -> str:
    output_dict = [
        item
        for item in list_array
        if item["country"] == "India" or item["country"] == "Sri Lanka"
    ]
    output_json = json.dumps({"list": output_dict}, indent=4, sort_keys=True)
    return output_json


def update_github(data: dict, path_: str, config: dict):
    repo = Github(config["ACCESS_TOKEN"]).get_repo(config["REPO_NAME"])
    json_file = repo.get_contents(path_)
    now: str = datetime.now().isoformat(" ", "seconds")
    commit_message = f"update {json_file.name} @ {now}"
    repo.update_file(json_file.path, commit_message, data, json_file.sha)
    logger.info("updated %s @ %s", json_file.name, now)


if __name__ == "__main__":
    f = open(os.path.join(THIS_DIR, "config.yaml"))
    config = yaml.safe_load(f)
    response = connect(config)
    radio_list = response["list"]
    if radio_list:
        india_list = get_india(radio_list)
        update_github(india_list, "radio_list.json", config)
        logger.info("File updated...")
    else:
        logger.info("Empty Response")
