import re

def extract_template_and_variables(llm_output: str):
    """Extracts the prompt template and input variables from the LLM output."""
    try:
        # Improved extraction using regex (more robust)
        match = re.search(r"\"\"\"(.*)\"\"\"", llm_output, re.DOTALL)  # Use DOTALL to match across lines
        if match:
          template = match.group(1).strip() # Extract the template and remove leading/trailing whitespace
        else:
          template = llm_output.strip() # If no match assume the whole output is the template
        
        # Extract variables using regex (more robust)
        variables = re.findall(r"\{([a-zA-Z0-9_]+)\}", template)
        unique_variables = list(set(variables)) # Remove duplicates

        return {"promptTemplate": template, "inputVariables": unique_variables}
    except Exception as e:
        print(f"Error extracting template and variables: {e}")
        return {"promptTemplate": "", "inputVariables":[]}