import pandas as pd
import numpy as np
from ortools.linear_solver import pywraplp
import os

# Assume NGO has main distribution hubs in these districts with their current inventory
NGO_HUBS = {
    "Khordha": {"food": 100000, "water": 300000, "medical": 10000, "shelter": 20000}, # Bhubaneswar hub
    "Cuttack": {"food": 80000, "water": 200000, "medical": 8000, "shelter": 15000},
    "Balasore": {"food": 50000, "water": 150000, "medical": 5000, "shelter": 10000}
}

# Approximate distances between hubs and all coastal districts (in km)
# Rows: Hubs, Cols: All districts
DISTANCES = {
    "Khordha": {"Kendrapara": 90, "Jagatsinghpur": 70, "Puri": 60, "Ganjam": 170, "Balasore": 200, "Bhadrak": 140, "Jajpur": 100, "Cuttack": 30, "Khordha": 0},
    "Cuttack": {"Kendrapara": 60, "Jagatsinghpur": 50, "Puri": 90, "Ganjam": 200, "Balasore": 170, "Bhadrak": 110, "Jajpur": 70, "Cuttack": 0, "Khordha": 30},
    "Balasore": {"Kendrapara": 140, "Jagatsinghpur": 160, "Puri": 230, "Ganjam": 350, "Balasore": 0, "Bhadrak": 60, "Jajpur": 100, "Cuttack": 170, "Khordha": 200}
}

def optimize_allocation(demand_df, date, resource_type):
    """
    Optimizes the allocation of a specific resource type for a given date.
    resource_type mapping: 'food_demand' -> 'food', etc.
    """
    # Filter demand for the specific date
    day_demand = demand_df[demand_df['date'] == date].copy()
    if day_demand.empty:
        return None
        
    districts = day_demand['district'].tolist()
    demands = day_demand[f"{resource_type}_demand"].tolist()
    
    # Map resource type to hub inventory key
    hub_res_key = resource_type
    
    hubs = list(NGO_HUBS.keys())
    supplies = [NGO_HUBS[h][hub_res_key] for h in hubs]
    
    # Cost matrix (distance as cost)
    costs = []
    for h in hubs:
        costs.append([DISTANCES[h][d] for d in districts])
        
    # Initialize OR-Tools Linear Solver
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return None
        
    # Variables: x[i][j] is the amount of resource sent from hub i to district j
    x = {}
    for i in range(len(hubs)):
        x[i] = {}
        for j in range(len(districts)):
            x[i][j] = solver.NumVar(0, solver.infinity(), f'x_{i}_{j}')
            
    # Constraints: Supply limit at each hub
    for i in range(len(hubs)):
        solver.Add(solver.Sum([x[i][j] for j in range(len(districts))]) <= supplies[i])
        
    # Constraints: Demand fulfillment at each district
    # If total supply < total demand, we just maximize coverage by prioritizing
    # highest demand districts. We use a relaxed constraint.
    total_supply = sum(supplies)
    total_demand = sum(demands)
    
    for j in range(len(districts)):
        if total_supply >= total_demand:
            # Must meet demand exactly
            solver.Add(solver.Sum([x[i][j] for i in range(len(hubs))]) == demands[j])
        else:
            # Can't exceed demand
            solver.Add(solver.Sum([x[i][j] for i in range(len(hubs))]) <= demands[j])
            
    # Objective: Minimize transportation cost (distance * amount)
    # If short on supply, add a large penalty for unmet demand
    objective_terms = []
    for i in range(len(hubs)):
        for j in range(len(districts)):
            # Normalize cost to prevent huge numbers
            cost_factor = costs[i][j] / 100.0
            objective_terms.append(cost_factor * x[i][j])
            
    if total_supply < total_demand:
        # Maximize allocation overall (negative cost for fulfilling demand)
        # We give higher priority to high-demand districts
        for j in range(len(districts)):
            priority = demands[j] / (total_demand + 1) # Priority weight
            for i in range(len(hubs)):
                objective_terms.append(-1000 * priority * x[i][j])
                
    solver.Minimize(solver.Sum(objective_terms))
    
    status = solver.Solve()
    
    results = []
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        for i in range(len(hubs)):
            for j in range(len(districts)):
                amount = x[i][j].solution_value()
                if amount > 0:
                    results.append({
                        "date": date,
                        "resource": resource_type,
                        "from_hub": hubs[i],
                        "to_district": districts[j],
                        "allocated_amount": int(amount),
                        "demand": int(demands[j]),
                        "distance_km": costs[i][j]
                    })
    
    return pd.DataFrame(results)

def run_optimization():
    demand_file = "data/processed/forecasted_demand.csv"
    if not os.path.exists(demand_file):
        print("Forecasted demand not found.")
        return
        
    df = pd.read_csv(demand_file)
    dates = df['date'].unique()
    
    all_allocations = []
    for date in dates:
        for res in ['food', 'water', 'medical', 'shelter']:
            res_df = optimize_allocation(df, date, res)
            if res_df is not None and not res_df.empty:
                all_allocations.append(res_df)
                
    if all_allocations:
        final_df = pd.concat(all_allocations, ignore_index=True)
        final_df.to_csv("data/processed/optimal_allocations.csv", index=False)
        print("Optimization completed and saved to optimal_allocations.csv")
    else:
        print("No allocations possible.")

if __name__ == "__main__":
    run_optimization()
