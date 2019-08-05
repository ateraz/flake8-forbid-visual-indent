# Flake8-forbid-visual-indent

[![Build Status](https://travis-ci.com/ateraz/flake8-forbid-visual-indent.svg?branch=master)](https://travis-ci.com/ateraz/flake8-forbid-visual-indent)

Flake8 plugin that disallows visual indentation. It raises error for indentation style like
```python
def my_function(first_arg: int,
                second_arg: int) -> int:
    ...
```
in favor of
```python
def my_function(
        first_arg: int, second_arg: int) -> int:
    ...
```
