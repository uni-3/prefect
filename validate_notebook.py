import nbformat
import json
import sys
import os
import shutil # For copying the file
from nbformat.validator import normalize # Import normalize

ORIGINAL_NOTEBOOK_PATH = 'notebooks/japanese_embedding_generator.ipynb'
TEMP_NOTEBOOK_PATH = 'temp_notebook_for_validation.ipynb' # Will be a copy of the original

def main():
    # 1. Copy the original notebook to a temporary path
    try:
        shutil.copy(ORIGINAL_NOTEBOOK_PATH, TEMP_NOTEBOOK_PATH)
    except Exception as e:
        print(f"Error copying original notebook to temporary path: {e}")
        sys.exit(1)

    # 2. Try to read from the temporary (copied) file
    notebook_node = None
    try:
        with open(TEMP_NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
            notebook_node = nbformat.read(f, as_version=4)
    except Exception as e:
        print(f"Error reading notebook from temporary (copied) file '{TEMP_NOTEBOOK_PATH}': {e}")
        try:
            os.remove(TEMP_NOTEBOOK_PATH)
        except OSError:
            pass
        sys.exit(1)

    # << NEW STEP: Normalize the notebook >>
    if notebook_node:
        try:
            normalize(notebook_node) # This will add cell IDs if missing, among other things
            print("Notebook node normalized (e.g., cell IDs added if missing).")
        except Exception as e:
            print(f"Error during notebook normalization: {e}")
            # Proceeding to validation even if normalization fails to see errors.

    # 3. Validate
    validation_errors = []
    if notebook_node: # Only validate if read and normalization (attempted)
        try:
            nbformat.validate(notebook_node)
            print(f"Notebook (read from temporary copy, and normalized) validated successfully against nbformat version 4.")
        except nbformat.ValidationError as e:
            error_detail = { "message": str(e), "type": "ValidationError" }
            if hasattr(e, 'path') and e.path: error_detail['path'] = list(e.path)
            if hasattr(e, 'validator') and e.validator: error_detail['validator'] = e.validator
            validation_errors.append(error_detail)
            print(f"Validation errors found in content (from temporary copy, after normalization attempt):")
            print(e)
        except Exception as e:
            validation_errors.append({ "message": str(e), "type": "GenericValidationError" })
            print(f"An unexpected error occurred during validation: {e}")
    else:
        print("Skipping validation as notebook_node is None.")


    # 4. Write the (potentially normalized and validated) node back to the ORIGINAL path
    if notebook_node:
        try:
            with open(ORIGINAL_NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
                nbformat.write(notebook_node, f)
            print(f"Notebook written back to original path: '{ORIGINAL_NOTEBOOK_PATH}'.")
        except Exception as e:
            print(f"Error writing notebook to original file '{ORIGINAL_NOTEBOOK_PATH}': {e}")

    # 5. Clean up temp file
    try:
        os.remove(TEMP_NOTEBOOK_PATH)
    except OSError:
        pass

    if validation_errors:
        print("\nSummary of Validation Errors:")
        for err in validation_errors:
             print(f"- Type: {err.get('type')}, Message: {err.get('message')}")
             if 'path' in err: print(f"  Path: {err.get('path')}")

if __name__ == '__main__':
    main()
