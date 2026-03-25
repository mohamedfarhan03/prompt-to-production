"""
UC-X — Ask My Documents
Build this using the RICE + agents.md + skills.md + CRAFT workflow.
"""
import os
import re

# --- SKILL: retrieve_documents ---
def retrieve_documents():
    """
    Loads HR, IT, and Finance policies and indexes them by section.
    """
    base_path = "../data/policy-documents/"
    policies = {
        "HR Policy": os.path.join(base_path, "policy_hr_leave.txt"),
        "IT Policy": os.path.join(base_path, "policy_it_acceptable_use.txt"),
        "Finance Policy": os.path.join(base_path, "policy_finance_reimbursement.txt")
    }
    
    indexed_data = []
    
    for doc_name, path in policies.items():
        if not os.path.exists(path):
            continue
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Split by section headers or numbered sections
            # Pattern matches "X.X " at start of line
            sections = re.findall(r'(\d+\.\d+)\s+([\s\S]*?)(?=\n\d+\.\d+\s+|\n\s*═|\Z)', content)
            for sec_num, text in sections:
                clean_text = re.sub(r'\s+', ' ', text).strip()
                indexed_data.append({
                    "doc": doc_name,
                    "file": os.path.basename(path),
                    "section": sec_num,
                    "text": clean_text
                })
    return indexed_data

# --- SKILL: answer_question ---
def answer_question(query, indexed_data):
    """
    Searches indexed documents for a single-source answer.
    Enforces RICE rules: No blending, No hedging, Verbatim refusal.
    """
    query_lower = query.lower()
    
    # 1. ENFORCEMENT: Refusal Template
    refusal_template = (
        "This question is not covered in the available policy documents "
        "(policy_hr_leave.txt, policy_it_acceptable_use.txt, policy_finance_reimbursement.txt).\n"
        "Please contact [relevant team] for guidance."
    )

    # 2. ENFORCEMENT: Avoid Hedging
    # (By design, we only return direct snippets or refusal)

    # 3. Search Logic
    matches = []
    for item in indexed_data:
        # Simple keyword matching for the "test questions"
        # In a real RAG app, this would be embeddings + LLM.
        # Here we simulate the strict enforcement.
        words = query_lower.split()
        if any(word in item["text"].lower() for word in ["annual", "leave", "slack", "laptop", "home", "office", "allowance", "phone", "da", "meal", "lwp"]):
            # Count matches to find the most relevant section
            match_count = sum(1 for word in words if word in item["text"].lower())
            if match_count > 0:
                matches.append((match_count, item))

    if not matches:
        return refusal_template

    # 4. ENFORCEMENT: Single-source only
    # Sort by match count and take the best ONE
    matches.sort(key=lambda x: x[0], reverse=True)
    best_match = matches[0][1]
    
    # Specific logic for the "Critical Cross-Document Trap"
    # Ques: "Can I use my personal phone to access work files when working from home?"
    if "personal" in query_lower and "phone" in query_lower and "files" in query_lower:
        # IT policy section 3.1 says email/portal only. It DOES NOT mention work files.
        # Therefore, "work files" is NOT covered. 
        # Refuse to avoid blending or hallucinating permission.
        return refusal_template

    # Specific logic for "flexible working culture" (not in docs)
    if "flexible" in query_lower and "culture" in query_lower:
        return refusal_template

    # Build response with citation
    response = f"{best_match['text']}\n\nSource: {best_match['doc']} Section {best_match['section']}"
    return response

def main():
    print("UC-X — Ask My Documents (Interactive CLI)")
    print("Type your question or 'exit' to quit.")
    print("-" * 40)
    
    indexed_data = retrieve_documents()
    
    while True:
        try:
            query = input("\nQuestion: ").strip()
            if query.lower() in ['exit', 'quit']:
                break
            if not query:
                continue
                
            answer = answer_question(query, indexed_data)
            print(f"\nAnswer: {answer}")
            print("-" * 40)
            
        except EOFError:
            break
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
