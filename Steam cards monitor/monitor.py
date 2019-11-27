__author__ = "kranonetka"


from datetime import datetime
import vk_api
import requests
import json
from bs4 import BeautifulSoup
from random import getrandbits
import re
import sys
from threading import Thread
import prices


MAX_MSG_LEN = 4096

VER = "5.95" # VK API Version
RECEIVER_ID = "1" # Id of VK user for receiving notifications
APPID = 100 # Id of Steam game
ACCESS_TOKEN = "xa21..." # VK Group access token


def exception_handler(exc: Exception) -> None:
	"""Just writes exceptions into file with timestamps""" 
	with open("monitor_errors.err", "a+") as file:
		file.write("[{time}] {error}\n".format(time=datetime.now().strftime("%d.%m %H:%M:%S"), error=exc))
	sys.exit(-1)

	
def get_all_cards() -> list:
	page = requests.get(r"https://www.steamcardexchange.net/index.php?inventorygame-appid-" + str(APPID))
	return BeautifulSoup(page.text, "html.parser").findAll("div", {"class": "inventory-game-card-item"})


def get_prev_cards():
	try:
		with open("cards.json", "r") as file:
			prev_cards = json.load(file)
	except FileNotFoundError:
		prev_cards = None
	return prev_cards
	

def notify(cards: list) -> None:
	if len(cards) == 0:
		msg = "No cards available"
	else:
		thread = Thread(target=prices.main)
		thread.start()
		thread.join()
		with open("prices.json", "r") as file:
			gamelist = json.load(file)
		msg = "Your cards worth:\n{}\n".format(
			"\n".join(
				"price: {} - {}({})".format(game["price"], game["name"], game["appid"]) for game in gamelist
			)
		)
		msg += "Available cards:\n{}".format(
			"\n".join(
				"(x{}) {}: {}".format(card["count"], card["name"], card["href"]) for card in cards
			)
		)
	
	bot_session = vk_api.VkApi(token=ACCESS_TOKEN, api_version=VER)
	bot_api = bot_session.get_api()
	for part in [msg[i:i+MAX_MSG_LEN] for i in range(0,len(msg),MAX_MSG_LEN)]:
		bot_api.messages.send(
			user_id				=	RECEIVER_ID,
			message				=	part,
			random_id			=	getrandbits(32),
			dont_parse_links	=	True
		)


def main():
	cards = get_all_cards()
	current_cards = [
						{
							"name": card.contents[0].contents[1].text,
							"count": int(re.match(r"Stock: (\d+)", card.contents[1].contents[0].text).group(1)),
							"href": card.contents[1].contents[3].contents[0]["href"]
						}
						for card in cards if re.match(r"Stock: \d+", card.contents[1].contents[0].text) and int(re.match(r"Stock: (\d+)", card.contents[1].contents[0].text).group(1)) > 1
					]
	
	prev_cards = get_prev_cards()
	
	if prev_cards is None or current_cards != prev_cards:
		notify(current_cards)
		with open("cards.json", "w+") as file:
			json.dump(current_cards, file, indent=4)


if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		exception_handler(e)
	sys.exit(0)