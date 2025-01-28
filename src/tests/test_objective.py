import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from ortools.linear_solver import pywraplp
from DataLoader import DataLoader
from Optimization import Optimization

@pytest.fixture
def test_set_objective_function():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))

    item_file = os.path.join(base_dir, "items_updated.csv")
    pricing_file = os.path.join(base_dir, "pricing.csv")
    supplier_file = os.path.join(base_dir, "suppliers.csv")
        
    loader = DataLoader(item_file, pricing_file, supplier_file)
    items, pricing, suppliers = loader.load_data()

    optimizer = Optimization(items, pricing, suppliers)
    
    optimizer.defineDecisionVariables()
    assert optimizer.order, "Decision variables were not defined."

    optimizer.setObjectiveFunction()
    assert optimizer.solver.Objective().minimization() is True, "Objective function is not set to minimize."

    result_status = optimizer.solver.Solve()
    assert result_status == pywraplp.Solver.OPTIMAL, "Solver did not find an optimal solution."

    output_file = os.path.join(os.path.dirname(__file__), '../solver_outputs/optimal_purchasing_plan.csv')
    assert os.path.exists(output_file), f"Solution file was not saved to {output_file}"
