__author__ = "kranonetka"


def s1(n, k):
	if n == k == 0:
		return 1
	if n == 0 or k == 0:
		return 0
	return s1(n - 1, k - 1) + ((n - 1) * s1(n - 1, k))
	
n = int(input("n == "))
k = int(input("k == "))
print("s1(n, k)", s1(n, k))