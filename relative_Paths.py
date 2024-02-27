# -------------------------------------------------#
#This function return the absolute paths of all the files
#For the GUI

import os
import json

class Path():

    def __init__(self, subdirectory, filename):

        self.subdir = subdirectory
        self.filename = filename
        self.current_directory = os.path.dirname(os.path.abspath(__file__))

    def get_relative_path(self):
        # Get the current directory
        # Construct the relative path
        relative_path = os.path.join(self.current_directory, self.subdir, self.filename)
        return relative_path

    def get_relative_path_test(*args):
        """
        Este método recibe una cantidad variable de argumentos que representan niveles de directorios y devuelve un 
        string con la ruta relativa.
        """
        return os.path.join(*args)
                
if __name__ == '__main__':
    path = Path ('iconos','Phistank.png')
    print(path.get_relative_path())       

    

    