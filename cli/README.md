# 🚀 Code2Docs CLI

**Code2Docs** is an AI-powered CLI tool that helps you generate high-quality documentation for your codebase — including inline docstrings, API documentation, database schema descriptions, and project READMEs.

> ⚠️ This project is still under active development. Expect new features and improvements regularly.

📚 **Base Repo:** [https://github.com/xKarinSan/Code2Docs](https://github.com/xKarinSan/Code2Docs)  
💬 **Community Discord:** [https://discord.gg/qugCeYBYud](https://discord.gg/qugCeYBYud)
🌐 **Landing Page:** [https://code2docs-open-source.netlify.app/](https://code2docs-open-source.netlify.app/)  
🔗 **LinkedIn:** [https://www.linkedin.com/company/code2docs](https://www.linkedin.com/company/code2docs)

## ✨ Features

- 📄 Inline documentation (docstrings + inline comments)
- 📡 API endpoint documentation *(coming soon)*
- 🧩 Database schema documentation *(coming soon)*
- 📘 README.md generation *(coming soon)*
- 🗂️ Architecture diagram generation *(coming soon)*

---
## 🔐 Requirements

- Python 3.8 or newer
- An OpenAI API key
- A Git-initialized codebase

---

## 🧪 Installation

1. Install the CLI:

    ```
    pip install c2d
    ```

2. Run the CLI:

    ```
    code2docs-cli
    ```

---

## 🚀 Getting Started

To begin using Code2Docs:

1. Make sure your project is inside a Git repository.
2. Get your OpenAI API key from [platform.openai.com](https://platform.openai.com/account/api-keys).
3. Save your API key locally using:

```
c2d save-key sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

4. You’re ready to generate documentation!

---

## 🛠️ CLI Commands

### `--help`
Lists ALL the commands for Code2Docs CLI


### `code-doc`
Generates inline documentation (docstrings and comments) for your codebase.
```
c2d code-doc
```

### `api-doc` (Coming Soon)
Generates documentation for your API endpoints.
```
c2d api-doc
```

### `db-doc` (Coming Soon)
Generates documentation for your database schema.
```
c2d db-doc
```

### `readme-doc` (Coming Soon)
Generates a project-level README.md based on your codebase.
```
c2d readme-doc
```

### `archi-doc` (Coming Soon)
Generates an architecture diagram based on the structure of your codebase.
```
c2d archi-doc
```

### `archi-doc` (Coming Soon)
Generates an architecture diagram based on the structure of your codebase.
```
c2d archi-doc
```

### `save-key`
Saves your OpenAI API key locally for authentication.
```
c2d save-key sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### `load-key`
Displays the currently saved OpenAI API key.
```
c2d load-key
```

### `--help`
Displays all available commands and usage.
```
c2d --help
```

