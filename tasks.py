"""
Setup tasks (requires invoke: pip install invoke)
"""
from invoke import task
import platform


@task
def setup(c, version=None):
    """
    Setup dev environment, requires conda
    """
    version = version or "3.10"
    suffix = "" if version == "3.10" else version.replace(".", "")
    env_name = f"sk-eval{suffix}"

    c.run(f"conda create --name {env_name} python={version} --yes")
    if platform.system() == "Windows":
        conda_hook = "conda shell.bash hook "
    else:
        conda_hook = 'eval "$(conda shell.bash hook)" '
    c.run(
        f"{conda_hook} && conda activate {env_name} && pip install --editable .[dev]"
        "&& pip install invoke lxml"
    )  # lxml needed for NotebookCollection.py example

    print(f"Done! Activate your environment with:\nconda activate {env_name}")


@task(aliases=["d"])
def doc(c, strict=False):
    """Build docs"""
    flags = "--warningiserror --keep-going" if strict else ""
    c.run(f"jupyter-book build docs/ {flags}")


@task(aliases=["v"])
def version(c):
    """Create a new version"""
    from pkgmt import versioneer

    versioneer.version(project_root=".", tag=True)


@task(aliases=["r"])
def release(c, tag, production=True):
    """Upload to PyPI"""
    from pkgmt import versioneer

    versioneer.upload(tag, production=production)
