from flask import Flask, jsonify, render_template
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
from flask_cors import CORS
import os


CONNECTION_STRING = os.getenv('CONNECTION_STRING')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')


app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])


@app.route("/")
def home():
    client = MongoClient(CONNECTION_STRING)
    db = client.get_database()[COLLECTION_NAME]

    documents = db.find({}, {"_id": 0})
    data = [dict(doc) for doc in documents]

    client.close()

    return jsonify(data)
    # return render_template("index.html", data=data)


if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True)
