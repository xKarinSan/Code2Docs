from langchain.prompts.chat import ChatPromptTemplate
"""
For inline docs
"""

inline_doc_templates = '''
You are an expert code reader and documentation assistant.
Your task is to overwrite each source file by adding high-quality inline documentation: docstrings and inline comments that explain the code's purpose, structure, and logic.

⚠️ CRITICAL PRESERVATION REQUIREMENTS:

1. PROCESS OVERVIEW: First READ the entire file to understand it. Then ADD documentation only. NEVER MODIFY existing code.

2. IMPORTS PRESERVATION:
   - Every import statement is SACRED. Compare your final output with the original to ensure ALL imports exist exactly as they were.
   - This applies to ALL import mechanisms: import statements, require calls, includes, uses, using directives, etc.
   - This applies to ALL languages and frameworks: JavaScript, TypeScript, Python, Java, Go, Ruby, PHP, C#, Rust, React, Vue, Angular, etc.
   - Even if an import appears unused, duplicated, or unnecessary, you MUST preserve it unchanged.
   - Check the EXACT order, spacing, and formatting of imports in your final output.

3. STRICT CONTENT PRESERVATION:
   - Character-for-character preservation of ALL code logic.
   - Do NOT change, remove, reorder, or reformat ANY code.
   - Do NOT rename ANY identifiers (variables, functions, classes, etc.).
   - Do NOT modify indentation, line breaks, or spacing patterns.
   - Do NOT fix any perceived errors, style issues, or inefficiencies.
   - Do NOT add or remove semicolons, brackets, or parentheses.

4. SPECIAL BLOCKS:
   - Any code between comment markers like:
     ```
     // DO NOT TOUCH THIS LINE: IMPORTS START
     ...
     // DO NOT TOUCH THIS LINE: IMPORTS END
     ```
     must be preserved character-for-character with identical whitespace.

✅ YOUR ONLY PERMITTED ACTIONS:
   - Add docstrings above functions, classes, and modules.
   - Add inline comments (using language-appropriate syntax) to explain logic.
   - Ensure comments follow language-specific conventions.

🔍 VERIFICATION PROCESS:
   1. After adding documentation, run a COMPLETE line-by-line comparison with the original code.
   2. Verify that ALL import statements remain EXACTLY as in the original.
   3. Verify ALL code logic remains unchanged.
   4. Only proceed if the comparison confirms all requirements are met.

🧩 OUTPUT FORMAT:
   - Return the ENTIRE modified file.
   - Do NOT wrap your output in code blocks or markdown formatting.
   - Do NOT include any explanation outside the documented code itself.

📝 DOCSTRING CONVENTIONS:
   - Function docstrings: Document purpose, parameters, return values, exceptions.
   - Class docstrings: Document purpose, attributes, methods.
   - Module docstrings: Document purpose, high-level functionality.
   - Use language-appropriate docstring formats (Python: triple quotes, JS/TS: JSDoc, etc.)

⚠️ FINAL VERIFICATION: After completing your work, perform one final check specifically for imports and dependencies to ensure not a single one was modified or removed.

'''

inline_doc_user_template = "Language:{language} \n {code}"

inline_doc_prompt = ChatPromptTemplate.from_template(inline_doc_templates + "\n\n" + inline_doc_user_template)


"""
For RAG (especially summarising each code)
"""
rag_file_summariser_template = """
You are a software engineer summarizing source code for internal documentation. \n
You need to retain key technical elements without formatting it for external readability.
"""

rag_file_summarise_user_template = """
Summarize the following file while keeping all important implementation details.

Include:
- All function and class definitions (keep signatures and bodies)
- Import statements
- Core logic (retain control flow and important operations)
- All environment variable usage (e.g., os.getenv, os.environ, process.env)

Ignore:
- Docstrings
- Markdown formatting
- Unnecessary comments

You may simplify some repeated logic, but do not omit anything important.

--- FILE START ---

{code}

--- FILE END ---"""

rag_file_summarise_prompt = ChatPromptTemplate.from_template(rag_file_summariser_template + "\n\n" + rag_file_summarise_user_template)



""" 
For the architectural diagram
"""

architecture_diagram_system_template = """
You are a senior software architect. You analyze codebases and produce accurate, high-level system architecture diagrams using Mermaid syntax.
"""

architecture_diagram_user_template = """
Given the following codebase context:\n\n
{context}\n\n
Determine whether the architecture is **monolithic** or **microservice-based** based on how the components are structured and interact.\n\n
Then, generate a **high-level architecture diagram** using **Mermaid syntax** in `graph TD` layout, following this visual style:\n
- For monoliths: group the business layer and data access layer inside a box, with the database below, and a single user interface at the top\n
- For microservices: place a shared user interface at the top, then several independent microservices below, each connecting to its own database\n
- Show **data flow** using directional arrows (`-->`) from UI to backend/microservices, and from those to their databases\n
- Use **`subgraph` blocks** to visually group Monolithic or Microservice components\n
- Use meaningful labels like `User Interface`, `Business Layer`, `Data Access Layer`, `Microservice A`, `Database/Store`, etc.\n\n
**Only output the Mermaid diagram inside a code block** — no explanation or extra text.\n\n
**Example structure for monolith:**\n
graph TD\n
   A[User Interface] --> B[Business Layer]\n
   B --> C[Data Access Layer]\n
   C --> D[(Database)]\n


**Example structure for microservices:**\n

graph TD\n
   UI[User Interface]\n
   UI --> MS1[Microservice A]\n
   UI --> MS2[Microservice B]\n
   MS1 --> DB1[(DB A)]\n
   MS2 --> DB2[(DB B)]\n
   MS1 --> MS2\n
"""

architecutre_diagram_prompt = ChatPromptTemplate.from_template(architecture_diagram_system_template + "\n\n" + architecture_diagram_user_template)
