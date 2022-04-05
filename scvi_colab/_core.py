import logging
import subprocess
import sys
from typing import Optional
from warnings import warn

logger = logging.getLogger(__name__)


def install(
    version: Optional[str] = None,
    branch: Optional[str] = None,
    run_outside_colab: bool = False,
    unfixed: bool = False,
) -> None:
    """
    Install scvi-tools in Google Colab.

    By default this installs the latest release of scvi-tools.

    Parameters
    ----------
    version
        The version to use to install from PyPI. Defaults to latest
        version.
    branch
        The GitHub branch to use to install directly from GitHub.
        Defaults to official installation. When not None, uses that
        branch.
    run_outside_colab
        Override to run install function outside of Google Colab.
    unfixed
        Only run the scvi-tools installation part and bypass specific
        fixes that are pinned in this function.
    """

    if not run_outside_colab:
        IN_COLAB = "google.colab" in sys.modules
        if not IN_COLAB:
            warn(
                """
                Not currently in Google Colab environment.\n
                Please run with `run_outside_colab=True` to override.\n
                Returning with no further action.
                """
            )

    if branch is not None and version is not None:
        raise ValueError("One of branch or version must be None.")

    logger.info("Installing scvi-tools.")

    if unfixed:
        _run_command("pip install pynndescent")
        # caching issues in colab causing pynndescent import to fail
        success = False
        while not success:
            try:
                import pynndescent  # noqa: F401

                success = True
            except:  # noqa: E722
                success = False

    if branch is None:
        command = "pip install --quiet scvi-tools[tutorials]"
        if version is not None:
            command += f"=={version}"
    else:
        _run_command("pip install --quiet --upgrade jsonschema")
        repo = (
            f"https://github.com/scverse/scvi-tools@{branch}#egg=scvi-tools[tutorials]"
        )
        command = f"pip install --quiet git+{repo}"
    _run_command(command)

    if unfixed:
        _run_command("pip install --upgrade rich==10.0.0")

    logger.info("Install successful. Testing import.")

    import scvi  # noqa: F401


def _run_command(command: str):

    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
