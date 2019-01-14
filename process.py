from PIL import Image, ImageEnhance
#from qrtools import qrtools
from pyzbar.pyzbar import decode
from picamera import PiCamera


class Processor:
    """
    Image capture and QR processing
    """

    def __init__(self, out_file):
        """
        Camera setup and default values

        :param out_file: output file path for captured image
        """
        # camera setup
        self.cam = PiCamera()
        self.cam.resolution = (1024, 768)

        # QR decoder
        #self.qr = qrtools.QR()

        self.out_file = out_file

        # default values for image processing:
        # crop region containing qr code
        self.crop=(300, 200, 700, 600)
        # sharpness enhancement factor (1.0 = no enhancement)
        self.sharpness=3.0
        # contrast enhancement factor (1.0 = no enhancement)
        self.contrast=2.0

    def __del__(self):
        self.cam.close()

    def capture(self):
        """
        Capture an image and pre-process it (crop, contrast, sharpness), decode QR code

        :returns: True if QR decoding was successful, False otherwise
        """
        # capture image
        self.cam.capture(self.out_file)

        # process image
        img = Image.open(self.out_file)
        img = img.crop((300, 200, 700, 600))
        img = ImageEnhance.Contrast(img).enhance(self.contrast)
        img = ImageEnhance.Sharpness(img).enhance(self.sharpness)
        #img.save(self.out_file)
        self.qr = decode(img)
        if self.qr:
            self.qr = self.qr[0]
        else:
            self.qr = None
        return self.qr

