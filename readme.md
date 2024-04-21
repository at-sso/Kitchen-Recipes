# Recipe Management Web Application

This is a simple web application built with Flask for managing recipes. It allows users to add, update, delete, search, and view recipes through a web interface.

## Installation

To install the required dependencies, use one of the following commands:

```
pip install -r ./env/requirements.txt
```

or

```
py -m pip install -r ./env/requirements.txt
```

## Usage

1. Clone the repository to your local machine.
2. Install the dependencies using the command mentioned above.
3. Run the Flask application using the provided Python script.
4. Access the web application in your browser.
5. To align the paths in the systemd unit file with your project's structure and update the Gunicorn and Nginx configurations accordingly read [this](env/readme.md).

## Overview of the Code

The code consists of a Flask web application that provides several routes for managing recipes:

- `/`: Main page with forms for adding, updating, and deleting recipes.
- `/add`: Route for adding a new recipe.
- `/update`: Route for updating an existing recipe.
- `/delete`: Route for deleting a recipe.
- `/view`: Route for viewing all recipes.
- `/results`: Route for fetching the latest recipes data.
- `/search`: Route for searching a recipe by ID.

The web application uses JavaScript to dynamically update the `responseGetter` on the main page without reloading the entire page whenever a form is submitted.

## Folder Structure

- `src/page`: Contains Python source code files.
- `./static/`: Contains static files such as JavaScript, CSS, and images.
- `./templates/`: Contains HTML templates used by Flask to render pages.

## License

This project is licensed under the MIT License - see the [license](license) file for details.
