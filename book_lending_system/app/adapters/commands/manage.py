import importlib
import os
import sys
import click

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))
SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "cli_tools")


@click.group()
def cli():
    pass


for file in os.listdir(SCRIPTS_DIR):
    if file.endswith(".py") and not file.startswith("_"):
        module_name = file[:-3]
        module_path = f"app.adapters.commands.cli_tools.{module_name}"
        module = importlib.import_module(module_path)

        if hasattr(module, "main"):
            cli.command(name=module_name)(module.main)


if __name__ == "__main__":
    cli()
