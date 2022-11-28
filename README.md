# QR-Bulk-Decoder
A QR Decoder using Open CV in Python.

This program will attempt to decode QR codes found inside images and provide options to export the data in form of CSV or PDF. This can be further extended
to other formats by implementing the <code>QRDataExporterBase</code> class.
This is a wrapper to Open-CV's <code>QRCodeDetector</code> function. It works in the command line and goes through the following procedure:

  1. It will scan the directory provided to it through the <code>path</code> argument and will pick out .jpg and .png files in a Python list.
  2. It will attempt to scan QR codes in the images collected. An optional argument is <code>--enhance</code> that will increase the images' brighness and
      contrast to increase Open-CV's chance to detect the QR codes in dark images. It is recommended to provide clear images to begin with.
  3. All images that were able to be decoded will have their data populated in a Python <code>dict</code>. This data can then be used to do the following:

      a. Generate marked-images using the <code>--mark</code> argument: This will create a sub-directory called <b>_MARKED</b> which will contain copies of 
         the original images that were decoded but will have the QR code highlighted in a red box.
         
      b. Generate the QR codes again as refined images and places them in a sub-directory called <b>_EXTRACTED</b>. This can be done by passing the
         <code>--extract</code> argument.
         
      c. Export the data decoded in CSV or PDF format by passing the <code>--export</code> argument which has two options <b>csv</b> or <b>pdf.</b>This export
         will be saved under the directory under the name <b>QR Export_CSV</b> or <b>QR Export_PDF</b> for the <b>csv</b> or <b>pdf</b> options respectively.
         
# Installation

The program has been compiled using pyinstaller. You can rebuild the program in your platform. Please refer to the <a href="https://pyinstaller.org/en/stable/"> pyinstaller</a> documentation.
You can download the Windows version here: <a href="https://drive.google.com/file/d/1zxaLhelsyCqY3SzaAN1c7bqs1zaXWpTV/view?usp=sharing"> LINK </a>
      
      
