import os


def create_directories_for_path(path):
    """Create directory tree along a path, if necessary.

    Parameters
    ----------
    path: str
        For which we create the directory tree.

    """
    dir_path = os.path.abspath(os.path.dirname(path))
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
