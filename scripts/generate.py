import shutil
import yaml
import csv
from datetime import datetime as dt, timedelta as td
import re
import json
import hashlib
import os
from pathlib import Path

BASE_FOLDER = Path(__file__).parent.parent.resolve()
TIME_REGEX = re.compile("\d{1,2}:\d{2}")
config = yaml.safe_load(open(BASE_FOLDER / "config.yaml", "r"))


def initialize():
    shutil.rmtree(BASE_FOLDER / "dist", ignore_errors=True)
    os.mkdir(BASE_FOLDER / "dist")


def dict_hash(dictionary):
    """MD5 hash of a dictionary."""
    dhash = hashlib.md5()
    # We need to sort arguments so {'a': 1, 'b': 2} is
    # the same as {'b': 2, 'a': 1}
    encoded = json.dumps(dictionary).encode()
    dhash.update(encoded)
    return dhash.hexdigest()


def load_timings(filepath: str, items: list):
    timings = list(csv.reader(open(filepath, "r")))
    header = timings[0]
    timings = timings[1:]
    if len(timings) < 365 or len(timings) > 366:
        raise Exception("Invalid Timings Data")
    data = {}
    first_date = dt.fromisoformat("2000-01-01")
    if len(timings) == 365:
        first_date = dt.fromisoformat("2001-01-01")
    for i, row in enumerate(timings):
        date = first_date + td(days=i)
        if len(row) != len(header):
            raise Exception("Invalid Timings Data")
        row_dict = {}
        for i in range(len(header)):
            if header[i] not in items:
                continue
            if not TIME_REGEX.match(row[i]):
                raise Exception(f"Invalid Timings Data @ {filepath} Row:{i+1}")
            row_dict[header[i]] = row[i]
        data[str(date.day).zfill(2) + str(date.month).zfill(2)] = row_dict

    return data


def load_iftarkar_timings(filepath: str, first_date: dt):
    timings = list(csv.reader(open(filepath, "r")))
    header = timings[0]
    timings = timings[1:]
    if len(timings) < 30 or len(timings) > 30:
        raise Exception("Invalid Timings Data")
    data = {}
    for i, row in enumerate(timings):
        date = first_date + td(days=i)
        if len(row) != len(header):
            raise Exception("Invalid Timings Data")
        row_dict = {}
        for i in range(len(header)):
            if not TIME_REGEX.match(row[i]):
                raise Exception(f"Invalid Timings Data @ {filepath} Row:{i+1}")
            row_dict[header[i]] = row[i].strip()
        data[str(date.day).zfill(2) + str(date.month).zfill(2)] = row_dict

    return data


def generate_data():
    data = {}
    for calendar in config["calendars"]:
        data[calendar["key"]] = {
            "name": calendar["name"],
            "description": calendar["description"],
            "timings": load_timings(
                BASE_FOLDER / ("raw_timings/" + calendar["timings"]),
                [x["key"] for x in calendar["items"]],
            ),
            "offsets": calendar["offsets"],
            "header": calendar["items"],
        }
    custom_config = config["custom_config"]
    for item in custom_config:
        description = ""
        if "description" in item:
            description = item["description"]
        item["description"] = f"{item['name']}. "
        if "fajrAngle" in item["parameters"]:
            item["description"] += f"Fajr Angle: {item['parameters']['fajrAngle']}. "
        if "maghribAngle" in item["parameters"]:
            item[
                "description"
            ] += f"Maghrib Angle: {item['parameters']['maghribAngle']}. "
        if "ishaAngle" in item["parameters"]:
            item["description"] += f"Isha Angle: {item['parameters']['ishaAngle']}. "
        if "ishaInterval" in item["parameters"]:
            item[
                "description"
            ] += f"Isha Angle: {item['parameters']['ishaInterval']} min. "
        item["description"] = item["description"].strip()
        item["description"] += f" {description}"
    hash_string = dict_hash(data)
    output = {"data": data, "hash": hash_string}
    json.dump(output, open(BASE_FOLDER / "dist/data.json", "w"))
    json.dump(custom_config, open(BASE_FOLDER / "dist/custom_config.json", "w"))
    json.dump({"hash": hash_string}, open(BASE_FOLDER / "dist/hash.json", "w"))


def generate_iftarkar():
    data = {}
    if config["iftarkar_calendars"] is not None:
        for calendar in config["iftarkar_calendars"]:
            data[calendar["key"]] = {
                "name": calendar["name"],
                "description": calendar["description"],
                "timings": load_iftarkar_timings(
                    BASE_FOLDER / ("raw_timings/" + calendar["timings"]),
                    dt.strptime(calendar["start_date"], "%d%m"),
                ),
                "offsets": [],
            }
    json.dump({"data": data}, open(BASE_FOLDER / "dist/iftarkar.json", "w"))


if __name__ == "__main__":
    initialize()
    generate_data()
    generate_iftarkar()
