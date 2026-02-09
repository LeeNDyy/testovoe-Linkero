# deployctl.py

## Quick Start
```bash
chmod +x deployctl.py
pip install requests
#for deploy
python3 deployctl.py up
#for rollback
python3 deployctl.py rollback
```

## Prerequisites
```
Ubuntu 22.04/24.04
Docker + Docker Compose
Python 3.8+
Required files:
├── docker-compose.yml
├── Dockerfile
├── requirements.txt  
├── app/main.py
└── migrations.sql
```

## Example Output
```
{
  "timestamp": "2026-02-10T01:00:00Z",
  "success": true,
  "message": "Deployment successful",
  "services": {
    "postgres": "healthy",
    "app": "healthy"
  }
}
```

## Full Workflow Demo
``` bash
# Initial deploy
python3 deployctl.py up

# Check status  
curl http://localhost:8000/health

# Rollback
python3 deployctl.py rollback
cat .deploy-tag

# Deploy again
python3 deployctl.py up
```