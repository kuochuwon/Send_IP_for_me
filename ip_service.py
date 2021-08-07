import subprocess
import re
from pathlib import Path
from log import logger, get_handler


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


def check_ip(curr_win_ip, curr_wsl_ip):
    try:
        with open("ip_memo.txt", "r") as f:
            raw = f.read()
            raw_list = raw.split(" ")
            prev_win_ip = raw_list[0]
            prev_wsl_ip = raw_list[1]

        if (curr_win_ip == prev_win_ip) and (curr_wsl_ip == prev_wsl_ip):
            logger.info("您的IP未偵測到變更")
            return
        elif (curr_win_ip == prev_win_ip) and (curr_wsl_ip != prev_wsl_ip):
            logger.info(f"偵測到WSL IP變更! old: {prev_wsl_ip}, new: {curr_wsl_ip}")
        elif (curr_win_ip != prev_win_ip) and (curr_wsl_ip == prev_wsl_ip):
            logger.info(f"偵測到Win IP變更! old: {prev_win_ip}, new: {curr_win_ip}")
        else:
            logger.info(f"您的Win and WSL IP皆已變更! old Win/WSL IP: {prev_win_ip} / {prev_wsl_ip}\n"
                        f"new Win/WSL IP: {curr_win_ip} / {curr_wsl_ip}")
        with open("ip_memo.txt", "w") as f:
            f.write(f"{curr_win_ip} {curr_wsl_ip}")
    except Exception as e:
        logger.error(f"{check_ip.__name__} failed: {e}")


def get_info_from_cmd(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output = p.stdout.read().decode("big5").strip()
    return output


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
    # HINT 此pattern允許字串中合法IP後面跟著其他字元，但只會擷取合法IP
    # ip_pattern_loose = "((25[0-5]|(2[0-4]|1\\d|[1-9]|)\\d)(\\.(?!$)|)){4}"
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


def readdata():
    keyword1 = '無線區域網路介面卡 Wi-Fi'
    keyword2 = '乙太網路卡 乙太網路'

    # HINT: ref: https://stackoverflow.com/questions/5284147/validating-ipv4-addresses-with-regexp
    ip_pattern = "((25[0-5]|(2[0-4]|1\\d|[1-9]|)\\d)(\\.(?!$)|$)){4}$"

    with open("ipoutput.txt", "r", encoding="utf-8") as r:
        output = r.readlines()
        for index, lines in enumerate(output):
            if lines.startswith(keyword1) or lines.startswith(keyword2):
                ipv4_rawdata = output[index+4]
                break
    ipv4_addr = re.search(ip_pattern, ipv4_rawdata).group(0)


if __name__ == "__main__":
    log_name = Path(Path.cwd(), "logs", "ip_info.log")
    logger.addHandler(get_handler(log_name))
    win_ipv4_addr, wsl_ipv4_addr = get_ip("var")
    check_ip(win_ipv4_addr, wsl_ipv4_addr)
