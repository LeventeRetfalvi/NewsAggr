# NewsAggr

## After installing VS Code and Python the following VS Code extensions should be installed

-   python
-   Python Indent
-   Gitlens
-   Ruff

The python related settings are in the `.vscode/settings.json` file that can be updated as per needed so everyone should have the same python-related VS code settings


## Before first run
- Install Pipenv (to use seapreted dependencies for our code)

```
- py -m pip install --user pipenv
```


- Copy the .env.template to .env and customize it according to your needs.

- Run the test data downloader

```
- pipenv run download_test_data.py
```

### Optional: Setting up Python interpreter in Visual Studio Code

- Ctrl+Shift+P -> select `"Python: Select Interpreter"`
- Optional: If you want the integrated terminal in VS Code to automatically activate your Pipenv environment, you can set the `python.terminal.activateEnvironment` setting to true in your workspace settings (`.vscode/settings.json`).   