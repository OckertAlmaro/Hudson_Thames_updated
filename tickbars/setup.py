from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='tickbars',
    version='0.3',
    author='Ockert Almaro de Villiers',
    author_email='almarodevilliers@gmail.com',
    description='A Python module for processing historical tick data and calculating bars',
    long_description=long_description,
    long_description_content_type="text/markdown",  # Indicate that it's Markdown
    url='https://github.com/OckertAlmaro/Hudson_Thames_updated',
    packages=find_packages(),
    install_requires=[
        'numpy', 'pandas', 'datetime', 'timedelta', 'math'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
