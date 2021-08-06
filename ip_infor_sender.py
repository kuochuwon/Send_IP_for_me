import requests as urllib_requests
from constant import LineConstant
from ip_service import get_ip

roy_id = "U9afa5683614c2f30296a92eb07984d57"


def execute():
    try:
        msg = get_ip()
        if roy_id and msg:
            token_identifier = "IP_service"
            json_for_msg = dict(
                to=roy_id,
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
    except Exception as e:
        print(f"execute failed: {e}")


if __name__ == "__main__":
    execute()
