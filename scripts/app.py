import os
import tkinter as tk
import glob
from tkinter import filedialog
from msg_box import MsgBox

'''
    l = label
    e = entry
    t = text
    f = frame
    b = button
    m = message
'''


class MainApplication(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self._images = []
        self._data = []
        self._key_path = None
        self._iv_path = None
        
        # SECTION: KEY GENERATION
        f_key_gen = tk.LabelFrame(root, text='Key generation')
        f_key_gen.grid(row=0, column=0, padx=5, pady=5)

        l_key_name = tk.Label(f_key_gen, text='key name:')
        l_key_name.grid(row=0, column=0, padx=10, pady=5)
        e_key_name = tk.Entry(f_key_gen, width=30)
        e_key_name.grid(row=0, column=1, padx=5, pady=5)

        l_iv_name = tk.Label(f_key_gen, text='iv name:')
        l_iv_name.grid(row=1, column=0, padx=10, pady=5)
        e_iv_name = tk.Entry(f_key_gen, width=30)
        e_iv_name.grid(row=1, column=1, padx=5, pady=5)

        b_gen_key = tk.Button(f_key_gen, text='Generate keys',
                              command=lambda:
                              m_box.key_gen_m_box(
                                  e_key_name.get(),
                                  e_iv_name.get()))
        b_gen_key.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        t_gen_comp = tk.StringVar()
        l_gen_comp = tk.Label(f_key_gen, textvariable=t_gen_comp)
        l_gen_comp.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # SECTION: SELECTION
        f_selection = tk.LabelFrame(root, text='Select keys and mode')
        f_selection.grid(row=1, column=0, padx=5, pady=5)

        l_key_file = tk.Label(f_selection, text='key file:')
        l_key_file.grid(row=0, column=0, padx=10, pady=5)

        b_open_key_file = tk.Button(f_selection, text='Select file',
                                    command=lambda:
                                    self.open_key('key', t_key_path))
        b_open_key_file.grid(row=0, column=1, padx=10, pady=5)

        t_key_path = tk.StringVar()
        l_key_path = tk.Label(f_selection, textvariable=t_key_path,
                              wraplength=350)
        l_key_path.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        l_iv_file = tk.Label(f_selection, text='iv file:')
        l_iv_file.grid(row=2, column=0, padx=10, pady=5)

        b_open_iv_file = tk.Button(f_selection, text='Select file',
                                   command=lambda:
                                   self.open_key('iv', t_iv_path))
        b_open_iv_file.grid(row=2, column=1, padx=10, pady=5)

        t_iv_path = tk.StringVar()
        l_iv_path = tk.Label(f_selection, textvariable=t_iv_path,
                             wraplength=350)
        l_iv_path.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        modes = [
            ('CTR', 'CTR'),
            ('CFB', 'CFB'),
            ('OFB', 'OFB')
        ]

        # NOTE: changing c into something like t_choice somehow messes it up
        c = tk.StringVar()
        c.set('CTR')

        for text, mode in modes:
            radio = tk.Radiobutton(
                f_selection, text=text, variable=c, value=mode)
            radio.grid(columnspan=2, padx=5, pady=5)

        # SECTION: ENCRYPTION
        f_enc = tk.LabelFrame(root, text='Encrypt files')
        f_enc.grid(row=0, rowspan=2, column=1, padx=5, pady=5)

        b_add_image = tk.Button(f_enc, text='Add image',
                                command=lambda:
                                self.add_item(
                                    'image', images_listbox, data_listbox))
        b_add_image.grid(row=0, column=0, padx=10, pady=5)

        b_del_image = tk.Button(f_enc, text='Delete',
                                command=lambda:
                                self.del_item(
                                    'image', images_listbox, data_listbox))
        b_del_image.grid(row=0, column=2, padx=10, pady=5)

        b_add_img_dir = tk.Button(f_enc, text='Add directory',
                                  command=lambda:
                                  self.add_dir(
                                      'image', images_listbox, data_listbox))
        b_add_img_dir.grid(row=1, column=0, padx=10, pady=5)

        b_del_img_all = tk.Button(f_enc, text='Delete all',
                                  command=lambda:
                                  self.del_all(
                                      'image', images_listbox, data_listbox))
        b_del_img_all.grid(row=1, column=2, padx=10, pady=5)

        images_listbox = tk.Listbox(f_enc)
        images_listbox.grid(row=2, column=0)
        scrollbar_image = tk.Scrollbar(f_enc)
        scrollbar_image.grid(row=2, column=1)
        images_listbox.config(yscrollcommand=scrollbar_image.set)
        scrollbar_image.config(command=images_listbox.yview)

        b_enc_image = tk.Button(f_enc, text='Encrypt',
                                command=lambda:
                                m_box.enc_dec_m_box(
                                    self._images, c.get(), self._key_path,
                                    self._iv_path, 'encrypt'))
        b_enc_image.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

        t_enc_comp = tk.StringVar()
        l_enc_comp = tk.Label(f_enc, textvariable=t_enc_comp)
        l_enc_comp.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

        # SECTION: DECRYPTION
        f_dec = tk.LabelFrame(root, text='Decrypt files')
        f_dec.grid(row=0, rowspan=2, column=2, padx=5, pady=5)

        b_add_data = tk.Button(f_dec, text='Add',
                               command=lambda: self.add_item(
                                   'data', images_listbox, data_listbox))
        b_add_data.grid(row=0, column=0, padx=10, pady=5)

        b_del_data = tk.Button(f_dec, text='Delete',
                               command=lambda: self.del_item(
                                   'data', images_listbox, data_listbox))
        b_del_data.grid(row=0, column=2, padx=10, pady=5)

        b_add_data_dir = tk.Button(f_dec, text='Add directory',
                                   command=lambda:
                                   self.add_dir(
                                       'data', images_listbox, data_listbox))
        b_add_data_dir.grid(row=1, column=0, padx=10, pady=5)

        b_del_data_all = tk.Button(f_dec, text='Delete all',
                                   command=lambda:
                                   self.del_all(
                                       'data', images_listbox, data_listbox))
        b_del_data_all.grid(row=1, column=2, padx=10, pady=5)

        data_listbox = tk.Listbox(f_dec)
        data_listbox.grid(row=2, column=0)
        scrollbar_data = tk.Scrollbar(f_dec)
        scrollbar_data.grid(row=2, column=1)
        data_listbox.config(yscrollcommand=scrollbar_data.set)
        scrollbar_data.config(command=data_listbox.yview)

        b_dec_image = tk.Button(f_dec, text='Decrypt',
                                command=lambda:
                                m_box.enc_dec_m_box(
                                    self._data, c.get(), self._key_path,
                                    self._iv_path, 'decrypt'))
        b_dec_image.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

        t_dec_comp = tk.StringVar()
        l_dec_comp = tk.Label(f_dec, textvariable=t_dec_comp)
        l_dec_comp.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

        # SECTION: MSG_BOX CONNECTION
        m_box = MsgBox(root, t_gen_comp, t_key_path,
                       t_iv_path, t_enc_comp, t_dec_comp)

    def open_key(self, key_type, label):
        filename = filedialog.askopenfilename(
            initialdir='../keys',
            title='Select a file',
            filetypes=(('txt files', '*.txt'),))
        label.set(filename)

        if key_type == 'key':
            self._key_path = filename
        elif key_type == 'iv':
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

    def add_dir(self, add_type, images_listbox, data_listbox):
        if add_type == 'image':
            dir_name = filedialog.askdirectory(
                initialdir='../images',
                title='select a directory')
            for filename in glob.iglob(dir_name + '**/*.jpg', recursive=True):
                images_listbox.insert(tk.END, os.path.basename(filename))
                self._images.append(filename)
            for filename in glob.iglob(dir_name + '**/*.png', recursive=True):
                images_listbox.insert(tk.END, os.path.basename(filename))
                self._images.append(filename)
        elif add_type == 'data':
            dir_name = filedialog.askdirectory(
                initialdir='../enc_images',
                title='select a directory')
            for filename in glob.iglob(dir_name + '**/*.bin', recursive=True):
                data_listbox.insert(tk.END, os.path.basename(filename))
                self._data.append(filename)

    def del_item(self, del_type, images_listbox, data_listbox):
        try:
            if del_type == 'image':
                selected = images_listbox.curselection()
                images_listbox.delete(selected[0])
                self._images.pop(selected[0])
            elif del_type == 'data':
                selected = data_listbox.curselection()
                data_listbox.delete(selected[0])
                self._data.pop(selected[0])
        except Exception as e:
            print(str(e))

    def del_all(self, del_type, images_listbox, data_listbox):
        try:
            if del_type == 'image':
                images_listbox.delete(0, tk.END)
                self._images = []
            elif del_type == 'data':
                data_listbox.delete(0, tk.END)
                self._data = []
        except Exception as e:
            print(str(e))


# SECTION: MAIN LOOP
if __name__ == '__main__':
    root = tk.Tk()
    MainApplication(root)
    root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='../icon.png'))
    root.title('AES Image Encryption')
    root.mainloop()
