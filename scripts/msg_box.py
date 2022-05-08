import tkinter as tk
from tkinter import messagebox as mbox
from enc_func import EncFunc


class MsgBox:
    def __init__(self, root, t_gen_comp, t_key_path,
                 t_iv_path, t_enc_comp, t_dec_comp):
        self._root = root
        self._t_gen_comp = t_gen_comp
        self._t_key_path = t_key_path
        self._t_iv_path = t_iv_path
        self._t_enc_comp = t_enc_comp
        self._t_dec_comp = t_dec_comp
        self._enc_func = EncFunc()

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
                self._t_gen_comp.set('Keys have been generated!')
            except Exception as e:
                mbox.showerror('ERROR', str(e))

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
                    self._enc_func.encrypt(paths, option, key_path, iv_path)
                    self._t_dec_comp.set('Images encrypted!')
                except Exception as e:
                    mbox.showerror('ERROR', str(e))

            elif func == 'decrypt':
                try:
                    self._enc_func.decrypt(paths, option, key_path, iv_path)
                    self._t_dec_comp.set('Data decrypted!')
                except Exception as e:
                    mbox.showerror('ERROR', str(e))
