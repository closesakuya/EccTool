# coding=utf-8

# from typing import List
import os
# import time
# import random
# import re
# import copy
import uuid
import json

from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

class AESHelper():
    @staticmethod
    def add_to_16(text):
        if isinstance(text, str):
            tt_len = len(text.encode('utf-8')) % 16
        else:
            tt_len = len(text) % 16
        if tt_len:
            add = 16 - tt_len
        else:
            add = 0
        if isinstance(text, str):
            text = text + ('\0' * add)
            return text.encode('utf-8')
        else:
            return text + (b'\0' * add)

    # 加密函数
    @staticmethod
    def encrypt(text, key, mode=AES.MODE_ECB, iv=None):
        if isinstance(key, str):
            key = key.encode('utf-8')
        text = AESHelper.add_to_16(text)
        if iv:
            cryptos = AES.new(key, mode, iv)
        else:
            cryptos = AES.new(key, mode)
        try:
            cipher_text = cryptos.encrypt(text)
        except Exception as e:
            print(e)
            cipher_text = None
        # 因为AES加密后的字符串不一定是ascii字符集的，输出保存可能存在问题，所以这里转为16进制字符串
        #return b2a_hex(cipher_text)
        return cipher_text

    # 解密后，去掉补足的空格用strip() 去掉
    @staticmethod
    def decrypt(text, key, mode=AES.MODE_ECB, iv=None):
        if isinstance(key, str):
            key = key.encode('utf-8')
        if iv:
            cryptos = AES.new(key, mode, iv)
        else:
            cryptos = AES.new(key, mode)
        raw_data = text
        if isinstance(text, str):
            raw_data = a2b_hex(text)
        try:
            plain_text = cryptos.decrypt(raw_data)
        except Exception as e:
            print(e)
            plain_text = None
        return plain_text
        #return bytes.decode(plain_text).rstrip('\0')


