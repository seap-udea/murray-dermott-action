Python packages: creation and management
========================================

This is a basic guide to create, manage, upload and update a Python
package.

Before start you will need:

- **A good idea for a package**. Not all what you program is good for
    converting to a package. You must respond to questions like:

    - Is my program useful for other people?.

    - Is it modular and can be developed for other people?.

    - Do you have a final version? including documentation, data and examples.

- **The package**. You need to have a proper organized package (see
    files required).

- **A proper name for the package**. You need a good and catchy name
    for your package before continue. To verify if your name has been already chosen check the name at:

    - https://test.pypi.org/project/<name_of_package>
    - https://pypi.org/project/<name_of_package>

- **The right modules to create the package**. In order to create a
    package you will need the following python prerrequisites:

    - `setuptools`: a set of tools to configure and distribute packages.
    
    - `twine`: a module to upload your package to the Pyhton Index
      repository.

- **Accounts in the Python Index**. Before start register in the
    Python Index website, both in the test repository
    (https://test.pypi.org/) as well as in the official one
    (https://pypi.org/).

The structure of a package
--------------------------

For writing a python package you need four basic files:

- `__init__.py`: This is the first file which is executed when you
  import the package.

- `setup.py`: This file contains the configuration of the package.

- `pyproject.toml`: This file describe the dependencies of your package.

- `README.md`: A basic README for the pacakge. This will be the
  landing page of your package in PyPI so it is better you write
  proper information on it.

- `LICENSE`: A license file. A complete list of licenses can be found
  at https://choosealicense.com/licenses/.

- `makefile`: Creating a package create a lot of noisy files. This
  file will allow you to clean your repo frequently.

All this files are packed in the `package.zip` file included in this
tutorial.

Creating the package
--------------------

1. Create a directory with all the files you need for the package. It
   is important to understand that this is not the directory of the
   package, but the directory of the package development, testing,
   uploading and installation. We will call it *package distribution
   directory*.

   ```
   mkdir -p mypack-dist
   ```

2. Place the basic files in the package distribution directory. In
   this repo you will find a basic set of files (see section below).
   Unpack the file there:

3. Create a directory inside the package distribution directory for
   all the source files that will be packed in your project:

   ```
   [mypack-dist]$ mkdir -p mypack
   ```

4. Move the specific package files into the package directory. For the
   basic files this includes one the `__init__.py` file:

   ```
   [mypack-dist]$ mv __init__.py mypack/
   ```

5. Test to import your package from the distribution directory. You
   may also test some basic functionalities:

   ```
   [mypack-dist]$ python -c 'import mypack;print(mypack.version)' 
   ```

   Make sure that your package is working properly.

6. Edit your `setup.py` file. Here are the explanation of what each
   line do.

7. Edit your `pyproject.toml` with the packages required for running
   your package.

8. Test to install locally your package:

   ```
   [mypack-dist]$ pip install -e .
   ```

   This command will install in your local python distribution the package.

9. Create a distribution.  A distribution is a set *tarball* with all
   the files included in your package:

   ```
   [mypack-dist]$ python setup.py sdist
   ```

10. Upload your package to the test repository:

   ```
   [mypack-dist]$ twine upload --repository-url https://test.pypi.org/legacy/ dist/*
   ```

11. Test to install your package from the test repository:

   ```
   [mypack-dist]$ pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple <your_package>
   ```

12. Upload your package to the main repository:

   ```
   [mypack-dist]$ twine upload dist/*
   ```

13. Install the package from the main repository:

   ```
   [mypack-dist]$ pip install <your_package>
   ```

And done! Now you have a public package.
