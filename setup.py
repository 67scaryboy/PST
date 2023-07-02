
from cx_Freeze import setup, Executable

#Pour compiler le projet, se rendre à l'endroit de ce fichier dans le cmd et tapper: python setup.py build

# Détails du gel
options = {
    'build_exe': {
        'packages': ['pygame'],
        'excludes': ['tkinter'],
        'include_files': ['sprites_paralax/','sprites_menu/','sprites_boss/','sprites_animation/','sprites/','sons/','Editeur.txt','SpaceCrusade.ico']
    }
}

# Création de l'exécutable
executables = [
    Executable('main.py', base=None, icon="SpaceCrusade.ico", targetName='SpaceCrusade')
    
    
]

setup(name='SpaceCrusade',
      version='1.0',
      description='Jeu SpaceCrusade',
      options=options,
      executables=executables)
