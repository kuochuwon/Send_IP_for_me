from dotenv import load_dotenv
import subprocess
import re
import os
import json
import time
from pathlib import Path


base_dir = os.path.abspath(os.path.dirname(__file__))  # noqa 為了在import app.main以前將環境變數載入，main/init裡面有config會呼叫到.env
dotenv_path = os.path.join(base_dir, ".env")  # noqa
load_dotenv(dotenv_path=dotenv_path)  # noqa
from app.main.log import logger, get_handler  # noqa
import requests as urllib_requests  # noqa


def get_ip(mode):
    """msg: 回傳訊息 var: 回傳win IP 與 WSL IP"""
    hostname = get_info_from_cmd("hostname")
    output = get_info_from_cmd("ipconfig")
    win_ipv4_addr = get_windows_ip_info(output)
    output = get_info_from_cmd('bash -c "ip addr"')  # HINT must use double quote
    wsl_ipv4_addr = get_wsl_ip_info(output)

    ip_infor = f"以下為: {hostname}的IP相關資訊\nWindows的IP為: {win_ipv4_addr}\nWSL2的IP為: {wsl_ipv4_addr}"
    logger.info(ip_infor)
    if win_ipv4_addr and wsl_ipv4_addr:
        if mode == "msg":
            return ip_infor
        elif mode == "var":
            return win_ipv4_addr, wsl_ipv4_addr
    else:
        return None


def load_ip():
    memo_path = os.getenv("IP_Path")
    file_path = Path(memo_path, "ip_memo.txt")
    with open(file_path, "r") as f:
        raw = f.read()
        raw_list = raw.split(" ")
        win_ip = raw_list[0]
        wsl_ip = raw_list[1]
    os_type = os.name
    if os_type == "nt":
        return win_ip
    else:
        return wsl_ip


def update_remote_ip_record(win_ip, wsl_ip):
    heroku_api_url = "https://linebot-kuochuwon.herokuapp.com/api/v1/ip/update_ip"
    ip_info = {"win_ip": win_ip, "wsl_ip": wsl_ip, "port": "unknown", "access_url": "unknown"}

    user_result = urllib_requests.post(
        heroku_api_url,
        headers={'content-type': 'application/json'},
        data=json.dumps(ip_info),  # 若失敗就試試改json=json.dumps()
    )
    print(f"Heroku HTTP狀態碼: {user_result.status_code}")


def check_ip_and_update_netsh_rule(curr_win_ip, curr_wsl_ip):
    try:
        memo_path = os.getenv("IP_Path")
        file_path = Path(memo_path, "ip_memo.txt")

        with open(file_path, "r") as f:
            raw = f.read()
            raw_list = raw.split(" ")
            prev_win_ip = raw_list[0]
            prev_wsl_ip = raw_list[1]

        # HINT netsh命令必須有系統管理員身分才可執行，已測試若在工作排程器將安全性選項設定以最高權限執行，可使命令生效
        delete_netsh_command = f"netsh interface portproxy delete v4tov4 listenport=1942 listenaddress={prev_win_ip}"
        add_netsh_command = (f"netsh interface portproxy add v4tov4 listenport=1942 listenaddress={curr_win_ip} "
                             f"connectport=1942 connectaddress={curr_wsl_ip}")

        if (curr_win_ip == prev_win_ip) and (curr_wsl_ip == prev_wsl_ip):
            logger.info("您的IP未偵測到變更")
            return
        elif (curr_win_ip == prev_win_ip) and (curr_wsl_ip != prev_wsl_ip):
            logger.info(f"偵測到WSL IP變更! old: {prev_wsl_ip}, new: {curr_wsl_ip}")
            get_info_from_cmd(delete_netsh_command)
            get_info_from_cmd(add_netsh_command)
        elif (curr_win_ip != prev_win_ip) and (curr_wsl_ip == prev_wsl_ip):
            logger.info(f"偵測到Win IP變更! old: {prev_win_ip}, new: {curr_win_ip}")
            get_info_from_cmd(delete_netsh_command)
            get_info_from_cmd(add_netsh_command)
        else:
            logger.info(f"您的Win and WSL IP皆已變更! old Win/WSL IP: {prev_win_ip} / {prev_wsl_ip}\n"
                        f"new Win/WSL IP: {curr_win_ip} / {curr_wsl_ip}")
            get_info_from_cmd(delete_netsh_command)
            get_info_from_cmd(add_netsh_command)

        update_remote_ip_record(curr_win_ip, curr_wsl_ip)
        with open(file_path, "w") as f:
            f.write(f"{curr_win_ip} {curr_wsl_ip}")
    except Exception as e:
        logger.error(f"{check_ip_and_update_netsh_rule.__name__} failed: {e}")


def get_info_from_cmd(command):
    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output = p.stdout.read().decode("big5").strip()
        return output
    except Exception as e:
        logger.error(f"{get_info_from_cmd.__name__} failed: {e}")


def get_wsl_ip_info(std_out):
    keyword1 = 'eth0: <BROADCAST,MULTICAST,UP,LOWER_UP>'
    keyword2 = 'eth0: <NO-CARRIER,BROADCAST,MULTICAST,UP,LOWER_UP>'
    output = std_out.split("\n")
    for index, lines in enumerate(output):
        if re.search(keyword1, lines) or re.search(keyword2, lines):
            ipv4_rawdata = output[index+2]
            ipv4_rawdata = ipv4_rawdata.split("/")[0]
            wsl_ipv4_addr = extract_ip(ipv4_rawdata)
            return wsl_ipv4_addr
    print("找不到WSL IP")


def extract_ip(string):
    ip_pattern = "((25[0-5]|(2[0-4]|1\\d|[1-9]|)\\d)(\\.(?!$)|$)){4}$"
    try:
        ipv4_addr = re.search(ip_pattern, string.strip()).group(0)
        return ipv4_addr
    except AttributeError:
        print("Not Found")
        return None


def get_windows_ip_info(std_out):
    keyword1 = '無線區域網路介面卡 Wi-Fi'
    keyword2 = '乙太網路卡 乙太網路'
    output = std_out.split("\n")
    for index, lines in enumerate(output):
        if re.search(keyword1, lines) or re.search(keyword2, lines):
            ipv4_rawdata = output[index+4]
            win_ipv4_addr = extract_ip(ipv4_rawdata)
            return win_ipv4_addr
    print("找不到Windows IP")


def init_log():
    log_name = Path(Path.cwd(), "logs", "ip_info.log")
    path = log_name.parent
    if not (path.exists() and path.is_dir()):
        Path.mkdir(path)
    logger.addHandler(get_handler(log_name))


if __name__ == "__main__":
    init_log()
    win_ipv4_addr, wsl_ipv4_addr = get_ip("var")
    check_ip_and_update_netsh_rule(win_ipv4_addr, wsl_ipv4_addr)
