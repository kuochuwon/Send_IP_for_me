import requests as urllib_requests
import os
from constant import LineConstant
from ip_service import get_ip

user_id = os.getenv("RECIPIENT_ID")


def _push_message_via_line(msg):
    token_identifier = "IP_service"
    json_for_msg = dict(
        to=user_id,
        messages=[{
            "type": "text",
            "text": msg
        }]
    )
    user_result = urllib_requests.post(
        LineConstant.OFFICIAL_PUSH_API,
        headers=LineConstant().generate_push_or_reply_header(token_identifier),
        json=json_for_msg  # HINT 這邊必須用JSON
    )
    print(f"Line PUSH HTTP狀態碼: {user_result.status_code}")


def execute():
    try:
        msg = get_ip()
        if user_id and msg:
            _push_message_via_line(msg)
    except Exception as e:
        print(f"execute failed: {e}")


if __name__ == "__main__":
    execute()
