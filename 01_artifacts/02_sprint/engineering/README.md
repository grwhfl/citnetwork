Once a collaborator pulls down your project - they can then install a fresh python environment:

'python3 -m venv local_python_environment'

And then activate that environment and install from your requirements.txt which you have included in your version control:

$ source local_python_environment/bin/activate

(local_python_environment) $ pip install -r requirements.txt
