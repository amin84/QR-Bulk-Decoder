from abc import ABCMeta, abstractmethod, abstractstaticmethod


class QRDataExporterBase(metaclass=ABCMeta):
    """Base from which QR data exporting classes must inherit. The base contains one static
    method which will facilitate the export
    """
    
    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, "export_QR_data") and callable(subclass.export_QR_data)

    @staticmethod
    @abstractmethod
    def export_QR_data(path: str, export_dict: dict):
        """
            Static method that will help export data.

            Args:
            path (str): a string representing the path to export data to.

            export_dict (dict): Dictionary representing QR data to export.
             This dictionary can be derived from DecodeQR.get_decoded_data_dict()."""

        raise NotImplementedError
