import os
import tkinter as tk
from tkinter import filedialog
from msg_box import MsgBox


class MainApplication(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self._images = []
        self._data = []
        self._key_path = None
        self._iv_path = None
        
        # SECTION: KEY GENERATION
        key_gen_f = tk.LabelFrame(root, text='Key generation')
        key_gen_f.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        l_key_name = tk.Label(key_gen_f, text='key name:')
        l_key_name.grid(row=0, column=0, padx=10, pady=5)
        e_key_name = tk.Entry(key_gen_f, width=30)
        e_key_name.grid(row=0, column=1, padx=5, pady=5)

        l_iv_name = tk.Label(key_gen_f, text='iv name:')
        l_iv_name.grid(row=1, column=0, padx=10, pady=5)
        e_iv_name = tk.Entry(key_gen_f, width=30)
        e_iv_name.grid(row=1, column=1, padx=5, pady=5)

        b_gen_key = tk.Button(key_gen_f, text='Generate keys',
                              command=lambda:
                              m_box.key_gen_m_box(
                                  e_key_name.get(),
                                  e_iv_name.get()))
        b_gen_key.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        whitespace_1 = tk.Label(key_gen_f, text=' ')
        whitespace_1.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # SECTION: SELECTION
        selection_f = tk.LabelFrame(root, text='Select keys and mode')
        selection_f.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        l_key_file = tk.Label(selection_f, text='key file:')
        l_key_file.grid(row=0, column=0, padx=10, pady=5)

        open_key_file = tk.Button(selection_f, text='Select file',
                                  command=lambda:
                                  self.open_key('key', selection_f))
        open_key_file.grid(row=0, column=1, padx=10, pady=5)

        whitespace_2 = tk.Label(selection_f, text=' ')
        whitespace_2.grid(row=1, column=0, padx=10, pady=5)

        l_iv_file = tk.Label(selection_f, text='iv file:')
        l_iv_file.grid(row=2, column=0, padx=10, pady=5)

        open_iv_file = tk.Button(selection_f, text='Select file',
                                 command=lambda:
                                 self.open_key('iv', selection_f))
        open_iv_file.grid(row=2, column=1, padx=10, pady=5)

        whitespace_3 = tk.Label(selection_f, text='')
        whitespace_3.grid(row=3, column=0, padx=10, pady=5)

        modes = [
            ('CTR', 'CTR'),
            ('CFB', 'CFB'),
            ('OFB', 'OFB')
        ]

        c = tk.StringVar()
        c.set('CTR')

        for text, mode in modes:
            radio = tk.Radiobutton(
                selection_f, text=text, variable=c, value=mode)
            radio.grid(columnspan=2, padx=5, pady=5)

        # SECTION: ENCRYPTION
        enc_f = tk.LabelFrame(root, text='Encrypt files')
        enc_f.grid(row=2, column=0, padx=5, pady=5)

        add_image = tk.Button(enc_f, text='Add',
                              command=lambda:
                              self.add_item(
                                  'image', images_listbox, data_listbox))
        add_image.grid(row=0, column=0, padx=10, pady=5)

        del_image = tk.Button(enc_f, text='Delete',
                              command=lambda:
                              self.del_item(
                                  'image', images_listbox, data_listbox))
        del_image.grid(row=0, column=2, padx=10, pady=5)

        images_listbox = tk.Listbox(enc_f)
        images_listbox.grid(row=1, column=0)
        scrollbar_image = tk.Scrollbar(enc_f)
        scrollbar_image.grid(row=1, column=1)
        images_listbox.config(yscrollcommand=scrollbar_image.set)
        scrollbar_image.config(command=images_listbox.yview)

        enc_image = tk.Button(enc_f, text='Encrypt',
                              command=lambda:
                              m_box.enc_dec_m_box(
                                  self._images, c.get(), self._key_path,
                                  self._iv_path, 'encrypt'))
        enc_image.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

        whitespace_4 = tk.Label(enc_f, text='')
        whitespace_4.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

        # SECTION: DECRYPTION
        dec_f = tk.LabelFrame(root, text='Decrypt files')
        dec_f.grid(row=2, column=1, padx=5, pady=5)

        add_data = tk.Button(dec_f, text='Add',
                             command=lambda: self.add_item(
                                 'data', images_listbox, data_listbox))
        add_data.grid(row=0, column=0, padx=10, pady=5)

        del_data = tk.Button(dec_f, text='Delete',
                             command=lambda: self.del_item(
                                 'data', images_listbox, data_listbox))
        del_data.grid(row=0, column=2, padx=10, pady=5)

        data_listbox = tk.Listbox(dec_f)
        data_listbox.grid(row=1, column=0)
        scrollbar_data = tk.Scrollbar(dec_f)
        scrollbar_data.grid(row=1, column=1)
        data_listbox.config(yscrollcommand=scrollbar_data.set)
        scrollbar_data.config(command=data_listbox.yview)

        dec_image = tk.Button(dec_f, text='Decrypt',
                              command=lambda:
                              m_box.enc_dec_m_box(
                                  self._data, c.get(), self._key_path,
                                  self._iv_path, 'decrypt'))
        dec_image.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

        whitespace_5 = tk.Label(dec_f, text='')
        whitespace_5.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

        # SECTION: MSG_BOX CONNECTION
        m_box = MsgBox(root, key_gen_f, enc_f, dec_f)

    def open_key(self, key_type, selection_f):
        filename = filedialog.askopenfilename(
            initialdir='../keys',
            title='Select a file',
            filetypes=(('txt files', '*.txt'),))
        l_file = tk.Label(selection_f, text=filename)

        if key_type == 'key':
            l_file.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
            self._key_path = filename
        elif key_type == 'iv':
            l_file.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
            self._iv_path = filename

    def add_item(self, add_type, images_listbox, data_listbox):
        if add_type == 'image':
            filename = filedialog.askopenfilename(
                initialdir='../images',
                title='Select a file',
                filetypes=(('jpg, png files', '*.jpg *.png'),))
            if filename != '':
                images_listbox.insert(tk.END, os.path.basename(filename))
                self._images.append(filename)

        elif add_type == 'data':
            filename = filedialog.askopenfilename(
                initialdir='../enc_images',
                title='Select a file',
                filetypes=(('bin files', '*.bin'),))
            if filename != '':
                data_listbox.insert(tk.END, os.path.basename(filename))
                self._data.append(filename)

    def del_item(self, del_type, images_listbox, data_listbox):
        if del_type == 'image':
            selected = images_listbox.curselection()
            images_listbox.delete(selected[0])
            self._images.pop(selected[0])
        elif del_type == 'data':
            selected = data_listbox.curselection()
            data_listbox.delete(selected[0])
            self._data.pop(selected[0])


# SECTION: MAIN LOOP
if __name__ == '__main__':
    root = tk.Tk()
    MainApplication(root)
    root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='../icon.png'))
    root.title('AES Image Encryption')
    root.mainloop()
