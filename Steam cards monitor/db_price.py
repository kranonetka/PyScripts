__author__ = "kranonetka"


import prices
import pickle
from datetime import datetime
from multiprocessing import Pool
import sys


def exception_handler(exc: Exception):
	"""Just writes exceptions into file with timestamps""" 
	with open("db_prices_errors.err", "a+") as file:
		file.write("[{time}] {error}\n".format(time=datetime.now().strftime("%d.%m %H:%M:%S"), error=exc))
	sys.exit(-1)


def main() -> None:
	inventory = prices.get_inventory_json(prices.steamid64, prices.language, prices.count)
	
	apps_with_cards = prices.get_appids_with_cards(inventory)
	
	with Pool() as pool:
		current_prices = [info for info in pool.map(prices.get_app_price, apps_with_cards) if info is not None]
	
	with open("prices_db.pkl", "ab+") as file:
		pickle.dump((datetime.now(), current_prices), file)
		
	if len(sys.argv) == 2 and sys.argv[1] == "diff":
		extremums = {}
		with open("prices_db.pkl", "rb") as file:
			while True:
				try:
					dt, current_prices = pickle.load(file)
				except EOFError:
					break
				for info in current_prices:
					if info["appid"] not in extremums:
						extremums[info["appid"]] = {"diff" : 0, "min" : info["price"], "max" : info["price"], "name" : info["name"]}
					else:
						extremums[info["appid"]]["min"] = min(extremums[info["appid"]]["min"], info["price"])
						extremums[info["appid"]]["max"] = max(extremums[info["appid"]]["max"], info["price"])
						extremums[info["appid"]]["diff"] = extremums[info["appid"]]["max"] - extremums[info["appid"]]["min"]
		print(*sorted(extremums.items(), key=lambda e: e[1]["diff"]), sep="\n")


if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		exception_handler(e)
	sys.exit(0)