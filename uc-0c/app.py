"""
UC-0C — Number That Looks Right
Build this using the RICE + agents.md + skills.md + CRAFT workflow.
"""
import argparse
import csv
import os
import sys

# --- SKILL: load_dataset ---
def load_dataset(file_path: str):
    """
    Reads CSV, validates columns, and identifies null rows before processing.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Budget file not found: {file_path}")
    
    required_columns = ["period", "ward", "category", "budgeted_amount", "actual_spend", "notes"]
    data = []
    null_rows = []
    
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # Validate schema
            if not all(col in reader.fieldnames for col in required_columns):
                missing = [col for col in required_columns if col not in reader.fieldnames]
                raise ValueError(f"Missing mandatory columns: {missing}")
            
            for row in reader:
                # Identify null actual_spend
                if not row["actual_spend"] or row["actual_spend"].strip() == "":
                    null_rows.append(row)
                data.append(row)
    except Exception as e:
        print(f"Dataset Loading Error: {e}")
        sys.exit(1)
        
    return data, null_rows

# --- SKILL: compute_growth ---
def compute_growth(data, ward, category, growth_type):
    """
    Computes growth for a specific ward and category. 
    Strictly follows RICE rules for null handling and transparency.
    """
    if not growth_type or growth_type.lower() not in ["mom", "yoy"]:
        print("Error: Growth type must be explicitly specified (MoM or YoY). Refusing to guess.")
        sys.exit(1)

    # Filter data for specific ward and category (robust alphanumeric match)
    import re
    def normalize(s):
        return re.sub(r'[^a-zA-Z0-9]', '', s).lower()
    
    target_ward = normalize(ward)
    target_category = normalize(category)
    
    filtered = [row for row in data if normalize(row["ward"]) == target_ward and normalize(row["category"]) == target_category]
    
    if not filtered:
        print(f"Error: No data found for Ward '{ward}' and Category '{category}'.")
        print("Available Wards:", sorted(set(row["ward"] for row in data)))
        print("Available Categories:", sorted(set(row["category"] for row in data)))
        sys.exit(1)

    # Sort by period
    filtered.sort(key=lambda x: x["period"])
    
    results = []
    prev_spend = None
    
    for i, row in enumerate(filtered):
        period = row["period"]
        actual = row["actual_spend"]
        
        # Rule: Report null reason instead of computing
        if not actual or actual.strip() == "":
            reason = row["notes"] if row["notes"] else "Null value without note"
            results.append({
                "period": period,
                "ward": ward,
                "category": category,
                "actual_spend": "NULL",
                "growth": "N/A",
                "formula": "N/A",
                "notes": reason
            })
            prev_spend = None # Break the chain for MoM
            continue
            
        curr_spend = float(actual)
        growth_val = "N/A"
        formula = "N/A"
        
        if i > 0 and prev_spend is not None:
            # MoM growth formula
            growth_pct = ((curr_spend - prev_spend) / prev_spend) * 100
            growth_val = f"{growth_pct:+.1f}%"
            formula = f"(({curr_spend} - {prev_spend}) / {prev_spend}) * 100"
        elif i == 0:
            growth_val = "N/A (First Period)"
            formula = "N/A"
            
        results.append({
            "period": period,
            "ward": ward,
            "category": category,
            "actual_spend": curr_spend,
            "growth": growth_val,
            "formula": formula,
            "notes": ""
        })
        prev_spend = curr_spend
        
    return results

def main():
    parser = argparse.ArgumentParser(description="UC-0C Budget Growth Analyst")
    parser.add_argument("--input", required=True, help="Path to ward_budget.csv")
    parser.add_argument("--ward", required=True, help="Name of the ward")
    parser.add_argument("--category", required=True, help="Budget category")
    parser.add_argument("--growth-type", help="MoM or YoY (Required)")
    parser.add_argument("--output", required=True, help="Path to write results CSV")
    args = parser.parse_args()

    # Step 1: Load and validate
    data, null_rows = load_dataset(args.input)
    
    # Step 2: Compute with RICE enforcement
    results = compute_growth(data, args.ward, args.category, args.growth_type)
    
    # Step 3: Write Output
    if results:
        fieldnames = ["period", "ward", "category", "actual_spend", "growth", "formula", "notes"]
        with open(args.output, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print(f"Growth analysis written to {args.output}")

if __name__ == "__main__":
    main()
