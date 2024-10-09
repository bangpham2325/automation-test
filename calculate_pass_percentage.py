from xml.etree import ElementTree
import os
import sys
def get_stats(results_dir):
    output_file_path = os.path.join(results_dir, "output.xml")
    if not os.path.exists(output_file_path):
        print(f"Error: {output_file_path} does not exist.")
        sys.exit(1)
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
    if len(sys.argv) != 2:
        print("Usage: python calculate_pass_percentage.py <results_directory>")
        sys.exit(1)

    results_dir = sys.argv[1]
    pass_percentage = get_stats(results_dir)
    print(f"{pass_percentage:.2f}")  # Output only the pass percentage
