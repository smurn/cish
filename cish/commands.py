import os.path
import shutil

def mkdirs(path):
    """
    Creates the given directory, creating parent directories if required.
    Has no effect if the directory already exists, throws an exception
    if the path exists but is not a directory.
    """
    path = os.path.abspath(path)
    if os.path.isdir(path):
        return
    elif os.path.exists(path):
        raise ValueError("Cannot create directory {path} it already exists " +
             "but is not a directory.".format(path=path))
    else:
        os.makedirs(path)

def rm(path):
    """
    Deletes the given file or directory, including the content.
    Has no effect if the path does not exist.
    """
    path = os.path.abspath(path)
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.exists(path):
        os.remove(path)


