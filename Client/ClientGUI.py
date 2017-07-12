import tkinter as tk
from tkinter import *

#function to bring frame to foreground
def raise_frame(frame):
    frame.tkraise()

#create initial window
root = Tk()
root.geometry("800x500")
root.configure(background='brown')

#create and set frames
user_setup = Frame(root, height = 500, width = 800, background='brown')
main_view = Frame(root, height = 500, width = 800, background= 'brown')
scrolling_text = Frame(root, height = 420, width = 700)

main_view.visible = False
#remove later
main_view.visible = True

user_setup.grid(row=0, column=0, sticky='news')
main_view.grid(row=0, column=0, sticky='news')
scrolling_text.place(x = 10, y = 10)

root.title("ChatClient")

#widgets for setup
chatroom = StringVar()
chatroom_entry = Entry(user_setup,highlightbackground='black', textvariable=chatroom)
chatroom_entry.place(x=200, y=170)
			
alias = StringVar()
alias_entry = Entry(user_setup,highlightbackground='black', textvariable=alias)
alias_entry.place(x=400, y=170)
		
chatroom_label = Label(user_setup, bg='brown', text = "Enter Chatroom")
chatroom_label.place(x=200, y=200)
		
alias_label = Label(user_setup, bg='brown', text = "Enter Alias")
alias_label.place(x=400, y=200)
		
join_button = Button(user_setup, text="Join Chatroom",highlightbackground='brown', command=lambda: login("join"))
join_button.place(x=200, y=220)
		
create_button = Button(user_setup, text="Create Chatroom",highlightbackground='brown', command=lambda: login("create"))
create_button.place(x=400, y=220)

#main_view
message = StringVar()
message_entry = Entry(main_view,highlightbackground='black', width = 70, textvariable=message)
message_entry.place(x=10, y=450)

send_button = Button(main_view, text="Send Message", highlightbackground='brown', command=lambda: send())
send_button.place(x=670, y = 450)

leave_button = Button(main_view, text="Leave", highlightbackground='brown', command=lambda: leave())
leave_button.place(x=720, y = 10)

message_text = Text(scrolling_text, width =90, height =28)
message_text.grid(row=0, column=0)

scrollbar = Scrollbar(scrolling_text, command = message_text.yview)
scrollbar.grid(row=0, column=1, sticky='nsew')
message_text['yscrollcommand'] = scrollbar.set

for i in range(1,28):
	message_text.insert(INSERT, "\n")
message_text.insert(INSERT, "You are in a chatroom -_-")
message_text['state'] = DISABLED


def login(method):
	#send data
	#receive error code
	#if good
	error_code = 1
	error_message = StringVar()
	error = Message(user_setup, bg = 'red',font=('times', 24, 'italic'), textvariable=error_message)
	if error_code == 1:
		error_message.set("Alias taken")
		error.place(x=300, y = 280)
		return None
	#elif error_code == 2:
		#error_code=1
		
	raise_frame(main_view)
	main_view.visible = True
	raise_frame(scrolling_text)
	
def send():
	#func to send message
	message_text['state'] = NORMAL
	message_text.insert(INSERT,"\n%s" % message_entry.get())
	message_text['state'] = DISABLED
	message_text.see(END)
	message_entry.delete(0, END)
	
def send_enter(event):
	if main_view.visible == True:
		#func to send message
		message_text['state'] = NORMAL
		message_text.insert(INSERT,"\n%s" % message_entry.get())
		message_text['state'] = DISABLED
		message_text.see(END)
		message_entry.delete(0, END)
	
def leave():
	#func to leave 
	raise_frame(user_setup)
	main_view.visible = False
	
def on_closing():
	print("goodbye")
	root.destroy()
	
		      

raise_frame(main_view)
raise_frame(scrolling_text)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.bind('<Return>', send_enter)
root.mainloop()

       	
       	