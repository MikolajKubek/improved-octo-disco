# improved-octo-disco
Some random project for Hackyeah 2024.
According to our current idea it should be a web application that evaluates posture during Yoga excercises.
The expected tech stack is [mmpose neural network](https://github.com/open-mmlab/mmpose?tab=readme-ov-file),
[Flask](https://flask.palletsprojects.com/en/3.0.x/) and [HTMX](https://htmx.org/).

# Setup development environment

1. Clone the repository
```console
git clone https://github.com/MikolajKubek/improved-octo-disco.git && cd improved-octo-disco
```

2. Setup python virtual environment
```console
python -m venv .venv
```

3. Install flask
```console
pip install flask
```

4. Install [mmdet](https://mmpose.readthedocs.io/en/latest/installation.html) according to the instructions


5. Run flask in debug mode
```console
flask --app main --debug run
```
