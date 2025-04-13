import requests
import socket
import json
import geocoder

banner = '''
🔥 Location Tracker 2025 💪
Created by: BBoyRahul x Dark Cyber Don
'''
print(banner)

def get_ip():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    return IPAddr

def track(ip):
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url)
    data = json.loads(response.text)
    
    if data['status'] == 'success':
        print(f"IP Address: {data['query']}")
        print(f"Country: {data['country']}")
        print(f"Region: {data['regionName']}")
        print(f"City: {data['city']}")
        print(f"ISP: {data['isp']}")
        print(f"Latitude: {data['lat']}")
        print(f"Longitude: {data['lon']}")
    else:
        print("Invalid IP Address")

print("[🔍] Tracking Location...")

ip = input("Enter Victim IP Address: ")

if ip == "my":
    my_ip = get_ip()
    track(my_ip)
else:
    track(ip)
