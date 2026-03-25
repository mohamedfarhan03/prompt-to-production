# skills.md — UC-0B Policy Compliance Summarizer

skills:
  - name: "retrieve_policy"
    description: "Load a policy .txt file and parse its content into structured, numbered sections for precise referencing."
    input: "Path to a policy document in .txt format (e.g., '../data/policy-documents/policy_hr_leave.txt')."
    output: "A dictionary or JSON object mapping clause numbers (e.g., '2.3', '5.2') to their full original text."
    error_handling: "If the source file is unreadable or lacks clause numbering, raise an error indicating the structural failure. Ensure no external text is added durante the loading process."

  - name: "summarize_policy"
    description: "Condense every numbered clause into a summary while maintaining all binding obligations and multi-condition approval requirements."
    input: "A structured dictionary of numbered policy sections provided by the retrieve_policy skill."
    output: "A summarized document (.txt) that includes all 10 ground truth clauses with their full obligations intact."
    error_handling: "If a summary silently drops a condition (e.g., mapping Clause 5.2 as requiring 'only' one approver), the system must correct the entry or quote it verbatim with a 'CRITICAL_OBLIGATION' flag. If mandatory verbs ('must', 'will') are missing, the output is considered invalid."
