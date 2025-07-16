import pickle
import random
import math
from pathlib import Path
from collections import defaultdict, Counter

MODEL_PATH = Path(__file__).resolve().parent / "q_table.pkl"
ACTIONS = ["rock", "paper", "scissors"]
WIN_MAP = {"rock": "paper", "paper": "scissors", "scissors": "rock"}
ACTION_TO_IDX = {a: i for i, a in enumerate(ACTIONS)}

# Load Q-table
try:
    with open(MODEL_PATH, "rb") as f:
        Q_TABLE = pickle.load(f)
        print(f"[INFO] Loaded Q-table with {len(Q_TABLE)} entries.")
except FileNotFoundError:
    Q_TABLE = {}
    print("[WARN] Q-table not found. Using empty table.")

NGRAM_N = 3


def softmax(q_values, temperature=1.0):
    max_q = max(q_values)
    exps = [math.exp((q - max_q) / temperature) for q in q_values]
    total = sum(exps)
    return [x / total for x in exps]


def sample_with_probs(probs):
    r = random.random()
    cumulative = 0
    for i, p in enumerate(probs):
        cumulative += p
        if r < cumulative:
            return ACTIONS[i]
    return ACTIONS[-1]


def q_table_move(state: tuple[str], temperature=0.7):
    if state not in Q_TABLE:
        return None, 0.0
    q_values = Q_TABLE[state]
    probs = softmax(q_values, temperature)
    move = sample_with_probs(probs)
    confidence = max(q_values) / (sum(map(abs, q_values)) + 1e-6)
    return move, round(confidence, 3)


def get_ngram_prediction(history: list[str], n=NGRAM_N):
    if len(history) < n:
        return None, 0.0

    patterns = defaultdict(Counter)
    for i in range(len(history) - n):
        key = tuple(history[i:i + n])
        next_move = history[i + n]
        patterns[key][next_move] += 1

    recent = tuple(history[-n:])
    if recent in patterns:
        likely = patterns[recent].most_common(1)[0][0]
        counter = WIN_MAP[likely]
        confidence = patterns[recent][likely] / sum(patterns[recent].values())
        return counter, round(0.5 + confidence / 2, 3)
    return None, 0.0


def frequency_baseline(history: list[str]):
    if not history:
        return random.choice(ACTIONS), 0.33
    freq = Counter(history)
    most_common = freq.most_common(1)[0][0]
    return WIN_MAP[most_common], 0.4


def get_bot_move(history: list[str]) -> dict:
    state = tuple(history[-2:]) if len(history) >= 2 else tuple(history)

    # 1. Try Q-table
    move, confidence = q_table_move(state)
    if move and confidence > 0.45:
        return {
            "bot_move": move,
            "confidence": confidence,
            "strategy": "q_table"
        }

    # 2. Try n-gram pattern recognition
    move, confidence = get_ngram_prediction(history)
    if move:
        return {
            "bot_move": move,
            "confidence": confidence,
            "strategy": "ngram"
        }

    # 3. Try statistical fallback
    move, confidence = frequency_baseline(history)
    if move:
        return {
            "bot_move": move,
            "confidence": confidence,
            "strategy": "frequency"
        }

    # 4. Fallback to random
    return {
        "bot_move": random.choice(ACTIONS),
        "confidence": 0.33,
        "strategy": "random"
    }