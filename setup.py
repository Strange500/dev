from setuptools import setup, find_packages

VERSION = '0.0.4'
DESCRIPTION = 'Database to manage media'
LONG_DESCRIPTION = "Ensure your media are here, no double, detect missing media, and can accept any metadata providers, sources"

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
