from bot import *
from tkinter import *
import threading
import time



arrr = 0


def thr():
    global arrr
    if start_btn["state"] == NORMAL:
        start_btn["state"] = DISABLED
    else:
        start_btn["state"] = NORMAL

    if dis_entry["state"] == NORMAL:
        dis_entry["state"] = DISABLED
    else:
        dis_entry["state"] = NORMAL

    if stop_btn["state"] == NORMAL:
        stop_btn["state"] = DISABLED
    else:
        stop_btn["state"] = NORMAL

    thread = threading.Thread(target=start)
    thread.start()
    arrr+=1


def start():
    global arrr
    global conn

    if arrr <= 0:
        conn = BotTriburile(user_vari.get(), pass_vari.get(), word_vari.get())
        conn.login()

    time.sleep(1)

    if atacw_var.get() == "on":

        conn.atac()

    if atacb_var.get() == "on":

        conn.barbari(dis_var.get())
    if recruit_var.get() == "on":

        conn.baraca()
    if buildings_var.get() == "on":

        pass


    arrr += 1
    time.sleep(1800)
    start()


def newwindow():
    # new window
    # global root
    global arrr, top_frame, check_frame

    root.geometry('450x600')
    frame_login.destroy()
    frame_text.destroy()
    if arrr > 0:
        top_frame.destroy()
        check_frame.destroy()
    ##Top Frame
    top_frame = Frame(root, bg="#0a22a9")
    top_frame.pack(fill=BOTH)
    setting = Label(top_frame, text="Setting", bg="#0a22a9", fg='white', pady=30, font="Verdana 20 bold")
    setting.pack()

    # Checkbutton Frame
    check_frame = Frame(root)
    check_frame.pack(fill=BOTH)
    atac_whitelist = Label(check_frame, text='Attack whitelist', font="Helvetica 16 bold italic")
    atac_barbarian = Label(check_frame, text='Attack barbarian', font="Helvetica 16 bold italic")
    recruit = Label(check_frame, text='Recruit', font="Helvetica 16 bold italic")
    buildings = Label(check_frame, text='Buildings', font="Helvetica 16 bold italic")
    select = Label(check_frame, text='Select', font='Times  12 bold')




    select.grid(row=0, column=1, columnspan=1, stick=W + E + N + S, padx=80, pady=10)
    atac_whitelist.grid(row=1, column=0, sticky=W, padx=20, pady=10)
    atac_barbarian.grid(row=2, column=0, sticky=W, padx=20, pady=10)
    recruit.grid(row=3, column=0, sticky=W, padx=20, pady=10)
    buildings.grid(row=4, column=0, sticky=W, padx=20, pady=10)
    # check buttons
    global atacw_var, atacb_var, recruit_var, buildings_var, start_btn
    atacw_var = StringVar()
    atacb_var = StringVar()
    recruit_var = StringVar()
    buildings_var = StringVar()

    atacw_check = Checkbutton(check_frame, text="Check", variable=atacw_var, onvalue="on", offvalue="off")
    atacb_check = Checkbutton(check_frame, text="Check", variable=atacb_var, onvalue="on", offvalue="off")
    recruit_check = Checkbutton(check_frame, text="Check", variable=recruit_var, onvalue="on", offvalue="off")
    buildings_check = Checkbutton(check_frame, text="Check", variable=buildings_var, onvalue="on", offvalue="off")
    atacw_check.deselect()
    atacb_check.deselect()
    recruit_check.deselect()
    buildings_check.deselect()
    atacw_check.grid(row=1, column=1)
    atacb_check.grid(row=2, column=1)
    recruit_check.grid(row=3, column=1)
    buildings_check.grid(row=4, column=1)
    # Start
    start_btn = Button(check_frame, text='Start', padx=50, bd=5, command=thr, state="normal")
    start_btn.grid(row=6, column=1)
    # distant
    global dis_var, dis_entry , stop_btn
    dis_var = IntVar()
    dis_label = Label(check_frame, text='Distance to barbarian villages ',font="Helvetica 10 bold italic")
    dis_entry = Entry(check_frame, textvariable=dis_var, state='normal')
    dis_entry.delete(0,'end')
    dis_entry.insert(0,15)
    dis_label.grid(row=5,column=0, padx= 20, pady= 10)
    dis_entry.grid(row=5, column=1, padx= 20, pady= 10)
    # Stop
    stop_btn = Button(check_frame, text='Stop', padx=50, bd=5,  command=newwindow  ,state='disabled')
    stop_btn.grid(row=6, column=0)



def window1():
    global root

    root = Tk()
    root.geometry('300x320')
    root.title(' Bot')
    root.resizable(False, False)
    # Top Frame
    global frame_text
    frame_text = Frame(root, bg="#0a22a9")
    frame_text.pack(fill=X)

    login_text = Label(frame_text, text='Login', fg='white', bg='#0a22a9', pady='50')
    login_text.pack()

    # Center Frame
    global frame_login
    frame_login = Frame(root, bg='orange')
    frame_login.pack(fill=X)
    # label
    username_label = Label(frame_login, text='Username', fg='white', bg='orange', pady='15')
    password_label = Label(frame_login, text='password', fg='white', bg='orange', pady='15')
    word_label = Label(frame_login, text='word', fg='white', bg='orange', pady='15')
    username_label.grid(row=0, column=0, padx='15')
    password_label.grid(row=1, column=0, padx='15')
    word_label.grid(row=2, column=0, padx='15')
    # entry
    global user_vari
    global pass_vari
    global word_vari
    user_vari = StringVar()
    pass_vari = StringVar()
    word_vari = StringVar()

    username_entry = Entry(frame_login, textvariable=user_vari)
    password_entry = Entry(frame_login, textvariable=pass_vari, show="*")
    word_entry = Entry(frame_login, textvariable=word_vari)
    username_entry.grid(row=0, column=1, padx='15')
    password_entry.grid(row=1, column=1, padx='15')
    word_entry.grid(row=2, column=1, padx='15')
    username_entry.focus_set()
    word_entry.insert(0, 'Ex: w34')

    login_btn = Button(frame_login, text='Login', padx=50, command=newwindow)
    login_btn.grid(row=3, column=1, pady=15)

    root.mainloop()



