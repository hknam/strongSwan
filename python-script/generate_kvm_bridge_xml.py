
from lxml import etree

network = etree.Element('network')

name = etree.Element('name')
name.text = 'default'
network.append(name)

forward = etree.Element("forward", mode="nat")
bridge = etree.Element("brigde", name="virbr0", stp="on", delay="0")
mac = etree.Element("mac", address="52:54:00:ca:6a:d7")
ip = etree.Element("ip", address = "192.168.122.1", netmask = "255.255.255.0")

dhcp = etree.SubElement(ip, 'dhcp')
range = etree.SubElement(dhcp, 'range', end='192.168.122.254', start='192.168.122.2')
client01 = etree.SubElement(dhcp, 'host', mac='52:54:00:a0:cc:19', name='client01', ip='192.168.122.2')
client02 = etree.SubElement(dhcp, 'host', mac='00:16:3e:26:a5:83', name='client02', ip='192.168.122.3')

network.append(forward)
network.append(bridge)
network.append(mac)
network.append(ip)

xml = etree.tostring(network, pretty_print=True)

tree = etree.ElementTree(network)
tree.write("test.xml")