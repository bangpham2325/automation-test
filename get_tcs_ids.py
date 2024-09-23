import re
from git import Repo

repo = Repo('.')
diff_files = [item.a_path for item in repo.head.commit.diff('HEAD~1')]

new_tcs_ids = []

regex_pattern = r'\(OL-T\d+(?:,\s*OL-T\d+)*\)'
for file in diff_files:
    if file.endswith('.robot'):
        # Get the content of the file in the current commit
        with open(file, 'r') as f:
            current_content = f.read()
            current_ids = set(re.findall(regex_pattern, current_content))

        # Get the content of the file in the previous commit
        previous_commit = repo.head.commit.parents[0]
        try:
            previous_content = previous_commit.tree[file].data_stream.read().decode('utf-8')
            previous_ids = set(re.findall(regex_pattern, previous_content))
        except KeyError:
            # If the file does not exist in the previous commit
            previous_ids = set()

        # Get the new test cases by subtracting the old ones from the current ones
        if len(previous_ids) != 0:
            new_ids = current_ids - previous_ids
            new_tcs_ids.extend(new_ids)

# Remove duplicates and print the new test cases
new_tcs_ids = set(new_tcs_ids)
log_file_name = "new_tcs.log"

# Open the log file for writing
with open(log_file_name, "w") as log_file:
    for item in new_tcs_ids:
        # Replace spaces with asterisks and format the string
        formatted_item = item.replace(" ", "*")
        log_entry = f"-t *{formatted_item}\n"
        # Write to the log file
        log_file.write(log_entry)
