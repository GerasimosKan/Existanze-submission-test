# The Star Wars API Submission for Python Developer Position

This project is a submission for the Python Developer position, designed to showcase proficiency in Python by consuming "The Star Wars API" (SWAPI).

## Prerequisites

Ensure the following requirements are met before running the application:

- **Python:** Version >= 3.9
- **Virtual Environment:** Installed and configured for Python 3.9

## Installation and Setup

Follow these steps to set up and run the application:

1. **Install Python:**

   - Download and install Python 3.9.
   - Verify the installation:
     ```bash
     python3 --version
     ```

2. **Create a Virtual Environment:**

   - Run the following command to create a virtual environment:
     ```bash
     python3 -m venv virtualenv-[yourname]
     ```

3. **Activate the Virtual Environment:**

   - Navigate to the `bin/` folder of your virtual environment:
     ```bash
     cd virtualenv-[yourname]/bin
     ```
   - Activate the environment:
     ```bash
     source activate
     ```

4. **Install Dependencies:**

   - Navigate to the project root directory and install required packages:
     ```bash
     pip install -r requirements.txt
     ```

## Features and Commands

### Level 1: Basic Character Search

Search for any Star Wars character by name:

```bash
python main.py search 'luke sky'
```

In case the character is not found (e.g. replace "luke sky" with "what is star wars?"), the application should respond with the following message:

```bash
The force is not strong within you
```

### Level 2: Character Search with Homeworld info

```bash
python main.py search 'luke sky' --world
```

### Level 3A: Character Search with Homeworld info from cache

```bash
python main.py search 'luke sky'
python main.py search 'luke sky' --world
```

In the response of the both commands,
a timestamp of the cache should be included like the following:

```bash
Cached at: 20-11-2024 21:56:05
```

### Level 3B: Clean the application cache

```bash
python main.py cache --clean
```

### Level 4: Search history

```bash
python main.py cache --history
```
