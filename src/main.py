def check_file_type(file_path):
    if os.path.isfile(file_path):
        return "Regular File"
    elif os.path.isdir(file_path):
        return "Directory"
    elif os.path.islink(file_path):
        return "Symbolic Link"
    else:
        return "Other"
