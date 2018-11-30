import json


def getjsonitems(search_keys):
    gifts = []
    with open("./items/items.json", "r", encoding="UTF-8") as search_file:
        items = json.loads(search_file.read())

    dict_items = dict(items)
    for key in dict_items:
        if dict_items[key][1:] == search_keys:
            gifts.append(tuple([key, dict_items[key][0]]))
    return gifts
