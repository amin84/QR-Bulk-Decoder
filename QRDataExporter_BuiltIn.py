"""Contains builtin export classes for saving QR data to CSV, PDF and Excel formats"""


from QRDataExporterBase import QRDataExporterBase
import csv
from pathlib import Path
from fpdf import FPDF, enums


class QRDataExporterCSV(QRDataExporterBase):
    """Class that contains a single static method to export decoded QR data from images to a CSV file."""

    def export_QR_data(path: Path, export_dict: dict):
        """Exports data in CSV format. The order will be: image_name, qr_data"""

        if len(export_dict) != 0:

            # used by csv writer
            __field_names = ['Image File', 'Qr Code Info.']

            # remapping the dictionary to what csv writer needs
            __rows_to_write = [{__field_names[0]:k, __field_names[1]:v[0]}
                               for k, v in export_dict.items()]

            p = path / 'QR Export_CSV.csv'

            with p.open('w', newline='') as csv_file:

                try:

                    writer = csv.DictWriter(
                        csv_file, __field_names, dialect='excel')

                    writer.writeheader()

                    writer.writerows(__rows_to_write)

                except:

                    raise Exception("Could not export data to the CSV file")

        else:

            raise Exception("No data found to export")


class QRDataExporterPDF(QRDataExporterBase):

    """Class that contains a single static method to export decoded QR data from images to a PDF file."""

    def export_QR_data(path: Path, export_dict: dict):
        """Exports data in PDF format."""

        if len(export_dict) != 0:

            p = path / 'QR Export_PDF.pdf'

            pdf_write = FPDF()
            pdf_write.add_page()

            pdf_write.set_font('helvetica', style="BI", size=13)
            pdf_write.cell(txt="Image Name", border='U')
            pdf_write.cell(txt="\t" * 6, border=0)
            pdf_write.cell(txt="QR Data", border='U',
                           new_x=enums.XPos.LMARGIN, new_y=enums.YPos.NEXT)

            pdf_write.set_font(style='', size=10)
            pdf_write.cell(txt="\r" * 4, new_x=enums.XPos.LMARGIN,
                           new_y=enums.YPos.NEXT)

            for k, v in export_dict.items():

                pdf_write.cell(txt=k)
                pdf_write.cell(txt="\t" * 6)
                pdf_write.cell(
                    txt=str(v[0]), new_x=enums.XPos.LMARGIN, new_y=enums.YPos.NEXT)
                pdf_write.cell(txt="\r" * 4, new_x=enums.XPos.LMARGIN,
                               new_y=enums.YPos.NEXT)

            pdf_write.output(p)

        else:

            raise Exception("No data found to export")
