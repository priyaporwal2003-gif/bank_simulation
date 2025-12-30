from tkinter import Tk,Label,Frame,Button,Entry,messagebox,simpledialog,filedialog
import time
import sqlite3
import TableCreator
import Generator
import EmailHandler
from datetime import datetime
TableCreator.create()
import re
from PIL import Image,ImageTk
import os


def update_time():                                                    #to define function
    curdate=time.strftime('%d-%b-%Y⏰%r')                             #to provide current date and time
    date.configure(text=curdate)                                       #to change date format
    date.after(1000,update_time)                                        #to call function after 1000 millisec repeatidly


def forgot_screen():                                            #to define function for forgot password
    def back():                                                 #to create nested function for deleting existuser_screen's frame 
        frm.destroy()
        existuser_screen()    

    def reset_click():                                      #when you click on the reset button all insert value will be deleted
        e_acn.delete(0,'end')
        e_adhar.delete(0,'end')
        e_acn.focus()

    def send_otp():                                    #to define function for sending otp to your mail to display your forgetten password
        gen_otp=Generator.generate_otp()
        acn=e_acn.get()
        adhar=e_adhar.get()

        if len(acn)==0 or len(adhar)==0:
            messagebox.showwarning('Forgot Pass','Empty fields are not allowed')
            return

        conobj=sqlite3.connect(database='mybank.sqlite')
        curobj=conobj.cursor()
        query='''select name,email,pass from accounts where acn=? and adhar=?'''
        curobj.execute(query,(acn,adhar))
        tup=curobj.fetchone()
        conobj.close()
        if tup==None:
            messagebox.showerror('Forgot Password','Record not found')
        else:
            EmailHandler.send_otp(tup[1],tup[0],gen_otp)
            attempts=1
            while attempts<=3:
                user_otp=simpledialog.askinteger('Password Recovery','Enter OTP')
                if gen_otp==user_otp:
                    messagebox.showinfo('Password Recovery',f'Your Password = {tup[2]}')
                    break
                else:
                    messagebox.showerror('Password Recovery','Invalid OTP')
                    if attempts==3:
                        messagebox.showerror('Password Recovery','Your attempts were completed')
                    attempts+=1
            otp_btn.configure(text='Resend OTP',width=10)

    frm=Frame(root,highlightbackground='black',highlightthickness=2)     #to create frame
    frm.configure(bg='pink')                                            #set color of frame
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.75)                #set frame's size  

    back_btn=Button(frm,text='Back',                 #to create back button for returning to previous window
                    font=('arial',20,'bold'),
                    fg='black',
                    bg='powder blue',
                    bd=5,
                    activebackground='purple',
                    activeforeground='white',
                    command=back)
    back_btn.place(relx=0,rely=0)

    lbl_acn=Label(frm,text='🪪Account No',font=('arial',20,'bold'),fg='white',bg='purple',        
                   width=12)
    lbl_acn.place(relx=.3,rely=.2)

    e_acn=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_acn.place(relx=.5,rely=.2)
    e_acn.focus()                             #by default cursor bliniking on the label entry

    lbl_adhar=Label(frm,text='Adhar',font=('arial',20,'bold'),fg='white',bg='purple',
                    width=12)
    lbl_adhar.place(relx=.3,rely=.3)

    e_adhar=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_adhar.place(relx=.5,rely=.3)      


    otp_btn=Button(frm,text='Send OTP',           #to create button for send otp to your mail                    
                    font=('arial',20,'bold'),
                    fg='black',
                    bg='powder blue',
                    bd=5,
                    width=8,
                    activebackground='purple',
                    activeforeground='white',command=send_otp)                
    otp_btn.place(relx=.35,rely=.5)     

    reset_btn=Button(frm,text='Reset',               #it returns all inserting entry cleared   
                    font=('arial',20,'bold'),
                    fg='black',
                    bg='powder blue',
                    bd=5,
                    width=8,
                    activebackground='purple',
                    activeforeground='white',command=reset_click)                
    reset_btn.place(relx=.5,rely=.5)

