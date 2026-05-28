import json
import heapq
from collections import deque

# Load dataset
try:
    with open("dataset.json", "r") as file:
        diseases = json.load(file)

except:
    print("dataset.json not found! Run scraper.py first.")
    exit()


# 1 Dynamic Programming (LCS)

def lcs(X, Y):

    m, n = len(X), len(Y)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m):

        for j in range(n):

            if X[i] == Y[j]:

                dp[i + 1][j + 1] = dp[i][j] + 1

            else:

                dp[i + 1][j + 1] = max(
                    dp[i][j + 1],
                    dp[i + 1][j]
                )

    return dp[m][n]


# 2 Greedy + Weighted Scoring

def calculate_score(user_symptoms, duration, severity):

    scores = {}

    for disease, details in diseases.items():

        score = 0

        disease_symptoms = list(details["symptoms"].keys())

        # DP similarity
        score += lcs(user_symptoms, disease_symptoms)

        # Weighted matching
        for s in user_symptoms:

            if s in details["symptoms"]:
                score += details["symptoms"][s]

        # Core symptom bonus
        if all(
            cs in user_symptoms
            for cs in details["core_symptoms"]
        ):
            score += 3

        # Duration match
        min_d, max_d = details["duration"]

        if min_d <= duration <= max_d:
            score += 2
        else:
            score -= 1

        # Severity match
        if severity == details["severity"]:
            score += 2

        scores[disease] = score

    return scores


# 3 Merge Sort

def merge_sort(arr):

    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2

    left = merge_sort(arr[:mid])

    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left, right):

    result = []

    i = j = 0

    while i < len(left) and j < len(right):

        if left[i][1] > right[j][1]:

            result.append(left[i])

            i += 1

        else:

            result.append(right[j])

            j += 1

    result.extend(left[i:])

    result.extend(right[j:])

    return result


# 4 Graph + BFS

def build_graph():

    graph = {}

    for disease, details in diseases.items():

        for symptom in details["symptoms"]:

            graph.setdefault(symptom, []).append(disease)

    return graph


def bfs_related(user_symptoms, graph):

    visited = set()

    queue = deque(user_symptoms)

    related = set()

    while queue:

        symptom = queue.popleft()

        if symptom in graph:

            for disease in graph[symptom]:

                if disease not in visited:

                    visited.add(disease)

                    related.add(disease)

    return list(related)


# 5 Priority Queue (Urgency)

def detect_urgency(severity, duration):

    heap = []

    if severity == "high":

        heapq.heappush(heap, (3, "HIGH"))

    elif severity == "medium":

        heapq.heappush(heap, (2, "MEDIUM"))

    else:

        heapq.heappush(heap, (1, "LOW"))

    if duration > 5:

        heapq.heappush(heap, (3, "HIGH"))

    return heapq.nlargest(1, heap)[0][1]


# 6 Test Optimization

def suggest_test(top_diseases):

    tests = set()

    for disease, _ in top_diseases:

        tests.add(diseases[disease]["test"])

    return list(tests)