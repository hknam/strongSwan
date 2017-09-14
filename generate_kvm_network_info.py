import random

def generate_random_mac_addr():
    mac = [0x00, 0x16, 0x3e,
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

def check(mac_list):
    unique_mac_list = list(set(mac_list))

    if len(mac_list) != len(unique_mac_list):
        return False
    else:
        return True


def main():

    mac_list = generate_unique_mac_list(generate_mac_list(255))


    ip_list = generate_ip_list(255)


    kvm_network_info = {}

    for count in range(len(ip_list)):
        kvm_network_info[ip_list[count]] = mac_list[count]


    for info in kvm_network_info.items():
        print(info)
if __name__ == "__main__":
    main()






