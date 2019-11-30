import socket


def get_deck() -> list:
	deck = [card + " " + suit
		for suit in ("Spades", "Hearts", "Diamonds", "Clubs")
			for card in ("Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King")
	]
	return deck


def transform(card: bytes, key: bytes) -> bytes:
	"""Encrypt/decrypt encoded card name using key"""
	return bytes(byte ^ key[i%len(key)] for i, byte in enumerate(card))


def readexactly(connection: socket.socket, bytes_count: int):
	"""Reads bytes_count bytes from connection
	
	thanks to andreymal https://ru.stackoverflow.com/a/982881/324059
	"""
	b = bytearray()
	while len(b) < bytes_count:
		part = connection.recv(bytes_count - len(b))
		if not part:
			raise IOError("Connection closed")
		b += part
	return bytes(b)


def read_message(connection: socket.socket):
	"""Simple Chunked transfer encoding mechanism implementation
	
	thanks to andreymal https://ru.stackoverflow.com/a/982881/324059
	"""
	b = bytearray()
	while True:
		part_len = int.from_bytes(readexactly(connection, 2), "big")
		if part_len == 0:
			break
		b += readexactly(connection, part_len)
	return bytes(b)


def send_message(connection: socket.socket, msg: bytes):
	"""Simple Chunked transfer encoding mechanism implementation
	
	thanks to andreymal https://ru.stackoverflow.com/a/982881/324059
	"""
	for chunk in (msg[i:i+65535] for i in range(0, len(msg), 65535)):
		connection.send(len(chunk).to_bytes(length=2, byteorder="big"))
		connection.send(chunk)
	connection.send(b"\x00\x00")