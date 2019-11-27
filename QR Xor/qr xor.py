__author__ = "kranonetka"


import sys


def decrypt(size: int, bits_per_pixel: int) -> None:
	with open("qr.enc.bmp", "rb") as fp:
		data = fp.read()
	
	key = bytearray()
	key += bytes(a ^ b for a,b in zip(data[ 0: 2], b"\x42\x4d")) # Signature (should be 0x424D)
	key += bytes(a ^ b for a,b in zip(data[ 2: 6], (691254).to_bytes(4, "little"))) # File size 691254 // horizontal resolution
	key += bytes(a ^ b for a,b in zip(data[ 6:10], (0).to_bytes(4, "little"))) # Reserved  // vertical resolution
	key += bytes(a ^ b for a,b in zip(data[10:14], (54).to_bytes(4, "little"))) # Offset to start of image data // Number of colors in image
	key += bytes(a ^ b for a,b in zip(data[14:18], (40).to_bytes(4, "little"))) # size of BITMAPINFOHEADER structure, must be 40 // Number of important colors
	key += bytes(a ^ b for a,b in zip(data[18:22], (size).to_bytes(4, "little"))) # image width in pixels
	key += bytes(a ^ b for a,b in zip(data[22:26], (size).to_bytes(4, "little"))) # image height in pixels
	key += bytes(a ^ b for a,b in zip(data[26:28], (1).to_bytes(2, "little"))) # Number of planes, must be 1
	key += bytes(a ^ b for a,b in zip(data[28:30], (bits_per_pixel).to_bytes(2, "little"))) # Number of bits per pixel(1, 4, 8, or 24)
	key += bytes(a ^ b for a,b in zip(data[30:34], (0).to_bytes(4, "little"))) # compression type(0=none, 1=RLE-8, 2=RLE-4)
	key += bytes(a ^ b for a,b in zip(data[34:36], (35840).to_bytes(2, "little"))) # Low bytes of size of image data in bytes (high is 0x0A00)

	new_data = bytes(map(lambda ie: ie[1]^key[ie[0] % len(key)], enumerate(data)))
	with open(f"qr.dec{bits_per_pixel}_{size}x{size}.bmp", "wb+") as fp:
		fp.write(new_data)


def main():
	decrypt(480, 24)
	
	
if __name__ == "__main__":
	main()
	sys.exit(0)