#FORMULARIO LOGIN - Escritorio

from tkinter import *
from tkinter import ttk
from tkinter import messagebox 
#Python image Library
from PIL import ImageTk, Image
#data local
from data import users_dict

class Login:
    users_data = users_dict.users

    def __init__(self,window_login):
        self.window = window_login  
        #nombre de la ventana
        self.window.title("Ventana de acceso")
        #tamaño
        self.window.geometry("420x370")
        self.window.resizable(0,0)
        #self.window.configure(background="#ffffff")
                
        #Encabezado
        frame_enc = Frame(window_login)
        frame_enc.pack()

        img_login = Image.open("img/login.png")
        img_render = ImageTk.PhotoImage(img_login.resize((30,30)))
        label_img = Label(frame_enc, image = img_render)
        label_img.image = img_render
        label_img.grid(row=0,column=0,sticky='s',padx=10,pady=30)

        Label(frame_enc, text="INICIAR SESION",fg="black",font=("Comic Sans", 15), pady=10).grid(row=0, column=1)

        #Formulario: campos username y password
        frame_form = LabelFrame(window_login, text="Datos",font=("Comic Sans", 11))
        frame_form.pack()

        Label(frame_form,text="Usuario: ",font=("Comic Sans", 13)).grid(row=0,column=0,padx=10,pady=(30,15))
        self.user = Entry(frame_form,width=25,font=("Comic Sans", 13))
        self.user.focus()
        self.user.grid(row=0, column=1, padx=10, pady=(30,15))

        Label(frame_form,text="Contraseña: ",font=("Comic Sans", 13)).grid(row=1,column=0,padx=10,pady=(15,30))
        self.passw = Entry(frame_form,width=25,font=("Comic Sans", 13))
        self.passw.focus()
        self.passw.grid(row=1, column=1, padx=10, pady=(15,30))

        #Botón
        frame_btn = Frame(window_login)
        frame_btn.pack()

        Button(frame_btn,text="Acceder", command = self.loginuser, height=2, width=12, bg="black",fg="#ffffff",font=("Comic Sans", 13)).grid(row=0, column=1, padx=10, pady=15)

    def getFormData(self):
        userfrm = self.user.get()
        passwfrm = self.passw.get()
        validate = self.validateData(userfrm, passwfrm)
        return validate

    def validateData(self, user, passw):
        #aqui hay que validar los datos
        valresult = None
        for ud in Login.users_data:
            if ud["nickname"] == user and ud["passw"] == passw:
                valresult = [user, passw]
        return valresult

    def loginuser(self):
        result = self.getFormData()
        if result:
            messagebox.showinfo("BIENVENIDO", f"Los datos son correctos {result[0]}") 
            self.open_window()
        else:
            messagebox.showinfo("No se ha podido acceder", f"Comprueba que los datos son correctos") 

    def open_window(self):

        window_login.destroy()
        new_window = Tk()
        new_window.title("Acceso al programa")
        new_window.geometry("600x500")
        #new_window.configure(background="#ffffff")

        frame_enc = Frame(new_window)
        frame_enc.pack()

        img_login = Image.open("img/user.png")
        img_render = ImageTk.PhotoImage(img_login.resize((50,50)))
        label_img = Label(frame_enc, image = img_render)
        label_img.image = img_render
        label_img.grid(row=0,column=0,sticky='s',padx=20,pady=50)

        Label(frame_enc, text="Bienvenido al programa",fg="black",font=("Comic Sans", 25), pady=50).grid(row=0, column=1)

        new_window.mainloop()



if __name__ == '__main__':
    window_login = Tk()
    application = Login(window_login)
    window_login.mainloop()



