from setuptools import setup, find_packages


setup(
    include_package_data=True,
    name='pymikro',
    version='0.15',
    description='API to control the Maschine Mikro MK3',
    url='https://github.com/flokapi/pymikro',
    author='flokapi',
    author_email='flokapi@pm.me',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    package_data={"pymikro": ["*.json", "*.ttf"]},
    install_requires=['hid', 'pillow'],
    license='LGPLv2',
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)