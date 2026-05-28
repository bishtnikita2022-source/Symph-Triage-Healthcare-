from flask import Flask, request, jsonify
from flask_cors import CORS

from main import (
    build_graph,
    bfs_related,
    calculate_score,
    merge_sort,
    detect_urgency,
    suggest_test
)

app = Flask(__name__)

CORS(app)


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.json

    user_symptoms = [
        s.strip().replace(" ", "_")
        for s in data["symptoms"]
    ]

    duration = int(data["duration"])

    severity = data["severity"].lower()

    graph = build_graph()

    related = bfs_related(
        user_symptoms,
        graph
    )

    scores = calculate_score(
        user_symptoms,
        duration,
        severity
    )

    filtered = [
        (d, scores[d])
        for d in related
        if d in scores
    ]

    if not filtered:
        filtered = list(scores.items())

    ranked = merge_sort(filtered)

    urgency = detect_urgency(
        severity,
        duration
    )

    tests = suggest_test(ranked[:2])

    return jsonify({

        "ranked": [

            {
                "disease": d,
                "score": s
            }

            for d, s in ranked[:3]
        ],

        "urgency": urgency,

        "tests": tests
    })


if __name__ == "__main__":

    app.run(debug=True)