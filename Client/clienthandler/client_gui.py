from tkinter import *
from clienthandler.client_handler import ClientHandler

class GUI:
	update_speed = 250 #Milliseconds

	def __init__(self):
		#function to bring frame to foreground
		def raise_frame(frame):
			frame.tkraise()

		client_handler = ClientHandler()

		#create initial window
		root = Tk()
		root.geometry("800x500")
		root.configure(background='#c53fff')

		#create and set frames
		user_setup = Frame(root, height = 500, width = 800, background='#c53fff')
		main_view = Frame(root, height = 500, width = 800, background= '#c53fff')
		scrolling_text = Frame(root, height = 420, width = 700)

		main_view.visible = False

		user_setup.grid(row=0, column=0, sticky='news')
		main_view.grid(row=0, column=0, sticky='news')
		scrolling_text.place(x = 10, y = 10)

		root.title("ChatClient")

		#user_setup widgets initialized

		#limit character to length N function
		def limit_entry_size(limited_text, N):
			if len(limited_text.get()) > N:
				limited_text.set(limited_text.get()[:N])

		chatroom = StringVar()
		chatroom_entry = Entry(user_setup,highlightbackground='black', textvariable=chatroom)
		chatroom_entry.place(x=200, y=170)

		alias = StringVar()
		alias_entry = Entry(user_setup,highlightbackground='black', textvariable=alias)
		alias_entry.place(x=400, y=170)

		alias.trace('w', lambda *args: limit_entry_size(alias, 15))
		chatroom.trace('w', lambda *args: limit_entry_size(chatroom, 15))

		chatroom_label = Label(user_setup, bg='#c53fff', text = "Enter Chatroom")
		chatroom_label.place(x=200, y=140)
		chatroom_label.config(font=("Courier", 21, 'bold'))

		alias_label = Label(user_setup, bg='#c53fff', text = "Enter Alias")
		alias_label.place(x=400, y=140)
		alias_label.config(font=("Courier", 21, 'bold'))
	
		join_button = Button(user_setup, text="Join Chatroom",highlightbackground='#c53fff',command=lambda: login("join"))
		join_button.place(x=200, y=200)
	
		create_button = Button(user_setup, text="Create Chatroom",highlightbackground='#c53fff', command=lambda: login("create"))
		create_button.place(x=400, y=200)

		#error message to later be set
		error_message = StringVar()
		error = Message(user_setup, bg = 'red',font=('times', 24, 'bold'), textvariable=error_message)

		#main_view widgets initialization
		message = StringVar()
		message_entry = Entry(main_view,highlightbackground='black', width = 70, textvariable=message)
		message_entry.place(x=10, y=450)

		message.trace('w', lambda *args: limit_entry_size(message, 140))

		send_button = Button(main_view, text="Send Message", highlightbackground='black',borderwidth = 0,highlightthickness=0, relief = RAISED, command=lambda: send())
		send_button.place(x=680, y = 420)
		send_image = PhotoImage(file="clienthandler/mail.gif")
		send_button.config(image=send_image)

		leave_button = Button(main_view, text="Leave", highlightbackground='black', borderwidth = 0,highlightthickness=0, command=lambda: leave())
		leave_button.place(x=680, y = 10)

		leave_image = PhotoImage(file="clienthandler/door.gif")
		leave_button.config(image=leave_image)

		message_text = Text(scrolling_text, width =90, height =28)
		message_text.grid(row=0, column=0)

		scrollbar = Scrollbar(scrolling_text, command = message_text.yview)
		scrollbar.grid(row=0, column=1, sticky='nsew')
		message_text['yscrollcommand'] = scrollbar.set
		
		#setup labels for current alias and room name
		roomname_message = StringVar()
		roomname = Message(main_view, bg = '#c53fff', width = 180, textvariable=roomname_message)
		roomname.config(font=("Times", 12, 'bold'))
		
		alias_message = StringVar()
		aliasname = Message(main_view, bg = '#c53fff', width = 180, textvariable=alias_message)
		aliasname.config(font=("Times", 12, 'bold'))

		#push index to bottom of text and disable typing
		for i in range(1,28):
			message_text.insert(INSERT, "\n")

		message_text.insert(INSERT, "You are in a chatroom -_-")
		message_text['state'] = DISABLED


		#recieve func
		def recieve():
			if main_view.visible == True:
				new_message = client_handler.update()
				if new_message is not None:
					message_text['state'] = NORMAL
					message_text.insert(END,"\n%s" % new_message)
					message_text['state'] = DISABLED
					message_text.see(END)
			root.after(self.update_speed, recieve)

		#function to either join or create a room
		#also initializes errors and chatroom and alias display on main_view
		def login(method):

			if method == "join":
				error_code = client_handler.join_room(chatroom_entry.get(), alias_entry.get())
			elif method == "create":
				error_code = client_handler.create_room(chatroom_entry.get(), alias_entry.get())

			#remove prior error message
			error.place_forget()
			
			# returned error code
			if error_code != 0:
				if error_code == 1:
					error_message.set("Alias Taken")
					error.place(x=300, y = 280)
					return None
				elif error_code == 2:
					error_message.set("Chatroom Name Taken")
					error.place(x=300, y = 280)
					return None
				elif error_code == 3:
					error_message.set("Chatroom Does not Exist")
					error.place(x=300, y = 280)
					return None
				elif error_code == 4:
					error_message.set("No Connection To Internet")
					error.place(x=300, y = 280)
					return None

			#set current room name and alias
			roomname_message.set("Room Name:\n" + chatroom_entry.get() +"\n")
			alias_message.set("Alias:\n" + alias_entry.get() +"\n")

			#go to main_view and show text display frame
			raise_frame(main_view)
			main_view.visible = True
			raise_frame(scrolling_text)
			
			#place
			roomname.place(x=675, y = 150)
			aliasname.place(x =675, y = 190)

		def send():
			#input func to send message
			client_handler.send_message(message_entry.get())
			message_text.see(END)
			message_entry.delete(0, END)

		def send_enter(event):
			if main_view.visible == True:
				#input func to send message
				client_handler.send_message(message_entry.get())
				message_text.see(END)
				message_entry.delete(0, END)

		def leave():
			#func to leave
			#delete text of prior chatroom
			message_text['state'] = NORMAL
			message_text.delete('29.0', END)
			message_text['state'] = DISABLED

			#leave room and return to starting page
			client_handler.leave_room()
			raise_frame(user_setup)
			main_view.visible = False

		def on_closing():
			#input function to leave
			client_handler.quit()
			print("goodbye")
			root.destroy()

		#begin recieving loop, adjust main window settings, and start loop
		raise_frame(user_setup)
		root.protocol("WM_DELETE_WINDOW", on_closing)
		root.bind('<Return>', send_enter)
		root.after(self.update_speed, recieve)
		root.mainloop()
