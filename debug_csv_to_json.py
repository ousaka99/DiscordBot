import json
import csv
import codecs

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
