import os
import subprocess


def pytest_configure():
    setup_database()


def pytest_unconfigure():
    shutdown_database()


def setup_database():
    print("Bringing up database...")
    subprocess.call(["docker-compose", "-f", "tests/docker-compose.yaml", "up", "-d"])

    subprocess.call(["sleep", "5"])
    subprocess.call(["docker", "exec", "postgres", "createdb", "-U", "postgres", "mmasters"])

    print("setting up database url as environment variable")
    os.environ["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:secret@localhost:5432/mmasters"

    print("setting up flask app as environment variable")
    os.environ["FLASK_APP"] = "run_app.py"

    print("Running migrations...")
    subprocess.call(["flask", "db", "upgrade"])


def shutdown_database():
    print("Shutting down database...")
    subprocess.call(["docker-compose", "-f", "tests/docker-compose.yaml", "down"])
