## About The Project

Build microservice web application for room/table booking that can be used to connect to other library main website.

## Dependencies

To get started, the following tools/account should be installed:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/)

## Getting Started

To clone a local copy up and running follow these simple example steps.

Go to the folder to clone e.g desktop
To use git clone command install Git

```sh
git clone https://github.com/hazamashoken/CC_Group7_CW2.git
```

### Prerequisites

You should update poetry to the latest version to improve the functionality or be obligatory for security purposes and install poetry as the package manager.

```sh
poetry install
```

### Usage
1. Run Docker Desktop
2. Go to the `app` folder

Create a `.env.local` file with a value for the enviroment variable. See `.env.sample` for reference.

3. Activate a Virtual enviroment
```sh
poetry shell
```
Once local enviroment variables are set, dependencies are installed and Docker Desktop is running in background. 
You can start the app 

```sh
python manage.py runserver
```
4. Visit `http://127.0.0.1:8000/` on your web browser.
5. That's all.

### Usage this project is done by:
- thanapol
- Kee Hui

## Acknowledgements

- [Django Project](https://www.djangoproject.com/)