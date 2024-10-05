import re
from git import Repo

# Regex pattern to find test cases IDs
TEST_CASE_PATTERN = r'\(OL-T\d+(?:,\s*OL-T\d+)*\)'

def extract_tags_from_line(line):
    """Extract tags from a line that starts with 'Default Tags'."""
    tags = re.findall(r'\b\w+\b', line[len("Default Tags"):])
    tags = [tag.upper() for tag in tags if tag.lower() != 'regression']
    return tags

def get_default_tags(file_path):
    """Extract default tags from a given file."""
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip().startswith("Default Tags"):
                    tags = extract_tags_from_line(line)
                    if len(tags) == 1:
                        return tags[0]
                    elif 'TEST' in tags:
                        return 'TEST'
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except IOError:
        print(f"Error reading file: {file_path}")
    return 'TEST'


def get_new_test_case_ids(previous_commit, diff_files):
    """
    Get the IDs of new test cases added in the commit by comparing
    current and previous version of test files.
    """
    new_test_case_ids = set()
    updated_test_file = ''

    for file_path in diff_files:
        if file_path.endswith('.robot') and file_path.startswith('src/tests_suites'):
            current_test_ids = extract_test_case_ids(file_path)
            previous_test_ids = extract_test_case_ids_from_commit(previous_commit, file_path)

            new_ids = current_test_ids - previous_test_ids
            if new_ids:
                updated_test_file = file_path
                new_test_case_ids.update(new_ids)

    # Log new test case IDs
    log_new_test_cases(new_test_case_ids)

    return updated_test_file


def extract_test_case_ids(file_path):
    """Extract test case IDs from the file content using the regex pattern."""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return set(re.findall(TEST_CASE_PATTERN, content))
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return set()


def extract_test_case_ids_from_commit(commit, file_path):
    """Extract test case IDs from a file in a previous commit."""
    try:
        previous_content = commit.tree[file_path].data_stream.read().decode('utf-8')
        return set(re.findall(TEST_CASE_PATTERN, previous_content))
    except KeyError:
        # File does not exist in the previous commit
        return set()


def log_new_test_cases(test_case_ids):
    """Log the new test case IDs into a log file."""
    log_file_name = "new_tcs.log"
    with open(log_file_name, "w") as log_file:
        if not test_case_ids:
            log_file.write("")
        for test_case_id in test_case_ids:
            formatted_id = test_case_id.replace(" ", "*")
            log_file.write(f"-t *{formatted_id}\n")


if __name__ == "__main__":
    repo = Repo('.')
    previous_commit = repo.head.commit.parents[0]
    diff_files = [item.a_path for item in repo.head.commit.diff('HEAD~1')]

    # Get the file name with new test cases
    updated_test_file = get_new_test_case_ids(previous_commit, diff_files)

    # Get the default tags from the updated file
    tag = get_default_tags(updated_test_file)

    # Write the tag to the tag file
    tag_file_path = "tag.txt"
    with open(tag_file_path, "w") as tag_file:
        tag_file.write(tag)

    print(f"Tag extracted: {tag}")
