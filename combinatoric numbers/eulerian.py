__author__ = "kranonetka"


def e(n: int, m: int) -> int:
	if n == 0:
		return int(m == 0)
	return (m + 1) * e(n - 1, m) + ((n - m )* e(n - 1, m - 1))
	
n = int(input("n == "))
m = int(input("m == "))
print("e(n, m)", e(n, m))