def welcome_screen(acn=None):                 #make a welcome screen
    def logout():                             # define logout function to return on the main screen
        frm.destroy()
        main_screen()

    def check_screen():                      #make function for display your account details like acn no,acn bal,acn adhar,acn email,acn opendate
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')    
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.8)

        title_lbl=Label(ifrm,text='This is Checked Details Screen',
                        font=('arial',20,'bold','underline'),bg='white',fg='purple')
        title_lbl.pack()

        conobj=sqlite3.connect(database='mybank.sqlite')
        curobj=conobj.cursor()
        query='''select acn,bal,adhar,email,opendate from accounts where acn=?'''
        curobj.execute(query,(acn,))
        tup=curobj.fetchone()
        conobj.close()

        details=f'''
            Account No = {tup[0]}\n
            Account Bal = {tup[1]}\n
            Account Adhar = {tup[2]}\n
            Account Email = {tup[3]}\n
            Account Opendate = {tup[4]}\n
'''
        lbl_details=Label(ifrm,text=details,bg='white',fg='purple',font=('arial',15,'bold'))
        lbl_details.place(relx=.2,rely=.2)
        
    def update_screen():             #make function for update your account registered details
        def update_btn():
            ifrm.destroy()           #destroy check screen and returned to welcome screen
            welcome_screen()
        
        def update_db():
            name=e_name.get()
            email=e_email.get()
            mob=e_mob.get()
            pwd=e_pass.get()

            conobj=sqlite3.connect(database='mybank.sqlite')
            curobj=conobj.cursor()
            query='''update accounts set name=?,email=?,mob=?,pass=? where acn=?'''
            curobj.execute(query,(name,email,mob,pwd,acn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo('Update Screen','Details updated successfully')
            welcome_screen(acn)

        conobj=sqlite3.connect(database='mybank.sqlite')
        curobj=conobj.cursor()
        query='''select name,email,mob,pass from accounts where acn=?'''
        curobj.execute(query,(acn,))
        tup=curobj.fetchone()
        conobj.close()        

        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)       #make inner frame to display your update details
        ifrm.configure(bg='white')    
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.8)

        title_lbl=Label(ifrm,text='This is Updated Details Screen',
                        font=('arial',20,'bold','underline'),bg='white',fg='purple')
        title_lbl.pack()

        lbl_name=Label(ifrm,text='👨‍💼Name',font=('arial',20,'bold'),fg='white',bg='purple',
                   width=7)
        lbl_name.place(relx=.05,rely=.2)

        e_name=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_name.place(relx=.2,rely=.2)
        e_name.focus()                             #by default cursor bliniking on the label entry

        lbl_pass=Label(ifrm,text='Pass',font=('arial',20,'bold'),fg='white',bg='purple',
                    width=7)
        lbl_pass.place(relx=.05,rely=.4)

        e_pass=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_pass.place(relx=.2,rely=.4)

        lbl_mob=Label(ifrm,text='📱Mob',font=('arial',20,'bold'),fg='white',bg='purple',
                  width=7)
        lbl_mob.place(relx=.55,rely=.2)

        e_mob=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_mob.place(relx=.7,rely=.2)

        lbl_email=Label(ifrm,text='Email',font=('arial',20,'bold'),fg='white',bg='purple',
                    width=7)
        lbl_email.place(relx=.55,rely=.4)

        e_email=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_email.place(relx=.7,rely=.4)

        e_name.insert(0,tup[0])
        e_email.insert(0,tup[1])
        e_mob.insert(0,tup[2])
        e_pass.insert(0,tup[3])
                     
        submit_btn=Button(ifrm,text='Submit',                        
                    font=('arial',20,'bold'),
                    fg='black',
                    bg='powder blue',
                    bd=5,
                    width=8,
                    activebackground='purple',
                    activeforeground='white',
                    command=update_db)                
        submit_btn.place(relx=.44,rely=.6)   


    def deposite_screen():             #make function for deposite ammount to your account 
        def deposite_btn():
            ifrm.destroy()            #destroy update screen and returned to welcome screen
            welcome_screen()

        def deposite_db():
            amt=float(e_amt.get())
            conobj=sqlite3.connect(database='mybank.sqlite')
            curobj=conobj.cursor()
            query='''update accounts set bal=bal+? where acn=?'''
            curobj.execute(query,(amt,acn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo('Deposite Screen',f'{amt} deposited successfully')
            e_amt.delete(0,'end')
            e_amt.focus()             
        
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)       #make inner frame to show deposite details
        ifrm.configure(bg='white')    
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.8)

        title_lbl=Label(ifrm,text='This is Deposite Details Screen',
                        font=('arial',20,'bold','underline'),bg='white',fg='purple')
        title_lbl.pack()

        lbl_amt=Label(ifrm,text='Amount',font=('arial',20,'bold'),fg='white',bg='purple',
                   width=7)
        lbl_amt.place(relx=.2,rely=.2)

        e_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_amt.place(relx=.4,rely=.2)
        e_amt.focus() 

        submit_btn=Button(ifrm,text='Submit',                        
                    font=('arial',20,'bold'),
                    fg='black',
                    bg='powder blue',
                    bd=5,
                    width=8,
                    activebackground='purple',
                    activeforeground='white',
                    command=deposite_db)  
                      
        submit_btn.place(relx=.44,rely=.6)        


    def withdraw_screen():              #make function to withdraw ammount from your account
        def withdraw_btn():       
            ifrm.destroy()              #destroy deposite screen and returned to welcome screen
            welcome_screen()

        def withdraw_db():
            amt=float(e_amt.get())
            conobj=sqlite3.connect(database='mybank.sqlite')
            curobj=conobj.cursor()
            query='''select bal,email,name from accounts where acn=?'''
            curobj.execute(query,(acn,))
            tup=curobj.fetchone()
            conobj.close() 

            if tup[0]>=amt:
                gen_otp=Generator.generate_otp()
                EmailHandler.send_otp_withdraw(tup[1],tup[2],gen_otp,amt)
                attempts=1
                while attempts<=3:
                    user_otp=simpledialog.askinteger('Withdraw OTP','OTP')
                    if gen_otp==user_otp:
                        conobj=sqlite3.connect(database='mybank.sqlite')
                        curobj=conobj.cursor()
                        query='''update accounts set bal=bal-? where acn=?'''
                        curobj.execute(query,(amt,acn))
                        conobj.commit()
                        conobj.close()
                        messagebox.showinfo('Withdraqw Screen',f'{amt} withdrawn successfully')
                        e_amt.delete(0,'end')
                        e_amt.focus()
                        break
                    else:
                        messagebox.showerror('Withdraw Screen','Invalid OTP')
                        if attempts==3:
                            messagebox.showerror('Withdraw Screen','Your attempts were completed')
                        attempts+=1
                submit_btn.configure(text='Resend Otp',width=10)

            else:
                messagebox.showwarning('Withdraw Screen',f'Insufficient Bal: {tup[0]}')           
  

        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)       #make inner frame for showing withdraw screen
        ifrm.configure(bg='white')    
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.8)

        title_lbl=Label(ifrm,text='This is Withdraw Details Screen',
                        font=('arial',20,'bold','underline'),bg='white',fg='purple')
        title_lbl.pack() 

        lbl_amt=Label(ifrm,text='Amount',font=('arial',20,'bold'),fg='white',bg='purple',
                   width=7)
        lbl_amt.place(relx=.2,rely=.2)

        e_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_amt.place(relx=.4,rely=.2)
        e_amt.focus() 

        submit_btn=Button(ifrm,text='Submit',                        
                    font=('arial',20,'bold'),
                    fg='black',
                    bg='powder blue',
                    bd=5,
                    width=8,
                    activebackground='purple',
                    activeforeground='white',
                    command=withdraw_db)  
                      
        submit_btn.place(relx=.44,rely=.6)     

    def transfer_screen():             #make function to transfer ammount to another account
        def transfer_btn():
            ifrm.destroy()            #to destroy  withdraw inner frame and returned to welcome screen 
            welcome_screen()

        def transfer_db():
            to_acn=int(e_to.get())
            amt=float(e_amt.get())

            conobj=sqlite3.connect(database='mybank.sqlite')
            curobj=conobj.cursor()
            query='''select * from accounts where acn=?'''
            curobj.execute(query,(to_acn,))
            tup=curobj.fetchone()
            conobj.close()
             
            if tup==None:
                messagebox.showerror('Transfer Screen','Invalid To ACN')  
                return         

            conobj=sqlite3.connect(database='mybank.sqlite')
            curobj=conobj.cursor()
            query='''select bal,email,name from accounts where acn=?'''
            curobj.execute(query,(acn,))
            tup=curobj.fetchone()
            conobj.close() 

            if tup[0]>=amt:
                gen_otp=Generator.generate_otp()
                EmailHandler.send_otp_transfer(tup[1],tup[2],gen_otp,amt,to_acn)
                attempts=1
                while attempts<=3:
                    user_otp=simpledialog.askinteger('Transfer OTP','OTP')
                    if gen_otp==user_otp:
                        conobj=sqlite3.connect(database='mybank.sqlite')
                        curobj=conobj.cursor()
                        query1='''update accounts set bal=bal-? where acn=?'''
                        query2='''update accounts set bal=bal+? where acn=?'''

                        curobj.execute(query1,(amt,acn))
                        curobj.execute(query2,(amt,to_acn))
                        conobj.commit()
                        conobj.close()
                        messagebox.showinfo('Transfer Screen',f'{amt} transfered successfully')
                        e_amt.delete(0,'end')
                        e_amt.focus()
                        break
                    else:
                        messagebox.showerror('Transfer Screen','Invalid OTP')
                        if attempts==3:
                            messagebox.showerror('Transfer Screen','Your Attempts were completed')
                        attempts+=1       
                transfer_btn.configure(text='Resend Otp',width=10)

            else:
                messagebox.showwarning('Transfer Screen',f'Insufficient Bal: {tup[0]}')            

        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)             #make inner frame to show transfer screen
        ifrm.configure(bg='white')    
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.8)

        title_lbl=Label(ifrm,text='This is Transfer Details Screen',
                        font=('arial',20,'bold','underline'),bg='white',fg='purple')
        title_lbl.pack()

        lbl_to=Label(ifrm,text='To ACN',font=('arial',20,'bold'),fg='white',bg='purple',
                   width=7)
        lbl_to.place(relx=.2,rely=.2)

        e_to=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_to.place(relx=.4,rely=.2)
        e_to.focus()         

        lbl_amt=Label(ifrm,text='Amount',font=('arial',20,'bold'),fg='white',bg='purple',
                   width=7)
        lbl_amt.place(relx=.2,rely=.35)

        e_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_amt.place(relx=.4,rely=.35)
        

        transfer_btn=Button(ifrm,text='Transfer',                        
                    font=('arial',20,'bold'),
                    fg='black',
                    bg='powder blue',
                    bd=5,
                    width=8,
                    activebackground='purple',
                    activeforeground='white',
                    command=transfer_db)  
                      
        transfer_btn.place(relx=.44,rely=.6)        

    conobj=sqlite3.connect(database='mybank.sqlite')
    curobj=conobj.cursor()
    query='''select name from accounts where acn=?'''
    curobj.execute(query,(acn,))
    tup=curobj.fetchone()
    conobj.close()


    frm=Frame(root,highlightbackground='black',highlightthickness=2)     #to create frame
    frm.configure(bg='pink')                                            #set color of frame
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.75) 

    logout_btn=Button(frm,text='Logout',
                    font=('arial',20,'bold'),
                    fg='black',
                    bg='powder blue',
                    bd=5,
                    activebackground='purple',
                    activeforeground='white',
                    command=logout)
    logout_btn.place(relx=.9,rely=0)

    lbl_wel=Label(frm,text=f'Welcome,{tup[0]}............',font=('arial',20,'bold'),fg='white',bg='purple')
    lbl_wel.place(relx=.001,rely=0)

    def update_pic():                        #create function for update your picture
        name=filedialog.askopenfilename()
        os.rename(name,f'{acn}.jpg')
        img_profile=Image.open(name).resize((270,150))  
        imgtk_profile=ImageTk.PhotoImage(img_profile,master=root)
        lbl_img_profile=Label(frm,image=imgtk_profile)
        lbl_img_profile.place(relx=.001,rely=.07)
        lbl_img_profile.image=imgtk_profile

    if os.path.exists(f'{acn}.jpg'):
        img_profile=Image.open(f'{acn}.jpg').resize((270,150)) 
    else:
        img_profile=Image.open('default.jpg').resize((270,150))

    imgtk_profile=ImageTk.PhotoImage(img_profile,master=root)

    lbl_img_profile=Label(frm,image=imgtk_profile)
    lbl_img_profile.place(relx=.001,rely=.07)
    lbl_img_profile.image=imgtk_profile

    pic_btn=Button(frm,text='Update Picture',
                    font=('arial',20,'bold'),
                    fg='white',
                    bg='blue',
                    bd=5,
                    width=15,
                    activebackground='purple',
                    activeforeground='white',
                    command=update_pic)
    pic_btn.place(relx=.001,rely=.35)

    check_btn=Button(frm,text='Check Details',
                    font=('arial',20,'bold'),
                    fg='black',
                    bg='powder blue',
                    bd=5,
                    width=15,
                    activebackground='purple',
                    activeforeground='white',
                    command=check_screen)
    check_btn.place(relx=.001,rely=.45)

    update_btn=Button(frm,text='Update Details',
                    font=('arial',20,'bold'),
                    fg='black',
                    bg='powder blue',
                    bd=5,
                    width=15,
                    activebackground='purple',
                    activeforeground='white',
                    command=update_screen)
    update_btn.place(relx=.001,rely=.56)

    deposite_btn=Button(frm,text='Deposite Amount',
                    font=('arial',20,'bold'),
                    fg='white',
                    bg='green',
                    bd=5,
                    width=15,
                    activebackground='purple',
                    activeforeground='white',
                    command=deposite_screen)
    deposite_btn.place(relx=.001,rely=.67)

    withdraw_btn=Button(frm,text='Withdraw Amount',
                    font=('arial',20,'bold'),
                    fg='white',
                    bg='red',
                    bd=5,
                    width=15,
                    activebackground='purple',
                    activeforeground='white',
                    command=withdraw_screen)
    withdraw_btn.place(relx=.001,rely=.78)   

    transfer_btn=Button(frm,text='Transfer Amount',
                    font=('arial',20,'bold'),
                    fg='white',
                    bg='red',
                    bd=5,
                    width=15,
                    activebackground='purple',
                    activeforeground='white',
                    command=transfer_screen)
    transfer_btn.place(relx=.001,rely=.89)      


   
