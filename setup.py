from setuptools import setup, find_packages

setup(
    name="seq2hla",
    author="Anna M. Diaz-Rovira",
    author_email="annadiarov@gmail.com",
    description=("Python package to get HLA alleles from protein sequences"),
    keywords="HLA, alleles, protein, sequences",
    url="https://github.com/annadiarov/seq2HLAallele",
    packages=find_packages(exclude=('tests', 'docs')),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
