from flask_restx import Namespace, api, fields


class IpDto:
    api = Namespace(
        "ip",
        description="存取IP相關要求"
    )
    header = api.parser().add_argument("Authorization", location="headers", help="Bearer ")
    # get_current_ip = api.model(
    #     "get_ip",

    # )
