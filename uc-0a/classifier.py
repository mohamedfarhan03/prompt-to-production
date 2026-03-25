"""
UC-0A — Complaint Classifier
Build this using the RICE → agents.md → skills.md → CRAFT workflow.
"""
import argparse
import csv
import os

# --- SKILL: classify_complaint ---
def classify_complaint(row: dict) -> dict:
    """
    Classify a single complaint row based on RICE enforcement rules.
    Returns: dict with keys: complaint_id, category, priority, reason, flag
    """
    description = row.get("description", "").lower()
    
    # 1. ENFORCEMENT: Category taxonomy
    categories = {
        "Pothole": ["pothole"],
        "Flooding": ["flooded", "flooding", "rain", "inaccessible"],
        "Streetlight": ["streetlight", "lights out", "flickering", "dark"],
        "Waste": ["garbage", "waste", "bins", "dumped", "dead animal"],
        "Noise": ["music", "noise", "loud"],
        "Road Damage": ["cracked", "sinking", "surface", "tiles broken", "footpath"],
        "Heritage Damage": ["heritage"],
        "Heat Hazard": ["heat"],
        "Drain Blockage": ["drain blocked", "drainage"]
    }
    
    found_categories = []
    for cat, keywords in categories.items():
        if any(keyword in description for keyword in keywords):
            found_categories.append(cat)
            
    # 2. ENFORCEMENT: Handle ambiguity
    category = "Other"
    flag = ""
    if len(found_categories) == 1:
        category = found_categories[0]
    elif len(found_categories) > 1:
        category = "Other"
        flag = "NEEDS_REVIEW"
    elif not found_categories:
        category = "Other"
        flag = "NEEDS_REVIEW"

    # 3. ENFORCEMENT: Priority rules
    severity_keywords = [
        "injury", "child", "school", "hospital", "ambulance", 
        "fire", "hazard", "fell", "collapse"
    ]
    
    priority = "Standard"
    if any(keyword in description for keyword in severity_keywords):
        priority = "Urgent"
    elif "standard" not in description and "urgent" not in description:
        # Default fallback
        priority = "Standard"

    # 4. ENFORCEMENT: Reason field (one sentence citing description)
    # Simple extraction of the first sentence or relevant snippet
    reason = f"Classified as {category} because description mentions: "
    matching_keywords = []
    if category != "Other":
        matching_keywords = [k for k in categories.get(category, []) if k in description]
    
    if matching_keywords:
        reason += f"'{matching_keywords[0]}'."
    elif flag == "NEEDS_REVIEW":
        reason = "Genuinely ambiguous category based on description alone."
    else:
        reason = "Could not identify specific keywords for classification."

    return {
        "complaint_id": row.get("complaint_id", "N/A"),
        "category": category,
        "priority": priority,
        "reason": reason,
        "flag": flag
    }

# --- SKILL: batch_classify ---
def batch_classify(input_path: str, output_path: str):
    """
    Read input CSV, classify each row, write results CSV.
    """
    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} not found.")
        return

    try:
        results = []
        with open(input_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                classified = classify_complaint(row)
                # Keep original data plus new fields
                row.update(classified)
                results.append(row)

        if not results:
            print("No data processed.")
            return

        fieldnames = list(results[0].keys())
        with open(output_path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
            
    except Exception as e:
        print(f"Failed to process batch: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UC-0A Complaint Classifier")
    parser.add_argument("--input",  required=True, help="Path to test_[city].csv")
    parser.add_argument("--output", required=True, help="Path to write results CSV")
    args = parser.parse_args()
    
    batch_classify(args.input, args.output)
    print(f"Done. Results written to {args.output}")