def existuser_screen():                                           #to create function for showing new window
    def back():                                                 #to create nested function for deleting existuser_screen's frame 
        frm.destroy()
        main_screen()

    def fp_click():
        frm.destroy()
        forgot_screen()
    
    def reset_click():
        e_acn.delete(0,'end')
        e_pass.delete(0,'end')
        e_acn.focus()

    def submit_click():
        acn=e_acn.get()
        pwd=e_pass.get()

        if len(acn)==0 or len(pwd)==0:
            messagebox.showwarning('Existing User','Empty fields are not allowed')
            return
    
        conobj=sqlite3.connect(database='mybank.sqlite')
        curobj=conobj.cursor()
        query='''select * from accounts where acn=? and pass=?'''
        curobj.execute(query,(acn,pwd))
        tup=curobj.fetchone()
        conobj.close()
        if tup==None:
            messagebox.showerror('Login','Invalid Credentials')
        else:
            acn=tup[0]
            frm.destroy()
            welcome_screen(acn)

    
    frm=Frame(root,highlightbackground='black',highlightthickness=2)     #to create frame
    frm.configure(bg='pink')                                            #set color of frame
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.75)                #set frame's size     

    back_btn=Button(frm,text='Back',                 #to create back button for returning to previous window
                    font=('arial',20,'bold'),
                    fg='black',
                    bg='powder blue',
                    bd=5,
                    activebackground='purple',
                    activeforeground='white',
                    command=back)
    back_btn.place(relx=0,rely=0)

    lbl_acn=Label(frm,text='🪪Account No',font=('arial',20,'bold'),fg='white',bg='purple',
                   width=12)
    lbl_acn.place(relx=.3,rely=.2)

    e_acn=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_acn.place(relx=.5,rely=.2)
    e_acn.focus()                             #by default cursor bliniking on the label entry

    lbl_pass=Label(frm,text='🔒Password',font=('arial',20,'bold'),fg='white',bg='purple',
                    width=12)
    lbl_pass.place(relx=.3,rely=.3)

    e_pass=Entry(frm,font=('arial',20,'bold'),bd=5,show='*')
    e_pass.place(relx=.5,rely=.3)      


    submit_btn=Button(frm,text='Submit',                        
                    font=('arial',20,'bold'),
                    fg='black',
                    bg='powder blue',
                    bd=5,
                    width=6,
                    activebackground='purple',
                    activeforeground='white',command=submit_click)                
    submit_btn.place(relx=.4,rely=.5)     

    reset_btn=Button(frm,text='Reset',                
                    font=('arial',20,'bold'),
                    fg='black',
                    bg='powder blue',
                    bd=5,
                    width=6,
                    activebackground='purple',
                    activeforeground='white',command=reset_click)                
    reset_btn.place(relx=.5,rely=.5) 

    fp_btn=Button(frm,text='Forgot Password',                
                    font=('arial',20,'bold'),
                    fg='black',
                    bg='powder blue',
                    bd=5,
                    width=15,
                    activebackground='purple',
                    activeforeground='white',command=fp_click)                
    fp_btn.place(relx=.4,rely=.62) 

