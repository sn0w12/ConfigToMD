from setuptools import setup, find_packages

setup(
    name="configtomd",
    version="0.1.0",
    description="Extract config settings from Python files and generate markdown documentation",
    author="Sn0w12",
    packages=find_packages(),
    py_modules=["scan"],
    entry_points={
        "console_scripts": [
            "configtomd=scan:main",
        ],
    },
    python_requires=">=3.6",
)
