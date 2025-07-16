import pickle
import random
import os
from collections import defaultdict

# === Configurable Parameters ===
ACTIONS = ["rock", "paper", "scissors"]
COUNTERS = {"rock": "paper", "paper": "scissors", "scissors": "rock"}
ACTION_TO_IDX = {a: i for i, a in enumerate(ACTIONS)}

STATE_LEN = 2
EPISODES = 100_000
EPSILON = 0.1
ALPHA = 0.5
GAMMA = 0.9
MODEL_PATH = "app/q_table.pkl"


# === Core Q-Learning Logic ===

def get_reward(bot, user):
    if bot == user:
        return 0
    elif COUNTERS[bot] == user:
        return -1
    else:
        return 1

def choose_action(state, q_table):
    if random.random() < EPSILON or state not in q_table:
        return random.choice(ACTIONS)
    q_values = q_table[state]
    max_q = max(q_values)
    best_actions = [a for i, a in enumerate(ACTIONS) if q_values[i] == max_q]
    return random.choice(best_actions)

def update_q_table(q_table, state, action, reward, next_state):
    if state not in q_table:
        q_table[state] = [0.0] * len(ACTIONS)
    if next_state not in q_table:
        q_table[next_state] = [0.0] * len(ACTIONS)

    idx = ACTION_TO_IDX[action]
    current_q = q_table[state][idx]
    max_future_q = max(q_table[next_state])
    new_q = current_q + ALPHA * (reward + GAMMA * max_future_q - current_q)
    q_table[state][idx] = new_q

# === Simulated User Logic ===

def simulate_user(history):
    """
    A fake user that has semi-predictable behavior:
    - Repeats moves sometimes
    - Favors switching if the same move was used 2x
    """
    if len(history) >= 2 and history[-2:] == ["rock", "rock"]:
        return "paper"
    if len(history) >= 3 and history[-3:] == ["scissors", "scissors", "scissors"]:
        return "rock"
    return random.choices(
        ACTIONS,
        weights=[0.4 if history and history[-1] == "rock" else 0.3,
                 0.4 if history and history[-1] == "paper" else 0.3,
                 0.4 if history and history[-1] == "scissors" else 0.3]
    )[0]

# === Training Loop ===

def train():
    q_table = {}
    user_history = []

    for i in range(EPISODES):
        state = tuple(user_history[-STATE_LEN:]) if len(user_history) >= STATE_LEN else ("",) * STATE_LEN

        bot_action = choose_action(state, q_table)
        user_action = simulate_user(user_history)

        reward = get_reward(bot_action, user_action)
        user_history.append(user_action)

        next_state = tuple(user_history[-STATE_LEN:])

        update_q_table(q_table, state, bot_action, reward, next_state)

        if i % 10_000 == 0 and i > 0:
            print(f"[Training] Episode {i}/{EPISODES} | States learned: {len(q_table)}")

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(q_table, f)

    print(f"\n[✅] Training complete — saved {len(q_table)} states to '{MODEL_PATH}'")

if __name__ == "__main__":
    train()