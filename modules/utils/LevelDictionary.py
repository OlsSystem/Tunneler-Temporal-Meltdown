# Level Dictionary data to be used for menus and level generation.
levelById = {
    "CH1": {
        "name": "Chapter 1",
        "levels": [
            {"id": "LV1", "name": "Level 1: The Beginning"},
            {"id": "LV2", "name": "Level 2: The Middle"},
        ]
    },
    "CH2": {
        "name": "Chapter 2",
        "levels": [
            {"id": "LV1", "name": "Level 1: What?"},
        ]
    },
}

def getLevelName(chapterId, levelId):
    for level in levelById[chapterId]["levels"]:
        if level["id"] == levelId:
            return level["name"]
    return None