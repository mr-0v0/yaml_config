from setuptools import setup

setup(
    name='yaml_config',
    version='1.0',
    description='This module can read a YAML file and replace any value starting with "$" with the corresponding environment variable. You can use this to create a configuration file that requires multiple environment variables, such as secrets, API keys, passwords, etc. When saving back to the configuration, it will read the existing config file and compare the new configu file, repace the value of new config file with coreponding variables in existing config.',
    packages=['yaml_config'],
    install_requires=['pyyaml',],
)