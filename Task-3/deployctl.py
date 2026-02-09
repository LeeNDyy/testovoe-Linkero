#!/usr/bin/env python3
import sys
import json
import time
import subprocess
import argparse
import requests

COMPOSE_FILE = "docker-compose.yml"
DB_SERVICE = "postgres"
APP_SERVICE = "app"
DB_USER = "app_user"
DB_NAME = "app_db"
APP_HEALTH = "http://localhost:8000/health"
MIGRATIONS_FILE = "migrations.sql"

class DeployError(Exception):
    pass

def run_cmd(cmd, cwd=None, check=True):
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, check=check)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {cmd}")
        if e.stdout:
            print(f"Output: {e.stdout.strip()}")
        if e.stderr:
            print(f"Error: {e.stderr.strip()}")
        raise DeployError(f"Command '{cmd}' exited with code {e.returncode}")

def wait_for_db(max_attempts=60, interval=3):
    print("Waiting for PostgreSQL...")
    for attempt in range(max_attempts):
        try:
            result = subprocess.run(
                f"docker compose exec -T {DB_SERVICE} pg_isready -U {DB_USER} -d {DB_NAME}", 
                shell=True, capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                print("PostgreSQL is ready")
                return True
        except subprocess.TimeoutExpired:
            print(f"DB check timeout on attempt {attempt+1}")
        except Exception:
            pass
        print(f"Waiting for DB... ({attempt+1}/{max_attempts})")
        time.sleep(interval)
    raise DeployError(f"PostgreSQL not ready after {max_attempts*interval}s. Check 'docker compose logs postgres'")

def apply_migrations():
    print("Applying database migrations...")
    if not subprocess.run(f"[ -f {MIGRATIONS_FILE} ]", shell=True).returncode == 0:
        raise DeployError(f"Migrations file '{MIGRATIONS_FILE}' not found")
    
    run_cmd(f"docker compose cp {MIGRATIONS_FILE} {DB_SERVICE}:/tmp/migrations.sql")
    run_cmd(f"docker compose exec -T {DB_SERVICE} psql -U {DB_USER} -d {DB_NAME} -f /tmp/migrations.sql")
    print("Migrations completed successfully")

def check_app_health(max_attempts=30, interval=1):
    print("Checking application health...")
    for attempt in range(max_attempts):
        try:
            resp = requests.get(APP_HEALTH, timeout=5)
            if resp.status_code == 200:
                print("Application health check passed")
                return resp.json()
        except requests.exceptions.ConnectionError:
            print(f"Cannot connect to app on attempt {attempt+1}/{max_attempts}")
        except requests.exceptions.Timeout:
            print(f"App healthcheck timeout on attempt {attempt+1}/{max_attempts}")
        except requests.RequestException as e:
            print(f"Healthcheck failed: {str(e)}")
        time.sleep(interval)
    raise DeployError("Application failed healthcheck after 30s. Check 'docker compose logs app'")

def print_status(success=True, message="Deploy completed"):
    status = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "success": success,
        "message": message,
        "services": {"postgres": "healthy" if success else "unknown", "app": "healthy" if success else "unknown"},
    }
    print(json.dumps(status, indent=2))

def deploy_up():
    try:
        print("Starting deployment...")
        run_cmd("docker compose down", check=False)
        run_cmd("docker compose up -d --build")
        wait_for_db()
        apply_migrations()
        check_app_health()
        print_status(True, "Deployment successful")
    except DeployError:
        raise
    except Exception as e:
        raise DeployError(f"Unexpected error: {str(e)}")

def deploy_rollback():
    try:
        print("Starting rollback...")
        
        try:
            with open(".deploy-tag", "r") as f:
                prev_tag = f.read().strip()
        except FileNotFoundError:
            prev_tag = "v1"
            print("No previous tag found, initializing with v1")
        
        current_tag = "v2" if prev_tag == "v1" else "v1"
        print(f"Switching from {prev_tag} to {current_tag}")
        
        run_cmd(f"docker compose build --build-arg TAG={current_tag} {APP_SERVICE}")
        run_cmd(f"docker compose up -d {APP_SERVICE}")
        
        with open(".deploy-tag", "w") as f:
            f.write(current_tag)
        print_status(True, f"Rolled back to version {current_tag}")
    except DeployError:
        raise
    except Exception as e:
        raise DeployError(f"Rollback failed: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Deploy Docker Compose stack")
    parser.add_argument("action", choices=["up", "rollback"], help="Deployment action")
    args = parser.parse_args()
    
    try:
        if args.action == "up":
            deploy_up()
        elif args.action == "rollback":
            deploy_rollback()
    except DeployError as e:
        print_status(False, str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
