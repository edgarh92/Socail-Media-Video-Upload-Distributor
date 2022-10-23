
import os

ACCEPTED_FORMATS = ('.avi', '.mp4', '.mp3', '.mxf', '.mov', '.wav', '.aif')


def build_file_list(source_path: str):
    file_list = []
    for files in source_path:
        if os.path.isdir(files):
            path_files = sorted(os.listdir(files))
            for file in path_files:
                if file.lower().endswith(ACCEPTED_FORMATS):
                    file_list.append(os.path.join(files, file))
        elif files.lower().endswith(ACCEPTED_FORMATS):
            file_list.append(os.path.abspath(files))

    return file_list
