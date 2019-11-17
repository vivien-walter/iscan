from setuptools import setup

setup(
    name="iSCAN",
    version="0.1",
    description="Analyse iSCAT pictures",
    author="Vivien WALTER",
    author_email="walter.vivien@gmail.com",
    license="MIT",
    packages=["iscan"],
    include_package_data=True,
    install_requires=[
        "numpy", "Pillow", "PyQt5", "pims", "scipy", "matplotlib", 'seaborn'
    ],
    entry_points = {
        'console_scripts': ['iscan=iscan:startYU']
    }
)
