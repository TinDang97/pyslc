# Project Name

## Description

This is a project that requires Poetry for dependency management. Follow the instructions below to install Poetry and install the project requirements.

## Installation

### !!!WARNING


                                   *add your openai key here*
                                   ***************************************************
    79:       - ZEP_OPENAI_API_KEY=sk-****************************************************



1. Install Poetry by running the following command in your terminal:

   ```shell
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Build docker images:

    ```shell
    make build
    ```

2. Run `dev`:

    ```shell
    make dev
    ```

Your server at `http://localhost:8000`


## Issues:

1. `alembic upgrade` -> ERROR

    -> Remove `pyslc` schema in `postgres` db

2. port used:

    -> edit $PORT
