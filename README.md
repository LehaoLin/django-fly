# django-fly
It is an <b>useful command line tool</b> to manage (initialize and update) the deploy settings with <b>NGINX, Supervisor, Gunicorn, Letsencrypt</b> in the `Linux web server`.
Current version only fits django 2.2.x.

It is my personal-used command to deploy django web app.

## Installation
```$ pip3 install django-fly```

If you are failed to do pip3 install, please git clone this repo, then ```python3 setup.py install```.

## Usage
#### 1. ```$ django-fly init```

To initialize the `__deploy__` directory and sample configurations.

#### 2. ```$ django-fly update```

After modificating and moving setting files under the right section under the `__deploy__` directory, you can use this command to update settings of NGINX and Supervisor.