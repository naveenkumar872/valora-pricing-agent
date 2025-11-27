
import random
from utils.reward import calculate_profit
# Q-table to store values across state-action pairs


# Q-learning parameters
LEARNING_RATE = 0.1
DISCOUNT = 0.95
EPSILON = 0.5  # 50% of the time we explore randomly
                                        # size of the possible actions
def train_q_table(env, possible_actions, episodes=10):
    q_table = {}

    for episode in range(episodes):
        if random.random() < EPSILON:
            action = random.choice(possible_actions)
        else:
            # Delta state for each action
            q_values = [q_table.get((a - env.state, a), 0) for a in possible_actions]
            max_q = max(q_values)
            max_actions = [a for a, q in zip(possible_actions, q_values) if q == max_q]
            action = random.choice(max_actions)

        # Simulate reward
        
        units_sold = env.simulate_sales(action, env.state)
        reward = calculate_profit(env.base_cost, action, units_sold)["profit"]

        # Delta state
        state = action - env.state


        # Q-learning update
        old_q = q_table.get((state, action), 0)
        new_q = old_q + LEARNING_RATE * (reward - old_q)  # Since environment is 1-step, future Q is 0 so discount * max_future_q will be 0 and hence it is removed
        q_table[(state, action)] = new_q


    return  q_table



def select_best_price(q_table, state, possible_prices):
    q_values = [q_table.get((a - state, a), 0) for a in possible_prices]
    max_q = max(q_values)
    best_actions = [a for a, q in zip(possible_prices, q_values) if q == max_q]

    return random.choice(best_actions)