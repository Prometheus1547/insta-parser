from flask import Flask, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return "Hello world"


class InstaData(Resource):
    def get(self):
        from insta_parser import get_dm
        return jsonify(get_dm())

    def get(self, dil_id):
        from insta_parser import get_dm, get_messages
        get_dm()
        return jsonify(get_messages(dil_id))


api.add_resource(HelloWorld, "/helloworld/")
api.add_resource(InstaData, "/dm/<int:dil_id>")
if __name__ == "__main__":
    app.run(debug=True)
