import os.path
import sys

class PyEnv(object):
    """
    Represents a python environment.
    An environment consists of a python interpeter, python library paths and utilities such as `pip`.
    Currenty we are only concerned about the paths were we find the interpeter and the utilities.
    """

    def __init__(self, search_paths):
        """
        Manually configure an enviroment.
        You might want to consider using the factory methods provided in this module.
        """
        self.search_paths = search_paths
        self.extensions = ['', 'w.exe' ,'.exe']

    def find_executable(name):
        """
        Finds an executable with the given name in this enviroment.
        
        :returns: Absolute path to the executable.

        :raises ValueError: if the exectuable could not be found.
        """
        candidate_names = [name + ext for ext in self.extensions]
        candidates = [os.path.join(path, name) for path in self.search_paths for name in candidate_names]
   
        match = None
        for candidate in candidates:
            if os.path.exists(candidate):
                match = candidate
                break
        else:
            raise ValueError("Unable to find {name}. Looked at {candidates}".format(
                name=repr(name),
                candidates=", ".join(candidates)
            ))


def interpeter_pyenv():
    """
    Returns the environment in which this script is running.
    """
    if not sys.executable:
        raise ValueError("Interpeter that runs this script cannot be identified.")
    return pyenv_from_interpreter(sys.executable)


def pyenv_from_interpreter(exe):
    """
    Attempts to construct the environment for a given python interpeter by guessing
    where the paths are relative to it.
 
    :param exe: Path to the python interpeter executable.
 
    :returns: Instance of :class:`PyEnv`
    """
    exeabs = os.path.abspath(interpreter)
    if not os.path.exists(exeabs):
        raise ValueError("Python interpreter {exe} does not exist here {exeabs}.".format(exe=exe, exeabs=exeabs))
    
    path = os.path.dirname(interpreter)
    return _pyenv_from_paths(path, ["Scripts", "scripts"])


def pyenv_from_virtualenv(path):
    """
    Attempts to construct the environment from the directory created by `virtualenv`.
    
    :param path: Directory containing the virtualenv.

    :returns: Instance of :class:`PyEnv`
    """
    return _pyenv_from_paths(path, ["bin"])    


def _pyenv_from_paths(path, subdirs):
    """
    Helper method to construct an environment.

    :param path: Base path of the environment.

    :param subdirs: Directory names that might contain the interpeter and utilities.

    :returns: Instance of :class:`PyEnv`
    """
    paths = [path] + [os.path.join(path, subdir) for subdir in subdirs]
    search_paths = []
    for path in paths:
        if os.isdir(path): 
            search_paths.append(path)
    if not search_paths:
        raise ValueError("Python environment not found. None of the directories exists {dirs}".format(
            dirs=", ".join(paths)))
    return PyEnv(search_paths)



