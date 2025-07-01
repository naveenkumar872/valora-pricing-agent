# env/pricing_env.py
import random

class PricingEnv:
    def __init__(self, base_cost=200):
        self.possible_prices = [399, 449, 499, 549, 599]
        self.base_cost = base_cost
        self.state = None  # state = avg_competitor_price
        self.reset()

    def get_competitor_prices(self):
        return [random.randint(400, 600) for _ in range(3)]

    def simulate_sales(self, your_price, competitor_avg):
        if your_price < competitor_avg:
            return random.randint(10, 20)
        elif your_price == competitor_avg:
            return random.randint(5, 10)
        else:
            return random.randint(0, 5)

    def calculate_reward(self, units_sold, price):
        cost_per_unit = self.base_cost
        revenue = units_sold * price
        cost = units_sold * cost_per_unit
        return revenue - cost  # net profit as reward

    def step(self, action_price):
        competitor_prices = self.get_competitor_prices()
        avg_comp = sum(competitor_prices) / len(competitor_prices)
        units_sold = self.simulate_sales(action_price, avg_comp)
        reward = self.calculate_reward(units_sold, action_price)

        # Update internal state
        self.state = round(avg_comp, 2)
        return self.state, reward, units_sold

    def reset(self):
        self.state = round(sum(self.get_competitor_prices()) / 3, 2)
        return self.state


