import matplotlib.pyplot as plt
from flask import Flask, request, jsonify
import time
import base64
import json
import os
from datetime import timedelta

import matplotlib
matplotlib.use("Agg")
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from database import db, Analysis


app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///analysis.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# JWT configuration - tokens are only ever read from the Authorization header
app.config["JWT_SECRET_KEY"] = os.environ.get(
    "JWT_SECRET_KEY", "batsindaqwertyKeynes123456Benoit"
)
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_HEADER_TYPE"] = "Bearer"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

db.init_app(app)

with app.app_context():
    db.create_all()

jwt = JWTManager(app)

# Accounts accepted by POST /login (override with env vars if you want)
USERS = {
    os.environ.get("JWT_USERNAME", "admin"): os.environ.get(
        "JWT_PASSWORD", "admin123"
    )
}

# Every rejection below answers 401 with the same message

@jwt.unauthorized_loader
def _reject_missing_token(*args):
    return jsonify({"error": "I don't know you"}), 401


@jwt.invalid_token_loader
def _reject_invalid_token(*args):
    return jsonify({"error": "I don't know you"}), 401


@jwt.expired_token_loader
def _reject_expired_token(*args):
    return jsonify({"error": "I don't know you"}), 401


@jwt.revoked_token_loader
def _reject_revoked_token(*args):
    return jsonify({"error": "I don't know you"}), 401


@jwt.needs_fresh_token_loader
def _reject_stale_token(*args):
    return jsonify({"error": "I don't know you"}), 401


@jwt.token_verification_failed_loader
def _reject_unverified_token(*args):
    return jsonify({"error": "I don't know you"}), 401


@jwt.user_lookup_error_loader
def _reject_unknown_user(*args):
    return jsonify({"error": "I don't know you"}), 401


# Issues a JWT, returned in the Authorization response header as "Bearer <token>"

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        data = {}

    username = data.get("username")
    password = data.get("password")

    if (
        not isinstance(username, str)
        or not isinstance(password, str)
        or username not in USERS
        or USERS[username] != password
    ):

        return jsonify({"error": "I don't know you"}), 401

    token = create_access_token(identity=username)

    response = jsonify({
        "username": username,
        "token_type": "Bearer",
        "access_token": token
    })

    response.headers["Authorization"] = f"Bearer {token}"

    return response, 200



# -------------------------
# Algorithms
# -------------------------

def linear_search(n):
    for i in range(n):
        pass


def bubble_sort(n):
    numbers = list(range(n, 0, -1))

    for i in range(n):
        for j in range(0, n - i - 1):
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = (
                    numbers[j + 1],
                    numbers[j]
                )


def binary_search(n):
    left = 0
    right = n - 1
    target = n - 1

    while left <= right:
        middle = (left + right) // 2

        if middle == target:
            return

        elif middle < target:
            left = middle + 1

        else:
            right = middle - 1


def nested_loops(n):
    for i in range(n):
        for j in range(n):
            pass


def insertion_sort(n):
    numbers = list(range(n, 0, -1))

    for i in range(1, n):
        key = numbers[i]
        j = i - 1

        while j >= 0 and numbers[j] > key:
            numbers[j + 1] = numbers[j]
            j -= 1

        numbers[j + 1] = key

def selection_sort(n):
    numbers = list(range(n, 0, -1))

    for i in range(n):
        min_index = i

        for j in range(i + 1, n):
            if numbers[j] < numbers[min_index]:
                min_index = j

        numbers[i], numbers[min_index] = (
            numbers[min_index],
            numbers[i]
        )    

# -------------------------
# Algorithm dictionary
# -------------------------

algorithms = {
    "linear_search": linear_search,
    "bubble_sort": bubble_sort,
    "binary_search": binary_search,
    "nested_loops": nested_loops,
    "insertion_sort": insertion_sort,
    "selection_sort": selection_sort
}


# -------------------------
# Visualizer
# -------------------------