def newuser_screen():                                           #to create function for showing new window
    def back():                                                 #to create nested function for deleting newuser_screen's frame 
        frm.destroy()
        main_screen()

    def reset_click():
        e_name.delete(0,'end')
        e_email.delete(0,'end')
        e_mob.delete(0,'end')
        e_adhar.delete(0,'end')
        e_name.focus()

    def createacn_db():
        name=e_name.get()
        email=e_email.get()
        mob=e_mob.get()
        adhar=e_adhar.get()

        if len(name)==0 or len(email)==0 or len(mob)==0 or len(adhar)==0:
            messagebox.showwarning('New User','Empty fields are not allowed')
            return
        
        match=re.fullmatch(r"[a-zA-Z0-9_.]+@[a-zA-Z]+\.[a-zA-Z]+",email)
        if match==None:
            messagebox.showwarning('New User','Invalid Email')
            return
        
        match=re.fullmatch("[6-9][0-9]{9}",mob)
        if match==None:
            messagebox.showwarning('New User','Invalid Mob')
            return

        match=re.fullmatch("[2-9][0-9]{11}",adhar)
        if match==None:
            messagebox.showwarning('New User','Invalid Adhar')
            return                 

        bal=0
        opendate=datetime.now()
        pwd=Generator.generate_pass()
        query='''insert into accounts values(?,?,?,?,?,?,?,?)'''
        conobj=sqlite3.connect(database='mybank.sqlite')
        curobj=conobj.cursor()
        curobj.execute(query,(None,name,pwd,mob,email,adhar,bal,opendate))
        conobj.commit()
        conobj.close()

        conobj=sqlite3.connect(database='mybank.sqlite')
        curobj=conobj.cursor()
        query='''select max(acn) from accounts'''
        curobj.execute(query)
        tup=curobj.fetchone()
        conobj.close()
        EmailHandler.send_credentials(email,name,tup[0],pwd)

        messagebox.showinfo('Account Creation','Your account is opened \nwe have mailed your credentials to given email')
        
    frm=Frame(root,highlightbackground='black',highlightthickness=2)     #to create frame
    frm.configure(bg='pink')                                            #set color of frame
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.75)                #set frame's size  

    back_btn=Button(frm,text='Back',                 #to create back button for returning to previous window
                    font=('arial',20,'bold'),
                    fg='black',
                    bg='powder blue',
                    bd=5,
                    activebackground='purple',
                    activeforeground='white',
                    command=back)
    back_btn.place(relx=0,rely=0)     

    lbl_name=Label(frm,text='👨‍💼Name',font=('arial',20,'bold'),fg='white',bg='purple',
                   width=7)
    lbl_name.place(relx=.1,rely=.2)

    e_name=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_name.place(relx=.2,rely=.2)
    e_name.focus()                             #by default cursor bliniking on the label entry

    lbl_email=Label(frm,text='Email',font=('arial',20,'bold'),fg='white',bg='purple',
                    width=7)
    lbl_email.place(relx=.1,rely=.3)

    e_email=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_email.place(relx=.2,rely=.3)

    lbl_mob=Label(frm,text='📱Mob',font=('arial',20,'bold'),fg='white',bg='purple',
                  width=7)
    lbl_mob.place(relx=.5,rely=.2)

    e_mob=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_mob.place(relx=.6,rely=.2)

    lbl_adhar=Label(frm,text='Adhar',font=('arial',20,'bold'),fg='white',bg='purple',
                    width=7)
    lbl_adhar.place(relx=.5,rely=.3)

    e_adhar=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_adhar.place(relx=.6,rely=.3)

    submit_btn=Button(frm,text='Submit',                        
                    font=('arial',20,'bold'),
                    fg='black',
                    bg='powder blue',
                    bd=5,
                    width=8,
                    activebackground='purple',
                    activeforeground='white',
                    command=createacn_db)                
    submit_btn.place(relx=.35,rely=.5)     

    reset_btn=Button(frm,text='Reset',                
                    font=('arial',20,'bold'),
                    fg='black',
                    bg='powder blue',
                    bd=5,
                    width=8,
                    activebackground='purple',
                    activeforeground='white',command=reset_click)                
    reset_btn.place(relx=.5,rely=.5) 




