import re
from git import Repo

repo = Repo('.')
diff_files = [item.a_path for item in repo.head.commit.diff('HEAD~1')]

new_tcs_ids = []

regex_pattern = r'\(OL-T\d+(?:,\s*OL-T\d+)*\)'
for file in diff_files:
    if file.endswith('.robot'):
        # Lấy nội dung file trong commit hiện tại
        with open(file, 'r') as f:
            current_content = f.read()
            current_ids = set(re.findall(regex_pattern, current_content))

        # Lấy nội dung file trong commit trước đó
        previous_commit = repo.head.commit.parents[0]
        try:
            previous_content = previous_commit.tree[file].data_stream.read().decode('utf-8')
            previous_ids = set(re.findall(regex_pattern, previous_content))
        except KeyError:
            # Nếu file không tồn tại trong commit trước đó
            previous_ids = set()

        # Lấy các test case mới bằng cách trừ các test case cũ khỏi các test case hiện tại
        new_ids = current_ids - previous_ids
        new_tcs_ids.extend(new_ids)

# Loại bỏ trùng lặp và in các test case mới
new_tcs_ids = set(new_tcs_ids)
log_file_name = "new_tcs.txt"

# Open the log file for writing
with open(log_file_name, "w") as log_file:
    for item in new_tcs_ids:
        # Replace spaces with asterisks and format the string
        formatted_item = item.replace(" ", "*")
        log_entry = f"-t *{formatted_item}\n"
        # Write to the log file
        log_file.write(log_entry)
    print(True)
