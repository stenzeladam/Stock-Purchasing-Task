# Stock Purchasing Optimization

## Overview

This repository contains a solution to the Stock Purchasing Task, which involves optimizing the purchasing of items from suppliers while considering constraints like stock requirements, supplier constraints, expiry conditions, and lead times. The problem is formulated as a Linear Programming (LP) problem and solved using Python’s OR-Tools.

## Problem Description

The task is to restock items while minimizing costs and ensuring that the stock is sufficient to meet daily sales without exceeding supplier constraints. The core challenge is to balance between stock levels, supplier capabilities, item expiry dates, and minimum/maximum pallet limits to arrive at an optimal purchasing plan.

### Key Constraints

- **Stock Constraints**: Ensure that the total units ordered for each item meet the minimum required stock while considering the current stock.
  
- **Supplier Constraints**:
  - **Minimum Pallets**: The supplier should fulfill a minimum number of pallets.
  - **Maximum Pallets**: The supplier should not exceed a maximum number of pallets.
  - **Lead Time**: The stock ordered from suppliers should meet the expected demand during the lead time period.
  
- **Expiry Constraints**: Ensure that stock ordered is sold before the expiry date (at least 15 days before the expiry).
  
- **Supplier Availability Constraint**: Ensure that orders are only placed with suppliers that are allowed to supply the item.

### Objective

The objective is to **minimize the total cost of purchasing** while ensuring all constraints are satisfied and stock is available to meet daily sales.

## Folder Structure

