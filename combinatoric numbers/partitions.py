__author__ = "kranonetka"


def p(n: int, k: int) -> int:
	if n == k == 0:
		return 1
	if n > 0 and k == 0:
		return 0
	if k <= n:
		return p(n, k - 1) + p(n - k, k)
	else:
		return p(n, n)

while True:
	n = int(input("n == "))
	print("p(n, n)", p(n, n))
	k = int(input("k == "))
	print("p(n, k)", p(n, k))