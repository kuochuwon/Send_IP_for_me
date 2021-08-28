from ip_service import load_ip
import os
import unittest
from flask_migrate import Migrate

from dotenv import load_dotenv

base_dir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(base_dir, ".env")
load_dotenv(dotenv_path=dotenv_path)

from app import blueprint  # noqa: E402
from app.main import create_app, db  # noqa: E402

app = create_app(os.getenv("FLASK_CONFIG") or "development")
app.register_blueprint(blueprint)

app.app_context().push()
migrate = Migrate(app, db)


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin",
                         "*")
    response.headers.add("Access-Control-Allow-Headers",
                         "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods",
                         "GET,PUT,POST,DELETE,OPTION")
    return response


def test():
    tests = unittest.TestLoader().discover("app/test",
                                           pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    return 0 if result.wasSuccessful() else 1


def run():
    app.run()


if __name__ == "__main__":
    # ip = load_ip()
    # app.run(host=str(ip), port=1942)
    app.run()
