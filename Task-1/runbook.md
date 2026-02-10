# DB Stack Runbook

## Server Preparetion

``` bash
apt update && apt install -y python3-pip ansible docker.io docker-compose
systemctl enable --now docker
pip3 install ansible docker ansible-lint
mkdir -p /srv/backups/postgres

```

## Clone Repo and encrypt Ansible vault
```bash
# Clone repository
git clone https://github.com/LeeNDyy/testovoe-Linkero.git
cd https://github.com/LeeNDyy/testovoe-Linkero.git

#Encrypt Ansible vault, dont't use it if you don't needed, just deploy
#and write password Ansible

ansible-vault encrypt ./Task-1/db_stack/roles/vars/vault.yaml

password: Ansible


cd ./Task-1
ansible-vault encrypt ./Task-1/db_stack/roles/vars/vault.yaml

#password: Ansible or any password
```

Also before deploy script, you need to create database app_db.

In the file ./roles/db_stack/templates/init-db.sql.j2 located script for create table, not db. It's just a test script!!!!

So first you need to create a database, then run the deployment script

## Deployment


# Deploy (first time)
1.cd ./Task-1

2.ansible-playbook -i inventory.ini deploy.yaml --ask-vault-pass

# Redeploy (updates config)
1.cd ./Task-1

2.ansible-playbook -i inventory.ini deploy.yaml --ask-vault-pass


## Test Data Base and connection

``` bash
psql -h 127.0.0.1 -p 6432 -U app_user app_db -c "SELECT 1;"

PGPASSWORD=1234 psql -h 127.0.0.1 -p 6432 -U app_user app_db -c "\dt"

PGPASSWORD=1234 psql "host=127.0.0.1 port=6432 user=app_user dbname=app_db" -c "SELECT * FROM test_table;"
```
