from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Database to manage media'
LONG_DESCRIPTION = ""

setup(name="mediaDB",
      version=VERSION,
      author="Benjamin Roget",
      author_email="benjamin.rogetpro@gmail.com",
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      packages=find_packages(),
      install_requires=[],
      keywords=["python", "media", "manage"],
      classifiers= [
            "Development Status :: 1 - Planning",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: POSIX :: Linux ",
            "Framework :: Flask ",
            "License :: Free For Home Use "
        ])