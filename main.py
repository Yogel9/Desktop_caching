import customtkinter as CTk
import tkinter as Tk
import os
from tkinter import messagebox

from LFU import LFUCache

Text = []


class App(CTk.CTk):

    def __init__(self):
        """ Функция инициализации и отрисовки окна """
        super().__init__()

        self.LFU = LFUCache(capacity=5)

        self.title("Визуализатор кеширования")
        self.geometry('600x700')
        # self.resizable(False, False)

        self.main_frame = CTk.CTkFrame(master=self,
                                       width=200,
                                       height=200)  # прозрачный задний фон fg_color="transparent",
        self.main_frame.pack()

        self.cache_Label = CTk.CTkLabel(master=self.main_frame, text='Данные в кэше', width=40, height=2)
        self.data_Label = CTk.CTkLabel(master=self.main_frame, text='Данные для загрузки', width=40, height=2)
        self.cache_Listbox = Tk.Listbox(master=self.main_frame, width=40, height=20)
        self.data_Listbox = Tk.Listbox(master=self.main_frame, width=40, height=20)

        self.cache_Label.grid(row=0, column=0, padx=(5, 5), pady=(30, 5))
        self.data_Label.grid(row=0, column=2, padx=(5, 5), pady=(30, 5))
        self.cache_Listbox.grid(row=1, column=0, padx=(5, 5), pady=(20, 5))
        self.data_Listbox.grid(row=1, column=2, padx=(5, 5), pady=(20, 5))

        self.set_listdir()

        self.btn_getFileData = CTk.CTkButton(master=self.main_frame, text='Получить данные',
                                             width=100, command=self.data_get, )
        self.btn_getFileData.grid(row=2, column=2, padx=(5, 5), pady=(20, 20))

        self.info_frame = CTk.CTkFrame(master=self,
                                       width=200,
                                       height=200)  # прозрачный задний фон fg_color="transparent",

        self.info_frame.pack(side='bottom')
        self.text_Label = CTk.CTkLabel(master=self.info_frame, text='Считанный текст:', width=40, height=5)
        self.text_Label.pack(side='top')
        self.text = CTk.CTkTextbox(master=self.info_frame, width=510, height=450)
        self.text.pack(side='left')

    def data_get(self):
        if len(self.data_Listbox.curselection()) == 0:
            messagebox.showerror('Ошибка',
                                 'Не выбран файл для считывания\nВыберите файл в списке "Данные для загрузки"')
        else:
            selected_file = self.data_Listbox.get(self.data_Listbox.curselection())
            file = os.getcwd() + '\\Data\\' + selected_file

            data = self.LFU.get(file)
            if data == -1:
                # messagebox.showinfo('Инфо', 'Текст из файла')
                with open(file, 'r', encoding='utf-8') as f:
                    text = f.read()
                    self.LFU.put(file, text)
                    data = text
            else:
                # messagebox.showinfo('Инфо', 'Текст из кэша')
                pass
            self.text.delete(1.0, 'end')
            self.text.insert(index=1.0, text=data)
            self.set_cache()


    def set_cache(self):
        self.cache_Listbox.delete(first=0, last='end')
        for key, value in self.LFU.freq_to_dll.items():
            for item in value.get_value():
                if item is not None:
                    self.cache_Listbox.insert('end', f'{key}-{item}')

    def set_listdir(self):
        """Заполняем Listbox файлами доступными для чтения"""
        content = os.listdir(os.getcwd() + '/Data')
        for filename in content:
            self.data_Listbox.insert(0, filename)


if __name__ == '__main__':
    app = App()
    app.mainloop()

