# Commit Summarizer

`commit_summarizer.py` is a Python script that extracts commit logs from the `.git` folder in your project, processes them, and saves them as a Markdown file in the current directory.

## Features

- Runs the `git log` command based on the `.git` folder in your project directory
- Extracts commit logs for specified author(s)
- Groups and de-duplicates extracted logs by month
- Saves the result as a Markdown file in the current directory

## Usage

### Prerequisites

- Python 3.x must be installed.
- There must be a `.git` folder in your project directory.

### How to Run

1. Download the `commit_summarizer.py` script.
2. Open the command line and navigate to the directory where the script is located.

3. Run the following command to execute the script:

    ```bash
    python commit_summarizer.py [project folder path] --authors [author1] [author2] ... --output [output filename]
    ```

    Here:
    - `[project folder path]` is the root path of the project that includes the `.git` folder.
    - `[author1]`, `[author2]` etc. are the names of authors you want to filter.
    - `[output filename]` is optional. If not specified, a default filename(commit_summary.md) is used.

### Example

```bash
python commit_summarizer.py /path/to/project --authors "Author Name1" "Author Name2" --output my_project_commits.md
```

## Output

The result file is created in the current directory where the script is run. If a filename is not specified, a default filename based on the name of the Git repository is used. The file is written in Markdown format and contains commit logs grouped by month.

**Note:** When generating a filename based on the name of the Git repository, the URL of the remote repository is extracted. Set the URL of the remote repository if you want to use the name of your local repository.
