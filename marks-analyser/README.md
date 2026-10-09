# Task 4.4 — Student Marks Analyser

A non-web Python command-line app. It reads fictional student records, validates marks, calculates average/highest/lowest marks and pass rate, counts grades, and saves a text report. Only the Python standard library is used.

## Run in Docker on your Mac

Open Terminal in this folder:

```bash
docker build -t task4-marks-analyser:v1 .
mkdir -p output
docker run --name task4-marks-run \
  -v "$PWD/data:/data:ro" \
  -v "$PWD/output:/output" \
  task4-marks-analyser:v1
cat output/report.txt
```

Input is read-only (`:ro`). The output folder is mounted from your Mac, so the report survives after the container exits. The container finishes normally with exit code 0; it is not a web server and has no browser URL.

If the named container already exists, use `docker start -a task4-marks-run` to rerun it, or use a different name when creating a new one.

## Demonstrate validation

This sample deliberately includes non-numeric, missing, out-of-range and non-finite marks, a missing name and a duplicate ID.

```bash
docker run --name task4-marks-validation \
  -v "$PWD/data:/data:ro" \
  -v "$PWD/output:/output" \
  task4-marks-analyser:v1 \
  --input /data/invalid-students.csv --output /output/validation-report.txt
```

Exit codes: **0** = all records valid; **2** = report generated with rejected records; **1** = file/schema error or no valid records. Code 2 in the validation demonstration is intentional, not a Docker crash. Correct a copy of the invalid CSV and rerun to demonstrate how errors are resolved.

## Run without Docker / tests

```bash
python3 analyser.py --input data/students.csv --output output/local-report.txt
python3 -m unittest -v
```

## Code explanation

- `grade_for`: simple if statements select demonstration grades (80 HD, 70 D, 60 C, 50 P, below 50 F).
- `read_students`: reads CSV, validates each record and collects readable line-number errors.
- `make_report`: calculates statistics over valid records only and formats a text report.
- `main`: handles command-line paths, writes the report and returns an exit code.
- `Dockerfile`: adds the script to a Python image and runs it as the entry point.

These grade boundaries are app design choices, not a claim about official university policy. Input headers are case-sensitive: student_id,name,mark. Additional named columns are ignored. Existing output files at the requested path are overwritten. Input and output cannot be the same file.

## Evidence for your assignment

Capture the Docker build, successful output, `docker ps -a --filter name=task4-marks`, report saved on your Mac, and intentional validation results. Explain the input problem, cause, handling and correction. Include public source/image links later; do not paste source into the report. No Docker Hub upload has been done for this app yet.
