from setuptools import setup

file_name = "flake8_forbid_visual_indent.py"


def get_version() -> str:
    with open(file_name) as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[-1].replace('"', "").strip()
        else:
            raise ValueError("Version not found")


setup(version=get_version())
