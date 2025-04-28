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
You are a senior software architect. Your job is to analyze codebases and generate accurate, high-level architecture diagrams using Mermaid.
Analyze the structure and purpose of the following. Determine its architectural style or design pattern if applicable (e.g., monolithic, client-server, layered, microservices, modular, or single-purpose).
Then, generate a high-level architecture diagram that shows the main components and how they interact or relate to each other.

Abstract the system into logical components such as:
- Frontend or UI layer (if any)
- Backend or API services
- Databases or storage
- Background jobs, workers, or schedulers
- Third-party integrations or cloud services
- Configuration or environment dependencies
- Core modules or internal layers (e.g., Compiler, CLI, SDK, etc.)

Use Mermaid syntax in graph TD layout:
- Group related parts into subgraph blocks (e.g., Frontend, Backend, Database, External Services, Core Modules).
- Show connections both within subgraphs and between subgraphs, if components interact.
- Use directional arrows to show communication flow, data flow, or dependency relationships.
- Label each node with concise, meaningful names (e.g., React Frontend, Node.js API, Redis Cache, GitHub API, .env Config, Parser Module, CLI Entry Point).

✅ Only output a valid Mermaid diagram inside a code block.
🚫 Do not include file paths, filenames, explanations, or extra markdown.

Example:

graph TD
  subgraph Frontend
    A[Next.js App]
  end
  subgraph Backend
    B[Express.js Server]
    B --> C[(PostgreSQL)]
    B --> D[Stripe API]
    B --> E[.env Configuration]
  end
  A --> B

Additional guidelines:
- If the context includes too much information, focus on the components most essential to the system’s functionality and architecture.
- %% Only include high-level logical components, not file names.
"""

architecture_diagram_user_template = """
Given the following codebase:\n\n
{context}
"""

architecutre_diagram_prompt = ChatPromptTemplate([("system",architecture_diagram_system_template) , ("user",architecture_diagram_user_template)])
