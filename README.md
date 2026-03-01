# StudBuddy Backend

StudBuddy is a comprehensive AI-powered backend service designed to support the StudBuddy Android application. It provides powerful Generative AI capabilities to enhance students' learning experiences, exposing features such as automated lecture audio summarization and intelligent resume reviews.

The backend is built entirely on AWS Serverless infrastructure (API Gateway, Lambda) and leverages Google's Gemini models for its GenAI processing capabilities. It utilizes a custom Python CLI (powered by `invoke`) for streamlined, production-grade deployment and stack management.

## Architecture Highlights
- **Serverless Compute**: Independent, scalable AWS Lambda functions for each feature (Summarizer, Resume Reviewer, etc.).
- **Secure APIs**: Amazon API Gateway leveraging API Keys and Usage Plans to strictly control access from the Android client application.
- **Secrets Management**: AWS Secrets Manager for safely storing third-party credentials (e.g., Gemini API keys) outside of the codebase.
- **Extensible Deployment**: A custom, modular `invoke` CLI specifically built to handle zip-packaging, Stack creation, and environment configuration.

---

## Developer Onboarding

Welcome to the StudyBuddy Backend repository! Follow these steps to get your local development environment set up for building and deploying infrastructure.

### 1. Create a Python Virtual Environment
We require an isolated Python 3.13 runtime to run the deployment scripts 

```bash
python3 -m venv venv
source venv/bin/activate
# On Windows use: venv\Scripts\activate
```

### 2. Install Development Tooling
To manage our dependencies cleanly, we use `pip-tools` alongside our `invoke` CLI framework:

```bash
pip install -r requirements/dev.txt
```

### 3. Verify Setup
Run our custom CLI to verify everything is wired up correctly and that `invoke` is successfully parsing the `config/config.yaml` application context:

```bash
inv about
```
You should see output similar to: `Welcome to Studbuddy`

## Acknowledgements
The Python deployment CLI architecture and modular folder structure are heavily inspired by the design patterns found in the [AWS Research and Engineering Studio (RES)](https://github.com/aws/res) open-source repository.

## License
Licensed under the [Apache License, Version 2.0](./LICENSE.txt).
