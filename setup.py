from setuptools import setup, find_packages

setup(name='client',
      version='0.1',
      description='Know Your Client Tools From News Sources',
      url='http://github.com/tcausero/Capstone_KYC',
      author='Jesse Cahill, Thomas Causero, James DeAntonis, Ryan McNally',
      author_email='jcahill225@gmail.com, tc3030@columbia.edu, jad2295@columbia.edu, rom2109@columbia.edu',
      license='MIT',
      packages=find_packages(),
      python_requires='>=3.5, <3.7',
      install_requires=[
            'pandas',
            'matplotlib',
            'python-dotenv',
            'pytrends',
            'geopandas',
            'colour',
            'numpy',
            'click',
            'bs4',
            'plotly',
	    'pyLDAvis',
	    'gensim',
	    'pickle',
	    'spacy',
	    'nltk'
      ],
      zip_safe=False)
