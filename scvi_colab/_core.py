import subprocess
import sys
from typing import Optional


def install(branch: Optional[str] = None, run_outside_colab: bool = False):

    if not run_outside_colab:
        IN_COLAB = "google.colab" in sys.modules
        if not IN_COLAB:
            raise ValueError(
                """
                Not currently in Google Colab environment.\n
                Please run with `run_outside_colab=True` to override.
                """
            )

    # temporary as pytorch 1.11 not in google colab
    # TODO: remove once pytorch 1.11 in colab with gpu
    _run_command("pip install pyro-ppl==1.8.0")

    _run_command("pip install pynndescent")

    if branch is None:
        command = "pip install --quiet 'scvi-tools[tutorials]'"
    else:
        _run_command("pip install --quiet --upgrade jsonschema")
        repo = (
            f"https://github.com/scverse/scvi-tools@{branch}#egg=scvi-tools[tutorials]"
        )
        command = f"pip install --quiet git+{repo}"
    _run_command(command)

    # caching issues in colab causing pynndescent import to fail
    success = False
    while not success:
        try:
            import pynndescent  # noqa: F401

            success = True
        except:  # noqa: E722
            success = False


def _run_command(command: str):

    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
