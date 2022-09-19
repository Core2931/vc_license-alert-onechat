import yaml
import json

import requests
from datetime import datetime, timedelta, date

from model.model_mongo import connect_mongodb

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

CONFIG_FILE = './config.yaml'
 
try:
    file_stream = open(CONFIG_FILE, "r", encoding='utf-8')
    # Load configuration into config
    Config = yaml.load(file_stream, Loader=Loader)
    file_stream.close()
except Exception as e:
    print("Read configuration file error:", e)
    exit(1)


def get_data_mongo():
    try:
        cluster = connect_mongodb()
        db = cluster["healthscore"]
        collection = db["vc_license_expried_detail"]
        
        ### Date
        date_today = date.today()
        date_future =  str(date.today() + timedelta(days=31))

        ### Query 
        # select_query_all = collection.find({'status':"Available"})
        select_query_all = collection.find({'$and':[{'status':"Available"},{'not_after':{'$lte':date_future}}]})
        vcenter_available = list(select_query_all)

        ip = ""
        print(vcenter_available)
        topic = "VC License Alert "+ str(date_today) + "\n"
        count = 0
        len_exp = len(vcenter_available)
        for i in vcenter_available:
            if len(vcenter_available) != 0 or vcenter_available is not None:
                count += 1
                if count %3 == 0:
                    ip += "Vcenter ip : " + i['vcenter_ip'] + "\n" + "Platform : " + i['platform'] + "\n" + "Profile Certification : " + i['store']+ "\n" + "Expiration Date : "+ i['not_after']+ "\n" + "Status : " + "Warning" + " \U0001F7E1	 \n"
                    msg = topic+ ip
                    send_to_onechat_group(msg)
                    # print("Count:"+str(count)+"if %3== 0")
                    ip = ""
                elif len_exp == 2:
                    ip += "Vcenter ip : " + i['vcenter_ip'] + "\n" + "Platform : " + i['platform'] + "\n" + "Profile Certification : " + i['store']+ "\n" + "Expiration Date : "+ i['not_after']+ "\n" + "Status : " + "Warning" + " \U0001F7E1 \n\n"
                    # print("Count:"+str(count)+"elif = 2 ")
                elif len_exp == 1:
                    ip += "Vcenter ip : " + i['vcenter_ip'] + "\n" + "Platform : " + i['platform'] + "\n" + "Profile Certification : " + i['store']+ "\n" + "Expiration Date : "+ i['not_after']+ "\n" + "Status : " + "Warning" + " \U0001F7E1 \n"
                    msg = topic+ ip
                    send_to_onechat_group(msg)
                    # print("Count:"+str(count)+"elif = 1 ")
                    ip = ""
                else:
                    ip += "Vcenter ip : " + i['vcenter_ip'] + "\n" + "Platform : " + i['platform'] + "\n" + "Profile Certification : " + i['store']+ "\n" + "Expiration Date : "+ i['not_after']+ "\n" + "Status : " + "Warning" + " \U0001F7E1 \n\n"
                    # print("Count:"+str(count)+ "else ")
                len_exp -=1
            else:
                print("length == 0 or vcenter_expired == none")
        # send_to_onechat(ip)
        # print(vcenter_available)
    except Exception as e:
        print(e)

def get_data_mongo_expired():
    try:
        cluster = connect_mongodb()
        db = cluster["healthscore"]
        collection = db["vc_license_expried_detail"]
        
        ### Query 
        select_query_all = collection.find({'status':"Expired"})
        vcenter_expired = list(select_query_all)

        ip = ""
        topic = "VC License Alert "+ str(date.today()) + "\n"
        count = 0
        len_exp = len(vcenter_expired)

        
        for i in vcenter_expired:
            if len(vcenter_expired) != 0 or vcenter_expired is not None:
                count += 1
                if count %3 == 0:
                    ip += "Vcenter ip : " + i['vcenter_ip'] + "\n" + "Platform : " + i['platform'] + "\n" + "Profile Certification : " + i['store']+ "\n" + "Expiration Date : "+ i['not_after']+ "\n" + "Status : " + i['status'] + " \U0001F534 \n"
                    msg = topic+ ip
                    # send_to_onechat(msg)
                    send_to_onechat_group(msg)
                    ip = ""
                elif len_exp == 2:
                    ip += "Vcenter ip : " + i['vcenter_ip'] + "\n" + "Platform : " + i['platform'] + "\n" + "Profile Certification : " + i['store']+ "\n" + "Expiration Date : "+ i['not_after']+ "\n" + "Status : " + i['status'] + " \U0001F534 \n\n"
                elif len_exp == 1:
                    ip += "Vcenter ip : " + i['vcenter_ip'] + "\n" + "Platform : " + i['platform'] + "\n" + "Profile Certification : " + i['store']+ "\n" + "Expiration Date : "+ i['not_after']+ "\n" + "Status : " + i['status'] + " \U0001F534 \n"
                    msg = topic+ ip
                    # send_to_onechat(msg)
                    send_to_onechat_group(msg)
                    ip = ""
                else:
                    ip += "Vcenter ip : " + i['vcenter_ip'] + "\n" + "Platform : " + i['platform'] + "\n" + "Profile Certification : " + i['store']+ "\n" + "Expiration Date : "+ i['not_after']+ "\n" + "Status : " + i['status'] + " \U0001F534 \n\n"
                len_exp -=1
            else:
                print("length == 0 or vcenter_expired == none")
        # print(msg)
        # print(len(vcenter_expired))
    except Exception as e:
        print(e)

onechat_token = Config['onechat']['token']
onechat_bot_id = Config['onechat']['bot_id']
onechat_user_id = Config['onechat']['user_id']


def get_listroom():
    url = "https://chat-api.one.th/manage/api/v1/getlistroom"

    payload = json.dumps({
    "bot_id": onechat_bot_id
    })
    headers = {
    'Authorization': onechat_token,
    'Content-Type': 'application/json'
    }
    list_one_id = []
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    response = response.json()
    for i in response['list_friend']:
        list_one_id.append(i['one_id'])
    return list_one_id

def send_to_onechat(msg):
    url = "https://chat-api.one.th/message/api/v1/push_message"

    payload = json.dumps({
        "to": onechat_user_id,
        "bot_id": onechat_bot_id,
        "type": "text",
        "message": msg,
        "custom_notification": "เปิดอ่านข้อความใหม่จากทางเรา"
    })
    headers = {
        'Authorization': onechat_token,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


def send_to_onechat_group(msg):
    url = "https://chat-api.one.th/bc_msg/api/v1/broadcast_group"

    payload = json.dumps({
        "bot_id": onechat_bot_id,
        "to": 
        get_listroom()
        ,
        "message": msg,
})
    headers = {
        'Authorization': onechat_token,
        'Content-Type': 'application/json'
}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
