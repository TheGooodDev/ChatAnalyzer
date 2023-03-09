from scapy.all import *
from scapy.layers.inet import TCP


# Define a function to capture and process packets
def process_packet(packet):
    if packet.haslayer(TCP) and packet.haslayer(Raw):
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport
        if dst_port == 5555 and 'POST' in str(packet[TCP].payload):
            # Dofus chat message found
            chat_message = str(packet[TCP].payload)
            # Extract the chat message from the payload
            chat_message = chat_message.split('\\r\\n')[-1].strip()
            print(chat_message)

# Start capturing packets
sniff(filter='tcp', prn=process_packet)
