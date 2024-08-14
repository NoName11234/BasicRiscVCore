[![Python application](https://github.com/NoName11234/BasicRiscVCore/actions/workflows/python-app.yml/badge.svg?branch=development)](https://github.com/NoName11234/BasicRiscVCore/actions/workflows/python-app.yml)

# Build instructions
Follow the tutorial below to build this project.
Currently only Ubuntu is supported.
If you use Windows, you should be able to use WSL as well.
## Ubuntu Guide

### Installation of Icarus Verilog
You can install Icarus Verilog via the command below directly with apt.
```
apt install iverilog
```
The following command needs to be executed in order to compile the verilog files.
```
iverilog -g2012 PathsToVerilogFiles -o NameOfOutputFile
```
### Installation of Python debug environment
First install the python, pip and virtualenv packages via apt.
```
apt install python3 python3-pip virtualenv
```
Change your directory to the cloned repository. 
Run the following command to create a new python environment in the repository.
> [!NOTE]
> The created directory is already excluded by the provided gitignore file.
```
python3 -m venv .venv
```
Activate the created environment by entering the following command.
> [!NOTE]
> Activation of the environemt always needs to be done before trying to execute test files of the project.
```
source .venv/bin/activate
```
Install the needed python packages, which are provided in `requirements.txt` via pip.
```
python3 -m pip install -r requirements.txt
```
Run the provided tests by executing pytest.
```
pytest
```