import os

def read_repository_files(repo_path):
    """
    Reads all files in the given repository path and returns an array with details for each file.

    :param repo_path: Path to the root directory of the repository
    :return: Array of dictionaries with file path, extension, and text content
    """
    files_data = []

    def read_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    for root, dirs, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1]
            name = os.path.splitext(file)[0]
            if(file_extension == '.js' or file_extension == '.tsx'):
                try:
                    content = read_file(file_path)
                    files_data.append({
                        'path': file_path,
                        'extension': file_extension,
                        'content': content,
                        'name': name
                    })
                except UnicodeDecodeError:
                    print(f"Skipping binary or non-text file: {file_path}")
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
    return files_data
