from lxml import etree
import subprocess

def get_client_info():
    config = './config/clients.csv'

    with open(config, 'r') as reader:
        clients = reader.read().split('\n')

    return clients

def get_client_mac():
    clients = get_client_info()
    macs = []
    for client in clients[:-1]:
        name = client.split(',')[0]
        grep_mac = 'virsh dumpxml ' + name + ' | grep -i "<mac"'
        mac = str(run_command(grep_mac)).split('=')[1].split('/')[0]
        mac = mac.replace("'", "")
        #print(name, mac)
        macs.append(mac)
    return macs

def run_command(cmd):
    command = subprocess.Popen(cmd, stdout = subprocess.PIPE, shell=True)
    output = command.communicate()
    return output[0]

def add_mac_info():
    clients = get_client_info()
    macs = get_client_mac()
    config = './config/clients.csv'

    with open(config, 'w') as writer:
        for index in range(len(macs)):
            client = clients[index].replace('\n', '')
            writer.write(client +',' +  macs[index] + '\n')

def make_xml():
    network = etree.Element('network')

    name = etree.Element('name')
    name.text = 'default'
    network.append(name)

    forward = etree.Element("forward", mode="nat")
    bridge = etree.Element("brigde", name="virbr0", stp="on", delay="0")
    mac = etree.Element("mac", address="52:54:00:ca:6a:d7")
    ip = etree.Element("ip", address="192.168.122.1", netmask="255.255.255.0")

    dhcp = etree.SubElement(ip, 'dhcp')
    clients = get_client_info()


    #name,ip_addr,mac_addr
    start_ip_addr = clients[0].split(',')[1]
    #end : \n
    end_ip_addr = clients[-2].split(',')[1]

    range = etree.SubElement(dhcp, 'range', end=end_ip_addr, start=start_ip_addr)

    for client in clients[:-2]:
        line = client.split(',')
        name = line[0]
        mac_addr = line[2]
        ip_addr = line[1]

        etree.SubElement(dhcp, 'host', mac=mac_addr, name=name, ip=ip_addr)



    #client01 = etree.SubElement(dhcp, 'host', mac='52:54:00:a0:cc:19', name='client01', ip='192.168.122.2')
    #client02 = etree.SubElement(dhcp, 'host', mac='00:16:3e:26:a5:83', name='client02', ip='192.168.122.3')

    network.append(forward)
    network.append(bridge)
    network.append(mac)
    network.append(ip)

    xml = etree.tostring(network, pretty_print=True)

    tree = etree.ElementTree(network)
    tree.write("./config/default.xml")


def apply_xml():
    define = 'virsh net-define ./config/default.xml'
    print(run_command(define))

    start = 'virsh net-start default'
    print(run_command(start))


def main():
    get_client_mac()
    make_xml()
    apply_xml()



if __name__ == '__main__':
    main()