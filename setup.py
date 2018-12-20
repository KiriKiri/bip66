import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='bip66',  
     packages=['bip66', 'test'],
     version='0.4',
     author="Kirill Kirikov",
     author_email="kk@4irelabs.com",
     description="Strict DER signature encoding/decoding.",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/KiriKiri/bip66",
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ]
 )

