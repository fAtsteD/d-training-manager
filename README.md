# DTrainingManager

Manager for your training routine.

## Developing project

It requires AWS SAM, uv preinstalled and set up.

1. Clone repository
2. Initialize virtual environment
3. Create from example file .env
4. Install project with dependencies for local develpment

    ```bash
    make init
    ```

5. Pull and up required services

    ```bash
    docker compose -f docker-compose.dev.yml up -d
    ```

6. Start local container with lambda function

    ```bash
    make sam-local-start
    ```

Project has linter and type checking thought make commands

- lint and type check

    ```bash
    make check
    ```

- lint check

    ```bash
    make lint
    ```

- lint check and fix

    ```bash
    make format
    ```

- type check

    ```bash
    make check-types
    ```

## Tests

The project uses tests for checking functionality. Run tests:

```bash
make test
```

Test with coverage information

```bash
make test-coverage
```
