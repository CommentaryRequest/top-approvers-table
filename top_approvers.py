#!/usr/bin/python3

import requests
import authsettings

HEADERS = {
    "User-Agent": "top approvers checker by user #1054326"
}

users = [
    "Temporarily", "Not_One_Of_Us", "Login_to_view", "Slacc", "Kuruma", "Farm", "magcolo", "heartattack", "Ardouru", "Machikado", "user_63619", "Dramorian", "Pork_Belly", "user_1141717", "user_900734", "LenaLatoya", "MiiaBestLamia", "oesla", "user_885514", "Laudividni", "Shallie", "user_827019", "user_59923", "Nephren", "m4rs", "user_266329", "Alex_MKW", "SciFi", "Cattywampus", "archaist", "UnknownDummy", "cnmanx", "keonas", "Miene", "NNescio", "Apollyon", "OniTea", "Mascarpone", "zigzag", "final_name", "Ephyon", "Nitrogen09", "fossilnix", "Bapabooiee", "NWSiaCB", "Himegami_Akane", "kiyah123", "Bibs", "maoko", "reiyasona", "TheodoricBlood", "FeKa", "Sauced", "user_10357", "Henduluin", ".grey", "pikuchan", "Cephalus", "Joe_Thighsman", "Nakoruru", "hipsterfont", "Tieria", "thraxus", "ePlus", "Altered", "alicemaiwaifu", "wareya", "Bloodletter", "Arantheus", "Log", "Xz", "MagicalAsparagus", "BlueFox", "DetBarkhorn", "Evangeline_A.K._McDowell", "HeaterOM", "Akaineko", "kurohanna", "Cherem", "Basil27", "DanKuno", "user_418493", "baybee09", "Cinnamon_Toast", "dispy", "user_166417", "yyflandre", "user_201502", "user_460797", "Coconut", "RumittanceWuzHere111", "homeless_homo", "0xCCBA696", "glahglahglah", "cheese", "cleartailcat", "bored_man", "thatdog", "darkship", "PoringSmasher", "user_98478", "LaC", "user_287254", "fuzzycat", "Snesso", "Enact", "ppayne", "StorminNorman", "Bansho", "KaitoDies", "15312134215123141", "Mr_GT", "Chun", "killerstickz", "igotcha", "Matroska56", "Magus", "roastbeefy", "7HS", "neoki3", "Eleven", "korehakoi", "RisaMadara", "reese"]
inactive_approvers = users.copy()

page = 1
while True:
    print(f"Fetching users page #{page}")
    resp = requests.get(
        "https://danbooru.donmai.us/users.json",
        params={
            "search[level]": ">=37",
            "page": page,
            "login": authsettings.LOGIN,
            "api_key": authsettings.APIKEY,
            "limit": 1000
        },
        headers=HEADERS
    ).json()
    page += 1
    if len(resp) == 0:
        break
    for user in resp:
        users.append(user["name"])

counts = {}
for user in users:
    print(f"Fetching approval count for {user}")
    while True:
        try:
            count = requests.get(
                "https://danbooru.donmai.us/counts/posts.json",
                params={
                    "tags": f"approver:{user}",
                    "login": authsettings.LOGIN,
                    "api_key": authsettings.APIKEY,
                },
                headers=HEADERS,
            ).json()["counts"]["posts"]
            break
        except requests.exceptions.JSONDecodeError:
            continue
    counts[user] = count

counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))
total_approvals = sum(counts.values())

print(f"Total approvals: {total_approvals}")
print("---===*** Top Approvers Table(tm) ***===---")
for i, (key, value) in enumerate(counts.items()):
    percentage = round(value / total_approvals * 100, 3)
    print(f"{i+1}. {key}{" (inactive)" if key in inactive_approvers else ""}: {value} approvals ({percentage}%)")
