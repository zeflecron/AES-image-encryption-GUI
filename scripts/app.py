import os
import tkinter as tk
from tkinter import filedialog
import msg_box

# SECTION: FUNCTIONS FOR TKINTER
images = []
data = []
aes_path = None
iv_path = None


def open_key(key_type):
    global aes_path
    global iv_path
    filename = filedialog.askopenfilename(initialdir='../keys',
                                          title='Select a file',
                                          filetypes=(('txt files', '*.txt'),))
    label_file = tk.Label(selection_frame, text=filename)

    if key_type == 'aes':
        label_file.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
        aes_path = filename
    elif key_type == 'iv':
        label_file.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
        iv_path = filename


def add_item(add_type):
    if add_type == 'image':
        filename = \
            filedialog.askopenfilename(initialdir='../images',
                                       title='Select a file',
                                       filetypes=(('jpg, jpeg, png files',
                                                   '*.jpg *.png *.jpeg'),))
        if filename != '':
            images_listbox.insert(tk.END, os.path.basename(filename))
            images.append(filename)

    elif add_type == 'data':
        filename = \
            filedialog.askopenfilename(initialdir='../enc_images',
                                       title='Select a file',
                                       filetypes=(('bin files', '*.bin'),))
        if filename != '':
            data_listbox.insert(tk.END, os.path.basename(filename))
            data.append(filename)


def del_item(del_type):
    if del_type == 'image':
        selected = images_listbox.curselection()
        images_listbox.delete(selected[0])
        images.pop(selected[0])
    elif del_type == 'data':
        selected = data_listbox.curselection()
        data_listbox.delete(selected[0])
        data.pop(selected[0])


# SECTION: INITIALIZATION
root = tk.Tk()
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='../icon.png'))
root.title('AES Image Encryption')

# SECTION: KEY GENERATION
key_gen_frame = tk.LabelFrame(root, text='Key generation')
key_gen_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

label_AES_name = tk.Label(key_gen_frame, text='AES key name:')
label_AES_name.grid(row=0, column=0, padx=10, pady=5)

entry_AES_name = tk.Entry(key_gen_frame, width=30)
entry_AES_name.grid(row=0, column=1, padx=5, pady=5)

label_iv_name = tk.Label(key_gen_frame, text='iv key name:')
label_iv_name.grid(row=1, column=0, padx=10, pady=5)

entry_iv_name = tk.Entry(key_gen_frame, width=30)
entry_iv_name.grid(row=1, column=1, padx=5, pady=5)

button_generate_key = tk.Button(key_gen_frame,
                                text='Generate keys',
                                command=lambda:
                                msg_box.key_gen_msg_box
                                (entry_AES_name.get(),
                                 entry_iv_name.get()))
button_generate_key.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

whitespace_1 = tk.Label(key_gen_frame, text=' ')
whitespace_1.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

# SECTION: SELECTION
selection_frame = tk.LabelFrame(root, text='Select keys and mode')
selection_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

label_AES_file = tk.Label(selection_frame, text='AES key file:')
label_AES_file.grid(row=0, column=0, padx=10, pady=5)

open_AES_file = tk.Button(selection_frame,
                          text='Select file',
                          command=lambda: open_key('aes'))
open_AES_file.grid(row=0, column=1, padx=10, pady=5)

whitespace_2 = tk.Label(selection_frame, text=' ')
whitespace_2.grid(row=1, column=0, padx=10, pady=5)

label_iv_file = tk.Label(selection_frame, text='iv key file:')
label_iv_file.grid(row=2, column=0, padx=10, pady=5)

open_iv_file = tk.Button(selection_frame,
                         text='Select file',
                         command=lambda: open_key('iv'))
open_iv_file.grid(row=2, column=1, padx=10, pady=5)

whitespace_3 = tk.Label(selection_frame, text='')
whitespace_3.grid(row=3, column=0, padx=10, pady=5)

MODES = [
    ('CTR', 'CTR'),
    ('CFB', 'CFB'),
    ('OFB', 'OFB')
]

c = tk.StringVar()
c.set('CTR')

for text, mode in MODES:
    radio = tk.Radiobutton(selection_frame, text=text, variable=c, value=mode)
    radio.grid(columnspan=2, padx=5, pady=5)

# SECTION: ENCRYPTION
encryption_frame = tk.LabelFrame(root, text='Encrypt files')
encryption_frame.grid(row=2, column=0, padx=5, pady=5)

add_image = tk.Button(encryption_frame,
                      text='Add',
                      command=lambda: add_item('image'))
add_image.grid(row=0, column=0, padx=10, pady=5)

del_image = tk.Button(encryption_frame,
                      text='Delete',
                      command=lambda: del_item('image'))
del_image.grid(row=0, column=2, padx=10, pady=5)

images_listbox = tk.Listbox(encryption_frame)
images_listbox.grid(row=1, column=0)

scrollbar_image = tk.Scrollbar(encryption_frame)
scrollbar_image.grid(row=1, column=1)

images_listbox.config(yscrollcommand=scrollbar_image.set)
scrollbar_image.config(command=images_listbox.yview)

enc_image = tk.Button(encryption_frame,
                      text='Encrypt',
                      command=lambda:
                      msg_box.enc_dec_msg_box
                      (images, c.get(), aes_path, iv_path, 'encrypt'))
enc_image.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

whitespace_4 = tk.Label(encryption_frame, text='')
whitespace_4.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

# SECTION: DECRYPTION
decryption_frame = tk.LabelFrame(root, text='Decrypt files')
decryption_frame.grid(row=2, column=1, padx=5, pady=5)

add_data = tk.Button(decryption_frame,
                     text='Add',
                     command=lambda: add_item('data'))
add_data.grid(row=0, column=0, padx=10, pady=5)

del_data = tk.Button(decryption_frame,
                     text='Delete',
                     command=lambda: del_item('data'))
del_data.grid(row=0, column=2, padx=10, pady=5)

data_listbox = tk.Listbox(decryption_frame)
data_listbox.grid(row=1, column=0)

scrollbar_data = tk.Scrollbar(decryption_frame)
scrollbar_data.grid(row=1, column=1)

data_listbox.config(yscrollcommand=scrollbar_data.set)
scrollbar_data.config(command=data_listbox.yview)

dec_image = tk.Button(decryption_frame,
                      text='Decrypt',
                      command=lambda:
                      msg_box.enc_dec_msg_box
                      (data, c.get(), aes_path, iv_path, 'decrypt'))
dec_image.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

whitespace_5 = tk.Label(decryption_frame, text='')
whitespace_5.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

# OPTIMIZE: remove this part
# SECTION: MSG_BOX CONNECTION
msg_box.root = root
msg_box.key_gen_frame = key_gen_frame
msg_box.encryption_frame = encryption_frame
msg_box.decryption_frame = decryption_frame

# SECTION: MAIN LOOP
if __name__ == '__main__':
    root.mainloop()
