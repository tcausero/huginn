from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='huginn',
      version='0.1.2',
      description='Tools to Detect Anomalous Events and News Related to Entities',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/tcausero/huginn',
      author='Jesse Cahill, Thomas Causero, James DeAntonis, Ryan McNally',
      author_email='jcahill225@gmail.com, tc3030@columbia.edu, jad2295@columbia.edu, rom2109@columbia.edu',
      license='MIT',
      packages=find_packages(exclude=('tests',)),
      include_package_data=True,
      python_requires='>=3.5, <3.7',
      install_requires=[
            'pandas',
            'matplotlib',
            'pytrends',
            'geopandas',
            'scikit-learn',
            'colour',
            'numpy',
            'click',
            'bs4',
            'plotly',
            'pyLDAvis',
            'gensim',
            'tokenizer',
            'spacy',
            'nltk',
            'torch',
            'transformers'
       ],
      zip_safe=False)
