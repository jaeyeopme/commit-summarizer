import os
import re
import argparse
import subprocess
from collections import defaultdict

def run_git_log(project_folder, authors):
    git_folder = os.path.join(project_folder, '.git')
    if not os.path.isdir(git_folder):
        raise ValueError("The provided folder does not contain a '.git' directory.")

    git_log_command = ["git", "-C", project_folder, "log", "--pretty=format:%ad: %n%s%n%b", "--no-merges", "--date=format:%Y-%m"]
    for author in authors:
        git_log_command.extend(["--author", author])
    
    result = subprocess.run(git_log_command, capture_output=True, text=True)
    return result.stdout

def get_git_repository_name(project_folder):
    try:
        result = subprocess.run(
            ["git", "-C", project_folder, "remote", "get-url", "origin"], 
            capture_output=True, text=True, check=True
        )
        url = result.stdout.strip()
        repo_name = url.split('/')[-1]
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]  # Remove '.git' extension
        return repo_name
    except subprocess.CalledProcessError:
        return None

def process_commit_log(log_content):
    entries = log_content.split('\n\n')
    parsed_entries = defaultdict(set)

    for entry in entries:
        parts = entry.split(': \n')
        if len(parts) == 2:
            date, message = parts
            match = re.search(r'(\d{4}-\d{2})', date.strip())
            if match:
                normalized_date = match.group(1)
                parsed_entries[normalized_date].add(message.strip())

    return parsed_entries

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process git commit logs from a project folder.')
    parser.add_argument('project_folder', type=str, help='Path to the project folder containing the .git directory.')
    parser.add_argument('--authors', nargs='+', help='List of authors to filter commits.', default=[])
    parser.add_argument('--output', type=str, help='Output file name (default is based on repository name)')

    args = parser.parse_args()

    git_log_content = run_git_log(args.project_folder, args.authors)
    processed_entries = process_commit_log(git_log_content)

    repo_name = get_git_repository_name(args.project_folder)
    default_output_name = f"{repo_name}_commit_summary.md" if repo_name else "commit_summary.md"
    output_file_name = args.output if args.output else default_output_name

    output_file_path = os.path.join(os.getcwd(), output_file_name)
    
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for date, messages in sorted(processed_entries.items()):
            file.write(f'## {date}\n')
            for message in sorted(messages):
                file.write(f'- {message}\n')
            file.write('\n')

