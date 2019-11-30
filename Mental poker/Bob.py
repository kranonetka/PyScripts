import socket
import random
import pickle
from base64 import b64encode
from helpers import *


def estable_connection() -> socket.socket:
	sock = socket.socket()
	print("Connecting to Alice...")
	sock.connect(("localhost", 48777))
	print("Connected!")
	return sock


def main():
	connection = estable_connection()
	
	print("Generating your key...")
	bob_key = bytes(random.getrandbits(8) for _ in range(256))
	
	print(f"Your base64(key): {b64encode(bob_key).decode()}")
	
	print("Shuffling the deck...")
	deck = get_deck()
	random.shuffle(deck)
	print("Shuffled deck: {}".format(deck))
	
	print("Encrypting deck...")
	encrypted_deck = list(map(lambda x: transform(x, bob_key), map(lambda x: x.encode(), deck)))
	
	print("Sending encrypted deck to Alice...")
	bytestream = pickle.dumps(encrypted_deck)
	send_message(connection, bytestream)
	
	print("Waiting your own 5 cards from Alice...")
	bytestream = read_message(connection)
	bob_cards = pickle.loads(bytestream)
	print("Your encrypted cards: {}".format(bob_cards))
	bob_cards = list(map(lambda x: transform(x, bob_key), bob_cards))
	bob_cards = list(map(lambda x: x.decode(), bob_cards))
	print("Your decrypted cards: {}".format(bob_cards))
	
	print("Waiting Alice's own 5 cards...")
	bytestream = read_message(connection)
	alice_cards = pickle.loads(bytestream)
	
	print("Sending Alice's decrypted cards back...")
	alice_cards = list(map(lambda x: transform(x, bob_key), alice_cards))
	bytestream = pickle.dumps(alice_cards)
	send_message(connection, bytestream)
	
	bytestream = read_message(connection)
	alice_cards, alice_key = pickle.loads(bytestream)
	print(f"Alice's cards: {alice_cards}\nAlice's base64(key): {b64encode(alice_key).decode()}")
	
	bytestream = pickle.dumps((bob_cards, bob_key))
	send_message(connection, bytestream)
	

if __name__ == "__main__":
	main()
