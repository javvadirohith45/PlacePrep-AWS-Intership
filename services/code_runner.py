"""Isolated execution service for PlacePrep Coding Arena.

All non-SQL submissions are executed in a Docker container with networking
removed and resource limits applied. SQL submissions run against an isolated
SQLite database inside a short-lived Python container.
"""
from __future__ import annotations

import os
import re
import subprocess
import tempfile
import time
from typing import Iterable

IMAGES = {
    "python": "python:3.12-slim",
    "javascript": "node:22-alpine",
    "java": "eclipse-temurin:21-jdk",
    "cpp": "gcc:14",
    "c": "gcc:14",
    "sql": "python:3.12-slim",
}


def _docker_available() -> bool:
    try:
        subprocess.run(["docker", "version", "--format", "{{.Server.Version}}"], capture_output=True, text=True, timeout=3, check=True)
        return True
    except Exception:
        return False


def _base_docker_args(workdir: str, image: str, command: list[str], timeout: int) -> list[str]:
    return [
        "docker", "run", "--rm",
        "--network", "none",
        "--cpus", "0.5",
        "--memory", "128m",
        "--pids-limit", "64",
        "--read-only",
        "--tmpfs", "/tmp:rw,noexec,nosuid,size=64m",
        "-v", f"{workdir}:/work:ro",
        image, *command,
    ]


def _write(path: str, text: str) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def _execute(language: str, code: str, test_input: str, timeout: int = 4) -> dict:
    if language not in IMAGES:
        return {"status": "unsupported", "message": f"Language '{language}' is not configured."}
    if not _docker_available():
        return {"status": "unconfigured", "message": "Docker is not installed or its daemon is unavailable. Install/start Docker Desktop to enable real isolated execution."}

    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="placeprep-run-") as workdir:
        if language == "python":
            _write(os.path.join(workdir, "main.py"), code)
            command = ["python", "/work/main.py"]
        elif language == "javascript":
            _write(os.path.join(workdir, "main.js"), code)
            command = ["node", "/work/main.js"]
        elif language == "java":
            _write(os.path.join(workdir, "Main.java"), code)
            command = ["sh", "-lc", "cp /work/Main.java /tmp/Main.java && javac -d /tmp /tmp/Main.java && java -cp /tmp Main"]
        elif language in ("c", "cpp"):
            filename = "main.c" if language == "c" else "main.cpp"
            compiler = "gcc" if language == "c" else "g++"
            _write(os.path.join(workdir, filename), code)
            command = ["sh", "-lc", f"{compiler} /work/{filename} -O2 -o /tmp/placeprep.out && /tmp/placeprep.out"]
        else:
            return _execute_sql(code, test_input, timeout)

        try:
            result = subprocess.run(
                _base_docker_args(workdir, IMAGES[language], command, timeout),
                input=test_input or "", text=True, capture_output=True, timeout=timeout,
            )
        except subprocess.TimeoutExpired as exc:
            return {"status": "timeout", "stdout": exc.stdout or "", "stderr": exc.stderr or "", "message": "Time Limit Exceeded", "runtime_ms": timeout * 1000}
        except FileNotFoundError:
            return {"status": "unconfigured", "message": "Docker is not installed or available."}

        runtime_ms = int((time.perf_counter() - started) * 1000)
        if result.returncode == 0:
            return {"status": "completed", "stdout": result.stdout, "stderr": result.stderr, "returncode": 0, "runtime_ms": runtime_ms}
        # C/C++ compilation diagnostics are printed by the compiler before the executable can run.
        if language in ("c", "cpp") and ("error:" in result.stderr or "fatal error" in result.stderr):
            status = "compilation_error"
        else:
            status = "runtime_error"
        return {"status": status, "stdout": result.stdout, "stderr": result.stderr, "returncode": result.returncode, "runtime_ms": runtime_ms}


def _execute_sql(query: str, fixture: str, timeout: int = 4) -> dict:
    script = r'''import sqlite3, sys
fixture=sys.stdin.read()
query=open('/work/query.sql',encoding='utf-8').read()
con=sqlite3.connect(':memory:')
try:
    con.executescript(fixture)
    cur=con.execute(query)
    rows=cur.fetchall()
    for row in rows:
        print('|'.join('' if v is None else str(v) for v in row))
except Exception as exc:
    print(type(exc).__name__ + ': ' + str(exc), file=sys.stderr)
    sys.exit(2)
finally:
    con.close()
'''
    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="placeprep-sql-") as workdir:
        _write(os.path.join(workdir, "query.sql"), query)
        _write(os.path.join(workdir, "runner.py"), script)
        try:
            result = subprocess.run(
                _base_docker_args(workdir, IMAGES["sql"], ["python", "/work/runner.py"], timeout),
                input=fixture or "", text=True, capture_output=True, timeout=timeout,
            )
        except subprocess.TimeoutExpired as exc:
            return {"status":"timeout","stdout":exc.stdout or "","stderr":exc.stderr or "","message":"Time Limit Exceeded","runtime_ms":timeout*1000}
        runtime_ms = int((time.perf_counter()-started)*1000)
        if result.returncode == 0:
            return {"status":"completed","stdout":result.stdout,"stderr":result.stderr,"returncode":0,"runtime_ms":runtime_ms}
        return {"status":"runtime_error","stdout":result.stdout,"stderr":result.stderr,"returncode":result.returncode,"runtime_ms":runtime_ms}


def run_test_cases(language: str, code: str, test_cases: Iterable[dict], timeout: int = 4) -> dict:
    """Run public/hidden cases and return honest per-case results."""
    cases = list(test_cases)
    results = []
    total_started = time.perf_counter()
    for index, case in enumerate(cases, start=1):
        result = _execute(language, code, case.get("input", ""), timeout=timeout)
        actual = (result.get("stdout") or "").strip()
        expected = (case.get("expected") or "").strip()
        passed = result.get("status") == "completed" and actual == expected
        item = {
            "index": index,
            "hidden": bool(case.get("hidden")),
            "passed": passed,
            "status": "passed" if passed else result.get("status", "error"),
            "input": case.get("input", "") if not case.get("hidden") else "Hidden test case",
            "expected": expected if not case.get("hidden") else "Hidden expected output",
            "actual": actual if not case.get("hidden") else (actual if result.get("status") == "completed" else ""),
            "stdout": result.get("stdout", ""),
            "stderr": result.get("stderr", ""),
            "runtime_ms": result.get("runtime_ms", 0),
            "message": result.get("message", ""),
        }
        results.append(item)
        if result.get("status") in {"unconfigured", "unsupported"}:
            return {"status": result["status"], "message": result.get("message", ""), "tests": results}
    passed_count = sum(1 for item in results if item["passed"])
    if passed_count == len(results):
        status = "accepted"
        message = "All Test Cases Passed"
    else:
        status = next((item["status"] for item in results if not item["passed"] and item["status"] in {"compilation_error","runtime_error","timeout"}), "wrong_answer")
        message = {
            "wrong_answer": "Wrong Answer",
            "compilation_error": "Compilation Error",
            "runtime_error": "Runtime Error",
            "timeout": "Time Limit Exceeded",
        }.get(status, "Execution failed")
    return {
        "status": status,
        "message": message,
        "tests": results,
        "passed": passed_count,
        "total": len(results),
        "runtime_ms": int((time.perf_counter()-total_started)*1000),
    }


def run_in_docker(language, code, test_input, timeout=3):
    """Backward-compatible single-test API."""
    return _execute(language, code, test_input, timeout)
