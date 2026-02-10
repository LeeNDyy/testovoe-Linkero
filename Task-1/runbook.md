# DB Stack Runbook

<<<<<<< HEAD
## Deployment

=======
## Server Preparetion

``` bash
apt update && apt install -y python3-pip ansible docker.io docker-compose
systemctl enable --now docker
pip3 install ansible docker ansible-lint
mkdir -p /srv/backups/postgres

```

## Clone Repo and encrypt Ansible vault
>>>>>>> 6c066a0 (answered on Task-1 and Task-3)
```bash
# Clone repository
git clone https://github.com/LeeNDyy/testovoe-Linkero.git
cd https://github.com/LeeNDyy/testovoe-Linkero.git

#Encrypt Ansible vault, dont't use it if you don't needed, just deploy
#and write password Ansible
<<<<<<< HEAD
ansible-vault encrypt ./Task-1/db_stack/roles/vars/vault.yaml

password: Ansible

=======
cd ./Task-1
ansible-vault encrypt ./Task-1/db_stack/roles/vars/vault.yaml

#password: Ansible or any password
```

## Deployment

``` bash
>>>>>>> 6c066a0 (answered on Task-1 and Task-3)
# Deploy (first time)
ansible-playbook -i inventory.ini deploy.yaml --ask-vault-pass

# Redeploy (updates config)
ansible-playbook -i inventory.ini deploy.yaml --ask-vault-pass
<<<<<<< HEAD


=======
```

# Test Data Base and connection

``` bash
PGPASSWORD=1234 psql -h 127.0.0.1 -p 6432 -U app_user app_db -c "\dt"

PGPASSWORD=1234 psql "host=127.0.0.1 port=6432 user=app_user dbname=app_db" -c "SELECT * FROM test_table;"
```
>>>>>>> 6c066a0 (answered on Task-1 and Task-3)
