from tkinter import *  
from PIL import Image, ImageTk  #pip install pillow
from customer import Cust_Win
from room import Room_Win
from details import DetailsRoom


class HotelManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("1550x800+0+0")

        # Load and resize the image
        img1 = Image.open(r"C:\Users\shiva\OneDrive\Desktop\HMS Project\images\hotel images\hotel1.png")
        img1 = img1.resize((1550, 140), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)  

        # # Display the image on a label
        lblimg = Label(self.root, image=self.photoimg1,bd=4,relief=RIDGE)
        lblimg.place(x=0, y=0, width=1550, height=140)

        #============LOGO=============#
        img2 = Image.open(r"C:\Users\shiva\OneDrive\Desktop\HMS Project\images\hotel images\logohotel.png")
        img2 = img2.resize((230, 140), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)  

        lblimg = Label(self.root, image=self.photoimg2,bd=4,relief=RIDGE)
        lblimg.place(x=0, y=0, width=230, height=140)

        #===========title===========#
        lbl_title=Label(self.root,text= "HOTEL DESK DASHBOARD", font=("times new roman",40,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
        lbl_title.place(x=0,y=140,width=1550,height=55)

        #=========Main Frame=========#
        main_frame=Frame(self.root,bd=4,relief=RIDGE)
        main_frame.place(x=0,y=190,width=1550,height=620)

        #==========Menu===========#
        lbl_menu=Label(main_frame,text= "MENU", font=("times new roman",20,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
        lbl_menu.place(x=0,y=0,width=230)

        #=========Button Frame=========#
        btn_frame=Frame(main_frame,bd=4,relief=RIDGE)
        btn_frame.place(x=0,y=35,width=230,height=190)

        cust_btn=Button(btn_frame,text="CUSTOMER",command=self.cust_details,font=("times new roman",12,"bold"),bg="black",fg="gold",bd=0,width=25,cursor="hand2")
        cust_btn.grid(row=0,column=0,pady=1)

        room_btn=Button(btn_frame,text="ROOM",command=self.roombooking_details,font=("times new roman",12,"bold"),bg="black",fg="gold",bd=0,width=25,cursor="hand2")
        room_btn.grid(row=1,column=0,pady=1)

        details_btn=Button(btn_frame,text="DETAILS",command=self.room_details,font=("times new roman",12,"bold"),bg="black",fg="gold",bd=0,width=25,cursor="hand2")
        details_btn.grid(row=2,column=0,pady=1)

        # report_btn=Button(btn_frame,text="REPORT",font=("times new roman",12,"bold"),bg="black",fg="gold",bd=0,width=25,cursor="hand2")
        # report_btn.grid(row=3,column=0,pady=1)

        logout_btn=Button(btn_frame,text="LOGOUT",command=self.logout,font=("times new roman",12,"bold"),bg="black",fg="gold",bd=0,width=25,cursor="hand2")
        logout_btn.grid(row=4,column=0,pady=1)


        #===============Right Side Image===========#
        img3 = Image.open(r"C:\Users\shiva\OneDrive\Desktop\HMS Project\images\hotel images\slide3.jpg")
        img3 = img3.resize((1300, 590), Image.Resampling.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)  

        # # Display the image on a label
        lblimg1 = Label(main_frame, image=self.photoimg3,bd=4,relief=RIDGE)
        lblimg1.place(x=225, y=0, width=1300, height=590)


        #========Left down image=========#

        img4 = Image.open(r"C:\Users\shiva\OneDrive\Desktop\HMS Project\images\hotel images\myh.jpg")
        img4 = img4.resize((230, 200), Image.Resampling.LANCZOS)
        self.photoimg4 = ImageTk.PhotoImage(img4)  

        lblimg1 = Label(main_frame, image=self.photoimg4,bd=4,relief=RIDGE)
        lblimg1.place(x=0, y=165, width=225, height=200)

        img5 = Image.open(r"C:\Users\shiva\OneDrive\Desktop\HMS Project\images\hotel images\khana.jpg")
        img5 = img5.resize((230, 225), Image.Resampling.LANCZOS)
        self.photoimg5 = ImageTk.PhotoImage(img5)  

        lblimg1 = Label(main_frame, image=self.photoimg5,bd=4,relief=RIDGE)
        lblimg1.place(x=0, y=365, width=225, height=225)

    def cust_details(self):
        self.new_window=Toplevel(self.root)
        self.app=Cust_Win(self.new_window)

    def roombooking_details(self):
        self.new_window=Toplevel(self.root)
        self.app=Room_Win(self.new_window)

    def room_details(self):
        self.new_window=Toplevel(self.root)
        self.app=DetailsRoom(self.new_window)

    def logout(self):
        self.root.destroy()

if __name__ == '__main__':
    root = Tk()
    obj=HotelManagementSystem(root)  
    root.mainloop()