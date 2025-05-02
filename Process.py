
import os
import tarfile
import zipfile


class FileProcessor:
    def __init__(self):
        self.file_path = None
        self.supported_extensions = [".txt", ".zip", ".tar.gz"]

    def set_file_path(self, file_path):
        """Set the file path for processing."""
        self.file_path = file_path

    def is_valid_file(self):
        """Check if the file path is valid and the file exists."""
        if not self.file_path:
            return False
        return os.path.isfile(self.file_path)

    def get_file_extension(self):
        """Get the file extension, handing .tar.gz."""
        if not self.is_valid_file():
            return None

        base, ext = os.path.splitext(self.file_path)
        # Check for compound extensions like .tar.gz
        if ext == '.gz' and base.endswith('.tar'):
            return '.tar.gz'
        return ext.lower()

    def get_file_name(self):
        """Get the file name from the path."""
        if not self.is_valid_file():
            return None
        return os.path.basename(self.file_path)

    def process_file(self):
        """Process the selected file based on its type."""
        if not self.is_valid_file():
            return "Error: Invalid or non-existent file path."

        file_extension = self.get_file_extension()
        print(file_extension)
        if file_extension in self.supported_extensions:
            try:
                match file_extension:
                    case '.txt':
                        with open(self.file_path, 'r') as file:
                            content = file.read()
                            return f"Text file processed.: {len(content)} "
                    case '.tar.gz':
                        print("condition met")
                        with tarfile.open(self.file_path, 'r:gz') as tar:
                            file_list = tar.getnames()
                            return f"TAR.GZ file count files: {len(file_list)}"
                    case '.zip':
                        with zipfile.ZipFile(self.file_path, 'r') as zip_file:
                            file_list = zip_file.namelist()
                            return f"ZIP file  count files: {len(file_list)}"
                    case _:
                        return f"Unsupported file type: {file_extension}"
            except Exception as e:
                return f"Error processing {file_extension} file: {str(e)}"
        else:
            print("File not in supported extensions")

    def save_file(self, content):
        """Save content to the file path."""
        if not self.file_path:
            return "Error: No file path specified."

        try:
            with open(self.file_path, 'w') as file:
                file.write(content)
            return f"File saved successfully: {self.file_path}"
        except Exception as e:
            return f"Error saving file: {str(e)}"
