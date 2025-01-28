# Stock Purchasing Optimization

## Overview

This repository contains a solution to the **Stock Purchasing Task**, which involves optimizing the purchasing of items from suppliers while adhering to constraints like stock requirements, supplier limitations, expiry conditions, and lead times. The problem is modeled as a **Linear Programming (LP)** problem and solved using Python's **OR-Tools** library.

## Problem Description

The task focuses on restocking items cost-effectively, ensuring sufficient stock to meet demand without exceeding supplier constraints. The key challenge lies in balancing stock levels, supplier capabilities, item expiry dates, and pallet limits to derive an optimal purchasing plan.

### **Key Constraints**

1. **Stock Constraints**
   - Total units ordered for each item must meet the minimum required stock, accounting for current stock levels:
      $$
      \sum_{j \in \text{Available Suppliers}} x_{ij} \cdot \text{Units Per Pallet} \geq \text{Min Required Stock}_i - \text{Current Stock}_i
      $$

2. **Supplier Constraints**
   - **Minimum Pallets**: Each supplier must fulfill a minimum number of pallets.
   - **Maximum Pallets**: Orders must not exceed the supplier’s maximum pallet limit.
   - **Lead Time**: Stock ordered should meet expected demand during the lead time without causing overstock:

      $$
      \sum_{j} x_{ij} \cdot \text{Units Per Pallet} + \text{Current Stock}_i \leq \text{Expected Demand During Lead Time}_i
      $$


3. **Expiry Constraints**
   - Ensure stock ordered for each item is sold at least 15 days before its expiry:
      $$
      \sum_{j} x_{ij} \cdot \text{Units Per Pallet} + \text{Current Stock}_i \leq \text{MaxStock}_i
      $$


4. **Supplier Availability**
   - Orders can only be placed with suppliers allowed for a specific item:
      $$
      x_{ij} = 0 \, \text{if } j \not\in \text{Available Suppliers for } i
      $$


### **Objective**

Minimize the total purchasing cost while ensuring all constraints are met:
$$
\text{Total Cost} = \sum_{j} \sum_{i} x_{ij} \cdot \text{Cost Per Pallet for Supplier } j
$$


---

## Solution

The solution is implemented in Python using **OR-Tools**, which provides efficient methods for defining and solving linear programming problems.

### **Implementation Steps**
1. **Data Preparation**
   - Load and preprocess data from CSV files (e.g., suppliers, items, and pricing).
   - Map items to their corresponding suppliers and constraints.

2. **Problem Formulation**
   - Define decision variables $ x_{ij} \quad \text{where} \quad x_{ij} \, \text{represents the number of pallets of item} \, i \, \text{ordered from supplier} \, j. $
   - Define constraints programmatically based on stock, supplier, expiry, and availability requirements.
   - Set up the objective function to minimize total cost.

3. **Optimization**
   - Use OR-Tools to solve the problem, ensuring feasibility and efficiency.

4. **Output**
   - Generate the optimal purchasing plan in tabular format (CSV).
   - Include details like the number of pallets per item per supplier, total cost, and constraint satisfaction.

---

## Folder Structure

```bash

Stock Purchasing Task/
│
├── data/
│   ├── items_updated.csv        # Item data (current stock, min required stock, etc.)
│   ├── suppliers.csv            # Supplier data (min/max pallets, lead times, etc.)
│   ├── pricing.csv              # Pricing data (cost per pallet for each supplier)
│
├── src/
│   ├── DataLoader.py            # Responsible for loading data from csv files in data folder
    ├── main.py                  # Main script to execute the optimization
    ├── Optimization.py          # Class containing the decision variable definition, objective function, and constraints.
    ├── tests/                       # Test cases for the solution
      └── test_objective.py        # Unit tests for the objective function
│   └── solver_outputs/          # Generated output files (CSV with optimal purchasing plan)
│       ├── optimal_purchasing_plan.csv # Generated csv file containing order details
├── requirements.txt             # Python dependencies
├── notes.txt                    # Personal notes documenting thought processes/challenges
└── README.md                    # Documentation

```

---

## Getting Started

### **Dependencies**

Install the required Python packages using:
```bash
pip install -r requirements.txt
```

## Running the Solution

To run the main script and execute the optimization, use the following command:

```bash
python src/main.py
```