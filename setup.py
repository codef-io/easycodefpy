import ast
from setuptools import setup, find_packages


def get_metadata(resource):
    filename = 'easycodefpy/__init__.py'
    with open(filename, 'r') as f:
        tree = ast.parse(f.read(), filename)
    for node in tree.body:
        if (isinstance(node, ast.Assign) and
                node.targets[0].id == resource):
            return ast.literal_eval(node.value)

    raise ValueError(f'could not find {resource}')


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()


with open('requirements.txt') as f:
    requires = f.read().strip().split('\n')

setup(
    name=get_metadata('__title__'),
    version=get_metadata('__version__'),
    author=get_metadata('__author__'),
    author_email='codef.io.dev@gmail.com',
    description='Easily develop codef api',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/codef-io/easycodefpy.git',
    packages=find_packages(exclude=['cmd']),
    keywords=[
        'easycodef',
        'codef',
        'codef-api',
        'codef-py',
        'codef-python'
    ],
    python_requires='>=3',
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    install_requires=requires
)