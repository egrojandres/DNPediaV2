from tkinter import IntVar
import ttkbootstrap as ttkb
from PIL import ImageTk
from relative_Paths import *

#initiallize App
class Mini_Frame(ttkb.Frame):
    def __init__(self, master, **kwards):
        super().__init__(master, **kwards)
        self.configure(bootstyle = "secondary")
        self.pack(expand = True, fill = 'both')

class App(ttkb.Window):
    def __init__(self):
        super().__init__()
        self.title("DNP recently added Domain")
        #root.eval("tk::PlaceWindow . center")
        x= self.winfo_screenwidth() // 2
        y = int(self.winfo_screenwidth()*0.1)
        self.geometry('500x600+' + str(x) + '+' + str(y))
        self.style.theme_use("sandstone")           # Use Theme

        def changeTheme():
            if Var1.get() == 1: 
                self.style.theme_use("cyborg")
                Select_theme.config(text = 'Dark')
            else: 
                self.style.theme_use("sandstone")
                Select_theme.config(text = 'Light')

        #Principal Frame
        Principal_Frame = ttkb.Frame(self, width=500, height=600)
        Principal_Frame.pack_propagate(False)
        Principal_Frame.pack()
        
        Var1 = IntVar()                    # selected variable
        Select_theme = ttkb.Checkbutton(Principal_Frame, bootstyle="info, round-toggle",
                                        text = 'Light',
                                        variable=Var1,
                                        onvalue=1,
                                        offvalue=0,
                                        command=changeTheme)
        Select_theme.pack(pady=10, padx=10)

        #Frame1
        logo_img = ImageTk.PhotoImage(file = "assets/gtld-search.png")
        logo_widget = ttkb.Label(Principal_Frame, 
                                image=logo_img)
        logo_widget.image = logo_img
        logo_widget.pack(padx=10, pady=10)
        
        Title = ttkb.Label(Principal_Frame, text="Get the recently added domains",
                        bootstyle= "default",
                        font=("TkMenuFont",14)
                        )
        Title.pack(padx=10, pady=10)

        def handle_submit(value):
            countries = list
            if value == 'Keyword':
                search_label.configure(text = "Introduce your Kwd")
                entry.pack(padx=10, pady=10)
                
            
            elif value == 'Dict. from Countries':

                search_label.configure(text = "choose a country:")
                file = Path('docs','customers.json')
                f = open(file)
                data = json.loads(f)
                
                for d in data:
                    countries.append(['country'][0])

        search_label = ttkb.Label(Principal_Frame, bootstyle= "primary")
        search_label.pack(padx=10, pady=10)

        search_method = IntVar()
        options  = ['Keyword', 'Dict. from Countries']

        for i, option in enumerate(options):
            radio_selector = ttkb.Radiobutton(Principal_Frame, text = option,
                                                value = option, variable= search_method,
                                                command = lambda x=option: handle_submit(x))
            radio_selector.pack(padx=10, pady=10)

        entry = ttkb.Entry(Principal_Frame, text = "Enter the keyword that you want to search")    

if __name__ == '__main__':  
    #Run App
    root = App()
    root.mainloop()

