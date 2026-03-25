# skills.md — UC-0A Complaint Classifier

skills:
  - name: "classify_complaint"
    description: "Classify a single citizen complaint into one of the ten allowed categories and determine its priority level based on severity keywords, supplemented with a mandatory justification sentence."
    input: "A dictionary or JSON object containing a 'description' string for one complaint."
    output: "A dictionary or JSON object with the following fields: 'category' (string), 'priority' (string), 'reason' (string), and 'flag' (string, e.g., 'NEEDS_REVIEW' or empty)."
    error_handling: "If the category cannot be determined from the description alone, set 'category' to 'Other' and 'flag' to 'NEEDS_REVIEW'. If any severity keyword (e.g., injury, child, school) is present, set 'priority' to 'Urgent'."

  - name: "batch_classify"
    description: "Reads a list of complaints from an input CSV file, applies the 'classify_complaint' skill to each row, and writes the results to an output CSV file."
    input: "Path to an input CSV file (e.g., '../data/city-test-files/test_pune.csv') containing complaint descriptions."
    output: "Path to an output CSV file (e.g., 'results_pune.csv') containing the original data along with 'category', 'priority', 'reason', and 'flag' columns."
    error_handling: "Log any rows that fail the 'classify_complaint' criteria and continue processing the batch. Ensure all output categories match the allowed taxonomy exactly."
