from flask import request
from flask_api import status
from flask_restx import Resource
from app.main.dto.ip import IpDto
from app.main.service import ret
from app.main.view.ip_response import get_current_ip, get_access_url

api = IpDto.api
_header = IpDto.header

response_status = {status.HTTP_200_OK: ret.get_code_full(ret.RET_OK),
                   status.HTTP_401_UNAUTHORIZED: ret.get_code_full(ret.RET_NO_CUST_ID),
                   status.HTTP_404_NOT_FOUND: ret.get_code_full(ret.RET_NOT_FOUND)}


@api.route("/get_ip")
class GetIP(Resource):
    @api.expect(_header, validate=True)
    @api.doc(responses=response_status)
    def get(self):
        """提供目前的Windows and WSL IP"""
        response = dict(
            win_ip=None,
            wsl_ip=None,
            access_url=None
        )
        # TODO Need exception handling
        port = 1942
        win_ip, wsl_ip = get_current_ip()
        flask_url = get_access_url(wsl_ip, port)
        response["win_ip"] = win_ip
        response["wsl_ip"] = wsl_ip
        response["access_url"] = flask_url
        return ret.http_resp(ret.RET_OK, extra=response), status.HTTP_200_OK
