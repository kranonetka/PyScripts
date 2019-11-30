import socket
import random
import pickle
from base64 import b64encode
from helpers import *


def estable_connection() -> socket.socket:
	sock = socket.socket()
	sock.bind(("", 48777))
	sock.listen(1)
	print("Waiting for Bob...")
	connection, _ = sock.accept()
	print("Bob connected!")
	return connection


def main():
	connection = estable_connection()
	
	print("Generating your key...")
	alice_key = bytes(random.getrandbits(8) for _ in range(256))
	
	print(f"Your base64(key): {b64encode(alice_key).decode()}")
	
	print("Waiting encrypted deck from Bob...")
	bytestream = read_message(connection)
	encrypted_deck = pickle.loads(bytestream)
	
	print("Choosing 10 random cards...")
	chosen_cards = random.sample(encrypted_deck, 10)
	print("Chosen: {}".format(chosen_cards))
	
	print("Sending first 5 cards to Bob...")
	bytestream = pickle.dumps(chosen_cards[:5])
	send_message(connection, bytestream)
	
	print("Encrypting second 5 cards using your key...")
	alice_encrypted_cards = list(map(lambda x: transform(x, alice_key), chosen_cards[5:]))
	print("Your encrypted cards: {}".format(alice_encrypted_cards))
	
	print("Sending your encrypted cards to Bob...")
	bytestream = pickle.dumps(alice_encrypted_cards)
	send_message(connection, bytestream)
	
	print("Waiting from Bob decrypted cards...")
	bytestream = read_message(connection)
	alice_encrypted_cards = pickle.loads(bytestream)
	print("Your encrypted cards: {}".format(alice_encrypted_cards))
	alice_cards = list(map(lambda x: transform(x, alice_key), alice_encrypted_cards))
	alice_cards = list(map(lambda x: x.decode(), alice_cards))
	print("Your decrypted cards: {}".format(alice_cards))
	
	bytestream = pickle.dumps((alice_cards, alice_key))
	send_message(connection, bytestream)
	
	bytestream = read_message(connection)
	bob_cards, bob_key = pickle.loads(bytestream)
	print(f"Bob's cards: {bob_cards}\nBob's base64(key): {b64encode(bob_key).decode()}")
	

if __name__ == "__main__":
	main()
