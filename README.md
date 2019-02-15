# efscape Model -- GUI client for efscape

## Summary

Provides a GUI client for efscape.

* A rectangular grid

## Installation

To install the dependencies use pip and the requirements.txt in this directory.
e.g.

```
    $ pip install -r requirements.txt
```

## How to Run

To run the model interactively, run ``mesa runserver`` in this directory. e.g.

```
    $ mesa runserver
```

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and
press Reset, then Run.

## Files

* ``efscape/model.py``: Defines the basic shape model and agents.
* ``efscape/server.py``: Sets up the interactive visualization server.
* ``run.py``: Launches a model visualization server.
