import nbformat
import json
import sys
from nbformat.validator import normalize

NOTEBOOK_PATH = 'notebooks/japanese_embedding_generator.ipynb'

def main():
    notebook_content_str = None
    # 1. Read the notebook file content (raw text)
    try:
        with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
            notebook_content_str = f.read()
        print(f"Successfully read raw content from '{NOTEBOOK_PATH}'.")
    except FileNotFoundError:
        print(f"Error: Notebook file not found at '{NOTEBOOK_PATH}'.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading raw notebook file: {e}")
        sys.exit(1)

    # 2. Strip whitespace
    stripped_content = notebook_content_str.strip()
    if not stripped_content.startswith('{'):
        print(f"Error: Notebook content after stripping does not start with '{{'. Actual start: {stripped_content[:20]}")
        sys.exit(1)
    print("Notebook content stripped of leading/trailing whitespace.")

    # 3. Parse with nbformat.reads()
    notebook_node = None
    try:
        notebook_node = nbformat.reads(stripped_content, as_version=4)
        print(f"Successfully parsed notebook content using nbformat.reads().")
    except Exception as e:
        print(f"Error parsing notebook content with nbformat.reads(): {e}")
        sys.exit(1)

    # 4. Normalize the notebook
    try:
        normalize(notebook_node)
        print("Notebook node normalized successfully (e.g., cell IDs added/updated).")
    except Exception as e:
        print(f"Error during notebook normalization: {e}")
        # Proceed with validation anyway

    # 5. Validate the notebook
    validation_errors_found = False
    try:
        nbformat.validate(notebook_node)
        print(f"Normalized notebook validated successfully against nbformat version 4.")
    except nbformat.ValidationError as e:
        validation_errors_found = True
        print(f"Validation errors found in normalized notebook:")
        print(str(e)) # Print the error message
    except Exception as e:
        validation_errors_found = True
        print(f"An unexpected error occurred during validation of normalized notebook: {e}")

    # 6. Write the notebook back to file
    try:
        with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
            nbformat.write(notebook_node, f)
        print(f"Normalized notebook written back to: '{NOTEBOOK_PATH}'.")
    except Exception as e:
        print(f"Error writing normalized notebook to file: {e}")
        sys.exit(1)

    if validation_errors_found:
        print("\nNote: Validation errors were reported above. The notebook was written back, but may still have issues if errors were severe.")
    else:
        print("\nNotebook validation and repair process completed successfully.")

if __name__ == '__main__':
    main()
