import main
import requests
import user
import json


def topLogin(data: list) -> str:

    rewards: user.Rewards = data[0]
    login: user.Login = data[1]
    bonus: user.Bonus or str = data[2]
    with open('login.json', 'r', encoding='utf-8')as f:
        data22 = json.load(f)

        name1 = data22['cache']['replaced']['userGame'][0]['name']
        fpids1 = data22['cache']['replaced']['userGame'][0]['friendCode']
    
    messageBonus = ''
    nl = '\n'

    if bonus != "No Bonus":
        messageBonus += f"__{bonus.message}__{nl}```{nl.join(bonus.items)}```"

        if bonus.bonus_name != None:
            messageBonus += f"{nl}__{bonus.bonus_name}__{nl}{bonus.bonus_detail}{nl}```{nl.join(bonus.bonus_camp_items)}```"

        messageBonus += "\n"

    return f"{name1} \\[{main.fate_region}] Lv.{rewards.level}\n已登录 {login.login_days}/{login.total_days} 天\n护符: {rewards.ticket}\n圣晶石: {rewards.stone} 圣晶片:{rewards.sqf01}\n"



def shop(item: str, quantity: int) -> str:

    return f"\\[兑换]{quantity} x {item}, AP -{40 * quantity}\n"



def drawFP(servants, missions) -> str:

    message_mission = ""
    message_servant = ""
    
    if (len(servants) > 0):
        servants_atlas = requests.get(
            f"https://api.atlasacademy.io/export/JP/basic_svt.json").json()

        svt_dict = {svt["id"]: svt for svt in servants_atlas}

        for servant in servants:
            objectId = servant.objectId
            if objectId in svt_dict:
                svt = svt_dict[objectId]
                message_servant += f"`{svt['name']}` "
            else:
                continue

    if(len(missions) > 0):
        for mission in missions:
            message_mission += f"__{mission.message}__\n{mission.progressTo}/{mission.condition}\n"

    return f"\\[友情池]\n{message_mission}\n{message_servant}"



def LTO_Gacha(servants) -> str:

    message_servant = ""
    
    if (len(servants) > 0):
        servants_atlas = requests.get(
            f"https://api.atlasacademy.io/export/JP/basic_svt.json").json()

        svt_dict = {svt["id"]: svt for svt in servants_atlas}

        for servant in servants:
            objectId = servant.objectId
            if objectId in svt_dict:
                svt = svt_dict[objectId]
                message_servant += f"`{svt['name']}` "
            else:
                continue

    
    return f"\\[限定友情池].\n{message_servant}"



def Present(name, namegift, object_id_count) -> str:
    
    return f"\\[兑换] \n{name}\n{namegift} x{object_id_count}\n"

