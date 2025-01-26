from __future__ import annotations

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
    for_tutorials: bool = True,
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
    for_tutorials
        Whether to install scvi-tools[tutorials] which consist of many
        more packages to install and thus will add time.
    unfixed
        Only run the scvi-tools installation part and bypass specific
        fixes that are pinned in this function.
    """
    from pkg_resources import ContextualVersionConflict

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
            return

    if branch is not None and version is not None:
        raise ValueError("One of branch or version must be None.")

    pip_command = "uv pip install --system "
    try:
        subprocess.call(["uv", "--version"])
    except FileNotFoundError:
        logger.debug("uv not installed, fallback to pip")
        pip_command = "pip install "

    logger.info("Installing scvi-tools.")

    if not unfixed:
        _run_command(pip_command + "scanpy")
        _run_command(pip_command + "pynndescent")
        # caching issues in colab causing pynndescent import to fail
        success = False
        while not success:
            try:
                import pynndescent  # noqa: F401

                success = True
            except:  # noqa: E722
                success = False

    if branch is None:
        if for_tutorials:
            command = pip_command + "--quiet scvi-tools[tutorials]"
        else:
            command = pip_command + "--quiet scvi-tools"
        if version is not None:
            command += f"=={version}"
    else:
        if for_tutorials:
            repo = f"https://github.com/scverse/scvi-tools@{branch}#egg=scvi-tools[tutorials]"
        else:
            repo = f"https://github.com/scverse/scvi-tools@{branch}#egg=scvi-tools"
        command = pip_command + f"--quiet git+{repo}"
    _run_command(command)

    logger.info("Install successful. Testing import.")

    try:
        import scvi  # noqa: F401
    except ContextualVersionConflict:
        logger.warning(
            "Import unsuccessful. Try restarting (not resetting) the session and running again."
        )


def _run_command(command: str):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
