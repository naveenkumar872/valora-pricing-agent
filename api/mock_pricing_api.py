# mock_pricing_api.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.q_learning_agent import train_q_table
from agent.q_learning_agent import select_best_price
from utils.reward_calculator import calculate_profit
from env.pricing_env import PricingEnv

all_state=[]
def run_pricing_simulation(query, rounds=5,base_cost=200):
    print(f"\n🚀 Starting simulation for: '{query}' ({rounds} rounds)")
    env = PricingEnv(search_query=query,base_cost=base_cost)

    result_history = []

    for round_num in range(rounds):
        print(f"\n🔥 ROUND {round_num + 1}")
        state= env.step()
        all_state.append(state)
        

        episodes = len(env.possible_prices)
        
        Q = train_q_table(env,env.possible_prices,episodes )
        # Select best price after training
        best_price = select_best_price(Q, state, env.possible_prices)

        # 👇 DEBUG: Print Q-table for current state
        print("\n📘 Full Q-table (state-action pairs):")
        for (s, a), q_val in sorted(Q.items()):
            print(f"  Q[{s}, {a}] = {round(q_val, 2)}")


        # Calculate reward using the selected best price
        units_sold = env.simulate_sales(best_price, state)
        result = calculate_profit(env.base_cost, best_price, units_sold)
        reward = int(result["profit"])

        round_result = {
            "round": round_num + 1,
            "avg_competitor_price": state,
            "reward": reward,
            "units_sold": units_sold,
            "picked_price": best_price,
            "competitor_prices": env.competitor_prices
        }
        env.plot_sales_curve()
        result_history.append(round_result)

    print("\n📘 Final Full Q-table after all rounds:")
    for (s, a), q_val in sorted(Q.items()):
        print(f"  Q[{s}, {a}] = {round(q_val, 2)}")

    final_state = round(sum(all_state) / len(all_state))  # 291 in this case
   
    rounded_state = (round(final_state / 10) * 10 ) +5
    print(f"\n🎯 Final Avg Competitor Price (State): {rounded_state}")
    
    final_possible_prices = env.get_dynamic_prices([rounded_state]) 
    print("\n Final Possible Process:", final_possible_prices)
    final_price = select_best_price(Q, final_state, final_possible_prices)
    print(f"\n✅ Suggested Final Price based on training: ₹{final_price}")

        
    return result_history


# Run as script
if __name__ == "__main__":
    result = run_pricing_simulation("red tshirt", rounds=5,base_cost=150)

    print("\n📊 Final Summary:")
    for r in result:
        print(f"🔸 Round {r['round']}: Sold {r['units_sold']} at ₹{r['picked_price']} → Profit ₹{r['reward']}")