class AdPicEcc:
    SCRIPT_KEY_PATH = ".ecc_script.ecc"
    def __init__(self):
        pass

    def _gen_key(self):
        key = None
        try:
            with open(self.SCRIPT_KEY_PATH, 'rb') as f:
                txt = f.read()
                pv_key = self.get_read_script_key(self.get_sys_info())
                txt = AESHelper.decrypt(txt, bytes(pv_key))
                try:
                    env = {}
                    exec(txt.rstrip(b'\0').decode("utf-8"), env)
                    func = env.get("get_key", None)
                    if callable(func):
                        key = func()
                except Exception as e:
                    print(e)

        except FileNotFoundError:
            print("not found enc private: ", self.SCRIPT_KEY_PATH)
        return key

    def gen_key(self):
        return self._gen_key()

    def gen_private(self, sys_info: str, input_path: str = None, output_path: str = None, aux_info: str = "None"):
        """秘钥生成接口，仅供研发使用"""
        try:
            if input_path is None:
                input_path = "private_key.py"
            with open(input_path, "r", encoding='utf-8') as f:
                txt_lst = f.read().split("\n")
                if txt_lst.__len__() > 0:
                    txt_lst[0] = '__KEY_BOOT__ = "{0}"'.format(sys_info)
                txt_lst.append('__AUX_INFO__ = "{0}"'.format(aux_info))
                txt = '\n'.join(txt_lst)
                txt = AESHelper.encrypt(txt.encode('utf-8'), self.get_read_script_key(sys_info))
                if not txt:
                    print("加密失败")
                    return False
                with open(output_path, 'wb') as fw:
                    fw.write(txt)
                    print("加密成功 to: ", output_path)
                    return True

        except FileNotFoundError:
            print("未找到秘钥原始文件 private_key.py")
            return False

    def enc_pic(self, input_path: str, output_path: str, aux_msg: str = None, aux_msg_len: int = 128):
        return self._enc_file(input_path, output_path, aux_msg, aux_msg_len)

    def dec_pic(self, input_path: str, output_path: str, has_aux_msg: bool = False, aux_msg_len: int = 128):
        return self._dec_file(input_path, output_path, has_aux_msg, aux_msg_len)

    def _enc_file(self, input_path: str, output_path: str, aux_msg, aux_msg_len: int = 128):
        key = self._gen_key()
        if not key:
            print("not found key ", self.SCRIPT_KEY_PATH)
            return False
        ret = False
        try:
            with open(input_path, 'rb') as f:
                txt = f.read()
                if aux_msg:  # 附加信息在头部 默认长度128
                    aux_msg = aux_msg.encode('utf-8')
                    if aux_msg.__len__() >= aux_msg_len:
                        aux_msg = bytes(bytearray(aux_msg)[:aux_msg_len])
                    else:
                        aux_msg = bytearray(aux_msg)
                        aux_msg += bytearray(b'\0'*(aux_msg_len - aux_msg.__len__()))
                    txt_len = txt.__len__().to_bytes(4, 'big')
                    # txt = bytes(aux_msg) + txt
                    txt = bytes(aux_msg) + txt_len + txt

                txt = AESHelper.encrypt(txt, key=key)
                if not txt:
                    print("加密失败: ", txt)
                    ret = False
                try:
                    with open(output_path, 'wb') as fw:
                        fw.write(txt)
                    ret = True
                except Exception as e:
                    print("创建文件 ", output_path, "失败: ", e)
                    ret = False
        except FileNotFoundError:
            print("文件不存在: ", input_path)
            ret = False
        except Exception as e:
            raise e
        return ret

    def _dec_file(self, input_path: str, output_path: str, has_aux_msg: bool = False, aux_msg_len: int = 128):
        ret = False
        aux_info = ""
        key = self._gen_key()
        if not key:
            print("not found key ", self.SCRIPT_KEY_PATH)
            return False, aux_info
        try:
            with open(input_path, 'rb') as f:
                txt = f.read()
                if has_aux_msg and txt.__len__() > aux_msg_len:
                    aux_raw = bytes(bytearray(txt)[:aux_msg_len])
                    txt = bytes(bytearray(txt)[aux_msg_len:])
                    aux_info = AESHelper.decrypt(aux_raw, key=key).strip(b'\0').decode('utf-8')

                txt = AESHelper.decrypt(txt, key=key)
                if txt.__len__() > 4:
                    txt_len = int.from_bytes(bytes(txt[:4]), 'big')
                    if txt_len > 0:
                        txt = txt[4: 4 + txt_len]
                if not txt:
                    print("解密失败: ", txt)
                    ret = False
                try:
                    with open(output_path, 'wb') as fw:
                        fw.write(txt)
                        ret = True
                except Exception as e:
                    print("创建文件 ", output_path, "失败: ", e)
                    ret = False
        except FileNotFoundError:
            print("文件不存在: ", input_path)
            ret = False
        except Exception as e:
            raise e
        return ret, aux_info

    @staticmethod
    def get_read_script_key(sys_info: str = None):
        if sys_info is None:
            sys_info = AdPicEcc.get_sys_info()
        sys_info = bytearray(sys_info.encode("utf-8"))
        ret = bytearray(b'Ux12#ad3agF9S$Q1')
        for i in range(sys_info.__len__()):
            ret[i % 15] = (ret[i % 15] + sys_info[i]) % 0xFF
        return ret

    @staticmethod
    def get_sys_info() -> str:
        import socket
        name = socket.gethostname()
        try:
            node = uuid.getnode()
            mac = uuid.UUID(int=node).hex[-12:]
        except Exception as e:
            print(e)
            mac = ""
        return name.strip() + "-" + mac.strip()

    @staticmethod
    def get_ip_info():
        import requests
        res = ""
        try:
            # HTTP GET
            r = requests.get('https://ipw.cn/api/ip/locate')
            ip_detail = json.loads(r.text)
            res = "ip:{0},isp:{1},locale:{2} {3}".format(
                ip_detail['IP'], ip_detail['ISP'], ip_detail['Address']['Province'],
                ip_detail['Address']['City']
            )
        except Exception as e:
            print(e)

        return res




# if __name__ == "__main__":
#     idd = AdPicEcc.get_read_script_key()
#
#     a = AdPicEcc()
#     #a._enc_file("raw.png", "raw.enc")
#     #a._dec_file("raw.enc", "haha.png")
#
#     # 用于生成秘钥(秘钥与仪器信息相关联)
#     # a.gen_private(a.get_sys_info(), output_path="ecc_script.enc")
#
#     dir = r"D:\share_dir\product_env\tmp\ad"
#     import os, sys
#     for item in os.listdir(dir):
#         if os.path.splitext(item)[-1].lower() == '.png':
#             print(item)
#             a._enc_file(dir + os.sep + item, dir + os.sep + os.path.splitext(item)[0] + ".enc",
#                         aux_msg="{this is aux_msg}")
#         if os.path.splitext(item)[-1].lower() == '.enc':
#             ret = a._dec_file(dir + os.sep + item, dir + os.sep + os.path.splitext(item)[0] + ".png"
#                               , has_aux_msg=True)
#             print(ret)
#     #a._dec_file("raw.enc", "opt.png")