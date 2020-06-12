from flask_restful import Resource


class GreetingsResource(Resource):

    def get(self) -> str:
        return "Hello World"
