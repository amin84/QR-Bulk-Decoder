import cv2
from pathlib import Path
import numpy as np
from QRDataExporterBase import QRDataExporterBase
from QRDataExporter_BuiltIn import QRDataExporterCSV, QRDataExporterPDF
from ImageEnhancer import ImageEnhancer


class DecodeQR:
    """This class contains methods that allow decoding of QR codes from images located in a directory using OpenCv
    and exporting the decoded data in various formats such as CSV, PDF, Excel (Supported by default). More ways
    for exporting can be implemented through QRDataExporterBase. It should be instanced with the path to
    the directory containing images (PNG, JPG) with the QR codes passed in the constructor. e.g.

        qr_decoded = Decode_QR(path_to_directory)

        NOTE: Due to the nature of opencv, some QR codes may not be derived from the images due to their quality and other factors.
    """

    __file_list = []

    # data retrieved from opencv after a successful decoding

    _decoded_data_dict = {}

    def __init__(self, QR_image_directory: str):

        self.__path = Path(QR_image_directory)

    def export_data(self, built_in_export:str='CSV', custom_export:QRDataExporterBase=None):
        """Exports QR Data from decoded QR data to different formats.
        Custom implementations of QRDataExporterBase
         can be passed here for export to other needed
         formats (built-in export supports: CSV, PDF, Excel formats).

        Args:
            custom_export (QRDataExporterBase, optional): A class that implements QRDataExporterBase can be passed here for custom export formats. Defaults to None.
            built_in_export (str, optional): Can be used to export data in one of the built_in export options i.e 'PDF', 'CSV', 'Excel' which
             are the possible values to pass to this parameter. Defaults to 'CSV'.


        NOTE: Exporting can currently only be done at a time for each format needed. Different formats require calling this method
                    each time for each format e.g.

                qr_decoded.export_data(built_in_export = 'PDF') # exports to PDF

                qr_decoded.export_data(built_in_export = 'Excel) # exports to Excel
        """

        if custom_export == None:

            if built_in_export.upper() == 'CSV':

                QRDataExporterCSV.export_QR_data(
                    self.__path, self.get_decoded_data_dict())
                

            if built_in_export.upper() == 'PDF':

                QRDataExporterPDF.export_QR_data(
                    self.__path, self.get_decoded_data_dict())
                

        elif QRDataExporterBase.__subclasshook__(custom_export):

            custom_export.export_QR_data(self.__path, self.get_decoded_data_dict())
            

        else:

            raise TypeError("class {} is not a subclass of {}".format(custom_export.__name__, QRDataExporterBase.__name__))
            

            

    def decode_qr(self, enhance_image: bool = False):
        """Loads the images (PNG, JPG) from the directory provided and decodes any QR codes found in them.


        Args:
            enhance_image (bool, optional): Whether to enhance the images to make the QR code more visible to opencv.This may help if
            the images are dark. Defaults to False.

             """

        # loads the images into a list which is then looped through to populate a dictionary with image name as key and
        # image paths as value
        self.__file_list = [png_file for png_file in self.__path.glob('*.png')]
        self.__file_list.extend(
            [jpg_file for jpg_file in self.__path.glob('*.jpg')])

        if len(self.__file_list) == 0:

            raise ValueError("No image files found in {}".format(self.__path))
            return

        else:

            decoder = cv2.QRCodeDetector()

            for file in self.__file_list:

                if enhance_image:

                    image_read = cv2.imread(str(
                        ImageEnhancer.increase_contrast(file)))

                else:
                    image_read = cv2.imread(str(file))

                # decoded_data is a tuple returned by opencv

                decoded_data = decoder.detectAndDecode(image_read)

                self._decoded_data_dict[file.name] = decoded_data

    def get_decoded_data_dict(self):
        """Returns a dictionary representing the QR data that may have been decoded from the images provided.
            Images that could not be decoded or that did not have QR codes in them will not be included.
            If no data was found at all, will return an empty dict


        """

        # first clean-up decoded data dictionary to remove images that did not have their QR codes decoded.
        # opencv returns tuple('', None, None) if nothing is detected. Will check if first element of tuple is ''
        # meaning no qr_data was recieved.

        return {k: v for k, v in self._decoded_data_dict.items() if v[0] != ''}

    def generate_marked_images(self):
        """Makes copies of the original images marking them with a box showing where the QR images were detected.
            These images will be saved under a new folder named '_MARKED'
        """

        marked_image_path = self.__path.joinpath("_MARKED")

        if not marked_image_path.exists():

            marked_image_path.mkdir(parents=True)
            # print("CREATING DIR")

        __data_dict = self.get_decoded_data_dict()

        
        if not len(__data_dict) == 0:


            for image in __data_dict.items():

                image_read = cv2.imread(str(self.__path.joinpath(image[0])))

                # drawing polygon requires the nparray to be in int32 format so...

                # image[1] to get the tuple (value) which is (qr_data, polygon_points, rectified_qr)
                polygon_points = np.array(image[1][1], np.int32)

                marked_image = cv2.polylines(
                    image_read, polygon_points, True, (0, 0, 255), 3, cv2.LINE_AA)

                try:

                    cv2.imwrite(
                        str(marked_image_path.joinpath(image[0])), marked_image)

                except:

                    raise Exception(
                        'Could not write the marked image to directory \'_MARKED\'')

        else:

            print("No QR code was decoded. Unable to mark images.")

    def extract_qr_code(self):
        """Extracts the QR codes from the original images, refines and saves them as new images.
            These images will be saved under a new folder named '_EXTRACTED'"""
        extracted_image_path = self.__path.joinpath("_EXTRACTED")

        if not extracted_image_path.exists():
            extracted_image_path.mkdir(parents=True)

        __data_dict = self.get_decoded_data_dict()

        if not len(__data_dict) == 0:

            for image in __data_dict.items():

                try:

                    cv2.imwrite(
                        str(extracted_image_path.joinpath(image[0])), image[1][2])

                except:

                    raise Exception(
                        'Could not write the extracted QR codes to directory \'_EXTRACTED\'')

        else:

             print("No QR code was decoded. Unable to extract QR code from images.")

    def __repr__(self):

        return f"""Decode_QR({self.__path})"""
