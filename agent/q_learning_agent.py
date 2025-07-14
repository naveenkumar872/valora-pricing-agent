
import random

# Q-table to store values across state-action pairs
Q = {}

# Q-learning parameters
LEARNING_RATE = 0.1
DISCOUNT = 0.95
EPSILON = 0.5  # 50% of the time we explore randomly

def train_q_table(env, possible_actions, episodes=10):

    state = env.state

    for episode in range(episodes):
        # Decide whether to explore or exploit
        if random.random() < EPSILON:
            action = random.choice(possible_actions)
        else:
            # Pick action with highest Q-value so far
            q_values = [Q.get((state, a), 0) for a in possible_actions]
            max_q = max(q_values)
            max_actions = [a for a, q in zip(possible_actions, q_values) if q == max_q]
            action = random.choice(max_actions)

        # Simulate reward for this price
        units_sold = env.simulate_sales(action, state)
        result = env.calculate_profit(env.base_cost, action, units_sold)
        reward = result["profit"]

        # Since environment is 1-step, future Q is 0
        max_future_q = 0

        # Q-learning update
        old_q = Q.get((state, action), 0)
        new_q = old_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q - old_q)
        Q[(state, action)] = new_q

    # After training, select best price for current state
    q_values = [Q.get((state, a), 0) for a in possible_actions]
    best_action_index = q_values.index(max(q_values))
    best_price = possible_actions[best_action_index]

    return best_price, Q