from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = Api(app)


class InstaData(Resource):
    def get(self, dil_id):
        from insta_parser import get_dm, get_messages
        get_dm()
        return jsonify(get_messages(dil_id))

    def post(self, dil_id):
        from insta_parser import get_dm, send_msg
        get_dm()
        body = request.get_json()
        text = body['text']
        send_msg(text, dil_id)
        return True


api.add_resource(InstaData, "/dm/<int:dil_id>")
if __name__ == "__main__":
    app.run(debug=True)
