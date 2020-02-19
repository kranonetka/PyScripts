import requests
from bs4 import BeautifulSoup as BS


DEBUG = False

LOGIN_URL = r"https://bipgame.io/public/users/login?online&domain=academy.galaxy.bipgame.io"
LOGIN = "login"
PASSWORD = "passwd"
API_URL = "https://academy.galaxy.bipgame.io/api"


def getAuthSession(login: str, password: str) -> requests.Session:
	api_session = requests.Session()
	
	if DEBUG:  # Enabling local proxy for intercepting
		requests.packages.urllib3.disable_warnings()
		api_session.proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
		api_session.verify = False
	
	api_session.get("https://bipgame.io/")  # Get cookies
	
	redirect = api_session.post(
		LOGIN_URL,
		data={"purse": LOGIN, "password": PASSWORD},
		headers={"X-Requested-With": "XMLHttpRequest"}
	).json()["redirect"]  # Get redirect url
	
	resp = api_session.get(redirect)  # Getting laravel_token & page with CSRF token
	
	# Getting CSRF token
	CSRF_TOKEN = BS(resp.text, "html.parser").find("meta", {"name": "csrf-token"}).get("content")
	
	# Adding necessary headers for API
	api_session.headers.update({"X-CSRF-TOKEN": CSRF_TOKEN, "X-Requested-With": "XMLHttpRequest"})
	
	return api_session


if __name__ == "__main__":
	session = getAuthSession(LOGIN, PASSWORD)
	
	# Example session usage
	resp = session.get(API_URL + "/planet/")
	print(resp.text)
	
	resp = session.get(API_URL + "/upgrade/2799542")
	print(resp.text)
