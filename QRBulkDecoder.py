from pathlib import Path
from DecodeQR import DecodeQR
from QRDataExporterBase import QRDataExporterBase
import argparse


def main():


    parser = argparse.ArgumentParser(prog='Bulk QR Decoder',
                                     description="""This program decodes QR codes in images found in a directory provided using OPENCV. It can do the following:\n
     
        \t\t1. Save the extracted QR codes in a PDF or CSV list.\n
        \t\t2. Generate new images containing the refined QR codes from the images.\n
        \t\t3. Mark the decoded QR code in the original images with a red box.\n
        
    NOTE: TO increase the chance of a QR code being decoded, please make sure the images are clear.""")

    parser.add_argument('path', help='Directory of images with QR codes to decode.', type=str)
    parser.add_argument('-e','--enhance',help='Increase contrast/brightness of images before decoding to increase chance of detection.',action='store_true')
    parser.add_argument('-m','--mark', help='''After a successful decoding, generate copies of the images with
    the decoded QR marked in a red box. These images will be in a directory called: _MARKED''',action='store_true')
    
    parser.add_argument('-ext','--extract',help='''After a successful decoding, generate refined images of the QR codes which will be
    stored in a directory called: _EXTRACTED''',action='store_true')
   
    parser.add_argument('-exp','--export',choices=['csv','pdf'], help='''Export the decoded QR data in CSV or PDF format
    in the current directory''',type=str,metavar='')

    args = parser.parse_args()  

    decode = DecodeQR(args.path)

    decode.decode_qr(args.enhance)

    if args.mark:

        decode.generate_marked_images()

    if args.extract:

        decode.extract_qr_code()

    if args.export != None:

        decode.export_data(args.export)
    #print("CLEANED DICT: {}".format(decode.get_decoded_data_dict()))


main()
