
from setuptools import find_packages
from distutils.core import setup
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
  name = 'banking',         # How you named your package folder (MyLib)
  packages = find_packages(exclude=['tests']),   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Hype API',  
  long_description=README,
  long_description_content_type="text/markdown",
  author = 'Jacopo Jannone',                   # Type in your name
  keywords = ['HYPE API'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'lxml',
          'requests',
          'click'
      ],
  classifiers=[
    'Development Status :: 5 - 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9'
  ],
  entry_points='''
        [console_scripts]
        hype=banking.scripts.hype:hype
        timpay=banking.scripts.timpay:timpay
    ''',
)