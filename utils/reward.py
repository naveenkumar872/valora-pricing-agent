
def calculate_profit(base_cost, selling_price, units_sold):
    revenue = selling_price * units_sold
    cost = base_cost * units_sold
    profit = revenue - cost
    return {
        "revenue": revenue,
        "cost": cost,
        "profit": profit,
        "margin": round((profit / revenue * 100), 2) if revenue > 0 else 0.0
    }

