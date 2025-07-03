import os
from flask import Flask, request, jsonify, render_template
from flask import send_from_directory
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MongoDB setup
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client.get_default_database()
actions_collection = db['actions']

# Helper: Format timestamp
def format_timestamp(ts):
    dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%fZ")
    return dt.strftime("%d %B %Y - %I:%M %p UTC")

# Webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    # Handle push event
    if 'pusher' in data and 'ref' in data:
        action_doc = {
            "request_id": data.get("after"),  # commit SHA
            "author": data["pusher"]["name"],
            "action": "PUSH",
            "from_branch": None,
            "to_branch": data["ref"].split('/')[-1],  # refs/heads/main -> main
            "timestamp": data.get("head_commit", {}).get("timestamp")
        }
        actions_collection.insert_one(action_doc)
        return jsonify({"status": "success"}), 201

    # Handle pull request event
    if "pull_request" in data:
        pr = data["pull_request"]
        action_type = "PULL_REQUEST"
        # Only log when a PR is opened (you can add more actions if you want)
        if data.get("action") == "opened":
            action_doc = {
                "request_id": str(pr.get("id")),
                "author": pr["user"]["login"],
                "action": action_type,
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": pr["created_at"]
            }
            actions_collection.insert_one(action_doc)
            return jsonify({"status": "success"}), 201

        # Handle merge event (when PR is closed and merged)
        if data.get("action") == "closed" and pr.get("merged"):
            action_doc = {
                "request_id": str(pr.get("id")),
                "author": pr["user"]["login"],
                "action": "MERGE",
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": pr["merged_at"]
            }
            actions_collection.insert_one(action_doc)
            return jsonify({"status": "success"}), 201

    return jsonify({"status": "ignored"}), 200

# API to fetch latest actions
@app.route('/api/actions', methods=['GET'])
def get_actions():
    # Get latest 20 actions, sorted by timestamp descending
    actions = list(actions_collection.find().sort("timestamp", -1).limit(20))
    for a in actions:
        a['_id'] = str(a['_id'])
    return jsonify(actions)

# Serve UI
@app.route('/')
def index():
    return render_template('index.html')

# Serve static files (CSS)
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)