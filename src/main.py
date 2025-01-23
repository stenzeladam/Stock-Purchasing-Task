from data_loader import DataLoader

if __name__ == "__main__":
    
    item_file = "data/items_updated.csv"
    pricing_file = "data/pricing.csv"
    supplier_file = "data/suppliers.csv"
    
    loader = DataLoader(item_file, pricing_file, supplier_file)
    items, pricing, suppliers = loader.load_data()

    print("\nData loaded successfully!")
    print(f"\nItems DataFrame:\n{items.head()}")
    print(f"\nPricing DataFrame:\n{pricing.head()}")
    print(f"\nSuppliers DataFrame:\n{suppliers.head()}")
