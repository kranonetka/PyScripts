__author__ = "kranonetka"


from datetime import datetime
import requests
import json
from bs4 import BeautifulSoup
import prices
from multiprocessing import Pool


def get_diff(new_prices: list, old_prices: list) -> dict:
	new_prices_ = {info["appid"]: {"name" : info["name"], "price": info["price"]} for info in new_prices}
	old_prices_ = {info["appid"]: {"name" : info["name"], "price": info["price"]} for info in old_prices}
	
	intersect = new_prices_.keys() & old_prices_.keys()
	
	diff = {
		appid : {
			"diff" : "{:+}".format(new_prices_[appid]["price"] - old_prices_[appid]["price"]),
			"name" : new_prices_[appid]["name"]
		}
		for appid in intersect if new_prices_[appid]["price"] - old_prices_[appid]["price"] != 0
	}
	
	return diff

	
def main() -> None:
	inventory = prices.get_inventory_json(prices.steamid64, prices.language, prices.count)
	
	apps_with_cards = prices.get_appids_with_cards(inventory)
	
	with Pool() as pool:
		new_prices = [info for info in pool.map(prices.get_app_price, apps_with_cards) if info is not None]

	with open("prices.json", "r") as prices_file:
		old_prices = json.load(prices_file)
	
	price_diff = get_diff(new_prices, old_prices)
	print(*price_diff.items(), sep="\n")
	
	
if __name__ == "__main__":
	main()
	sys.exit(0)