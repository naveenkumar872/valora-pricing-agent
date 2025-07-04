import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random
from tool.web_scrape import scrape_flipkart_prices

class PricingEnv:
    def __init__(self, base_cost=200, search_query="red tshirt"):
        self.base_cost = base_cost
        self.search_query = search_query
        self.page = 1
        self.slice_offset = 0
        self.retry_count = 0  # ✅ Added retry limit
        self.state = None
        self.competitor_prices = []
        self.possible_prices = []
        self.reset()

    def get_competitor_prices(self):
        print(f"\n🔄 Getting competitor prices (Page {self.page}, Slice Offset {self.slice_offset})")
        prices = scrape_flipkart_prices(self.search_query, self.page)
        clean_prices = [p for p in prices if 50 <= p <= 5000]
        unique_prices = sorted(set(clean_prices))  # ✅ Remove duplicates and sort
        print(f"🧹 Cleaned & Unique prices: {unique_prices}")

        top_prices = unique_prices[self.slice_offset:self.slice_offset + 3]
        print(f"🎚️ Using slice [{self.slice_offset}:{self.slice_offset + 3}] → {top_prices}")

        if len(top_prices) < 3:
            self.retry_count += 1
            if self.retry_count > 10:
                raise Exception("❌ Too many retries! Flipkart results might be too sparse.")

            print("⚠️ Not enough unique prices. Retrying with next page...")
            self.page += 1
            if self.page > 10:
                self.page = 1
                self.slice_offset += 3
            return self.get_competitor_prices()  # 🔁 Retry again

        self.retry_count = 0  # ✅ Reset retry count after success
        self.page += 1
        if self.page > 10:
            print("🔁 Page reset! Moving to next slice of prices")
            self.page = 1
            self.slice_offset += 3

        self.competitor_prices = top_prices
        return top_prices

    def get_dynamic_prices(self, competitors):
        min_price = min(competitors) - 20
        max_price = max(competitors) + 20
        dynamic_prices = list(range(min_price, max_price + 1, 10))
        print(f"💡 Dynamic price range: {dynamic_prices}")
        return dynamic_prices

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


# 🔁 Run simulation
if __name__ == "__main__":
    env = PricingEnv(search_query="red tshirt")
    for round_num in range(15):
        print(f"\n🔥 ROUND {round_num + 1}")
        current_prices = env.possible_prices
        if not current_prices:
            print("⚠️ No valid prices to pick from! Skipping round.")
            continue

        action_price = current_prices[len(current_prices) // 2]
        print(f"🔍 Picking action price: ₹{action_price}")
        state, reward, units_sold = env.step(action_price)
