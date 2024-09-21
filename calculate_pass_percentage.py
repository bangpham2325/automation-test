from xml.etree import ElementTree


def get_stats():
    output_file_path = r"results/output.xml"
    tree = ElementTree.parse(output_file_path)
    root = tree.getroot()
    total_stats = root.find('.//statistics/total/stat')

    stats = {
        "passed": 0,
        "failed": 0,
        "skipped": 0
    }

    if total_stats is not None:
        stats = {
            "passed": int(total_stats.get('pass')),
            "failed": int(total_stats.get('fail')),
            "skipped": int(total_stats.get('skip'))
        }

    # Tính tổng số TCS (passed + failed)
    total_tcs = stats["passed"] + stats["failed"]
    # Calculate pass percentage
    pass_percentage = 0
    if total_tcs > 0:
        pass_percentage = (stats["passed"] / total_tcs) * 100

    return pass_percentage

if __name__ == "__main__":
    pass_percentage = get_stats()
    print(f"{pass_percentage:.2f}")  # Output only the pass percentage
