__author__ = "kranonetka"

from functools import reduce
import os
import socket


def calc_checksum(packet: bytes) -> int:
	words = [int.from_bytes(packet[_:_+2], "big") for _ in range(0, len(packet), 2)]
	return 0xffff - reduce(lambda x, y: ((x + y) & 0xffff) + ((x + y) >> 16), words)


def test() -> None:
    """
    Для самопроверки отловил ICMP пакет в Wireshark,
    Заменил в нём байты контрольной суммы на нули
    """
    packet = \
    b"\x08\x00\x00\x00\x1c\x64\x7a\x69\x64\x41\x45\x63\x64\x57\x34\x65" \
	b"\x57\x7a\x65\x75\x73\x63\x79\x64"
    excepted = int.from_bytes(b"\x75\x19", "big") # Ожидаемая контрольная сумма
    checksum = calc_checksum(packet)
    if (checksum == excepted):
        print("ok")
    else:
        print("got", checksum, "but excepted", excepted)
	

def main() -> None:
	ICMP_TYPE = b"\x08"
	ICMP_CODE = b"\x00"
	ICMP_CHECKSUM = b"\x00\x00"
	ICMP_ID = (os.getpid() & 0xffff).to_bytes(2, "big")
	ICMP_ID = b"\xae\x58"
	ICMP_SEQ = b"\x7a\x69"
	ICMP_DATA = b"\x64\x41\x45\x63\x64\x57\x34\x65\x57\x7a\x65\x75\x73\x63\x79\x64"
	packet = bytearray(ICMP_TYPE + ICMP_CODE + ICMP_CHECKSUM + ICMP_ID + ICMP_SEQ + ICMP_DATA)
	checksum = calc_checksum(packet)
	checksum = checksum.to_bytes(2, "big")
	packet[2], packet[3] = checksum[0], checksum[1]
	packet = bytes(packet)	
	sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
	print(packet)
	while packet:
		sent = sock.sendto(packet, ("95.213.199.155", 1))
		packet = packet[sent:]
	reply, _ = sock.recvfrom(1024)
	reply = reply[20:]
	print("RESPONSE:")
	print("type", reply[0])
	print("code", reply[1])
	print("checksum", "0x" + "".join(hex(_)[2:] for _ in reply[2:4]))
	print("Identifier", int.from_bytes(reply[4:6], "big"), "0x" + "".join(hex(_)[2:] for _ in reply[4:6]))
	print("Sequence number", int.from_bytes(reply[6:8], "big"), "0x" + "".join(hex(_)[2:] for _ in reply[6:8]))
	print("data", reply[8:])


if __name__ == "__main__":
	try:
		#test()
		main()
	except KeyboardInterrupt:
		exit(0)