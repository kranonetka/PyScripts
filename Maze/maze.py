__author__ = "kranonetka"

import socket
import sys
import multiprocessing
import queue


ip = "maze.training.hackerdom.ru"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)


directions = {
	b"right":	1,
	b"down":	256,
	b"left":	-1,
	b"up":		-256
}


def visit(port: int, password: bytes, ports_queue: multiprocessing.Queue) -> None:
	for _ in range(3):
		try:
			sock.sendto(password, (ip, port))
			reply = sock.recv(1024)
		except socket.timeout:
			continue
		else:
			break
	else:
		print(f"Failed {port} {password}")
		return
	#print(reply.decode())
	if b"RUCTF" in reply:
			print(reply.decode())
	reply = b"\n".join(reply.split(b"\n")[1:]).replace(b"(port 1280) ", b"").replace(b"(port 1025) ", b"")
	for line in reply.split(b"\n"):
		tokens = line.split(b" ")
		ports_queue.put((port + directions[tokens[3]], tokens[6]))


def solve(init_port: int, password: bytes) -> set:
	visited = set()
	ports_queue = multiprocessing.Queue()
	ports_queue.put((init_port, password))
	while True:
		try:
			current = ports_queue.get(timeout=6)
		except queue.Empty:
			break
		if current[0] not in visited:
			proc = multiprocessing.Process(target=visit, args=(*current, ports_queue, solutions))
			proc.daemon = True
			proc.start()
			visited.add(current[0])
	print(f"Visited ports: {visited}")


def main():
	solve(1024, b"3k8bbz032mrap75c8iz8tmi7f4ou00")
	
	
if __name__ == "__main__":
	main()
	sys.exit(0)
