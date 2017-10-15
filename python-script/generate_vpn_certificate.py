import subprocess
import os

server_ip = '192.168.122.2'

def run_haveged():
    enable = 'systemctl enable haveged'
    run_command(enable)
    start = 'systemctl start haveged'
    run_command(start)


def create_server_certificate():
    ipsec_pki_gen = 'ipsec pki --gen --type rsa --size 4096 --outform der > /etc/ipsec.d/private/strongswanKey.der'
    run_command(ipsec_pki_gen)
    chmod = 'chmod 600 /etc/ipsec.d/private/strongswanKey.der'
    run_command(chmod)

    gen_self_signed_rootCA = 'ipsec pki --self --ca --lifetime 3650 --in /etc/private/strongswanKey.der --type rsa --dn "C=NL, O=Example Company, CN=strongSwan Root CA" --outform der > /etc/ipsec.d/cacerts/strongswanCert.der'
    run_command(gen_self_signed_rootCA)

    gen_public_key = 'ipsec pki --pub --in /etc/ipsec.d/private/vpnHostKey.der --type rsa | ipsec pki --issue --lifetime 930 --cacert /etc/ipsec.d/cacerts/strongswanCert.der --cakey /etc/ipsec.d/private/strongswanKey.der --dn "O=Example Company, CN=vpn.example.org" --san '+ server_ip + ' --flag serverAuth --flag ikeIntermediate --outform der > certs/vpnHostCert.der'
    run_command(gen_public_key)

    print_certificate = 'openssl x509 -inform DER -in /etc/ipsec.d/certs/vpnHostCert.der -noout -text'
    run_command(print_certificate)

    with open('/etc/ipsec.secrets', 'a') as outfile:
        outfile.write(': RSA vpnHostKey.der')

    print_ipsec_certs = 'ipsec listcerts'
    run_command(print_ipsec_certs)

def get_client_list():
    with open('./config/clients.csv', 'r') as f:
        clients = f.read()

    return clients

def create_client_certificate():
    #name, mac_addr, ip_addr
    clients = get_client_list()

    server_ip = clients[0].split(',')[2]

    for client in clients[1:]:
        name = client.split(',')[0]
        ip_addr = client.split(',')[2]
        client_config_dir = './config/' + name

        if not os.path.exists(client_config_dir):
            os.makedirs(client_config_dir)

        output_filename = client_config_dir + '/' + name
        ipsec_pki_gen = 'ipsec pki --gen --type rsa --size 2048 --outform der > ' + output_filename + 'Key.der'
        run_command(ipsec_pki_gen)

        chmod = 'chmod 600 ' + output_filename + 'Key.der'
        run_command(chmod)

        gen_public_key = 'ipsec pki --pub --in ' + output_filename + '.der' + ' --type rsa | ipsec pki --issue --lifetime 730 --cacert cacerts/strongswanCert.der --cakey private/strongswanKey.der --dn "C=NL, O=Example Company, CN=' + name + '@example.org" --san ' + ip_addr + ' --outform der > ' + output_filename + 'Cert.der'
        run_command(gen_public_key)

        private_pem = 'openssl rsa -inform DER -in ' + output_filename + '.der' + ' -out ' + output_filename + 'Key.pem -outform PEM'
        run_command(private_pem)

        cert_pem = 'openssl rsa -inform DER -in ' + output_filename + '.der' + ' -out ' + output_filename + 'Cert.pem -outform PEM'
        run_command(cert_pem)


def create_ipsec_conf(server_ip, client_ip, client_name):
    with open('ipsec.conf', 'w') as outfile:
        outfile.writelines('# ipsec.conf - strongSwan IPsec configuration file\n')
        outfile.write('config setup\n\n')

        outfile.write('conn %default\n')
        outfile.write('	ikelifetime=60m\n')
        outfile.write('	keylife=20m\n')
        outfile.write('	rekeymargin=3m\n')
        outfile.write('	keyingtries=1m\n')

        outfile.write('\n')

        outfile.write('conn home\n')
        outfile.write('	left=' + client_ip + '\n')
        outfile.write('	leftcert=' + client_name + '.pem' + '\n')
        outfile.write('	leftfirewall=yes\n')
        outfile.write('	leftconfig=%config\n')
        outfile.write('	right=' + server_ip + '\n')
        outfile.write('	rightsubnet=0.0.0.0/0\n')
        outfile.write('	auto=add\n')


def run_command(cmd):

    command = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    print(command.stdout.read())



