# Copyright (c) 2014, Stefan C. Mueller
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

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
        self.exec_patterns = ['{name}' ,'{name}.exe']
        self.python_patterns = ['{name}', 'w{name}.exe' ,'{name}.exe']

    def find_executable(self, name):
        """
        Finds an executable with the given name in this enviroment.
        
        :returns: Absolute path to the executable.

        :raises ValueError: if the exectuable could not be found.
        """
        
        patterns = self.python_patterns if name == "python" else self.exec_patterns
        candidate_names = [ext.format(name=name) for ext in patterns]
        candidates = [os.path.join(path, name) for path in self.search_paths for name in candidate_names]
   
        for candidate in candidates:
            if os.path.exists(candidate):
                return candidate
            
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
    exeabs = os.path.abspath(exe)
    if not os.path.exists(exeabs):
        raise ValueError("Python interpreter {exe} does not exist here {exeabs}.".format(exe=exe, exeabs=exeabs))
    
    path = os.path.dirname(exeabs)
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
        if os.path.isdir(path): 
            search_paths.append(path)
    if not search_paths:
        raise ValueError("Python environment not found. None of the directories exists {dirs}".format(
            dirs=", ".join(paths)))
    return PyEnv(search_paths)



