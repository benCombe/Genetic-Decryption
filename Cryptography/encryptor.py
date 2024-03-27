import os
import pickle
from zipfile import ZipFile, ZIP_DEFLATED
from cryptography.fernet import Fernet



class Encryptor():
    key = None
    cipher = None
    def __init__(self, bin_path=None):
        if bin_path is None:
            self.key = Fernet.generate_key()
            self.cipher = Fernet(self.key)
        else:
            self.LoadFromFile(bin_path)

    def EncryptFile(self, file_path, overwrite_original=False):
        out_path = file_path if overwrite_original else f"{os.path.splitext(file_path)}.enc"

        try:
            with open(file_path, 'rb') as file:
                file_content = file.read()
            enc_content = self.cipher.encrypt(file_content)
        except:
            raise FileNotFoundError(f"ERROR: Cannot Find File: '{file_path}'")

        with open(out_path, 'wb') as file:
            file.write(enc_content)

        return out_path

    def DecryptFile(self, enc_file_path, delete_original_enc_file=False):
        out_path = f"{os.path.splitext(enc_file_path)}.dec"

        try:
            with open(enc_file_path, 'rb') as enc_file:
                enc_content = enc_file.read()
        except:
            raise FileNotFoundError(f"ERROR: Cannot Find File: '{enc_file_path}'")

        dec_content = self.cipher.decrypt(enc_content)
        with open(out_path, 'wb') as dec_file:
            dec_file.write(dec_content)
        #TODO add delete original
        return out_path
    

    def EncryptDirectory(self, dir_path, overwrite_original=False):
        zip_path = f"{dir_path}.enczip"
        with ZipFile(zip_path, 'w', ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(dir_path):
                for file in files:
                    abs_path = os.path.join(root, file)
                    rel_path = os.path.relpath(abs_path, dir_path)
                    zipf.write(abs_path, rel_path)
        self.EncryptFile(zip_path, True)
        return zip_path
    
    def DecryptDirectory(self, zip_path, delete_original_zip=False):
        dec_zip_path = self.DecryptFile(zip_path, True)
        dir_path = os.path.splitext(dec_zip_path)
        with ZipFile(dec_zip_path, 'r') as zip_ref:
            zip_ref.extractall(dir_path)
        #TODO add delete original
            
    def SaveEncryptorToBinary(self, bin_path):
        with open(bin_path, 'wb') as file:
            pickle.dump(self, file)

    def LoadFromFile(self, bin_path):
        with open(bin_path, 'rb') as file:
            obj = pickle.load(file)
            self.__dict__.update(obj.__dict__)

        