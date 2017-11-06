import os


class PicLocalStore:
    """PicLocalStore provides storage access to local filesystem.

        Attributes:
            root (str): The default filesystem root, which is relative to the project path.
            file_path (str): The joined full path from root and input filename.
            data (bytes): The file data.
    """
    root = 'images'
    
    def __init__(self, filename, data):
        """Init.

        Args:
            filename (str): The filepath including the filename.
            data (bytes): The file data.
        """
        self.file_path = os.path.join(self.root, filename)
        self.data = data

    def save(self):
        """Save file.

        This method saves the data to the file_path.

        Returns:
            (str): The constructed full path including root and filepath.
            (bool): True for success, False otherwise.
        """
        if not os.path.exists(os.path.dirname(self.file_path)):
            os.makedirs(os.path.dirname(self.file_path))
        try:
            with open(self.file_path, 'wb') as file:
                file.write(self.data)
        except IOError:
            return '', False
        return self.file_path, True

    def get(self):
        """Get file.

        This method gets the data from the file_path.

        Returns:
            (bytes): Actual file data in binary.
            (bool): True for success, False otherwise.
        """
        try:
            with open(self.file_path, 'rb') as file:
                self.data = file.read()
        except IOError:
            return None, False
        return self.data, True
