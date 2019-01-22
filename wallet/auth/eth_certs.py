# coding:utf-8
import os
import base64
import json
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key


class EthCert(object):

    def __init__(self, username="anonymous"):
        cert_dir = os.path.dirname(os.path.realpath(__file__))
        self.pems = os.path.join(cert_dir, "pems")
        self.pems_user_dir = os.path.join(self.pems, username)
        self.thiscert = {
            "private": os.path.join(self.pems, username, "private_key.pem"),
            "public": os.path.join(self.pems, username, "public_key.pem"),
        }
        self.private_key_str = None
        self.public_key_str = None
        self.private_key = None
        self.public_key = None
        self.style = None
        self.error = ""

    def init_dir(self, username):
        """
        设置用户目录
        :param username:
        :return:
        """
        self.pems_user_dir = os.path.join(self.pems, username)
        self.thiscert = {
            "private": os.path.join(self.pems, username, "private_key.pem"),
            "public": os.path.join(self.pems, username, "public_key.pem"),
        }

    def generate(self, size=2048):
        """
        生成公钥和私钥
        :param size:
        :return:
        """
        # Generate the public/private key pair.
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=size,
            backend=default_backend(),
        )
        self.private_key_str = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
        self.public_key_str = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return True

    def load_key_from_file(self):
        """
        从用户的目录中读取公钥或者私钥，读取到的文本会保存在变量中
        :return:
        """
        try:
            if os.path.isfile(self.thiscert['private']):
                with open(self.thiscert['private'], 'rb') as kfd:
                    self.private_key_str = kfd.read()
            if os.path.isfile(self.thiscert['public']):
                with open(self.thiscert['public'], 'rb') as kfd:
                    self.public_key_str = kfd.read()
            if not self.private_key_str and not self.public_key_str:
                self.error = "provide private or public key"
                return False
        except Exception as e:
            self.error = f"{e}"
            return False
        return True

    def init_key(self, private_key_str=None, public_key_str=None):
        if not private_key_str and not public_key_str:
            self.error = "should provide private or public key"
            return False
        if private_key_str:
            self.private_key_str = self.convert(private_key_str)
        if public_key_str:
            self.public_key_str = self.convert(public_key_str)
        return True

    def serialization(self):
        """
        序列化公钥和私钥，用于加密、解密、签名、验签
        :return:
        """
        try:
            if self.private_key_str:
                self.private_key = serialization.load_pem_private_key(
                    self.private_key_str,
                    password=None,
                    backend=default_backend()
                )
            if self.public_key_str:
                self.public_key = load_pem_public_key(self.public_key_str, default_backend())
        except Exception as e:
            self.error = f"serialization error: {e}"
            return False
        return True

    def convert(self, origin_str):
        if isinstance(origin_str, bytes):
            return origin_str
        if isinstance(origin_str, str):
            return bytes(origin_str, encoding='utf8')
        if isinstance(origin_str, (list, dict)):
            return bytes(json.dumps(origin_str, ensure_ascii=False), encoding='utf8')
        else:
            return bytes(str(origin_str), encoding='utf8')

    def save_file(self):
        """
        保存公钥或者私钥到用户目录中
        :return:
        """
        if not os.path.isdir(self.pems_user_dir):
            os.mkdir(self.pems_user_dir)
        if self.private_key_str:
            try:
                # Save the private key to a file.
                with open(self.thiscert['private'], 'wb') as f:
                    f.write(self.private_key_str)
            except Exception as e:
                self.error = f"{e}"
                return False
        if self.public_key_str:
            try:
                # Save the public key to a file.
                with open(self.thiscert['public'], 'wb') as f:
                    f.write(self.public_key_str)
            except Exception as e:
                self.error = f"{e}"
                return False
        return True

    def sign2_str(self, origin_data):
        signature = self.sign2(origin_data)
        if signature is not False:
            return signature.decode()
        else:
            return signature

    def sign2(self, origin_data):
        if self.private_key is None:
            self.error = "serialization private key first"
            return False
        signature = base64.b64encode(
            self.private_key.sign(
                self.convert(origin_data),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
        )
        return signature

    def sign_str(self, origin_data):
        signature = self.sign(origin_data)
        if signature is not False:
            return signature.decode()
        else:
            return signature

    def sign(self, origin_data):
        if self.private_key is None:
            self.error = "serialization private key first"
            return False
        signature = base64.b64encode(self.private_key.sign(
                self.convert(origin_data),
                padding.PKCS1v15(),
                hashes.SHA256(),
            )
        )
        return signature

    def verify2(self, origin_data, signature):
        if self.public_key is None:
            self.error = "serialization public key first"
            return False
        try:
            signature_decode = base64.b64decode(signature)
            self.public_key.verify(
                signature_decode,
                self.convert(origin_data),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
        except InvalidSignature as e:
            self.error = f'ERROR: signature failed verification! {e}'
            return False
        return True

    def verify(self, origin_data, signature):
        if self.public_key is None:
            self.error = "serialization public key first"
            return False
        try:
            signature_decode = base64.b64decode(signature)
            self.public_key.verify(
                signature_decode,
                self.convert(origin_data),
                padding.PKCS1v15(),
                hashes.SHA256(),
            )
        except InvalidSignature:
            self.error = "ERROR: signature failed verification!"
            return False
        return True

    def encrypt_str(self, origin_data):
        encrypt_data_encode = self.encrypt(origin_data)
        if encrypt_data_encode is not False:
            return encrypt_data_encode.decode()
        else:
            return encrypt_data_encode

    def encrypt(self, origin_data):
        if not self.public_key:
            self.error = "serialization public key first"
            return False
        encrypt_length = int(self.public_key.key_size / 8 - 11)
        bytes_data = self.convert(origin_data)
        bytes_len = len(bytes_data)
        offset = 0
        en_res = []
        while bytes_len - offset > 0:
            en_res.append(
                self.public_key.encrypt(
                    bytes_data[offset: offset + encrypt_length],
                    padding.PKCS1v15(),
                )
            )
            offset += encrypt_length
        if bytes_data[offset:]:
            en_res.append(
                self.public_key.encrypt(
                    bytes_data[offset: offset + encrypt_length],
                    padding.PKCS1v15(),
                )
            )
        encrypt_data_encode = base64.b64encode(b''.join(en_res))
        return encrypt_data_encode

    def get_publickey(self):
        return self.public_key_str.decode()

    def get_privatekey(self):
        return self.private_key_str.decode()

    def decrypt_str(self, encrypt_data):
        decrypt_data_res = self.decrypt(encrypt_data)
        if decrypt_data_res is not False:
            return decrypt_data_res.decode()
        else:
            return decrypt_data_res

    def decrypt(self, encrypt_data):
        if not self.private_key:
            self.error = "serialization private key first"
            return False
        try:
            bytes_data = self.convert(encrypt_data)
            decrypt_data = base64.b64decode(bytes_data)
            decrypt_length = int(self.private_key.key_size / 8)
            bytes_len = len(decrypt_data)
            de_res = []
            offset = 0
            while bytes_len - offset > 0:
                de_res.append(
                    self.private_key.decrypt(
                        decrypt_data[offset: offset + decrypt_length],
                        padding.PKCS1v15(),
                    )
                )
                offset += decrypt_length
            if decrypt_data[offset: offset + decrypt_length]:
                de_res.append(
                    self.private_key.decrypt(
                        decrypt_data[offset: offset + decrypt_length],
                        padding.PKCS1v15(),
                    )
                )
            decrypt_data_res = b''.join(de_res)
        except Exception as e:
            self.error = f"ERROR: Decryption failed!"
            return False
        return decrypt_data_res


if __name__ == "__main__":
    ec = EthCert("text")
    # 生成私钥与公钥, 长度默认为2048
    ec.generate(4096)
    print(ec.get_publickey())
    print(ec.get_privatekey())
    if ec.save_file():
        ec.serialization()
        origin = "XiaMen City"
        # 数据签名与验证方式一
        sign = ec.sign_str(origin)
        print(ec.verify(origin, sign))
        # 数据签名与验证方式二
        sign = ec.sign2_str(origin)
        print(ec.verify2(origin, sign))
        # 加密数据
        edata = ec.encrypt_str(origin)
        # 解密数据
        ddata = ec.decrypt_str(edata)
        print(ddata)
    else:
        print(ec.error)





