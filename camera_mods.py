#-------------------------------------------------------------------------------
# Name:        Capture JPG from Raspberry Pi Camera
# Purpose:      to utilise the raspberry pi camera to take a photo
#				and if the output file already exists, delete,
#				and then save to disk.
#
# Examples taken from http://picamera.readthedocs.org/en/release-1.10/recipes1.html
#
# Author:      benva
#
# Created:     20/01/2016
# Copyright:   (c) benva 2016
#-------------------------------------------------------------------------------

import os
import picamera
import time

# Define Variables
output_img = 'image'
output_vid = 'video'
extension_img = '.jpg'
extension_vid = '.h264'


def option1():
	with picamera.PiCamera() as camera:
		camera.resolution = (1024, 768)
		camera.start_preview()
		# Camera warm-up time
		time.sleep(2)
		if os.path.exists(output_img+extension_img):
			os.remove(output_img+extension_img)
		camera.capture(output_img+extension_img)


def option2():
	# Explicitly open a new file called my_image.jpg
	my_file = open(output_img+extension_img, 'wb')
	with picamera.PiCamera() as camera:
        camera.start_preview()
        time.sleep(2)
        camera.capture(my_file)
	# At this point my_file.flush() has been called, but the file has
	# not yet been closed
	my_file.close()


def option3():
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        camera.capture(output_img+extension_img, resize=(320, 240))


def option4():
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        camera.framerate = 30
        # Wait for the automatic gain control to settle
        time.sleep(2)
        # Now fix the values
        camera.shutter_speed = camera.exposure_speed
        camera.exposure_mode = 'off'
        g = camera.awb_gains
        camera.awb_mode = 'off'
        camera.awb_gains = g
        # Finally, take several photos with the fixed settings
        camera.capture_sequence(['image%02d.jpg' % i for i in range(10)])


def option5():
	def continuous():
        with picamera.PiCamera() as camera:
            camera.start_preview()
            time.sleep(2)
            for filename in camera.capture_continuous('img{counter:03d}.jpg'):
                print('Captured %s' % filename)
                time.sleep(30) # wait 0.5 minute
	def capture_at_time():
		from datetime import datetime, timedelta
		def wait():
            # Calculate the delay to the start of the next hour
            next_hour = (datetime.now() + timedelta(hour=1)).replace(
                minute=0, second=0, microsecond=0)
            delay = (next_hour - datetime.now()).seconds
            time.sleep(delay)

		with picamera.PiCamera() as camera:
            camera.start_preview()
            wait()
            for filename in camera.capture_continuous('img{timestamp:%Y-%m-%d-%H-%M}.jpg'):
                print('Captured %s' % filename)
                wait()

	timelapse = raw_input('Continuous [1] or On the Hour [2]:\n')

	if timelapse == '1':
		continuous()
	elif timelapse == '2':
		capture_at_time()
	else:
		option5()


def option6():
    from time import sleep
    from fractions import Fraction

    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        # Set a framerate of 1/6fps, then set shutter
        # speed to 6s and ISO to 800
        camera.framerate = Fraction(1, 6)
        camera.shutter_speed = 6000000
        camera.exposure_mode = 'off'
        camera.iso = 800
        # Give the camera a good long time to measure AWB
        # (you may wish to use fixed AWB instead)
        sleep(10)
        # Finally, capture an image with a 6s exposure. Due
        # to mode switching on the still port, this will take
        # longer than 6 seconds
        camera.capture('dark.jpg')


def option7():
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.start_recording(output_vid+extension_vid)
        camera.wait_recording(60)
        camera.stop_recording()


def option8():
	stream = io.BytesIO()
	with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.start_recording(stream, format='h264', quality=23)
        camera.wait_recording(15)
        camera.stop_recording()


def option9():
	with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        for filename in camera.record_sequence(
                '%d.h264' % i for i in range(1, 11)):
            camera.wait_recording(5)


def option10():
    from PIL import Image
    from time import sleep

    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        camera.framerate = 24
        camera.start_preview()

        # Load the arbitrarily sized image
        img = Image.open('overlay.png')
        # Create an image padded to the required size with
        # mode 'RGB'
        pad = Image.new('RGB', (
            ((img.size[0] + 31) // 32) * 32,
            ((img.size[1] + 15) // 16) * 16,
            ))
        # Paste the original image into the padded one
        pad.paste(img, (0, 0))

        # Add the overlay with the padded image as the source,
        # but the original image's dimensions
        o = camera.add_overlay(pad.tostring(), size=img.size)
        # By default, the overlay is in layer 0, beneath the
        # preview (which defaults to layer 2). Here we make
        # the new overlay semi-transparent, then move it above
        # the preview
        o.alpha = 128
        o.layer = 3

        # Wait indefinitely until the user terminates the script
        while True:
            sleep(1)


def main():

	print '\n'
	print 'Please make a selection from below options:'
	print '1. Take Picture'
	print '2. Capture to Stream'
	print '3. Resized Image'
	print '4. Consistent Images'
	print '5. Timelapse Sequence'
	print '6. Low light Image'
	print '7. Record video to a file'
	print '8. Record video to a stream'
	print '9. Record over Multiple Files'
	print '10. Overlay Image on the preview'
	print 'To quit, enter "q"\n'

	var = raw_input("Selection [1-10]:\n")

	string = 'option'+str(var)

	if var == 'q':
		return None
	else:pass

	dict = {'option1':option1
			,'option2':option2
			,'option3':option3
			,'option4':option4
			,'option5':option5
			,'option6':option6
			,'option7':option7
			,'option8':option8
			,'option9':option9
			,'option10':option10}

	if string in dict:
		dict[string]()

	main()  # loop back as the user has not selected 'q' yet


if __name__ == '__main__':
    main()
