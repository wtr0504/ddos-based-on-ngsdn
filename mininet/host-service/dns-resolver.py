from dnslib import DNSRecord, RR, QTYPE, A
from dnslib.server import DNSServer, DNSHandler, BaseResolver, DNSLogger
# h2 python /mininet/host-service/dns-resolver.py &
class SimpleResolver(BaseResolver):
    def resolve(self, request, handler):
        reply = request.reply()
        qname = request.q.qname
        qtype = request.q.qtype
        
        if qtype == QTYPE.AAAA:
            reply.add_answer(RR(qname, QTYPE.AAAA, ttl=300, rdata=A('6:6:6'))) 
            print("reply AAAA")
        elif qtype == QTYPE.A:
            reply.add_answer(RR(qname, QTYPE.A, ttl=300, rdata=A('6.6.66.66')))  
            print("reply A")
        return reply

if __name__ == '__main__':
    resolver = SimpleResolver()
    logger = DNSLogger()
    server = DNSServer(resolver, port=53, address='2001:1:2::1', logger=logger)  
    server.start_thread()

    import time
    while True:
        time.sleep(1)
