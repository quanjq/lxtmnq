# -*-encoding:utf-8-*-
# __auther__='xiaopt'

from Crypto.Cipher import DES3
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
import base64

pub_key_file = './/file//1_pub.key'
pri_key_file = './/file//1_pri.key'
keyfile = ""
basekey = "333705661205A5E3D950933325240713"
key01 = 'UB7F6jKC15GrRQnjdr98IQ=='


class CryptoUtil(object):
    def __init__(self):
        super(CryptoUtil, self).__init__()
        self.padmode = 2

    def _encrypt_key(self, key):
        rsakey = RSA.importKey(self._pub_key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        return base64.b64encode(cipher.encrypt(key))

    def _decrypt_key(self, enc_key):
        rsakey = RSA.importKey(self._pri_key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        random_generator = Random.new().read
        return cipher.decrypt(base64.b64decode(enc_key), random_generator)

    def _encrypt_text(self, key, msg):
        text = self._pad(msg)
        iv = ''.join([chr(x) for x in [0x12, 0x34, 0x56, 0x78, 0x90, 0xAB, 0xCD, 0xEF]])
        cipher = DES3.new(key, DES3.MODE_ECB, iv)
        return base64.b64encode(cipher.encrypt(text))

    def _decrypt_text(self, key, msg):
        iv = ''.join([chr(x) for x in [0x12, 0x34, 0x56, 0x78, 0x90, 0xAB, 0xCD, 0xEF]])
        cipher = DES3.new(key, DES3.MODE_ECB, iv)
        return self._unpad(cipher.decrypt(base64.b64decode(msg)))

    def _pad(self, x):
        len_x = len(x)
        filling = 8 - len_x % 8
        if self.padmode == 2:
            fill_char = chr(filling)
        else:
            fill_char = "\0"
        return (x + fill_char * filling)

    def _unpad(self, x):
        if self.padmode == 2:
            return x[0:-ord(x[-1])]
        return x.rstrip("\0")

    def hexValueof(self, num):
        if (num >= 48 and num <= 57):
            return num - 48
        if (num >= 97 and num <= 102):
            return (num - 97) + 10
        if (num >= 65 and num <= 70):
            return (num - 65) + 10
        return 0

    def fromHexString(self, numlist, num):
        list01 = []
        for i in range(0, num, 2):
            newnum = (self.hexValueof(numlist[i]) << 4) | (self.hexValueof(numlist[i + 1]))
            list01.append(newnum)
        return list01

    def getStrFormat(self, strtoformat):
        return [ord(item) for item in strtoformat]

    def _str_pad(self, strpad):
        if len(strpad) == 1:
            return "0" + strpad
        return strpad

    def _msg_format(self, msg):
        list01 = [str(hex(ord(item)).replace("0x", "").upper()) for item in base64.b64decode(msg)]
        str03 = "".join(map(self._str_pad, list01))
        list04 = self.getStrFormat(str03)
        newlist01 = self.fromHexString(list04, 32)
        strliststr = "".join([chr(item) for item in newlist01])
        return base64.b64encode(strliststr)

    def _base_key_generator(self, basekey):
        basekeylist = self.getStrFormat(basekey)
        basekeyhexlist = self.fromHexString(basekeylist, 32)
        print (basekeyhexlist)#[51, 55, 5, 102, 18, 5, 165, 227, 217, 80, 147, 51, 37, 36, 7, 19]
        return "".join([chr(item) for item in basekeyhexlist])

    def _get_key_value(self, key_sqe):
        pass

    def get_real_key(self, keymsg):#获取建行真是加密秘钥
        msgstr = self._msg_format(keymsg)
        basekeystr = self._base_key_generator(basekey)
        realkeystr = self._decrypt_text(basekeystr, msgstr)
        return realkeystr


if __name__ == "__main__":
    crypt = CryptoUtil()
    realkeystr = crypt.get_real_key(key01)
    print [ord(item) for item in realkeystr]