def main_screen():                                           #to define function

    def newuser_click():                                      #to create nested function for deleting newuser_screen's frame
        frm.destroy()                                         
        newuser_screen()


    def existuser_click():
        frm.destroy()
        existuser_screen()

    frm=Frame(root,highlightbackground='black',highlightthickness=2)           #to create frame
    frm.configure(bg='pink')                                                    #set color of frame
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.75)                         #set frame's size                      

    lbl=Label(frm,text='🤗Welcome to Banking Simulation of Canara Bank🤗',          #to create lbl
              font=('arial',25,'bold','underline'),bg='pink')                 #to set font size & background of lbl
    lbl.place(relx=.25,rely=.1)                                                #to place lbl in frame

    newuser_btn=Button(frm,text='New User\nCreate Account',           #to create button for new user
                       font=('arial',20,'bold'),                      #to set font size
                       fg='black',                                    
                       bg='powder blue',
                       bd=5,
                       width=15,
                       activebackground='purple',                   #it changes the button background color while clicking         
                       activeforeground='white',                    #it changes the button text color while clicking
                       command=newuser_click)            
    newuser_btn.place(relx=.3,rely=.3)                                #to place button in frame

    existuser_btn=Button(frm,text='Existing User\nSign In',           #to create button for exist user
                       font=('arial',20,'bold'),                      #to set font size
                       fg='black',                                   #it changes text color
                       bg='powder blue',                             #it changes background color
                       bd=5,                                         #it make border of the button
                       width=15,                                     #it sets button size
                       activebackground='purple',                    #it changes the button background color while clicking
                       activeforeground='white',
                       command=existuser_click)                     #it changes the button text color while clicking
    existuser_btn.place(relx=.5,rely=.3)                             #to place button in frame



