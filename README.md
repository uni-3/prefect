# Infrastructure Setup

This document outlines the infrastructure setup for our project.

## MotherDuck

We use MotherDuck for data storage and analytics.

- Access the MotherDuck dashboard: [https://app.motherduck.com](https://app.motherduck.com)

## Modal

We use Modal for serverless compute. Follow these steps to set up Modal:

https://modal.com/apps

1. Install the Modal CLI (if not already installed):
   ```
   pip install modal
   ```

2. Set up Modal and create token ID and token secret:
   ```
   modal setup
   ```

3. Login to Modal in your browser when prompted.

4. After setup, you can view your Modal configuration:
   ```
   cat ~/.modal.toml
   ```

// ... existing content ...

## github

- add block for github token

```
prefect cloud login
```

```
prefect block register -f blocks/github.py
```

## deploy flow

cli

```
prefect deploy
```