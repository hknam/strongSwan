import random
import subprocess
import sys

def generate_random_mac_addr():
    mac = [0x52, 0x54, 0x00,
    random.randint(0x00, 0x7f),
    random.randint(0x00, 0xff),
    random.randint(0x00, 0xff)]

    return ':'.join(map(lambda x: "%02x" % x, mac))


def generate_unique_mac_list(mac_list):
    if not check(mac_list):
        unique_mac_list = list(set(mac_list))
        diff = len(mac_list) - len(unique_mac_list)

        unique_mac_list.append(generate_mac_list(diff))

        generate_unique_mac_list(unique_mac_list)

    else:
        return mac_list


def generate_ip_list(count):
    base_ip = "192.168.122."

    ip_list = []
    for count in range(1, count):
        ip = base_ip + str(count)
        ip_list.append(ip)

    return ip_list

def generate_mac_list(count):
    mac_list = []
    for count in range(count):
        mac_list.append(generate_random_mac_addr())

    return mac_list

def generate_clone_list(count, ip_list, mac_list):
    clone_list = {}
    clone_list['server'] = ip_list[0] + '/' + mac_list[0]

    for index in range(1, count-1):
        clone_list['client'+str(index)] = ip_list[index] + '/' + mac_list[index]


    return clone_list

def check(mac_list):
    unique_mac_list = list(set(mac_list))

    if len(mac_list) != len(unique_mac_list):
        return False
    else:
        return True


def run_virt_clone(kvm_image_list):

    for kvm in kvm_image_list:
        new_image_name = kvm[0]

        command = 'virt-clone --original base-image --name ' + new_image_name + ' --file ../images/' + new_image_name + '.img'

        run_command = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

        print(run_command.stdout.read())




def main():

    try:
        number_of_client = int(sys.argv[1])
    except IndexError as e:
        print('NEED CLIENT COUNT')
        sys.exit(1)

    mac_list = generate_unique_mac_list(generate_mac_list(number_of_client))
    ip_list = generate_ip_list(number_of_client)

    kvm_image_list = generate_clone_list(number_of_client, mac_list, ip_list)

    run_virt_clone(kvm_image_list.items())

    '''
    kvm_network_info = {}

    for count in range(len(ip_list)):
        kvm_network_info[ip_list[count]] = mac_list[count]


    for info in kvm_network_info.items():
        print(info)
    '''



if __name__ == "__main__":
    main()






