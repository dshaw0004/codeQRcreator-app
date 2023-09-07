import os, tkinter
from webbrowser import open_new
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror
from getpass import getuser
import customtkinter, qrcode
from PIL import Image

customtkinter.set_default_color_theme("green")


class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x300+0+0")
        self.resizable(0,0)
        self.after(250, lambda : self.iconbitmap("assets/codeQRcreator-icon.ico"))

        self.title("codeQRcreator - info")
        about_frame = self.about()
        about_frame.pack(expand=True, fill='both')
        key_bind_frame = self.keybinds()
        key_bind_frame.pack(expand=True, fill='both')
        self.author = customtkinter.CTkButton(
            master=self,
            text="made by - dshaw0004",
            fg_color="transparent",
            text_color=("#0000ff", "#4444ff"),
            hover_color=("#ebebeb", "#242424"),
            command=lambda: open_new(url="https://github.com/dshaw0004")
        )
        self.author.place(rely=0.9, relx=0.7, relheight=0.1, relwidth=0.3)

    def keybinds(self):
        frame = customtkinter.CTkFrame(self, fg_color='transparent')
        title = customtkinter.CTkLabel(frame, text='Key Binds', font=('Times New Roman', 24, 'bold', 'underline'))
        title.pack()
        ins = customtkinter.CTkLabel(frame, text='press INS( Insert ) key to put focus on the input bar')
        ins.pack()
        rtrn = customtkinter.CTkLabel(frame, text='press Enter( Return ) key after entering text in input bar to create qr code')
        rtrn.pack()
        esc = customtkinter.CTkLabel(frame, text='press ESC( Escape ) key to close the app')
        esc.pack()

        return frame

    def about(self):
        frame = customtkinter.CTkFrame(self, fg_color='transparent')
        title = customtkinter.CTkLabel(frame, text='About', font=('Times New Roman', 24, 'bold', 'underline'))
        title.pack()
        about = '''
codeQRcreator is a Python app that allows you to create QR codes for any type of data.
With a simple and intuitive interface, you can generate custom QR codes for your 
specific needs. Whether you need to share a website, contact information, or any
 other data, codeQRcreator makes it easy to create and share QR codes.'''
        about_label = customtkinter.CTkLabel(frame, text=about,)
        about_label.pack(anchor='w')
        subframe = customtkinter.CTkFrame(frame, fg_color='transparent')
        subframe.pack(anchor='w')
        customtkinter.CTkLabel(subframe, text='Website: ').grid(column=0, row=0)
        customtkinter.CTkButton(subframe,
                                text='https://pyapps.web.app',
                                fg_color="transparent",
            text_color=("#0000ff", "#4444ff"),
            hover_color=("#ebebeb", "#242424"),
            command=lambda :open_new("https://pyapps.web.app")
                                ).grid(column=1, row=0)

        return frame


class codeQRcreator(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.current_qr = None
        self.current_qr_filename = None
        self.geometry("500x300+200+100")
        self.minsize(400, 250)
        self.maxsize(600, 400)
        self.title("codeQRcreator")
        self.iconbitmap("assets/codeQRcreator-icon.ico")
        gui_top_area = self.gui_top()
        gui_top_area.place(relx=0, rely=0, relheight=0.5, relwidth=1.0)
        gui_bottom_area, self.get_input, self.inputbar, self.save_btn = self.gui_bottom()
        gui_bottom_area.place(relx=0, rely=0.5, relheight=0.5, relwidth=1.0)
        info = customtkinter.CTkButton(self, text="",
                                       image=customtkinter.CTkImage(light_image=Image.open('assets/info_48.png'),
                                                                    size=(18,18)),
                                       fg_color="transparent",
                                       hover_color=("#ebebeb", "#242424"),
                                       command=self.open_toplevel
                                       )
        self.toplevel_window = None
        info.place(relx=0.93, rely=0, relheight=0.08, relwidth=0.07)
        self.inputbar.bind("<Return>", lambda event: self.getdata())
        self.bind("<Escape>", lambda e: self.quit())
        self.bind("<Insert>", lambda e: self.inputbar.focus_set())

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self) 
        else:
            self.toplevel_window.focus()

    def create_QR_code(self, text):
        self.current_qr = qrcode.make(text)
        self.current_qr_filename = f'codeQRcreator ({text})'
        if not os.path.exists('temp'):
            os.makedirs('temp')
        self.current_qr.save(f"temp/{self.current_qr_filename}.png", format="png")
        self.img.configure(dark_image=Image.open(f"temp/{self.current_qr_filename}.png"))
        self.save_btn.configure(state='normal')

    def getdata(self, *args):
        input_text = self.get_input()
        if input_text == '':
            showerror('Error', 'Input is empty\nPlease enter something')
        else:
            self.create_QR_code(text=input_text)

    def gui_top(self):
        top_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        self.img = customtkinter.CTkImage(dark_image=Image.open(
            "assets/codeQRcreator-icon.png"), size=(150, 150))
        label = customtkinter.CTkLabel(master=top_frame, text=" ", image=self.img)
        label.pack(fill='y', expand=True)
        return top_frame

    def gui_bottom(self):
        bottom_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        bottom_frame.columnconfigure(index=0, weight=2)
        bottom_frame.columnconfigure(index=1, weight=2)
        bottom_frame.columnconfigure(index=2, weight=1)
        bottom_frame.columnconfigure(index=3, weight=2)
        bottom_frame.rowconfigure(index=0, weight=2)
        bottom_frame.rowconfigure(index=1, weight=2)
        bottom_frame.rowconfigure(index=2, weight=2)
        bottom_frame.rowconfigure(index=3, weight=2)
        inputbar = customtkinter.CTkEntry(master=bottom_frame,
                                          placeholder_text="Enter your text :",
                                          placeholder_text_color=(
                                              "#73025a", "#efefef"),
                                          text_color=("#73025a", "#efefef"),
                                          fg_color=("#decee5", "#444444"),
                                          font=("Constantia", 18, "bold"),
                                          corner_radius=10)
        inputbar.grid(row=1, column=0, columnspan=4, sticky='ew', padx=10)
        def get_input():
            return inputbar.get()

        generate_btn = customtkinter.CTkButton(
            master=bottom_frame,
            text="Generate",
            fg_color="transparent",
            border_color=("#ffff00", "#00ffff"),
            border_width=1,
            hover_color=("#dede00", "#006969"),
            text_color=("#008080", "#fce554"),
            font=("Constantia", 16, "bold"),
            command=self.getdata
        )
        generate_btn.grid(row=2, column=1)
        download_img = customtkinter.CTkImage(light_image=Image.open('assets/download_light.png'), size=(16, 16))
        download_btn = customtkinter.CTkButton(bottom_frame,
                                               text='save', image=download_img,
                                               command=self.save_qr_locally,
                                               state='disabled')
        download_btn.grid(row=2, column=2)
        return bottom_frame, get_input, inputbar, download_btn

    def save_qr_locally(self):
        PATH = fr'C:\Users\{getuser()}\Pictures\codeQRcreator'
        if not os.path.exists(PATH):
            os.makedirs(PATH)
        location = askdirectory(initialdir=PATH,
                                title="select a folder")
        self.current_qr.save(os.path.join(location, f"{self.current_qr_filename}.png"), format="png")




if __name__ == '__main__':
    app = codeQRcreator()
    app.mainloop()
    for f in os.listdir('temp'):
        if f.startswith('codeQRcreator') and f.endswith('.png'):
            os.remove(os.path.join('temp/', f))
