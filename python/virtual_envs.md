Virtualenv :
- Unix & mac : $VIRTUAL_ENV/pip.conf
- Windows : %VIRTUAL_ENV%\pip.ini

uv :
- install with curl, must not be linked to a python env
- init : `uv init --build-backend=pdm -p=3.11 --name=project_name`

Pyenv :
- Install pyenv and pyenv-virtualenv
- Afficher les version de python que l'on peut installer : pyenv install -l
- Installer une version de python : pyenv install 3.6.1
- Creer un virtual env : pyenv virtualenv 3.6.1 virtual_env_name_3.6.1
- Activation : pyenv local virtual_env_name_3.6.1
- Activation auto du virtualenv : ajouter dans le .bashrc :
    if which pyenv > /dev/null; then eval "$(pyenv init -)"; fi
    if which pyenv-virtualenv-init > /dev/null; then eval "$(pyenv virtualenv-init -)"; fi

Anaconda :
- Update Anaconda : `conda update conda`
- Virtualenv :
  - Create : `conda create -n envname python=x.x pip` 
  - Activate : `conda activate envname` | `conda deactivate`
  - Delete : `conda remove -n envname -all`
- Install package / export package list : 
  - `conda install [-n envname] package`
  - `conda install --file requirements.txt`
  - `conda list --export > requirements.txt`
