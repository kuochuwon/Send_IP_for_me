from flask_restx import Namespace, fields
import random


class RandomNumber(fields.Raw):
    def output(self, key, obj):
        return random.random()


class IpDto:
    api = Namespace(
        "ip",
        description="存取IP相關要求"
    )
    header = api.parser().add_argument("Authorization", location="headers", help="Bearer ")

    var_passing = api.model(
        "var_passing", {
            'name': fields.String,
            # todo_resource is the endpoint name when you called api.route()
            'uri': fields.Url('todo_resource'),
            'random': RandomNumber,
        }
    )
