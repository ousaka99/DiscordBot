import json
import csv
import codecs
from itertools import groupby
from collections import defaultdict

json_data = {}

# ship_table.csvの読み込み
json_list = []
with open('../ship_table.csv', 'r') as f:
    kind_list = ['空母', '戦艦', '巡洋', '駆逐']
    # list of dictの作成
    for line in csv.DictReader(f):
        json_list.append(line)

    # data check
    for x in json_list:
        x['hp_add'] = round(float(x['hp_add']))
        if 0 == len(x['nation']):
            raise ValueError("nation error!")
        if 1 > int(x['tier']) or int(x['tier']) > 10:
            raise ValueError("tier error!")
        if 0 == len(x['kind']):
            raise ValueError("kind error!")
        if x['kind'] not in kind_list:
            raise ValueError("kind_list error!")
        if 0 == len(x['name']):
            raise ValueError("name error!")
        if 1 > int(x['hp']) or int(x['hp']) > 250000:
            raise ValueError("hp error!")
        if 0 > int(x['hp_add']) or int(x['hp_add']) > 200000:
            raise ValueError("hp_add error!")

    json_data["ships"] = json_list

# ship_table.jsonへの出力
with codecs.open('./ship_table.json', 'w', encoding="utf-8_sig") as f:
    # JSONへの書き込み
    json.dump(json_data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


json_data = {}

# luck_table.csvの読み込み
csv_list = []
luck_item_list = defaultdict(list)
luck_comment_list = {}
with open('../luck_table.csv', 'r') as f:
    # list of dictの作成
    for line in csv.DictReader(f):
        csv_list.append(line)

    # data check
    for x in csv_list:
        if x['kind'] != '〃':
            kind = x['kind']
            comment = x['comment']
        else:
            x['kind'] = kind
            x['comment'] = comment

        if 0 == len(x['kind']):
            raise ValueError("kind error!")
        if 0 == len(x['comment']):
            raise ValueError("comment error!")
        if 0 == len(x['item']):
            raise ValueError("item error!")
        if 1 > int(x['weight']) or int(x['weight']) > 100:
            raise ValueError("weight error!")

    # data
    for (kind, kind_group) in groupby(csv_list, lambda e: e['kind']):
        comment = ""
        for x in kind_group:
            items = [x['item'], x['weight']]
            luck_item_list[kind].append(items)
            comment = x['comment']
        luck_comment_list[kind] = comment

    json_data["luck_items"] = luck_item_list
    json_data["luck_comment"] = luck_comment_list

# luck_table.jsonへの出力
with codecs.open('./luck_table.json', 'w', encoding="utf-8_sig") as f:
    # JSONへの書き込み
    json.dump(json_data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
