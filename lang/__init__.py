import os
import sys

import yaml

languages = {}
languages_present = {}


def get_string(lang: str):
    return languages[lang]


for filename in os.listdir(r"./lang/"):
    if not filename.endswith(".yml"):
        continue
    if "en" not in languages:
        languages["en"] = yaml.safe_load(
            open(r"./lang/en.yml",
                 encoding="utf8")
        )
        languages_present["en"] = languages["en"]["name"]
    if filename.endswith(".yml"):
        language_name = filename[:-4]
        if language_name == "en":
            continue
        languages[language_name] = yaml.safe_load(
            open(f"./lang/{filename}",
                 encoding="utf8")
        )

        for item in languages["en"]:
            if item not in languages[language_name]:
                languages[language_name][item] = languages["en"][item]
    try:
        languages_present[language_name] = languages[language_name]["name"]
    except Exception as e:
        print(f"Error while loading {language_name} language: {e}")
        sys.exit()
