# skills.md — UC-X Policy Information Retrieval Agent

skills:
  - name: "retrieve_documents"
    description: "Load all three policy files (HR, IT, Finance) and parse them into a collection of indexed sections by document name and section number."
    input: "Paths to 'policy_hr_leave.txt', 'policy_it_acceptable_use.txt', and 'policy_finance_reimbursement.txt'."
    output: "A structured repository of indexed policy sections, accessible by specific document and section IDs."
    error_handling: "If any document is missing or unreadable, report the retrieval error and ensure the session is alert to document unavailability."

  - name: "answer_question"
    description: "Search the indexed repository for a single-source answer to a user query, providing exact citations or a refusal notice."
    input: "A user's natural language question string."
    output: "A response string that includes a direct answer citing the source document name and section number OR the verbatim refusal template if the answer is not found."
    error_handling: "If a query triggers multiple possible sources, refuse to blend the answers and instead select only the single most relevant source. Apply the refusal template for any question falling outside the provided texts, avoiding all hedging phrases."
