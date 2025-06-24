```markdown
# AGENTS.md - Guidelines for AI Agents

This document provides guidelines and information for AI agents working with the `prefect-dlt` repository.

## 1. Repository Overview

This project utilizes Prefect for workflow orchestration, dlt for data loading, and dbt for data transformation. Data is primarily stored in MotherDuck, and serverless compute is handled by Modal.

Key technologies and tools:
- Python (>=3.11.0)
- Prefect
- dlt
- dbt (with BigQuery and DuckDB adapters)
- MotherDuck
- Modal
- Docker
- uv (Python package installer/resolver)
- Hatchling (Build backend)

## 2. Repository Structure

- **`.dlt/`**: Configuration for dlt.
- **`.github/`**: GitHub-specific files, including workflows for CI.
    - **`workflows/`**: Contains CI checks (e.g., `sqlfmt.yml`, `yamllint.yml`).
- **`.devcontainer/`**: Configuration for VS Code Dev Containers.
- **`blocks/`**: Prefect blocks (e.g., `github.py` for GitHub integration).
- **`databases/`**: Database-related utilities or configurations.
- **`dbt_project/`**: Contains the dbt project, including models, seeds, tests, and `dbt_project.yml`.
- **`dlt_project/`**: dlt pipeline definitions, organized by data source (e.g., `estat`, `github`, `pokemon`).
- **`flows/`**: Prefect flow definitions.
- **`src/`**: General Python source code (e.g., `config.py`).
- **`tasks/`**: Prefect task definitions.
- **`templates/`**: Templates, such as for Modal job configurations.
- **`Makefile`**: Contains common development and deployment commands. Run `make help` to see available commands.
- **`pyproject.toml`**: Python project definition, dependencies (managed by `hatchling` and `uv`).
- **`requirements.txt`**: Pip-style requirements file (though `uv` and `pyproject.toml` are preferred for dependency management).
- **`uv.lock`**: Lockfile for `uv`.
- **`Dockerfile`**: For building Docker images.
- **`prefect.yaml`**: Prefect project configuration file.

## 3. Programming Languages and Style

### 3.1. Python
- **Version**: >=3.11.0
- **Style Guide**: Follow PEP 8.
- **Formatting**:
    - **Black**: This project is expected to use Black for Python code formatting. Please ensure any Python code you write or modify is formatted with Black. (Agent: Configuration for Black was not found in `pyproject.toml`, but it's a common tool. Please confirm if it's used and if there's a specific configuration).
- **Linting**: (Agent: No specific Python linter like Flake8 or Pylint was explicitly found. Please confirm if one is used).

### 3.2. SQL (primarily for dbt models)
- **Style Guide**: Follow general SQL best practices.
- **Formatting**:
    - **shandy-sqlfmt**: Used for formatting SQL files.
    - Configuration is in `pyproject.toml` (`[tool.sqlfmt]`).
        - `line_length = 99`
    - A GitHub Action in `.github/workflows/sqlfmt.yml` automatically formats and commits changes to `.sql` files in pull requests.
- **Linting**: No specific SQL linter found beyond `sqlfmt`'s checking capabilities.

### 3.3. YAML
- **Style Guide**: Follow general YAML best practices.
- **Formatting & Linting**:
    - **yamllint**: Used for linting YAML files.
    - Configuration is in `.yamllint.yaml`.
        - `line-length`: max 120 (warning)
        - `indentation`: 2 spaces
    - A GitHub Action in `.github/workflows/yamllint.yml` checks YAML files and reports issues.

## 4. Dependency Management
- **Primary Tool**: `uv` is used for Python package installation and resolution.
- **Configuration**: Dependencies are defined in `pyproject.toml`.
- **Lock File**: `uv.lock` ensures reproducible builds.
- **dbt Dependencies**: Managed within the `dbt_project/` directory, typically using `dbt deps` (see `Makefile`).

## 5. Build, Test, and CI Process
- **Makefile**: Contains various helper scripts for common tasks like running dbt, building Docker images, deploying flows, etc. Refer to `make help`.
- **dbt**:
    - Run dbt models: `make run-dbt`
    - Install dbt dependencies: `make dbt-deps`
    - Generate dbt docs: `make gen-dbt-docs`
- **Docker**:
    - Build image: `make docker-build`
    - Push image: `make docker-push`
- **Prefect**:
    - Deploy flows: `make deploy` or `prefect deploy`
- **Continuous Integration (CI)**:
    - GitHub Actions are used (see `.github/workflows/`).
    - `sqlfmt` checks and formats SQL files.
    - `yamllint` checks YAML files.

## 6. Commit Message and Branching Conventions

**(Agent: User input needed for this section)**

- **Commit Messages**:
    - *Please provide the preferred style (e.g., Conventional Commits, imperative mood, subject line length).*
- **Branch Naming**:
    - *Please provide the preferred naming convention (e.g., `feature/xxx`, `bugfix/yyy`, `chore/zzz`, `issue-number/description`).*

## 7. Working with dlt and Prefect
- **dlt Pipelines**: Defined in `dlt_project/`. When adding new data sources or modifying existing ones, ensure configurations in `.dlt/config.toml` (if applicable) and pipeline scripts are correct.
- **Prefect Flows and Tasks**: Defined in `flows/` and `tasks/`. Follow existing patterns for creating and registering flows and tasks.
- **Prefect Blocks**: Custom blocks are in `blocks/`. Use `prefect block register -f <file_path>` to register them.

## 8. AI Agent Specific Instructions

**(Agent: User input needed for this section)**

- *Please specify any particular behaviors you expect from the AI agent.*
- *Are there files or directories the agent should generally avoid modifying unless explicitly asked?*
- *How should the agent handle potentially breaking changes or ask for clarification on complex tasks?*
- *Are there any anti-patterns in this codebase the agent should be aware of and avoid?*

## 9. Important Files to Check
- `README.md`: General project information and manual setup steps.
- `Makefile`: For common commands and workflows.
- `pyproject.toml`: For Python dependencies and tool configurations.
- `.github/workflows/`: For CI processes.
- `.yamllint.yaml`: For YAML linting rules.
- `prefect.yaml`: For Prefect project settings.

By following these guidelines, AI agents can contribute more effectively to this repository.
```
