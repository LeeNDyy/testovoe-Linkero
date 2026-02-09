# DB Stack Runbook

## Deployment

```bash
# Clone repository
git clone https://github.com/LeeNDyy/testovoe-Linkero.git
cd https://github.com/LeeNDyy/testovoe-Linkero.git

#Encrypt Ansible vault, dont't use it if you don't needed, just deploy
#and write password Ansible
ansible-vault encrypt ./Task-1/db_stack/roles/vars/vault.yaml

password: Ansible

# Deploy (first time)
ansible-playbook -i inventory.ini deploy.yaml --ask-vault-pass

# Redeploy (updates config)
ansible-playbook -i inventory.ini deploy.yaml --ask-vault-pass


