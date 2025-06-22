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

5. Build dev environment for local usage

   ```bash
   sam build --config-env dev
   ```

6. Start local container with lambda function

   ```bash
   sam local start-api --config-env dev
   ```
