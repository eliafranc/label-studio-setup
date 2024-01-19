import os
import sys
import argparse


def generate_directory_list(name: str, input_directory: str):
    """Generate a text file that contains a list of subdirectories relative to
    the input_directory"""

    if not os.path.exists(input_directory):
        print(f"Error: Directory '{input_directory}' not found.")
        return

    directories = []

    # Walk through the input directory and get all subdirectories
    for dirpath, dirnames, filenames in os.walk(input_directory):
        for dirname in dirnames:
            directories.append(f"./{dirname}")
        break

    output_file_path = f"data_config/{name}.txt"
    with open(output_file_path, "w") as output_file:
        output_file.write("\n".join(directories))

    print(f"Directory list generated and saved to {output_file_path}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Generate a list of subdirectories relative to the input"
            " directory."
        )
    )
    parser.add_argument(
        "name",
        help=(
            "Name of the dataset. Same as what was used in the docker-compose"
            " file under the volumes section."
        ),
    )
    parser.add_argument(
        "dataset",
        help=(
            "Path to the dataset directory that holds folders/subfolders"
            " containing samples."
        ),
    )

    args = parser.parse_args()

    generate_directory_list(args.name, args.dataset)
