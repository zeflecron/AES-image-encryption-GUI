import tkinter as tk
from tkinter import messagebox
import enc_functions

# OPTIMIZE: remove the 4 None
root = None
key_gen_frame = None
encryption_frame = None
decryption_frame = None


# to show pop-ups when `generate_key` button is pressed
def key_gen_msg_box(aes_name, iv_name):
    ans = messagebox.askyesno('???', 'Are you sure you want '
                                     'to generate new keys?\n'
                                     '(Keys with same name '
                                     'will be overwritten)')

    if aes_name == iv_name:
        messagebox.showerror('ERROR', 'AES and iv filename cannot be the same')

    elif ans == 1:
        try:
            enc_functions.generate_key(aes_name, iv_name)
            label_gen = tk.Label(key_gen_frame,
                                 text='Keys have been generated!')
            label_gen.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
        except Exception as e:
            messagebox.showerror('ERROR', e)


# to show pop-ups when `encrypt` or `decrypt` button is pressed
def enc_dec_msg_box(paths, option, aes_path, iv_path, func):
    ans = messagebox.askyesno('Confirmation required',
                              'Same file names will be overwritten, confirm?')

    if ans == 0:
        pass

    elif aes_path is None or iv_path is None:
        messagebox.showerror('ERROR', 'AES or iv file path not selected')

    elif ans == 1:
        if func == 'encrypt':
            try:
                enc_functions.encrypt(paths, option, aes_path, iv_path)
                label_enc = tk.Label(encryption_frame,
                                     text='Images encrypted!')
                label_enc.grid(row=3, column=0, columnspan=3, padx=10, pady=5)
            except Exception as e:
                messagebox.showerror('ERROR', e)

        elif func == 'decrypt':
            try:
                enc_functions.decrypt(paths, option, aes_path, iv_path)
                label_dec = tk.Label(decryption_frame,
                                     text='Data decrypted!')
                label_dec.grid(row=3, column=0, columnspan=3, padx=10, pady=5)
            except Exception as e:
                messagebox.showerror('ERROR', e)
