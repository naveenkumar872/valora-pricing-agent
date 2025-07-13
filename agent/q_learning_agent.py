# A dictionary to store the Q-values for each (state, action) pair
Q = {}

# 👇 Let's say we're in a state where avg competitor price is ₹120
state = 120.0

# 👇 We're testing the action of setting our price to ₹150
action = 150

# 👇 After choosing ₹150, we earned a profit of ₹200
reward = 200

# 👇 We estimate the best possible future reward if we act smart next time
max_future_q = 250

# 👇 Learning rate (how quickly we update our beliefs) — 0.1 = slow and stable
LEARNING_RATE = 0.1

# 👇 Discount factor (how much we value future reward) — 0.95 = we care a lot
DISCOUNT = 0.95

# 👇 Update the Q-value using the Q-learning formula
# Q(s, a) = Q(s, a) + α * [r + γ * max(Q(s', a')) - Q(s, a)]
Q[state, action] = Q.get((state, action), 0) + LEARNING_RATE * (
    reward + DISCOUNT * max_future_q - Q.get((state, action), 0)
)

# 👇 Print the updated Q-value for this (state, action) pair
print(f"Updated Q[{state}, {action}] =", Q[state, action])
