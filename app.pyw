import ttkbootstrap as ttkb
from PIL import ImageTk

#initiallize App
root  = ttkb.Window(themename="sandstone")
root.title("DNP recently added Domain")
#
#root.eval("tk::PlaceWindow . center")
x= root.winfo_screenwidth() // 2
y = int(root.winfo_screenwidth()*0.1)
root.geometry('500x600+' + str(x) + '+' + str(y))

#Principal Frame
Principal_Frame = ttkb.Frame(root, width=500, height=600)
Principal_Frame.grid(row=0, column=0)
Principal_Frame.pack_propagate(False)

#frame1
logo_img = ImageTk.PhotoImage(file = "assets/gtld-search.png")
logo_widget = ttkb.Label(Principal_Frame, 
                         image=logo_img)
logo_widget.image = logo_img
logo_widget.pack()

Title = ttkb.Label(Principal_Frame, text="Get the recently added domains",
                   bootstyle= "Dark",
                   font=("TkMenuFont",14)
                   ).pack()

logo_widget.pack()



#Run App
root.mainloop()
