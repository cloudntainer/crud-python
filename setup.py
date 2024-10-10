from setuptools import setup, find_packages

setup(
    name='my-python-project',
    version='0.1.0',
    packages=find_packages(exclude=['tests', 'docs']),
    install_requires=[
    ],
    python_requires='>=3.12',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    package_data={
        '': ['*.txt', '*.md'],
    },
)
