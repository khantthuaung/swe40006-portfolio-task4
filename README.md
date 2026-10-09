# SWE40006 Portfolio — Task 4

Docker deployment source code for SWE40006 Software Deployment and Evolution.

| Subtask | Folder | Application |
| --- | --- | --- |
| 4.2 | `python-hello` | Python greeting and runtime information |
| 4.2 | `hello-web` | Hello World page served by Python HTTP server |
| 4.3 | `task-tracker` | React task tracker served by Nginx |
| 4.4 | `marks-analyser` | Non-web Python CSV marks analyser |

Task 4.1 uses the official `hello-world` image. Build each application from its own folder. Detailed instructions for the tracker and analyser are in their READMEs.

## Python application

```bash
cd python-hello
docker build -t task4-python:v1 .
docker run --rm task4-python:v1
```

## Hello World web server

The published v2 image supports Linux AMD64 and ARM64.

```bash
docker pull khantthuaung/task4-hello-web:v2
docker run -d --name hello-web-demo -p 8080:8000 khantthuaung/task4-hello-web:v2
```

Open http://localhost:8080. To build locally, run `docker build -t task4-hello-web:v1 .` from `hello-web`.

## Task tracker

Add tasks with optional due dates, mark them complete, delete them and filter by status. Data is saved per browser using localStorage. The current published v1 image was built for ARM64; use the supplied Dockerfile to build for other architectures.

```bash
cd task-tracker
docker build -t task4-task-tracker:local .
docker run -d --name task-tracker-demo -p 8082:80 task4-task-tracker:local
```

Open http://localhost:8082. No account or backend is required.

## Marks analyser

Published v1 supports Linux AMD64 and ARM64. Sample CSV records are fictional. Reports use demonstration grade boundaries: HD >=80, D >=70, C >=60, P >=50, F <50.

Run these commands in Bash/zsh from `marks-analyser`:

```bash
mkdir -p output
docker pull khantthuaung/task4-marks-analyser:v1
docker run --rm -v "$PWD/data:/data:ro" -v "$PWD/output:/output" khantthuaung/task4-marks-analyser:v1
```

`output/report.txt` remains on the host after the container exits. See the analyser README for invalid-input testing and exit codes.

## Published images

- https://hub.docker.com/r/khantthuaung/task4-hello-web
- https://hub.docker.com/r/khantthuaung/task4-task-tracker
- https://hub.docker.com/r/khantthuaung/task4-marks-analyser

## Verification status

The apps have been built and run locally in Docker. The Hello World v2 image was also pulled and run on a separate Windows AMD64 computer. The analyser includes five unit tests and valid/invalid sample CSV files.

Public website hosting is not yet configured. Localhost addresses above only work on the machine running the container. This repository supplies source code for verification; the assessment report and screenshots are submitted separately.
