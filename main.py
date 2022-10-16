import sys

import cv2
from PIL import Image
from PIL import ImageFilter

import numpy


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

		# TODO: Is Image.NEAREST the best for green screens?
		pil_image_rgb = pil_image_rgb.resize((int(sys.argv[3]), int(sys.argv[4])), Image.NEAREST)

		pil_image_rgb = replace_green_screen_with_purple_screen(cv2.cvtColor(numpy.array(pil_image_rgb), cv2.COLOR_RGB2BGR))

		pil_image_palette = pil_image_rgb.convert(mode="RGB").quantize(palette=palette_image, dither=False)

		pil_image_palette.save("output-frames/{}{:03}.png".format(sys.argv[2], frame_index))

		frame_index += 1


# Source of and documentation for this function:
# https://stackoverflow.com/a/72279520/13279557
def replace_green_screen_with_purple_screen(img):
	lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
	a_channel = lab[:,:,1]
	th = cv2.threshold(a_channel,127,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
	masked = cv2.bitwise_and(img, img, mask = th)    # contains dark background
	m1 = masked.copy()
	m1[th==0]=(255,0,255)                          # contains white background

	mlab = cv2.cvtColor(masked, cv2.COLOR_BGR2LAB)
	dst = cv2.normalize(mlab[:,:,1], dst=None, alpha=0, beta=255,norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

	threshold_value = 100
	dst_th = cv2.threshold(dst, threshold_value, 255, cv2.THRESH_BINARY_INV)[1]

	mlab2 = mlab.copy()
	mlab[:,:,1][dst_th == 255] = 127

	img2 = cv2.cvtColor(mlab, cv2.COLOR_LAB2RGB)
	img2[th==0]=(255,0,255)

	pil_image_rgb = Image.fromarray(img2)
	return pil_image_rgb


if __name__ == "__main__":
	main()
