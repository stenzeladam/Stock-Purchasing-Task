from ortools.linear_solver import pywraplp

class Optimization:
    def __init__(self, items, pricing, suppliers):
        self.items = items
        self.pricing = pricing
        self.suppliers = suppliers
        
        # Indices for the IDs in the csv files start at 1, while indices in Python start at 0
        # Subtract 1 from all IDs in the csv files to make them match Python's indexing
        self.items['ItemID'] -= 1
        self.suppliers['SupplierID'] -= 1
        self.pricing['ItemID'] -= 1
        self.pricing['SupplierID'] -= 1

        self._UNITS_PER_PALLET = 24 # Protected, supposed to be treated as a constant

        # CBC solver for Mixed-Integer Linear Programming (MILP) to enforce integer decision variables
        self.solver = pywraplp.Solver.CreateSolver('CBC')
        if not self.solver:
            raise Exception("Solver not available")
        self.order = {}
        self._supplier_item_map = self._createSupplierItemMap()

    def _createSupplierItemMap(self):
        # Creates a mapping between SupplierID and the items they can supply, along with the cost per pallet.
        # Returns a dictionary: {SupplierID: {ItemID: CostPerPallet, ...}, ...}
        supplier_item_map = {}
        for _, row in self.pricing.iterrows():
            supplier_id = row['SupplierID']
            item_id = row['ItemID']
            cost_per_pallet = row['CostPerPallet']

            if supplier_id not in supplier_item_map:
                supplier_item_map[supplier_id] = {}

            supplier_item_map[supplier_id][item_id] = cost_per_pallet

        return supplier_item_map
    
    def setObjectiveFunction(self):
        objective = self.solver.Objective()

        for i in self.items['ItemID']:
            for j in self.suppliers['SupplierID']:
                if i in self._supplier_item_map.get(j, {}): # conditional to ensure the supplier actually supplies the item
                    costPerUnit = self._supplier_item_map[j][i] / self._UNITS_PER_PALLET
                    objective.SetCoefficient(self.order[(i, j)], costPerUnit * self._UNITS_PER_PALLET)

                    # minimize the total cost
                    objective.SetMinimization()


    def defineDecisionVariables(self):
        # Each variable represents the number of pallets ordered for an item-supplier pair.
        for i in self.items['ItemID']:
            for j in self.suppliers['SupplierID']:
                self.order[(i, j)] = self.solver.IntVar(0, 1000, f"order_{i}_{j}") 
    
    def addStockConstraints(self):
        # Defines the constraints for items
        for i in self.items['ItemID']:
            minStock = self.items.loc[self.items['ItemID'] == i, 'MinStock'].values[0]
            currentStock = self.items.loc[self.items['ItemID'] == i, 'CurrentStock'].values[0]

            # Ensure total units ordered for each item i meet the minimum required stock while considering the current stock:
            # ∑_j ∈ Available suppliers for i (x_ij * Units Per Pallet) >= MinRequired Stock_i - CurrentStock_i
            self.solver.Add(
                sum(self.order[(i, j)] * self._UNITS_PER_PALLET for j in self.suppliers['SupplierID']) >= minStock - currentStock
            )

    def addSupplierConstraints(self):
        # Defines the constraints from suppliers
        for j in self.suppliers['SupplierID']:
            minPallets = self.suppliers.loc[self.suppliers['SupplierID'] == j, 'MinPallets'].values[0]
            maxPallets = self.suppliers.loc[self.suppliers['SupplierID'] == j, 'MaxPallets'].values[0]
            leadTime = self.suppliers.loc[self.suppliers['SupplierID'] == j, 'LeadTime (days)'].values[0]

            # Minimum Pallets: ∑_i (x_ij) >= MinPallets for supplier j
            self.solver.Add(
                sum(self.order[(i, j)] for i in self.items['ItemID']) >= minPallets
            )

            # Maximum Pallets: ∑_i (x_ij) <= MaxPallets for supplier j
            self.solver.Add(
                sum(self.order[(i, j)] for i in self.items['ItemID']) <= maxPallets
            )

            # Lead Time: ∑_j(x_ij * Units per pallet + CurrentStock_i) <= Expected Demand During Expiry Period_i
            # Assume the expected demand during the expiry period is going to be the AverageDailySale * Expiry (days) for each item.
            for i in self.items['ItemID']:
                if i in self._supplier_item_map.get(j, {}):  # Only consider items supplied by supplier j
                    currentStock = self.items.loc[self.items['ItemID'] == i, 'CurrentStock'].values[0]
                    avgDailySale = self.items.loc[self.items['ItemID'] == i, 'AverageDailySale'].values[0]
                    expiryDays = self.items.loc[self.items['ItemID'] == i, 'Expiry (days)'].values[0]

                    # Expected demand during expiry period
                    expectedDemand = avgDailySale * expiryDays

                    # Add the constraint: current stock + order quantity >= expected demand
                    self.solver.Add(
                        currentStock + sum(self.order[(i, j)] * self._UNITS_PER_PALLET for j in self.suppliers['SupplierID']) >= expectedDemand
                    )

                    # Lead time demand
                    leadTimeDemand = avgDailySale * leadTime

                    # Add the constraint: current stock + order quantity >= lead time demand
                    self.solver.Add(
                        currentStock + sum(self.order[(i, j)] * self._UNITS_PER_PALLET for j in self.suppliers['SupplierID']) >= leadTimeDemand
                    )

    
    def addExpiryConstraints(self):
        # Ensure that the stock ordered for each item is sold at least 15 days before its expiry date:
        for j in self.suppliers['SupplierID']:
            for i in self.items['ItemID']:
                if i in self._supplier_item_map.get(j, {}): # if the item is available from the supplier
                    expiry = self.items.loc[self.items['ItemID'] == i, 'Expiry (days)'].values[0]
                    currentStock = self.items.loc[self.items['ItemID'] == i, 'CurrentStock'].values[0]
                    maxStock = self.items.loc[self.items['ItemID'] == i, 'MaxStock'].values[0]
                    avgDailySale = self.items.loc[self.items['ItemID'] == i, 'AverageDailySale'].values[0]
                    
                    # Calculate the number of days before expiry that we need to ensure stock is sold
                    daysBeforeExpiry = expiry - 15  # Stock should be sold before 15 days of expiry
                    expectedDemandExpiryConstraint = avgDailySale * daysBeforeExpiry

                    # ∑_j(x_ij * Units Per Pallet + Current Stock_i) <= MaxStock_i
                    self.solver.Add(
                        sum(self.order[(i, j)] * self._UNITS_PER_PALLET for j in self.suppliers['SupplierID']) + currentStock <= expectedDemandExpiryConstraint
                    )

                    # Ensure the stock ordered does not exceed max stock
                    self.solver.Add(
                        sum(self.order[(i, j)] * self._UNITS_PER_PALLET for j in self.suppliers['SupplierID']) + currentStock <= maxStock
                    )

    def addSupplierAvailabilityConstraint(self):
        # Ensure orders are only placed with allowed suppliers for each item:
        # x_ij = 0 if j !∈ Available suppliers for item i

        for j in self.suppliers['SupplierID']:
            for i in self.items['ItemID']:
                if i not in self._supplier_item_map.get(j, {}):
                    # If the supplier does not supply the item, enforce the availability constraint x_ij = 0
                    self.solver.Add(self.order[(i, j)] == 0)

    def mixedPalletConstraint(self): 
        # Handle scenarios where a pallet contains ratios of different items from the same supplier, and ensure to not exceed MaxPallets
        for j in self.suppliers['SupplierID']:
            self.solver.Add(
                sum(self.order[(i, j)] for i in self.items['ItemID']) <= self.suppliers.loc[self.suppliers['SupplierID'] == j, 'MaxPallets'].values[0]
            )
            
    def solve(self):
        status = self.solver.Solve()
        if status == pywraplp.Solver.OPTIMAL:
            print("Optimal solution found!")
            for (i, j), var in self.order.items():
                print(f"Order for item {i} from supplier {j}: {var.solution_value()} pallets")
        elif status == pywraplp.Solver.INFEASIBLE:
            print("No feasible solution!")
        else:
            print("Solver did not converge!")
