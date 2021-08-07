from flask_restx import Api
from flask import Blueprint
from app.main import jwt
from app.main.controller.ip_controller import api as ip_ns

blueprint = Blueprint("api",
                      __name__,
                      url_prefix="/api/v1")
api = Api(blueprint,
          title="Roy's Toolkits",
          version="0.1.0",
          description="Roy的IAAS")

jwt._set_error_handler_callbacks(api)

api.add_namespace(ip_ns,
                  path="/ip")
