from setuptools import setup, find_packages

setup(
    name='tone_generation',
    version='0.1.1',
    url='https://github.com/tomasderner97/tone_generation.git',
    author='Tomáš Derner',
    packages=['tone_generation'],
    include_package_data=True,
    install_requires=[
        'numpy', 'sounddevice', "IPython"
    ],
)
