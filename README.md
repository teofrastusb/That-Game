Looking to play the game? Checkout the [slime_ai wiki](https://github.com/ikottman/slime_ai/wiki/Welcome-to-Slime-Mind!)  for game details and [example code](https://github.com/ikottman/slime_ai).

# Packaging

Run the following commands to package this library:
```
rm -rf dist build */*.egg-info *.egg-info

python3 setup.py sdist bdist_wheel

twine upload dist/*
```
