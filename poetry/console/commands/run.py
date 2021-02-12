from typing import Any
from typing import Union

from cleo import argument

from .env_command import EnvCommand


class RunCommand(EnvCommand):

    name = "run"
    description = "Runs a command in the appropriate environment."

    arguments = [
        argument("args", "The command and arguments/options to run.", multiple=True)
    ]

    def __init__(self):  # type: () -> None
        from poetry.console.args.run_args_parser import RunArgsParser

        super().__init__()

        self.config.set_args_parser(RunArgsParser())

    def handle(self):  # type: () -> Any
        args = self.argument("args")
        script = args[0]
        scripts = self.poetry.local_config.get("scripts")

        if scripts and script in scripts:
            return self.run_script(scripts[script], args)

        return self.env.execute(*args)

    def run_script(self, script, args):  # type: (Union[str, dict], str) -> Any
        if isinstance(script, dict):
            script = script["callable"]

        module, callable_ = script.split(":")

        src_in_sys_path = "sys.path.append('src'); " if self._module.is_in_src() else ""

        cmd = ["python", "-c"]

        cmd += [
            "import sys; "
            "from importlib import import_module; "
            "sys.argv = {!r}; {}"
            "import_module('{}').{}()".format(args, src_in_sys_path, module, callable_)
        ]

        return self.env.execute(*cmd)
