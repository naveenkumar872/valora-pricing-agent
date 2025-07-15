import sys
import os
import random
import matplotlib.pyplot as plt
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tool.web_scrape import scrape_flipkart_prices

class PricingEnv:
    def __init__(self, base_cost, search_query):
        self.base_cost = base_cost
        self.search_query = search_query
        self.page = 1
        self.slice_index = 0  # ✅ Tracks current slice in all_prices
        self.retry_count = 0
        self.state = None
        self.competitor_prices = []
        self.possible_prices = []
        self.all_prices = []  # ✅ Store all prices from current page

    def get_competitor_prices(self):
        while True:
            if not self.all_prices:
                print(f"\n📥 Fetching fresh prices from Flipkart (Page {self.page})")
                prices = scrape_flipkart_prices(self.search_query, self.page)
                clean_prices = [p for p in prices if 50 <= p <= 5000]
                self.all_prices = list(set(clean_prices))
                self.slice_index = 0
                print(f"🧹 Cleaned & Unique prices: {self.all_prices}")

            top_prices = self.all_prices[self.slice_index:self.slice_index + 3]
            print(f"🌺 Using slice [{self.slice_index}:{self.slice_index + 3}] → {top_prices}")

            if len(top_prices) < 3:
                self.page += 1
                if self.page > 10:
                    raise Exception("❌ Out of pages and no more prices to extract")
                self.all_prices = []
                self.slice_index = 0
                continue

            self.slice_index += 3
            if self.slice_index >= len(self.all_prices):
                self.page += 1
                self.all_prices = []
                self.slice_index = 0

            self.competitor_prices = top_prices
            return top_prices

    def get_dynamic_prices(self, competitors):
        min_price = min(competitors) - 20
        max_price = max(competitors) + 20
        dynamic_prices = list(range(min_price, max_price + 1, 10))
        print(f"💡 Dynamic price range: {dynamic_prices}")
        return dynamic_prices

    def simulate_sales(self, your_price, competitor_avg):
        # Gaussian model based simulation
        sigma = 30  # spread
        k = 20      # scale of max units sold
        exponent = -((your_price - competitor_avg) ** 2) / (2 * sigma ** 2)
        units_sold = int(k * np.exp(exponent))
        return units_sold

    def plot_sales_curve(self):
        if self.state is None:
            print("⚠️ No state available to plot. Run at least one step.")
            return

        competitor_avg = self.state
        prices = list(range(int(competitor_avg) - 100, int(competitor_avg) + 100, 5))
        units = [self.simulate_sales(p, competitor_avg) for p in prices]

        plt.figure(figsize=(10, 4))
        plt.plot(prices, units, marker='o', color='purple')
        plt.title(f"Demand Curve (Avg Competitor Price: ₹{competitor_avg})")
        plt.xlabel("Price (₹)")
        plt.ylabel("Expected Units Sold")
        plt.grid(True)
        plt.tight_layout()
        plt.show()


    
  
    def step(self):
        new_competitors = self.get_competitor_prices()

        avg = sum(new_competitors) / len(new_competitors)
        self.state = (round(avg / 10) * 10) +5  # 👈 round to nearest 10 and add 5 to it
        
        self.possible_prices = self.get_dynamic_prices(new_competitors)

        # action_price = self.possible_prices[len(self.possible_prices) // 2]
        avg_comp = self.state
        # units_sold = self.simulate_sales(action_price, avg_comp)
        # result = calculate_profit(self.base_cost, action_price, units_sold)
        # reward = result["profit"]

        print(f"\n🔯 [STEP]")
        print(f"📈 Competitor Prices: {new_competitors}")
        print(f"📈 Avg Competitor Price: ₹{avg_comp}")
        print(f"🎯 Possible Dynamic Prices: {self.possible_prices} (count: {len(self.possible_prices)})")
        # print(f"💡 Your Price: ₹{action_price}")
        # print(f"🛍️ Units Sold: {units_sold}")
        # print(f"💰 Profit (Reward): ₹{reward}")
        # print(f"🔁 New State (next avg competitor): ₹{self.state}")

        # return self.state, reward, units_sold
        return self.state


    #def reset(self):
    #   competitors = self.get_competitor_prices()
    #   self.state = round(sum(competitors) / len(competitors), 2)
    #   self.possible_prices = self.get_dynamic_prices(competitors)

    #   print(f"\n🔄 [RESET]")
    #   print(f"🗳️ Competitor Prices (reset): {competitors}")
    #   print(f"📈 Starting avg competitor price: ₹{self.state}")
    #   print(f"🌟 Initial Possible Prices: {self.possible_prices} (count: {len(self.possible_prices)})")
    #   return self.state


