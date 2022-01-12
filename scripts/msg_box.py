import tkinter as tk
from tkinter import messagebox as mbox
from enc_func import EncFunc


class MsgBox:
    def __init__(self, root, key_gen_f, enc_f, dec_f):
        self._root = root
        self._key_gen_f = key_gen_f
        self._enc_f = enc_f
        self._dec_f = dec_f
        self._enc_func_1 = EncFunc()

    # to show pop-ups when `generate_key` button is pressed
    def key_gen_m_box(self, key_name, iv_name):
        ans = mbox.askyesno(
            '???',
            'Are you sure you want to generate new keys?\n'
            '(Keys with same name will be overwritten)')

        if key_name == iv_name:
            mbox.showerror('ERROR', 'key and iv filename cannot be the same')

        elif ans == 1:
            try:
                EncFunc.generate_key(key_name, iv_name)
                l_gen = tk.Label(
                    self._key_gen_f,
                    text='Keys have been generated!')
                l_gen.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
            except Exception as e:
                mbox.showerror('ERROR', e)

    # to show pop-ups when `encrypt` or `decrypt` button is pressed
    def enc_dec_m_box(self, paths, option, key_path, iv_path, func):
        ans = mbox.askyesno(
            'Confirmation required',
            'Same file names will be overwritten, confirm?')

        if ans == 0:
            pass

        elif key_path is None or iv_path is None:
            mbox.showerror('ERROR', 'key or iv file path not selected')

        elif ans == 1:
            if func == 'encrypt':
                try:
                    self._enc_func_1.encrypt(paths, option, key_path, iv_path)
                    l_enc = tk.Label(self._enc_f, text='Images encrypted!')
                    l_enc.grid(row=3, column=0, columnspan=3, padx=10, pady=5)
                except Exception as e:
                    mbox.showerror('ERROR', e)

            elif func == 'decrypt':
                try:
                    self._enc_func_1.decrypt(paths, option, key_path, iv_path)
                    l_dec = tk.Label(self._dec_f, text='Data decrypted!')
                    l_dec.grid(row=3, column=0, columnspan=3, padx=10, pady=5)
                except Exception as e:
                    mbox.showerror('ERROR', e)
