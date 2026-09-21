import base64
import io
import os
from datetime import datetime

import matplotlib.pyplot as plt
from flask import Flask, jsonify, request

from Algorithm import time_complexity_visualizer
from algorithms import ALGORITHMS

app = Flask(__name__)

SNAPSHOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "snapshots")
os.makedirs(SNAPSHOT_DIR, exist_ok=True)


@app.route("/analyze", methods=["GET"])
def analyze():
    algo_name = request.args.get("algo", type=str)
    step = request.args.get("step", type=int)
    n_max = request.args.get("n_max", type=str)

    if not algo_name:
        return jsonify(error="Missing required query parameter: algo"), 400
    algo_name = algo_name.strip().strip("'\"").lower()

    if algo_name not in ALGORITHMS:
        return jsonify(
            error=f"Unknown algorithm '{algo_name}'",
            supported_algorithms=sorted(ALGORITHMS.keys()),
        ), 400

    if step is None or step <= 0:
        return jsonify(error="Query parameter 'step' must be a positive integer"), 400

    if n_max is None:
        return jsonify(error="Missing required query parameter: n_max"), 400
    try:
        n_max_value = int(n_max.replace(",", ""))
    except ValueError:
        return jsonify(error="Query parameter 'n_max' must be an integer"), 400

    if n_max_value <= 0:
        return jsonify(error="Query parameter 'n_max' must be greater than 0"), 400

    algorithm = ALGORITHMS[algo_name]

    fig, input_sizes, times = time_complexity_visualizer(
        algorithm, n_min=0, n_max=n_max_value, n_step=step, algo_name=algo_name
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{algo_name}_{timestamp}.png"
    filepath = os.path.join(SNAPSHOT_DIR, filename)
    fig.savefig(filepath, format="png")

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    plt.close(fig)
    buffer.seek(0)
    encoded_image = base64.b64encode(buffer.read()).decode("utf-8")

    return jsonify(
        algo=algo_name,
        step=step,
        n_min=0,
        n_max=n_max_value,
        input_sizes=input_sizes,
        times=times,
        snapshot_path=filepath,
        image_base64=encoded_image,
    )


@app.route("/algorithms", methods=["GET"])
def list_algorithms():
    return jsonify(supported_algorithms=sorted(ALGORITHMS.keys()))


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
