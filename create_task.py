import time
import sys
import subprocess
from pathlib import Path


def cmd_create_task(task_path, python_path, script_name, start_time):
    """每小時執行一次"""
    s = f"""SCHTASKS /CREATE /SC HOURLY /TN "{task_path}" """\
        f"""/TR "{python_path} """\
        f"""{script_name}" /ST {start_time} /f"""
    return s


def cmd_delete_task(task_name):
    # top folder default as EmergencyResponse
    s = f'SCHTASKS /DELETE /TN "{task_name}" /f'
    return s


def create_task_check_ip(start_time):
    base_path = Path.cwd()
    task_path = Path("Roy toolkits", "IP checking")
    python_path = Path(base_path, "venv/Scripts/python.exe")
    script_name = Path(base_path, "ip_service.py")
    create_command = cmd_create_task(str(task_path), str(python_path), str(script_name), start_time)
    subprocess.Popen(create_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)


def delete_task_by_name(task_name="IP checking"):
    task_name = Path("Roy toolkits", task_name)
    delete_command = cmd_delete_task(str(task_name))
    subprocess.Popen(delete_command, stdout=subprocess.PIPE, shell=True)


def main():
    if len(sys.argv) >= 2:
        task_mode = sys.argv[1]
        if task_mode == "create":
            timeslot = sys.argv[2]
            create_task_check_ip(timeslot)

        elif task_mode == "delete":
            if len(sys.argv) >= 3:
                task_name = sys.argv[2]
                delete_task_by_name(task_name)
            else:
                delete_task_by_name()
        else:
            input("請輸入正確的變數，例如: 'create' 'HH:MM' or 'delete'... 按任意鍵結束")
    else:
        input("請輸入正確的變數，例如: 'create' 'HH:MM' or 'delete'... 按任意鍵結束")


if __name__ == "__main__":
    main()
