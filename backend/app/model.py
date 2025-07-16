import pickle
import os
import random
import math

ACTIONS = ["rock", "paper", "scissors"]
ACTION_TO_IDX = {a: i for i, a in enumerate(ACTIONS)}
IDX_TO_ACTION = {i: a for i, a in enumerate(ACTIONS)}

class QLearningBot:
    def __init__(self, model_path="app/q_table.pkl", state_len=2, temperature=1.0):
        self.model_path = model_path
        self.q_table = self.load_model()
        self.state_len = state_len
        self.temperature = temperature  # for softmax sampling

    def load_model(self):
        if not os.path.exists(self.model_path):
            print(f"[WARN] Q-table not found at {self.model_path}, using empty table.")
            return {}
        with open(self.model_path, "rb") as f:
            print("[INFO] Q-table loaded.")
            return pickle.load(f)

    def save_model(self):
        with open(self.model_path, "wb") as f:
            pickle.dump(self.q_table, f)
        print("[INFO] Q-table saved.")

    def predict(self, user_history, return_confidence=False):
        state = self._get_state(user_history)

        if state in self.q_table:
            q_values = self.q_table[state]
        else:
            # Fallback: soft match by partial prefix
            q_values = self._fallback_q(state)

        if self.temperature > 0:
            probs = self._softmax(q_values)
            chosen_idx = self._sample_with_probs(probs)
        else:
            max_q = max(q_values)
            best_indices = [i for i, q in enumerate(q_values) if q == max_q]
            chosen_idx = random.choice(best_indices)

        move = IDX_TO_ACTION[chosen_idx]

        if return_confidence:
            confidence = max(q_values) / (sum([abs(v) for v in q_values]) + 1e-6)
            return move, round(confidence, 3)

        return move

    def update_q_table(self, state, action, reward, next_state, alpha=0.5, gamma=0.9):
        if state not in self.q_table:
            self.q_table[state] = [0.0] * len(ACTIONS)
        if next_state not in self.q_table:
            self.q_table[next_state] = [0.0] * len(ACTIONS)

        idx = ACTION_TO_IDX[action]
        old_q = self.q_table[state][idx]
        max_future_q = max(self.q_table[next_state])
        new_q = old_q + alpha * (reward + gamma * max_future_q - old_q)
        self.q_table[state][idx] = new_q

    def _get_state(self, user_history):
        return tuple(user_history[-self.state_len:]) if len(user_history) >= self.state_len else ("",) * self.state_len

    def _fallback_q(self, state):
        # Use empty Q values or attempt simple matching (e.g., first element)
        for key in self.q_table:
            if key[0] == state[0]:  # Soft match first element
                return self.q_table[key]
        return [0.33, 0.33, 0.33]

    def _softmax(self, q_values):
        max_q = max(q_values)
        exp_q = [math.exp((q - max_q) / self.temperature) for q in q_values]
        total = sum(exp_q)
        return [x / total for x in exp_q]

    def _sample_with_probs(self, probs):
        r = random.random()
        cumulative = 0
        for i, p in enumerate(probs):
            cumulative += p
            if r < cumulative:
                return i
        return len(probs) - 1  # fallback