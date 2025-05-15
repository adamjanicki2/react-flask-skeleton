from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
from flask_session import Session
from pymongo import MongoClient
import os
import awsgi
import pathlib
from dotenv import load_dotenv

load_dotenv()

MONGO_SRV = os.environ.get("MONGO_SRV")
SESSION_SECRET = os.environ.get("SESSION_SECRET")

if not SESSION_SECRET:
    raise RuntimeError("Missing SESSION_SECRET in .env")

if not MONGO_SRV:
    raise RuntimeError("Missing MONGO_SRV in .env")

app = Flask(__name__)
CORS(app)

client = MongoClient(MONGO_SRV)
app.config["SESSION_TYPE"] = "mongodb"
app.config["SESSION_MONGODB"] = client
app.config["SESSION_MONGODB_DB"] = "sessions"
app.config["SESSION_MONGODB_COLLECT"] = "flask_sessions"
app.secret_key = SESSION_SECRET
Session(app)


@app.route("/api/test")
def hello():
    return jsonify({"data": {"message": "Hello from your API!"}})


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    dist_dir = pathlib.Path(__file__).parent.parent / "client" / "build"
    file_path = dist_dir / path
    return send_from_directory(dist_dir, "index.html")


def handler(event, context):
    return awsgi.response(app, event, context)
