# mock_pricing_api.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from env.pricing_env import PricingEnv


def run_pricing_simulation(query, rounds=5,base_cost=200):
    print(f"\n🚀 Starting simulation for: '{query}' ({rounds} rounds)")
    env = PricingEnv(search_query=query,base_cost=base_cost)

    result_history = []

    for round_num in range(rounds):
        print(f"\n🔥 ROUND {round_num + 1}")
        state, reward, units_sold = env.step()
     

        round_result = {
            "round": round_num + 1,
            "avg_competitor_price": state,
            "reward": reward,
            "units_sold": units_sold,
            "picked_price": env.possible_prices[len(env.possible_prices) // 2],
            "competitor_prices": env.competitor_prices
        }
        env.plot_sales_curve()
        result_history.append(round_result)
    return result_history


# Run as script
if __name__ == "__main__":
    result = run_pricing_simulation("red tshirt", rounds=5,base_cost=150)

    print("\n📊 Final Summary:")
    for r in result:
        print(f"🔸 Round {r['round']}: Sold {r['units_sold']} at ₹{r['picked_price']} → Profit ₹{r['reward']}")
