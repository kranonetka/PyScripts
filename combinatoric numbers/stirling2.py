__author__ = "kranonetka"


def s2(n, k):
	if k == 0 or n == 0:
		return 0
	if k == n:
		return 1
	return s2(n - 1, k - 1) + (k * s2(n - 1, k))
	
n = int(input("n == "))
k = int(input("k == "))
print("s2(n, k)", s2(n, k))