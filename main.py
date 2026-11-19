from scapy.all import sniff, wrpcap, IP, TCP, UDP, Raw

PACKET_COUNT = 30   # stop after this many packets...
TIMEOUT = 60        # ...or after this many seconds
PROTOCOLS = {1: "ICMP", 6: "TCP", 17: "UDP"}   # IP protocol number -> name


def show(packet):
    """Scapy calls this function once for every captured packet."""
    # Some packets (ARP, IPv6...) have no IP layer, so skip them
    if not packet.haslayer(IP):
        return

    ip = packet[IP]   # the IP layer: it holds the source, destination and protocol
    protocol = PROTOCOLS.get(ip.proto, f"other ({ip.proto})")

    print("-" * 60)
    print(f"Source IP      : {ip.src}")
    print(f"Destination IP : {ip.dst}")
    print(f"Protocol       : {protocol}")

    # TCP and UDP packets also carry port numbers
    if packet.haslayer(TCP):
        print(f"Ports          : {packet[TCP].sport} -> {packet[TCP].dport}")
    elif packet.haslayer(UDP):
        print(f"Ports          : {packet[UDP].sport} -> {packet[UDP].dport}")

    # The structure of the packet, layer by layer
    print(f"Layers         : {packet.summary()}")

    # The payload (the actual data) lives in the Raw layer, if the packet has one
    if packet.haslayer(Raw):
        payload = bytes(packet[Raw].load)
        print(f"Payload        : {len(payload)} bytes, starts with {payload[:40]!r}")
    else:
        print("Payload        : none")


if __name__ == "__main__":
    print(f"Sniffing up to {PACKET_COUNT} packets ({TIMEOUT}s max). Open a website to create traffic...")
    packets = sniff(prn=show, count=PACKET_COUNT, timeout=TIMEOUT)

    wrpcap("capture.pcap", packets)   # save the capture so Wireshark can open it
    print(f"\nDone. Captured {len(packets)} packets, saved to capture.pcap")