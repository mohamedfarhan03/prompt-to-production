# skills.md — UC-0C Budget Growth Analyst

skills:
  - name: "load_dataset"
    description: "Read the ward budget CSV file, validate that all required columns are present, and identify rows with null actual_spend values."
    input: "Path to a budget CSV file (e.g., '../data/budget/ward_budget.csv')."
    output: "A clean internal representation of the dataset and a separate report of null rows and their reasons."
    error_handling: "Reject any file that does not contain the mandatory schema (period, ward, category, budgeted_amount, actual_spend, notes). Ensure each null value is logged by its ward and category before returning."

  - name: "compute_growth"
    description: "Calculates MoM (Month-on-Month) or YoY (Year-on-Year) growth for a subset of the dataset specified by ward and category."
    input: "Specific ward, category, and growth_type (MoM or YoY) strings."
    output: "A time-series table including month, actual_spend, growth_rate, and the formula used for each calculation."
    error_handling: "Do not calculate growth for periods with null actual_spend; instead, report the string from the 'notes' column. Mark growth as 'N/A' for the first period of the series. Refuse to execute if the growth_type is not accurately provided."
