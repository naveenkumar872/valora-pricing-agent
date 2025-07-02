import random

class PricingEnv:
    def __init__(self, base_cost=200):
        self.base_cost = base_cost
        self.state = None
        self.competitor_prices = []
        self.possible_prices = []
        self.reset()

    def get_competitor_prices(self):
        prices = [random.randint(400, 600) for _ in range(3)]
        self.competitor_prices = prices
        return prices

    def get_dynamic_prices(self, competitors):
        min_price = min(competitors) - 20
        max_price = max(competitors) + 20
        return list(range(min_price, max_price + 1, 10))

    def simulate_sales(self, your_price, competitor_avg):
        if your_price < competitor_avg:
            return random.randint(10, 20)
        elif your_price == competitor_avg:
            return random.randint(5, 10)
        else:
            return random.randint(0, 5)

    def calculate_reward(self, units_sold, price):
        revenue = units_sold * price
        cost = units_sold * self.base_cost
        return revenue - cost

    def step(self, action_price):
        avg_comp = self.state
        units_sold = self.simulate_sales(action_price, avg_comp)
        reward = self.calculate_reward(units_sold, action_price)

        # Now generate new state and possible prices
        new_competitors = self.get_competitor_prices()
        self.state = round(sum(new_competitors) / len(new_competitors), 2)
        self.possible_prices = self.get_dynamic_prices(new_competitors)

        print(f"\n👉 [STEP]")
        print(f"📊 Competitor Prices: {new_competitors}")
        print(f"📈 Avg Competitor Price: ₹{avg_comp}")
        print(f"🎯 Possible Dynamic Prices: {self.possible_prices} (count: {len(self.possible_prices)})")
        print(f"💡 Your Price: ₹{action_price}")
        print(f"🛍️ Units Sold: {units_sold}")
        print(f"💰 Profit (Reward): ₹{reward}")
        print(f"🔁 New State (next avg competitor): ₹{self.state}")

        return self.state, reward, units_sold

    def reset(self):
        competitors = self.get_competitor_prices()
        self.state = round(sum(competitors) / len(competitors), 2)
        self.possible_prices = self.get_dynamic_prices(competitors)

        print(f"\n🔄 [RESET]")
        print(f"🧾 Competitor Prices (reset): {competitors}")
        print(f"📊 Starting avg competitor price: ₹{self.state}")
        print(f"🎯 Initial Possible Prices: {self.possible_prices} (count: {len(self.possible_prices)})")

        return self.state



env = PricingEnv()

for round_num in range(20):
    print(f"\n🔥 ROUND {round_num + 1}")

    current_prices = env.possible_prices
    min_price = min(current_prices)
    max_price = max(current_prices)

    # Pick a mid-range price
    action_price = current_prices[len(current_prices) // 2]

    # ✅ Validate price before step (in range check)
    print(f"🔍 Picking action price: ₹{action_price}")
    if not (min_price <= action_price <= max_price):
        raise ValueError(f"❌ Price ₹{action_price} is out of range ({min_price} to {max_price})")

    # ✅ Call step AFTER validation
    state, reward, units_sold = env.step(action_price)