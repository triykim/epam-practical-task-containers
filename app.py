from flask import Flask, request, jsonify
import redis
import os

app = Flask(__name__)

r = redis.Redis(
    host=os.environ.get("REDIS_HOST"),
    port=6379,
    decode_responses=True
)

# CREATE
@app.route("/item/<key>", methods=["POST"])
def create(key):
    value = request.json.get("value")
    r.set(key, value)
    return jsonify({"message": "created"}), 201

# READ
@app.route("/item/<key>", methods=["GET"])
def read(key):
    value = r.get(key)
    if value is None:
        return jsonify({"error": "not found"}), 404
    return jsonify({"key": key, "value": value})

# UPDATE
@app.route("/item/<key>", methods=["PUT"])
def update(key):
    if not r.exists(key):
        return jsonify({"error": "not found"}), 404
    value = request.json.get("value")
    r.set(key, value)
    return jsonify({"message": "updated"})

# DELETE
@app.route("/item/<key>", methods=["DELETE"])
def delete(key):
    if not r.exists(key):
        return jsonify({"error": "not found"}), 404
    r.delete(key)
    return jsonify({"message": "deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)