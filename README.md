# Getting started

```bash
python3 --version # check version
pip --version # check installer version

sudo apt-get install python3-venv

python3 -m venv ./python-project

source ./python-project/bin/activate # activates virtual environment to prevent install on global python system wide.

pip install "fastapi[standard]"

touch main.py # paste some example code.*

# made static directory - Ill use this for css and js code I write myself.

# templates directory (I'll use jinja2 for returning html templates )
pip install jinja2

# I want to run and test with uvicorn since it can rebuild really fast as I develop and test stuff.
uvicorn main:app --reload

# or I can let vscode handle this so I can just click a button

#paste in .vscode/launch.json
{
  // Use IntelliSense to learn about possible attributes.
  // Hover to view descriptions of existing attributes.
  // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python Debugger: FastAPI",
      "type": "debugpy",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "main:app",
        "--reload"
      ],
      "jinja": true
    }
  ]
}
```
