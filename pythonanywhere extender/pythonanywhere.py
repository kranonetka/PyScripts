__author__ = "kranonetka"


from datetime import datetime
import requests
from html.parser import HTMLParser
import sys


LOGIN = "login" # pythonanywhere.com login
PASSWORD = "password" # pythonanywhere.com password
TASK_ID = 111111 # Scheduled task ID


LOGIN_URL = "https://www.pythonanywhere.com/login/"
TASK_URL = "https://www.pythonanywhere.com/user/{}/schedule/task/{}/extend".format(LOGIN, TASK_ID)
WEB_APP_URL = "https://www.pythonanywhere.com/user/{}/webapps/{}.pythonanywhere.com/extend".format(LOGIN, LOGIN)


def handle_exception(err: Exception):
	with open("errors.err", "a+") as errors:
		errors.write("[{}] {}\n".format(datetime.now().strftime("%d.%m %H:%M:%S"), err))
	sys.exit(-1)


class csrfgetter(HTMLParser):
	def __init__(self, markup=""):
		self.csrfToken = None
		self._currentTag = None
		super().__init__()
		self.feed(markup)
	
	def handle_starttag(self, tag, attrs):
		if self.csrfToken is None:
			self._currentTag = tag
			attrs = dict(attrs)
			if tag == "input" and attrs.get("name") == "csrfmiddlewaretoken":
				self.csrfToken = attrs["value"]
	
	def handle_data(self, data):
		if self.csrfToken is None and self._currentTag == "script":
			i = data.find('Anywhere.csrfToken = "')
			if i != -1:
				i += 22
				self.csrfToken = data[i:i+64]
	

def login(login: str, password: str) -> requests.sessions.Session:
	session = requests.session()
	r = session.get(LOGIN_URL)
	csrfmiddlewaretoken = csrfgetter(r.text).csrfToken
	session.post(
		LOGIN_URL,
		headers={
			"Referer": LOGIN_URL
		},
		data={
			"csrfmiddlewaretoken": csrfmiddlewaretoken,
			"auth-username": login,
			"auth-password": password,
			"login_view-current_step": "auth"
		}
	)
	return session


def extend_task(session: requests.sessions.Session) -> None:
	r = session.get("https://www.pythonanywhere.com/user/{}/tasks_tab/".format(LOGIN))
	CSRFToken = csrfgetter(r.text).csrfToken
	r = session.post(
		TASK_URL,
		headers={
			"Referer": "https://www.pythonanywhere.com/user/{}/tasks_tab/".format(LOGIN),
			"X-CSRFToken": CSRFToken
			}
	)
	if r.headers.get("Content-Type") == "application/json":
		r = r.json()
		if r.get("status") != "success":
			raise Exception("[Update task] status != success. Response json: {}".format(r))
	else:
		raise Exception("[Update task] Server returns non json")


def extend_webapp(session: requests.sessions.Session) -> None:
	r = session.get("https://www.pythonanywhere.com/user/{}/webapps/".format(LOGIN))
	csrfmiddlewaretoken = csrfgetter(r.text).csrfToken
	session.post(
		WEB_APP_URL,
		headers={
			"Referer": "https://www.pythonanywhere.com/user/{}/webapps/".format(LOGIN)
		},
		data={
				"csrfmiddlewaretoken": csrfmiddlewaretoken
		}
	)


def main() -> None:
	auth_session = login(LOGIN, PASSWORD)
	extend_task(auth_session)
	extend_webapp(auth_session)


if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		handle_exception(e)
	sys.exit(0)
