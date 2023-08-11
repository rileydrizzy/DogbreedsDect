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
