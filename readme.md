# Main

Goals:

1. Build keywords using synonyms
2. Build potential usernames using synonyms combination
3. Validate usernames to see if they are valid

# Usage

## Setup VENV

1. Install python
2. Setup .venv folder: `python -m venv .venv`
3. Activate virtual environment: `. .venv/Scripts/activate`

## Install Dependencies

`pip install -r requirements.txt`

## Run program

`python main.py`

# TODO

All of these are nice-to-haves, but not necessary for program utilization:

- logging
- method to safe-build directory
- gen username, delimiters before and after first and last tokens
- parts of speech generation
- user accepts synonyms in user_accepted.txt file for each synonym. reduce unecessary compute time for unwanted synonyms
- have the delimeter strategy applied to user accepted usernames. reduce initial computer time

# Dev details

## File Structure

```
.venv/
  |-- *
data
  |-- synonyms
    |-- *
      |-- raw
      |-- utilized
      |-- unique
  |-- usernames
    |-- potential
    |-- valid
```