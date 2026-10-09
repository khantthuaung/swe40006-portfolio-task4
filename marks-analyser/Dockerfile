# Python includes every module used here, so pip installation is not needed.
FROM python:3.13-slim
WORKDIR /app
COPY analyser.py .
# Mount the input and output folders when starting the container.
ENTRYPOINT ["python", "analyser.py"]
