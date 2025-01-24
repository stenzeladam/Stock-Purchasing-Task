import pandas as pd

class DataLoader:
    def __init__(self, item_file, pricing_file, supplier_file):
        # These instance variables are the paths to their respective CSV files 
        self.item_file = item_file
        self.pricing_file = pricing_file
        self.supplier_file = supplier_file
    
    def load_data(self):
        try: 
            items = pd.read_csv(self.item_file)
            pricing = pd.read_csv(self.pricing_file)
            suppliers = pd.read_csv(self.supplier_file)

            self._inspect_data(items, "Items")
            self._inspect_data(pricing, "Pricing")
            self._inspect_data(suppliers, "Suppliers")

            return items, pricing, suppliers
        except Exception as e:
            print(f"Error loading data: {e}")
            raise

    def _inspect_data(self, dataFrame, name):
        print(f"\n{name} Data Preview:")
        print(dataFrame.head())
        print(f"\n{name} Data Info:")
        print(dataFrame.info())