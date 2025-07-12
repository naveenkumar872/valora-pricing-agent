import numpy as np
import random
import pickle
from env.pricing_env import PricingEnv

# Hyperparameters
EPISODES = 200
LEARNING_RATE = 0.1
DISCOUNT = 0.95
EPSILON = 1.0
EPSILON_DECAY = 0.995
MIN_EPSILON = 0.1

# State and action discretization
def round_state(state):
    return round(state / 10) * 10  # Round to nearest 10

def round_action(price):
    return round(price / 10) * 10

# Initialize Q-table as dictionary
Q_table = {}  # Format: Q[state][action] = value

# Track rewards for plotting
episode_rewards = []

# Initialize environment
env = PricingEnv(base_cost=150, search_query="red tshirt")

for ep in range(EPISODES):
    print(f"\n🎬 EPISODE {ep+1}/{EPISODES}")
    total_reward = 0

    # Step into env to get initial state
    state, _, _, = env.step()
    state = round_state(state)

    done = False
    for step_num in range(1):  # Single-step pricing task

        if state not in Q_table:
            Q_table[state] = {}

        # Populate Q-table for all possible actions
        for a in env.possible_prices:
            rounded_a = round_action(a)
            if rounded_a not in Q_table[state]:
                Q_table[state][rounded_a] = 0

        # Choose action using epsilon-greedy
        if random.uniform(0, 1) < EPSILON:
            action = round_action(random.choice(env.possible_prices))  # Explore
        else:
            action = max(Q_table[state], key=Q_table[state].get)  # Exploit

        print(f"👉 Action Chosen: ₹{action}")

        # Execute action and get reward
        new_state, reward, units_sold = env.step()
        new_state = round_state(new_state)

        # Update Q-value
        if new_state not in Q_table:
            Q_table[new_state] = {round_action(a): 0 for a in env.possible_prices}

        max_future = max(Q_table[new_state].values(), default=0)
        current_q = Q_table[state][action]

        new_q = current_q + LEARNING_RATE * (reward + DISCOUNT * max_future - current_q)
        Q_table[state][action] = new_q

        print(f"🧠 Q[{state}][{action}] updated to {new_q:.2f}")

        state = new_state
        total_reward += reward

    episode_rewards.append(total_reward)

    # Decay epsilon
    if EPSILON > MIN_EPSILON:
        EPSILON *= EPSILON_DECAY

# ✅ Save Q-table to disk
with open("q_table.pkl", "wb") as f:
    pickle.dump(Q_table, f)
print("\n💾 Q-table saved as q_table.pkl")

# ✅ Plot rewards
import matplotlib.pyplot as plt
plt.plot(episode_rewards)
plt.xlabel("Episode")
plt.ylabel("Total Profit (Reward)")
plt.title("Q-Learning Profit Trend")
plt.grid(True)
plt.tight_layout()
plt.show()
