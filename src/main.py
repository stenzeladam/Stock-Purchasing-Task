from DataLoader import DataLoader
from Optimization import Optimization

def main():
    item_file = "data/items_updated.csv"
    pricing_file = "data/pricing.csv"
    supplier_file = "data/suppliers.csv"
    
    loader = DataLoader(item_file, pricing_file, supplier_file)
    items, pricing, suppliers = loader.load_data()

    optimizer = Optimization(items, pricing, suppliers)
    optimizer.defineDecisionVariables()

    # constraints
    optimizer.addStockConstraints()
    optimizer.addSupplierConstraints()
    optimizer.addExpiryConstraints()
    #optimizer.addSupplierAvailabilityConstraint()
    #optimizer.mixedPalletConstraint()

    optimizer.setObjectiveFunction()
    optimizer.solve()

if __name__ == "__main__":
    main()