import os
import requests
import time
import json
import fgourl
import user
import coloredlogs
import logging

userIds = os.environ['userIds'].split(',')
authKeys = os.environ['authKeys'].split(',')
secretKeys = os.environ['secretKeys'].split(',')
userFlags = os.environ['userFlags'].split(',')
tgBotToken = os.environ.get('tgBotToken')
tgChatID = os.environ.get('tgChatID')
device_info = os.environ.get('DEVICE_INFO_SECRET')
appCheck = os.environ.get('APP_CHECK_SECRET')
user_agent_2 = os.environ.get('USER_AGENT_SECRET_2')
fate_region = 'JP'

userNums = len(userIds)
authKeyNums = len(authKeys)
secretKeyNums = len(secretKeys)
flagNums = len(userFlags)

logger = logging.getLogger("FGO Daily Login")
coloredlogs.install(fmt='%(asctime)s %(name)s %(levelname)s %(message)s')

def get_latest_verCode():
    endpoint = "https://raw.githubusercontent.com/DNNDHH/FGO-VerCode-extractor/JP/VerCode.json"
    response = requests.get(endpoint).text
    response_data = json.loads(response)

    return response_data['verCode']
    
def get_latest_appver():
    endpoint = "https://raw.githubusercontent.com/DNNDHH/FGO-VerCode-extractor/JP/VerCode.json"
    response = requests.get(endpoint).text
    response_data = json.loads(response)

    return response_data['appVer']


def main():
    if userNums == authKeyNums and userNums == secretKeyNums and userNums == flagNums:
        fgourl.set_latest_assets()
        SendMessageToAdmin("我要帮大家签到了哦! (●ˇ∀ˇ●)")
        currentID = 0
        for i in range(userNums):
            try:
                if not checkEnabled(userFlags[i], 0):
                    continue
                currentID = currentID + 1
                tMsg = f"{currentID}."
                instance = user.user(userIds[i], authKeys[i], secretKeys[i])
                time.sleep(1)
                logger.info(f"\n {'=' * 40} \n [+] 登录账号 \n {'=' * 40} " )
                tStr = instance.topLogin()
                tMsg = tMsg + str(tStr)
                time.sleep(2)
                # 登录
                instance.topHome()
                time.sleep(0.5)
                # 获取礼物盒数据
                instance.lq001()
                time.sleep(0.5)
                tStr = instance.Present()
                tMsg = tMsg + str(tStr)
                time.sleep(0.5)
                # 自动领取部分类型的礼物
                if checkEnabled(userFlags[i], 1):
                    instance.lq002()
                    time.sleep(2)
                # 自动兑换体力
                if checkEnabled(userFlags[i], 2):
                    tStr = instance.buyBlueApple()
                    tMsg = tMsg + str(tStr)
                    time.sleep(1)
                # 兑换护符
                if checkEnabled(userFlags[i], 3):
                    tStr = instance.lq003()
                    tMsg = tMsg + str(tStr)
                    time.sleep(1)
                # 日常友情池
                if checkEnabled(userFlags[i], 4):
                    tStr = instance.drawFP()
                    tMsg = tMsg + str(tStr)
                    time.sleep(1)
                # 活动友情池
                if checkEnabled(userFlags[i], 5):
                    tStr = instance.LTO_Gacha()
                    tMsg = tMsg + str(tStr)
                SendMessageToAdmin(tMsg)


            except Exception as ex:
                SendMessageToAdmin("\\[出错]\n" + str(ex))

        SendMessageToAdmin("全部结束! ( •̀ ω •́ )y")


def checkEnabled(string: str, pos: int) -> bool:
    if pos < 0 or pos >= len(string):
        return false
    return string[pos] == '1'


def SendMessageToAdmin(message):
    if tgBotToken != 'nullvalue' and tgChatID != 'nullvalue':
        url = f'https://api.telegram.org/bot{tgBotToken}/sendMessage?chat_id={tgChatID}&parse_mode=markdown&text={message}'
        # print(str(base64.b64encode(url.encode('utf-8')), 'utf-8'))
        result = json.loads(requests.get(url, verify=False).text)
        if not result['ok']:
            print(result)
            print(message)




if __name__ == "__main__":
    main()

