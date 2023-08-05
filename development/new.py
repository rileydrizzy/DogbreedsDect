import os


def list_files_in_directory(directory_path):
    try:
        # Get a list of files and directories in the specified path
        files_and_directories = os.listdir(directory_path)

        # Filter out only the files from the list
        files_list = [
            file
            for file in files_and_directories
            if os.path.isfile(os.path.join(directory_path, file))
        ]

        return files_list

    except FileNotFoundError:
        print(f"Directory not found: {directory_path}")
        return []
    except Exception as e:
        print(f"Error while listing files: {e}")
        return []


# Example usage:
if __name__ == "__main__":
    directory_path = (
        "data/raw/stanford-dogs-dataset/annotations/Annotation/n02110958-pug"
    )
    if os.path.exists(directory_path):
        files_list = list_files_in_directory(directory_path)
        if files_list:
            print("Files in the directory:")
            for file in files_list:
                print(file)
        else:
            print("No files found in the directory.")
    else:
        print("Directory not found.")