root=Tk()                                 #to create top level window 
root.state('zoomed')                      #to make full screen window
root.resizable(width=False,height=False)  #to desable window's resizable property
root.configure(bg='powder blue')          #to set background color

title=Label(root,text='Banking Simulation',
            font=('arial',45,'bold','underline'),
            bg='powder blue')                      #to make and formate title
title.pack()                                       #to set title on the top

curdate=time.strftime('%d-%b-%Y⏰%r')              #to provide current date and time
date=Label(root,text=curdate,
           font=('arial',20,'bold'),
           bg='powder blue',fg='blue')            #to create date formate
date.pack(pady=10)                                #to create gap b/w title and date vertically
update_time()

img=Image.open('logo.png').resize((200,130))  
imgtk=ImageTk.PhotoImage(img,master=root)

lbl_img=Label(root,image=imgtk)
lbl_img.place(relx=0,rely=0) 

img2=Image.open('logo2.jpg').resize((200,130))  
imgtk2=ImageTk.PhotoImage(img2,master=root)

lbl_img2=Label(root,image=imgtk2)
lbl_img2.place(relx=.88,rely=0)

footer=Label(root,text='Development By:Priya Porwal\n📱9999999999',
            font=('arial',20,'bold'),
            bg='powder blue')                      #to make and formate footer
footer.pack(side='bottom')                         #to set footer on the bottom 


main_screen()                                      #to call function

root.mainloop()                                    #to make window visible


