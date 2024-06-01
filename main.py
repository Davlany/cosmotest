import telnetlib
import re

def expand_ranges(input_str):
    result = []
    parts = input_str.split(',')

    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            result.extend(range(start, end + 1))
        else:
            result.append(int(part))

    return ','.join(map(str, result))

def string_to_list(input_str):
    return [int(x) for x in input_str.split(',')]


print("connect")
tn = telnetlib.Telnet("10.6.50.38",23,timeout=5)
print("login")
response = tn.read_until(b"UserName:",timeout=5)

tn.write(b"smile\n")
print("password")

response = tn.read_until(b"Password:",timeout=5)

tn.write(b"xibypew\n")
print("in")
response = tn.read_until(b"#",timeout=5)

print("command")
tn.write(b"show vlan \n")


response = tn.read_until(b"#",timeout=5)


response_str = response.decode("utf-8")

vids = re.findall(r"VID\s+:\s+(\d+)", response_str)


vlan_info = re.findall(r"VID\s+:\s+(\d+).*?Untagged Ports\s+:\s*(.*?)(?:\n|$)", response_str, re.DOTALL)


vlan_dict = {}
nums = ['1','2','3','4','5','6','7','8','9']
for vid, untagged_ports in vlan_info:
    untagged_ports = untagged_ports.strip()
    if untagged_ports[0] in nums:
        ex = expand_ranges(untagged_ports)
        vlan_dict[vid] = string_to_list(ex)

print("VLAN Dictionary:", vlan_dict)

finalList = []

for vid, ports in vlan_dict.items():
    for port in ports:
        query = f"show fdb port {port}\n"
        tn.write(query.encode('utf-8'))
        res = tn.read_until(b"#",timeout=5)
        mac_address = re.search(r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", res.decode("utf-8"))
        if mac_address is None:
            finalList.append((vid,port,""))
        else:
            finalList.append((vid,port,mac_address.group(0)))

print(finalList)


tn.close()