__author__ = "kranonetka"


from datetime import datetime
import requests
import json
from bs4 import BeautifulSoup
import re
from multiprocessing import Pool
import diff


STEAMID64 = 77777777777777777 # Your SteamID64
LANGUAGE = "english"
COUNT = 5000


def exception_handler(exc: Exception):
	"""Just writes exceptions into file with timestamps"""
	with open("prices_errors.log", "a+") as file:
		file.write("[{time}] {error}\n".format(time=datetime.now().strftime("%d.%m %H:%M:%S"), error=exc))
	exit(-1)


def get_inventory_json(steamid64: int, language: str, count: int) -> dict:
	payload = {
		"l": language,
		"count": str(count)
	}
	page = requests.get(r"https://steamcommunity.com/inventory/"+str(steamid64)+r"/753/6", params=payload)
	return page.json()


def get_appids_with_cards(json_inventory: dict) -> list:
	app_ids = []
	for descr in json_inventory["descriptions"]:
		if descr["market_fee_app"] not in app_ids and descr["market_fee_app"] != 753:
			for tag in descr["tags"]:
				if tag["localized_category_name"] == "Item Type" and tag["localized_tag_name"] == "Trading Card":
					for tag in descr["tags"]:
						if tag["localized_category_name"] == "Card Border" and tag["localized_tag_name"] == "Normal":
							app_ids.append(descr["market_fee_app"])
							break
					break
	return app_ids


def get_app_price(appid: int) -> dict:
	exchange = requests.get(r"https://www.steamcardexchange.net/index.php?inventorygame-appid-"+str(appid))
	game_info = BeautifulSoup(exchange.text, "html.parser").find("div", {"id" : "inventory-game-info"})
	if game_info:
		print("got " + str(appid))
		return {
				"appid" : appid,
				"name" : game_info.contents[0].contents[1].contents[0].text,
				"price" : int(re.search(r"Worth: (\d+)c", game_info.contents[0].contents[2].text).group(1))
			}


def main():
	inventory = get_inventory_json(STEAMID64, LANGUAGE, COUNT)
	
	appids = get_appids_with_cards(inventory)

	with Pool() as pool:
		current_prices = [info for info in pool.map(get_app_price, appids) if info is not None]
	
	current_prices.sort(key=lambda e: (-e["price"], e["name"]))
	
	try:
		with open("prices.json", "r") as file:
			old_prices = json.load(file)
			price_diff = diff.get_diff(current_prices, old_prices)
			print(*price_diff.items(), sep="\n")
			with open("diff.json", "w+") as diff_file:
				json.dump(price_diff, diff_file, indent=4)
	except FileNotFoundError:
		pass
	with open("prices.json", "w+") as file:
			json.dump(current_prices, file, indent=4)


if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		exception_handler(e)
	sys.exit(0)