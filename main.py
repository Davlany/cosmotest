import telnetlib

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

response = tn.read_until(b"L",timeout=5)
tn.write(b"a \n")
response = tn.read_until(b"#",timeout=5)
tn.close()
print(response.decode("utf-8"))