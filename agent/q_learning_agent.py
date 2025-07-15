
import random
from utils.reward_calculator import calculate_profit
# Q-table to store values across state-action pairs
Q = {}

# Q-learning parameters
LEARNING_RATE = 0.1
DISCOUNT = 0.95
EPSILON = 0.5  # 50% of the time we explore randomly
                                        # size of the possible actions
def train_q_table(env, possible_actions, episodes=10):


    for episode in range(episodes):
        if random.random() < EPSILON:
            action = random.choice(possible_actions)
        else:
            # Delta state for each action
            q_values = [Q.get((a - env.state, a), 0) for a in possible_actions]
            max_q = max(q_values)
            max_actions = [a for a, q in zip(possible_actions, q_values) if q == max_q]
            action = random.choice(max_actions)

        # Simulate reward
        
        units_sold = env.simulate_sales(action, env.state)
        reward = calculate_profit(env.base_cost, action, units_sold)["profit"]

        # Delta state
        state = action - env.state


        # Q-learning update
        old_q = Q.get((state, action), 0)
        new_q = old_q + LEARNING_RATE * (reward - old_q)  # Since environment is 1-step, future Q is 0 so discount * max_future_q will be 0 and hence it is removed
        Q[(state, action)] = new_q


    # # After training, select best price for current state
    # q_values = [Q.get((state, a), 0) for a in possible_actions]
    # best_action_index = q_values.index(max(q_values))
    # best_price = possible_actions[best_action_index]

    return  Q



def select_best_price(Q, state, possible_prices):
    q_values = [Q.get((a - state, a), 0) for a in possible_prices]
    max_q = max(q_values)
    best_actions = [a for a, q in zip(possible_prices, q_values) if q == max_q]

    return random.choice(best_actions)