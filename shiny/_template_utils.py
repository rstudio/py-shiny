import os
import shutil
import sys
from pathlib import Path
from typing import Optional

import questionary
from questionary import Choice

from ._custom_component_template_questions import (
    ComponentNameValidator,
    install_js_dependencies,
    updateComponentNameInTemplate,
)

styles_for_questions = questionary.Style(
    [
        (
            "secondary",
            "italic",
        ),
    ]
)
# Prebuild some common choices
cancel_choice = Choice(title=[("class:secondary", "[Cancel]")], value="cancel")
back_choice = Choice(title=[("class:secondary", "← Back")], value="back")


def template_query(question_state: Optional[str] = None):
    """
    This will initiate a CLI query which will ask the user which template they would like.
    If called without arguments this function will start from the top level and ask which
    type of template the user would like.

    You can also specify a question state to return to another level. For example if you
    were at level 5 of a question chain and wanted to return to level 4.
    This is not that useful currently because we only have two levels of questions.


    :param question_state: The question state you would like to return to. Currently, the options are:
        "cancel": Cancel the operation and exit.
        "js-component": Start the questions for creating a custom JavaScript component.
    """

    if question_state is None:
        template = questionary.select(
            "Which template would you like to use?:",
            choices=[
                Choice(title="Basic App", value="basic-app"),
                Choice(title="Express app", value="express"),
                Choice(title="Dashboard", value="dashboard"),
                Choice(title="Multi-page app with modules", value="multi-page"),
                Choice(title="Custom JavaScript Component", value="js-component"),
                cancel_choice,
            ],
            style=styles_for_questions,
        ).ask()
    else:
        template = question_state

    # Define the control flow for the top level menu
    if template is None or template == "cancel":
        sys.exit(1)
    elif template == "js-component":
        jsComponentQuestions()
        return
    else:
        appTemplateQuestions(template)


def appTemplateQuestions(template: str):
    appdir = questionary.path(
        "Enter destination directory:",
        default=buildPathString(),
        only_directories=True,
    ).ask()

    app_dir = copyTemplateFiles(appdir, template)
    print(f"Created Shiny app at {app_dir}")


def jsComponentQuestions():
    """
    Hand question branch for the custom js templates. This should handle the entire rest
    of the question flow and is responsible for placing files etc. Currently it repeats
    a lot of logic from the default flow but as the custom templates get more
    complicated the logic will diverge
    """

    component_type = questionary.select(
        "What kind of component do you want to build?:",
        choices=[
            Choice(title="Input component", value="js-input"),
            Choice(title="Output component", value="js-output"),
            Choice(title="React component", value="js-react"),
            back_choice,
            cancel_choice,
        ],
        style=styles_for_questions,
    ).ask()

    if component_type == "back":
        template_query()
        return

    if component_type is None:
        sys.exit(1)

    # As what the user wants the name of their component to be
    component_name = questionary.text(
        "What do you want to name your component?",
        instruction="Name must be dash-delimited and all lowercase. E.g. 'my-component-name'",
        validate=ComponentNameValidator,
    ).ask()

    if component_name is None:
        sys.exit(1)

    appdir = questionary.path(
        "Enter destination directory:",
        default=buildPathString(component_name),
        only_directories=True,
    ).ask()

    if appdir is None:
        sys.exit(1)

    app_dir = copyTemplateFiles(appdir, component_type)

    # Print messsage saying we're building the component
    print(f"Setting up {component_name} component package...")
    updateComponentNameInTemplate(app_dir, component_name)

    shouldInstallDeps = questionary.confirm(
        "Do you want to install js dependencies now?"
    ).ask()

    if shouldInstallDeps:
        install_js_dependencies(app_dir)
    else:
        print("Skipping installing NPM deps. Run `npm install` to install them later.")

    print(f"Successfully created {component_name} component package!")
    print("Next steps:")
    print(f"- Run `cd {app_dir}` to change into the new directory")
    if not shouldInstallDeps:
        print("- Run `npm install` to install dependencies")
    print("- Run `npm run build` to build the component")
    print("- Install package locally with `pip install -e .`")
    print("- Open and run the example app in the `example-app` directory")


def buildPathString(*path: str):
    """
    Build a path string that is valid for the current OS
    """
    # If no args are provided we should add an empty path to the list
    # so that the result is properly formed. E.g. "./" on Unix systems
    prefix = f".{os.path.sep}"
    if len(path) == 0:
        return prefix
    return f"{prefix}{str(Path(*path))}"


def copyTemplateFiles(dest: str, template: str):
    if dest == ".":
        dest = buildPathString(template)

    app_dir = Path(dest)
    template_dir = Path(__file__).parent / "templates" / template
    duplicate_files = [
        file.name for file in template_dir.iterdir() if (app_dir / file.name).exists()
    ]

    if any(duplicate_files):
        err_files = ", ".join(['"' + file + '"' for file in duplicate_files])
        print(
            f"Error: Can't create new files because the following files already exist in the destination directory: {err_files}"
        )
        sys.exit(1)

    if not app_dir.exists():
        app_dir.mkdir()

    for item in template_dir.iterdir():
        if item.is_file():
            shutil.copy(item, app_dir / item.name)
        else:
            shutil.copytree(item, app_dir / item.name)

    return app_dir
