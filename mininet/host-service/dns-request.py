import socket
from dnslib import DNSRecord
# h1 python /mininet/host-service/dns-request.py
def query_dns_server(query_name, server_address, query_type):
    q = DNSRecord.question(query_name, query_type)
    server = (server_address, 53)
    
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.settimeout(3)
    
    try:
        sock.sendto(q.pack(), server)
        response, _ = sock.recvfrom(1024)
        print(DNSRecord.parse(response))
    except socket.timeout:
        print("Request timed out")
    finally:
        sock.close()

if __name__ == '__main__':
    for _ in range(10):
        query_dns_server('example.com', '2001:1:2::1', 'AAAA')  
        query_dns_server('example.com', '2001:1:2::1', 'A')     
