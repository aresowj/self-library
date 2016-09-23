import zipfile
import os

def _unzip_and_delete(self, file_path, target_folder=None):
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return False
        
    target_folder = target_folder if target_folder is not None else os.path.dirname(file_path)
    
    with zipfile.ZipFile(file_path) as zip_file:
        zip_file.extractall(path=target_folder)
        
    # remove the zip file after extraction.
    os.remove(file_path)
    
    return True
