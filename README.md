# Smart Import


![pypi](https://img.shields.io/pypi/v/smartimport.svg?display=inline-block) 
![travis](https://img.shields.io/travis/jrmi/smartimport.svg?display=inline-block) 
![readthedocs](https://readthedocs.org/projects/smartimport/badge/?version=latest?display=inline-block)
![github](https://pyup.io/repos/github/jrmi/smartimport/shield.svg?display=inline-block)


Smart file import with auto type detection.

# Installation

For now you can clone the repository then in your favorite python>=3.6 virtualenv in the clone dir :
    
```console
$ python setup.py develop
```

This install a dev version of smartimport package.

Now you can execute `smartimport` but you should create a directory where you will copy all your data/models.

```console
$ mkdir project && cd project
$ touch settings_local.py
```

You can change variable in the `settings_local.py` file. More information on this will comme later.

# Training

First you need some training data. Must be a csv file named after the `settings.TRAINING_DATA_PATH` configuration.
This CSV must contains two cols (data, type). Then execute ::


```console
$ smartimport train # --confusion option to show confusion plot
```

A model will be saved in `settings.MODEL_PATH`.

# Usage

When a model file have been created, you can run smartimport on any CSV file :

```console
$ smartimport load <path_to_your_file>
```

and json should describe your file.


# Legal information

* Free software: BSD license
* Documentation: https://smartimport.readthedocs.io.


This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
