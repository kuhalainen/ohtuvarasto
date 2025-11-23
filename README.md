# ohtuvarasto
[![CI](https://github.com/kuhalainen/ohtuvarasto/actions/workflows/main.yml/badge.svg)](https://github.com/kuhalainen/ohtuvarasto/actions/)
[![codecov](https://codecov.io/github/kuhalainen/ohtuvarasto/graph/badge.svg?token=LBCQRBUAF1)](https://codecov.io/github/kuhalainen/ohtuvarasto)

A modern warehouse management system with a Flask web interface.

## Features

- 📦 Create and manage multiple warehouses
- ➕ Add items to warehouses
- ➖ Remove items from warehouses
- ✏️ Edit warehouse details
- 🗑️ Delete warehouses
- 🌓 Dark/light mode toggle
- 📱 Responsive design

## Installation

```bash
# Install dependencies
pip install poetry
poetry install
```

## Running the Application

### Web Interface

```bash
# Start the Flask application
cd src
FLASK_APP=app.py poetry run flask run
```

Then open your browser to `http://localhost:5000`

### Command Line (Legacy)

```bash
cd src
poetry run python index.py
```

## Testing

### Unit Tests

```bash
# Run pytest tests
poetry run pytest src/tests/

# With coverage
poetry run coverage run --branch -m pytest
poetry run coverage report
```

### Robot Framework Tests

```bash
# Make sure the Flask app is running first
cd src
FLASK_APP=app.py poetry run flask run

# In another terminal, run Robot tests
poetry run robot --outputdir results src/tests/robot/
```

## Linting

```bash
poetry run pylint src
```

## Technology Stack

- **Backend**: Flask 3.1
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Font**: Inter (Google Fonts)
- **Testing**: pytest, Robot Framework, SeleniumLibrary
- **Code Quality**: pylint, coverage
