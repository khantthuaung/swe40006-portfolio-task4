# Simple Task Tracker

React + Vite app for SWE40006 Task 4.3. The expense dashboard is kept separately as a backup.

Features: add tasks with optional due dates, mark complete/incomplete, delete, filter All/Pending/Completed and save in browser localStorage.

## Development

Use Node 22.12 or later.

```bash
npm ci
npm run dev
npm run build
```

## Docker

```bash
docker build -t khantthuaung/task4-task-tracker:v1 .
docker run -d --name task4-task-tracker -p 127.0.0.1:8082:80 khantthuaung/task4-task-tracker:v1
```

Open http://127.0.0.1:8082. Node builds the app in the first Docker stage; Nginx serves it in the final stage.

## Code guide

- `src/App.jsx`: ordinary JavaScript functions and React state for tasks, form fields and filtering. Comments explain loading, saving and filtering.
- `src/styles.css`: a single-column layout with a small phone breakpoint.
- `src/main.jsx`: starts React.
- `Dockerfile`: two-stage build.

Data is stored only in this browser and origin. Clearing browser data removes tasks; there is no backend, account system or cross-device synchronisation. Deletion removes a task immediately.

## Report evidence

Capture task creation, completing a task, each filter, persistence after refresh, Docker build and the running container. Include the public deployment/source URLs later; this localhost URL is not publicly accessible. Describe the code in your own words without pasting source into the report.
