import os

def create_project_structure():

    # Folder structure
    dirs = [
        "agent",
        "config",
        "exception",
        "logger",
        "notebook",
        "prompt_library",
        "tools",
        "utils",
    ]

    files = {

        # agent
        "agent/__init__.py": "",
        "agent/agentic_workflow.py": "# Agent workflow logic",

        # config
        "config/__init__.py": "",
        "config/config.yaml": "# configuration settings",

        # exception
        "exception/__init__.py": "",
        "exception/exceptionhandling.py": "# custom exception handling",

        # logger
        "logger/__init__.py": "",
        "logger/logging.py": "# logging configuration",

        # notebook
        "notebook/experiments.ipynb": "",

        # prompt library
        "prompt_library/__init__.py": "",
        "prompt_library/prompt.py": "# prompts for LLM",

        # tools
        "tools/__init__.py": "",
        "tools/arthamatic_op_tool.py": "# arithmetic operations tool",
        "tools/currency_conversion_tool.py": "# currency conversion tool",
        "tools/expense_calculator_tool.py": "# expense calculator tool",
        "tools/place_search_tool.py": "# place search tool",
        "tools/weather_info_tool.py": "# weather information tool",

        # utils
        "utils/__init__.py": "",
        "utils/config_loader.py": "# config loader",
        "utils/currency_converter.py": "# currency conversion logic",
        "utils/expense_calculator.py": "# expense calculator logic",
        "utils/model_loader.py": "# model loader",
        "utils/place_info_search.py": "# place search logic",
        "utils/save_to_document.py": "# save outputs to document",
        "utils/weather_info.py": "# weather api logic",

        # root files
        ".env": "OPENAI_API_KEY=\nGROQ_API_KEY=\nWEATHER_API_KEY=",
        "requirements.txt": "langchain\nlanggraph\nstreamlit\npython-dotenv"
    }

    # Create directories
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"Created directory: {d}")

    # Create files
    for path, content in files.items():
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Created file: {path}")

    print("\n✅ Project structure initialized successfully!")


if __name__ == "__main__":
    create_project_structure()