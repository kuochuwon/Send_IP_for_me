import subprocess
import re
from sys import stdout


def get_ip():
    win_command = "ipconfig"
    p = subprocess.Popen(win_command, stdout=subprocess.PIPE, shell=True)
    output = p.stdout.read().decode("big5")
    ipv4_rawdata = get_windows_ip_info(output)
    win_ipv4_addr = extract_ip(ipv4_rawdata)
    wsl_command = 'bash -c "ip addr"'  # HINT must use double quote
    p = subprocess.Popen(wsl_command, stdout=subprocess.PIPE, shell=True)
    output = p.stdout.read().decode("big5")
    print("wsl:")
    print(output)
    ipv4_rawdata = get_wsl_ip_info(output)
    wsl_ipv4_addr = extract_ip(ipv4_rawdata)
    print(f"您在Windows的IP為{win_ipv4_addr}")
    print(f"您在WSL2的IP為{wsl_ipv4_addr}")


def get_wsl_ip_info(std_out):
    keyword1 = 'eth0: <BROADCAST,MULTICAST,UP,LOWER_UP>'
    keyword2 = 'eth0: <NO-CARRIER,BROADCAST,MULTICAST,UP,LOWER_UP>'
    output = std_out.split("\n")
    for index, lines in enumerate(output):
        if re.search(keyword1, lines) or re.search(keyword2, lines):
            ipv4_rawdata = output[index+2]
            ipv4_rawdata = ipv4_rawdata.split("/")[0]
            return ipv4_rawdata
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
            return ipv4_rawdata
    print("找不到Windows IP")
    return None


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
    get_ip()