def time_complexity_visualizer(algorithm, n_min, n_max, n_step):

    times = []

    input_sizes = list(
        range(n_min, n_max + 1, n_step)
    )

    for n in input_sizes:

        start_time = time.perf_counter()

        algorithm(n)

        end_time = time.perf_counter()

        elapsed_time = end_time - start_time

        times.append(elapsed_time)

    # -------------------------
    # Create graph
    # -------------------------

    plt.figure()

    plt.plot(input_sizes, times, "o-")

    plt.xlabel("Input size")
    plt.ylabel("Running time (seconds)")
    plt.title(f"{algorithm.__name__} Time Complexity")

    plt.grid(True)

    # -------------------------
    # Save graph
    # -------------------------

    os.makedirs("snapshots", exist_ok=True)

    image_path = f"snapshots/{algorithm.__name__}.png"

    plt.savefig(image_path)

    plt.close()

    # -------------------------
    # Convert image to Base64
    # -------------------------

    with open(image_path, "rb") as image_file:

        encoded_image = base64.b64encode(
            image_file.read()
        ).decode("utf-8")

    return {
        "input_sizes": input_sizes,
        "times": times,
        "image": encoded_image,
        "image_path": image_path
    }


# -------------------------
# Flask endpoint
# -------------------------

@app.route("/analyze", methods=["GET"])
def analyze():

    # Get query parameters
    algo = request.args.get("algo")
    step = request.args.get("step")
    n_max = request.args.get("n_max")

    # -------------------------
    # Check parameters
    # -------------------------

    if algo is None or step is None or n_max is None:

        return jsonify({
            "error": "Please provide algo, step and n_max"
        }), 400

    # Remove quotes if user writes:
    # algo='linear_search'

    algo = algo.strip("'\"")

    # -------------------------
    # Convert numbers
    # -------------------------

    try:

        step = int(step)
        n_max = int(n_max)

    except ValueError:

        return jsonify({
            "error": "step and n_max must be integers"
        }), 400

    # -------------------------
    # Validate step
    # -------------------------

    if step <= 0:

        return jsonify({
            "error": "step must be greater than 0"
        }), 400

    # -------------------------
    # Validate n_max
    # -------------------------

    if n_max < 0:

        return jsonify({
            "error": "n_max must be greater than or equal to 0"
        }), 400

    # -------------------------
    # Validate algorithm
    # -------------------------

    if algo not in algorithms:

        return jsonify({
            "error": "Unknown algorithm",
            "available_algorithms": list(
                algorithms.keys()
            )
        }), 400

    # Minimum input size
    n_min = 0

    # -------------------------
    # Run algorithm visualizer
    # -------------------------

    result = time_complexity_visualizer(
        algorithms[algo],
        n_min,
        n_max,
        step
    )

    # -------------------------
    # Return JSON response
    # -------------------------

    return jsonify({

        "algorithm": algo,

        "n_min": n_min,

        "n_max": n_max,

        "step": step,

        "input_sizes": result["input_sizes"],

        "times": result["times"],

        "image_path": result["image_path"],

        "image_base64": result["image"]

    })



# Save analysis endpoint

@app.route("/save_analysis", methods=["POST"])
@jwt_required()
def save_analysis():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):

        return jsonify({
            "error": "Please provide JSON data"
        }), 400

    required_fields = [
        "algorithm",
        "n_min",
        "n_max",
        "step",
        "input_sizes",
        "times",
        "image_path"
    ]

    for field in required_fields:

        if field not in data:

            return jsonify({
                "error": f"Missing field: {field}"
            }), 400

    analysis = Analysis(
        algorithm=data["algorithm"],
        n_min=data["n_min"],
        n_max=data["n_max"],
        step=data["step"],
        input_sizes=json.dumps(data["input_sizes"]),
        times=json.dumps(data["times"]),
        image_path=data["image_path"]
    )

    db.session.add(analysis)
    db.session.commit()

    return jsonify({
        "message": "Analysis saved successfully",
        "analysis_id": analysis.id
    }), 201


# -------------------------
# Start Flask server
# -------------------------

if __name__ == "__main__":

    app.run(
        host="localhost",
        port=8000,
        debug=True
    )