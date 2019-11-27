__author__ = "kranonetka"


import requests


def login_with_password(login: str, password: str) -> requests.sessions.Session:
	"""Авторизация для старых аккаунтов, где используется связка логин+пароль
	:param login: Логин (email или телефон) для авторизации
	:type login: str
	:param password: Пароль для авторизации
	:type password: str
	
	:return: Авторизованная сессия
	:rtype: requests.sessions.Session
	"""
	session = requests.Session()
	
	# Получаем CSRF токен в cookies для дальнейшей работы
	response = session.get('https://auth.auto.ru/login/')
	
	# Дублируем CSRF токен из cookies в заголовок x-csrf-token,
	# чтобы не передавать его вручную при каждом запросе
	CSRF_token = response.cookies['_csrf_token']
	session.headers.update({"x-csrf-token": CSRF_token})
	
	json_for_login = {
		"items": [
			{
				"path": "auth/login",
				"params": {
					"login": login,
					"password": password
				}
			}
		]
	}
	# Авторизируемся
	session.post("https://auth.auto.ru/-/ajax/auth/", json=json_for_login)
	
	return session # Возвращаем авторизованную сессию


def login_with_email(email: str) -> requests.sessions.Session:
	"""Авторизация для новых аккаунтов, где используется связка почта+код с почты
	:param email: Email для авторизации
	:type login: str
	
	:return: Авторизованная сессия
	:rtype: requests.sessions.Session
	"""
	session = requests.Session()
	
	# Получаем CSRF токен в cookies для дальнейшей работы
	response = session.get('https://auth.auto.ru/login/') 
	
	# Дублируем CSRF токен из cookies в заголовок x-csrf-token,
	# чтобы не передавать его вручную при каждом запросе
	CSRF_token = response.cookies['_csrf_token']
	session.headers.update({"x-csrf-token": CSRF_token})
	
	json_for_code = {
		"items": [
			{
				"path": "auth/login-or-register",
				"params": {
					"email": email
				}
			}
		]
	}
	# Отправляем серверу запрос, чтобы он отправил
	# нам почту email 6-ти значный код
	session.post("https://auth.auto.ru/-/ajax/auth/", json=json_for_code)

	# Тут любым образом достаёте этот код с почты
	# ...
	
	json_for_login = {
		"items": [
			{
				"path": "user/confirm",
				"params": {
					"email": email,
					"code": "666666" # 6-ти значный код с почты
				}
			}
		]
	}
	# Авторизируемся
	session.post("https://auth.auto.ru/-/ajax/auth/", json=json_for_login)
	
	return session # Возвращаем авторизованную сессию