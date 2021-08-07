import setuptools

setuptools.setup(
    name="google-drive-tool",
    version="0.0.1",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        "coverage==5.5",
        "pytest==6.2.4",
        "pytest-cov==2.11.1"
    ]
)
