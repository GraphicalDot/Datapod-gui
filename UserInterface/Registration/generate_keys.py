

from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
import base64
import ipfsapi
import json
import os
##https://media.readthedocs.org/pdf/python-ipfs-api/latest/python-ipfs-api.pdf


class GenerateKeys(object):


    def __init__(self):
        self.private_key_str = None 
        self.public_key_str = None
        self.private_key = None 
        self.public_key = None
        self.private_filename = "privatekey.pem"
        self.public_filename = "publickey.pem"

    def generate_keys(self, save_keys=False):
        """
        Generate public privatekeys

        https://sawtooth.hyperledger.org/docs/core/releases/1.0/_autogen/sdk_submit_tutorial_python.html

        context = create_context('secp256k1')
        private_key = context.new_random_private_key()
        signer = CryptoFactory(context).new_signer(private_key)

        self.private_key_hex =  private_key.as_hex()
        self.signer_public_key=signer.get_public_key().as_hex(),
        return (private_key_hex, signer_public_key)

        """

        # generate private/public key pair
        self.private_key = rsa.generate_private_key(backend=default_backend(), public_exponent=65537, key_size=2048)

        # get public key in OpenSSH format
        self.public_key = self.private_key.public_key()


        pem_public = self.public_key.public_bytes(serialization.Encoding.OpenSSH, serialization.PublicFormat.OpenSSH)

        # get private key in PEM container format
        pem = self.private_key.private_bytes(encoding=serialization.Encoding.PEM, 
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption())

        
        if save_keys:
            with open(self.private_filename, 'wb') as pem_out:
                pem_out.write(pem)

            with open(self.public_filename, 'wb') as pem_out:
                pem_out.write(pem_public)
    	    # decode to printable strings
            self.private_key_str = pem.decode('utf-8')
            self.public_key_str = pem_public.decode('utf-8')
            
            print('Private key = ')
            print(self.private_key_str)
            print('Public key = ')
            print(self.public_key_str)

        return (pem, pem_public)




        



    def load_private_key(filename):
        with open(self.private_filename, 'rb') as pem_in:
            pemlines = pem_in.read()
        private_key = load_pem_private_key(pemlines, None, default_backend())
        return private_key

    def load_public_key(self):
        with open(self.public_filename, 'rb') as pem_in:
            pemlines = pem_in.read()
        public_key = load_pem_private_key(pemlines, None, default_backend())
        return private_key


    @staticmethod
    def encrypt_json(self, message, private_key, public_key):
    	#https://medium.com/@raul_11817/rsa-with-cryptography-python-library-462b26ce4120
        message = message.encode('ascii')
        ciphertext = public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
                )
            )

        ciphertext  = str(base64.b64encode(ciphertext), encoding='utf-8')

        data_to_sign = bytes(message, encoding='utf8') if not isinstance(message, bytes) else message

        signer = private_key.signer(
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
        hashes.SHA256()
            )

        signer.update(data_to_sign)
        signature = str(
                base64.b64encode(signer.finalize()),
            encoding='utf8'
        )


        return (ciphertext, signature)

    def test_keys(self):
        """
        Test if the encryption and decryption process
        """












class GetUserDetails:

    def __init__(self, identity_image, self_image):
        """
        to check if there is a match between the image of the person and get
        the relevant details from the adhaar 

        """
        self.identity_image = identity_image
        self.self_image = self
        
        
        
        
    def adhaar(self):
        """
        If the identity_image is of kind adhaar
        
        TODO: Use any thirdparty of write your own functions for convolution neural nets to get the 
        similirity between the two
        True if there is a match in the identities 
        """


        return (fake.credit_card_number(), fake.address(), fake.name(), True)



if __name__ == "__main__":
    _instance = GenerateKeys()
    _instance.generate_keys()
    (ciphertext, signature) = _instance.encrypt_object("hey now, Dude how are you")
    print (ciphertext, signature)
    ipfs_object_hash = StoreDetails.storedetails((ciphertext, signature))

