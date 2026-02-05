import zipfile
import os

def unpack_dataset(zip_path, dest_dir):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(dest_dir)
    # Проверка прав доступа
    os.chmod(dest_dir, 0o755)
    for root, dirs, files in os.walk(dest_dir):
        for file in files:
            os.chmod(os.path.join(root, file), 0o644)
unpack_dataset('yolo.zip','datasets')