import subprocess

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

def create_ipsec_conf():
    with open('ipsec.conf', 'w') as outfile:
        outfile.writelines('# ipsec.conf - strongSwan IPsec configuration file\n')
        outfile.write('config setup\n\n')

        outfile.write('conn %default\n')
        outfile.write('	ikelifetime=60m\n')
        outfile.write('	keylife=20m\n')
        outfile.write('	rekeymargin=3m\n')
        outfile.write('	keyingtries=1m\n')


def run_command(cmd):

    command = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    print(command.stdout.read())



