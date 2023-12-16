import setuptools
setuptools.setup(
    name='codecraft',
    version='1.0',
    entry_points = {
        'console_scripts': ['codecraft=codecraft.codecraft:start'],
    },
    author='Federico Barbato',
    description='CodeCraft: A robust C++ project management tool designed for building of C++ projects',
    long_description_content_type = 'text/markdown',
    long_description="Features include automated file structure generation, seamless integration with CMake, and easy management of external libraries.",
    install_requires=[
        'beautifulsoup4==4.12.2',
        'click==8.1.7',
        'colorama==0.4.6',
        'lxml==4.9.3',
        'markdown-it-py==3.0.0',
        'mdurl==0.1.2',
        'Pygments==2.17.2',
        'rich==13.7.0',
        'shellingham==1.5.4',
        'soupsieve==2.5',
        'typer==0.9.0',
        'typing_extensions==4.9.0'
    ],
    python_requires='>=3.0'
)
