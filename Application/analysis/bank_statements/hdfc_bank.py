

from os import listdir
from os.path import isfile, join


class HDFCBank(object):
    def __init__(self, pdf_password, pdf_folder_path):
        """
        Args:
            Password to open PDF file for hdfc bank, This is generally the 
                Customer id of the user
        
            pdf_folder_path 
                Path for the pdf folder it could be dowloaded 
                from any gmail client 
        
        """
        self.pdf_password = pdf_password
        self.pdf_folder_path = pdf_folder_path
        pass

    @staticmethod
    def is_hdfc(subject):
        """
        Find out from the email subject if this pdf is from HDFC bank
        """
        if subject.lower().find("hdfc") != -1:
            return True
        return 

    def collect_pdfs(self):
        """
        Args:
        Return :
            array of pdf file name which belongs to 
        
        Open the folder, and filter out the PDF which belongs to 
        HDFC bank

        """
        all_files = [f for f in listdir(self.pdf_folder_path) \
                    if isfile(join(self.pdf_folder_path, f))]

        return [filename for filename in all_files if filename.lower().find("hdfc")]



