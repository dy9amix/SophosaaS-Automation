import paramiko

def configure_vlan(vmID, vlan):
    server = '192.168.4.82'
    user_id = 'root'
    passwd = '!@#Supp0rt1'
    ssh_client =paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(server, username=user_id, password=passwd)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(f'pvesh set /nodes/saas/qemu/{vmID}/config --net2 e1000,bridge=vmbr1,firewall=1,tag={vlan}')

