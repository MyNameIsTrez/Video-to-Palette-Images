import sys

import cv2
from PIL import Image


def main():
	if len(sys.argv) != 5:
		raise ValueError("usage: python main.py <video path> <image name> <integer resized width> <integer resized height>")

	vidcap = cv2.VideoCapture(sys.argv[1])

	palette_image = Image.open("palette.bmp")

	frame_index = 0
	while True:
		success, cv2_image_bgr = vidcap.read()
		if not success:
			break

		cv2_image_rgb = cv2.cvtColor(cv2_image_bgr, cv2.COLOR_BGR2RGB)
		pil_image_rgb = Image.fromarray(cv2_image_rgb)

		pil_image_rgb = pil_image_rgb.resize((int(sys.argv[3]), int(sys.argv[4])), Image.ANTIALIAS)

		pil_image_palette = pil_image_rgb.convert(mode="RGB").quantize(palette=palette_image, dither=False)

		pil_image_palette.save("output-frames/{}{:03}.png".format(sys.argv[2], frame_index))

		frame_index += 1


if __name__ == "__main__":
	main()
