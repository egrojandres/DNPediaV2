from tkinter import IntVar
import ttkbootstrap as ttkb
from PIL import ImageTk

#initiallize App
class App(ttkb.Window):
    def __init__(self):
        super().__init__()
        self.title("DNP recently added Domain")
        #root.eval("tk::PlaceWindow . center")
        x= self.winfo_screenwidth() // 2
        y = int(self.winfo_screenwidth()*0.1)
        self.geometry('500x600+' + str(x) + '+' + str(y))
        self.style.theme_use("sandstone")           # Use Theme
        self.main_window()



    def main_window(self):

        #Principal Frame
        Principal_Frame = ttkb.Frame(self, width=500, height=600)
        Principal_Frame.grid(row=0, column=0)
        Principal_Frame.pack_propagate(False)
        
        def changeTheme():
            if Var1.get() == 1: 
                self.style.theme_use("cyborg")
                Select_theme.config(text = 'Dark')
            else: 
                self.style.theme_use("sandstone")
                Select_theme.config(text = 'Light')

        Var1 = IntVar()                    # selected variable
        Select_theme = ttkb.Checkbutton(Principal_Frame, bootstyle="info, round-toggle",
                                        text = 'Light',
                                        variable=Var1,
                                        onvalue=1,
                                        offvalue=0,
                                        command=changeTheme)
        Select_theme.pack(pady=10)

        #frame1
      
        logo_img = ImageTk.PhotoImage(file = "assets/gtld-search.png")
        logo_widget = ttkb.Label(Principal_Frame, 
                                image=logo_img)
        logo_widget.image = logo_img
        logo_widget.pack()

        Title = ttkb.Label(Principal_Frame, text="Get the recently added domains",
                        bootstyle= "default",
                        font=("TkMenuFont",14)
                        ).pack()


if __name__ == '__main__':  
    #Run App
    root = App()
    root.mainloop()

