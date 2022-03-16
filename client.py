import threading
import socket
import argparse
import os
import sys
import tkinter as tk
import tkinter.filedialog
import json
import sympy as sy


class Send(threading.Thread):
    # Listens for user input from command line

    # sock the connected sock object
    # name (str) : The username provided by the user

    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):
        # Listen for the user input from the command line and send it to the server
        # Type "QUIT" to exit the app

        while True:
            print("""{}: """.format(self.name), end='')
            sys.stdout.flush()
            message = sys.stdin.readline()[:-1]

            # type "QUIT" to leave the app

            if message == "QUIT":
                self.sock.sendall("[message];Server: {} has left.;[end]""".format(self.name).encode('utf-8'))
                break

            # send message to server for broadcasting
            else:
                self.sock.sendall("[message];{} : {};[end]".format(self.name, message).encode('utf-8'))

        print('\nQuitting...')
        self.sock.close()
        os._exit(0)


class Receive(threading.Thread):
    # Listens for incoming messages from the server
    
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name
        self.messages = None
        self.questions = None
        self.answers = None

    def run(self):

        # Receives data from the server and displays it in the gui

        while (True):
            message = self.receive()

            if message:
                signals = message.split(';')[0]

                if signals == "[response]":
                    if message.split(';')[1] == "fail":
                        print('\nAuthentication Failed!\n')
                        print('\nQuitting...')
                        self.sock.close()
                        os._exit(0)

                    elif message.split(';')[1] == "ok":
                        print('\nAuthentication Success!\n')
                        
                elif signals == "[data]":
                    # if we receive a response from server
                    if self.questions and self.answers:
                        # load data
                        data = json.loads(message.split(';')[1])

                        # clear list
                        self.questions.delete(0, tk.END)
                        self.answers.delete(0, tk.END)

                        for i, j in enumerate(data):
                            self.questions.insert(i, j['question'])
                            self.answers.insert(i, j['answer'])

                        # add space at the end
                        self.questions.insert(tk.END, "")
                        self.answers.insert(tk.END, "")

                elif signals == "[new data]":
                    index = int(message.split(';')[3])
                    if self.questions and self.answers:
                        self.questions.delete(index)
                        self.answers.delete(index)

                        self.questions.insert(index, message.split(';')[1])
                        self.answers.insert(index, message.split(';')[2])
                        
                        if len(self.questions.get(tk.END)) > 0:
                            self.questions.insert(tk.END, "")
                            self.answers.insert(tk.END, "")
                        
                elif signals == "[message]":
                    if self.messages:
                        self.messages.insert(tk.END, message.split(';')[1])

                    self.messages.see(tk.END)
                    print('\r{}\n{}: '.format(message.split(';')[1], self.name), end='')

            else:
                print('\n Lost connection to the server!')
                print('\nQuitting...')
                self.sock.close()
                os._exit(0)
        
    def receive(self):
        message = ""
        while (True):
            try: message += self.sock.recv(1024).decode('utf-8')
            except: return None

            if message.__contains__("[end]"):
                return message


class Client:
    # management of client-server connection and integration of GUI
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(
            socket.AF_INET, 
            socket.SOCK_STREAM
        )
        self.name = None
        self.messages = None
        self.questions = None
        self.answers = None

    def start(self):
        print('Trying to connect to {}:{}....'.format(self.host, self.port))

        self.sock.connect((self.host, self.port))

        print('Succesfully connected to {}:{}'.format(self.host, self.port))
        print('')

        name = input('Your Name: ')
        self.name = name

        # Create send and receive threads
        send = Send(self.sock, self.name)
        receive = Receive(self.sock, self.name)
        
        # start send and receive thread
        send.start()
        receive.start()

        self.sock.sendall("[auth];{};[end]".format(name).encode('utf-8'))
        
        print('Welcome, {}! Getting ready to send and receive messages...'.format(self.name))
        
        print("""\rReady! Type 'QUIT' to cabskuy""")
        print('{}: '.format(self.name), end= '')
        
        return receive

    def send(self, message):
        # Sends textInput data from the GUI
        if self.messages:

            # Type 'QUIT' to leave the chat
            if message == "QUIT":
                self.quit()

            # SEND message to the server for broadcasting
            else:
                self.messages.see(tk.END)
                try:
                    self.sock.sendall('[message];{}: {};[end]'.format(self.name, message).encode('utf-8'))
                except Exception as e:
                    print(str(e))
                    return
            
            self.messages.insert(tk.END, '{}: {}'.format(self.name, message))

    def sendData(self, id, question, answer):
        if not self.questions or not self.answers:
            return
        
        if len(question) <= 0:
            question = " "
            
        if len(answer) <= 0:
            answer = " "

        try:
            self.sock.sendall("[new data];{};{};{};[end]".format(question, answer, id[0]).encode('utf-8'))
        except Exception as e:
            print(str(e))
            return

        self.questions.delete(id)
        self.questions.insert(id, question)
        
        self.answers.delete(id)
        self.answers.insert(id, answer)

        if len(self.questions.get(tk.END)) > 0:
            self.answers.insert(tk.END, '')
            self.questions.insert(tk.END, '')

        self.questions.see(id[0] + 1)
        self.answers.see(id[0] + 1)

    def sendFile(self, id, file):
        if not self.questions or not self.answers:
            return

        message = "[file];"
        for i, content in enumerate(file):
            message += content + ";"
            self.questions.insert((id[0] + i,), content)
            self.answers.insert((id[0] + i,), " ")

        message += "[end]"

        try:
            self.sock.sendall(message.encode('utf-8'))
        except Exception as e:
            print(str(e))
            return

    def request(self):
        self.sock.sendall("[request data];[end]".encode('utf-8'))

    def quit(self):
        self.sock.sendall('[message];Server: {} has left the chat;[end]'.format(self.name).encode('utf-8'))
        print('\nQuitting...')
        self.sock.close()
        os._exit(0)


def main(host, port):
    # initialize and run GUI app

    client = Client(host, port)
    receive = client.start()

    window = tk.Tk()
    window.title("Megalitikum Robotikum (versi lite)")

    fromMessage = tk.Frame(master=window)
    scrollBar = tk.Scrollbar(master=fromMessage)
    messages = tk.Listbox(master=fromMessage, yscrollcommand=scrollBar.set)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
    messages.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def scroll(*args):
        messages.yview(*args)
    
    scrollBar.config(command=scroll)

    client.messages = messages
    receive.messages = messages

    fromMessage.grid(row=0, column=0, columnspan=3, sticky="nsew")
    fromEntry = tk.Frame(master=window)
    textInput = tk.Entry(master=fromEntry)

    def send():
        message = textInput.get()

        if message.__contains__("[math]"):
            try:
                equation = message.split('[math] ')[1]
                message += " = " + str(sy.sympify(equation))
            except:
                messages.insert(tk.END, "System: [ERROR] wrong input for math")
                return

        textInput.delete(0, tk.END)
        client.send(message)

    textInput.pack(fill=tk.BOTH, expand=True)
    textInput.bind("<Return>", lambda x: send())
    textInput.insert(0, "Insert your message here!")

    btnSend = tk.Button(
        master=window,
        text="Send",
        command=lambda: send()
    )
    btnGdocs = tk.Button(
        master=window,
        text="GDocs",
        command=lambda: openGDocs(window, btnGdocs, client, receive)
    )

    fromEntry.grid(row=1, column=0, padx=10, sticky="ew")
    btnSend.grid(row=1, column=1, pady=10, sticky="ew")
    btnGdocs.grid(row=1, column=2, pady=10, sticky="ew")

    window.rowconfigure(0, minsize=500, weight=1)
    window.rowconfigure(1, minsize=50, weight=0)
    window.columnconfigure(0, minsize=500, weight=1)
    window.columnconfigure(1, minsize=100, weight=0)
    window.columnconfigure(2, minsize=100, weight=0)

    window.mainloop()

    client.quit()


def openGDocs(parent, button, client, receive):
    window = tk.Toplevel(parent)
    window.title("The Jidoks (versi lite)")

    fromMessage = tk.Frame(master=window)
    scrollBar = tk.Scrollbar(master=fromMessage)
    questions = tk.Listbox(master=fromMessage, yscrollcommand=scrollBar.set)
    answers = tk.Listbox(master=fromMessage, yscrollcommand=scrollBar.set)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
    questions.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    answers.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
    
    client.answers = answers
    client.questions = questions

    receive.answers = answers
    receive.questions = questions

    def scroll(*args):
        questions.yview(*args)
        answers.yview(*args)

    def mousewheel(event, lb):
        lb.yview_scroll(int(-4*(event.delta/120)), "units")

    scrollBar.config(command=scroll)

    questions.bind("<MouseWheel>", lambda e: mousewheel(e, answers))
    answers.bind("<MouseWheel>", lambda e: mousewheel(e, questions))

    client.request()

    answers.bind('<<ListboxSelect>>', lambda x: questions.selection_clear(0))
    questions.bind('<<ListboxSelect>>', lambda x: answers.selection_clear(0))

    fromMessage.grid(row=0, column=0, columnspan=4, sticky="nsew")
    fromEntry = tk.Frame(master=window)
    textInput = tk.Entry(master=fromEntry)
    textInput.insert(0, "Insert your question/answer here!")

    def sendQnA():
        if len(questions.curselection()) > 0:
            index = questions.curselection()
            client.sendData(
                index, 
                textInput.get(),
                answers.get(index)
            )
            answers.selection_clear(0)
            questions.selection_set(index[0] + 1)

        elif len(answers.curselection()) > 0:
            index = answers.curselection()
            client.sendData(
                index, 
                questions.get(index),
                textInput.get()
            )
            questions.selection_clear(0)
            answers.selection_set(index[0] + 1)

        else:
            return

        textInput.delete(0, tk.END)

    textInput.pack(fill=tk.BOTH, expand=True)
    textInput.bind(
        "<Return>", 
        lambda x: sendQnA()
    )
    
    btnSend = tk.Button(
        master=window,
        text="Send",
        command=sendQnA
    )

    btnRefresh = tk.Button(
        master=window,
        text="Refresh",
        command=lambda: client.request()
    )

    def sendFile():
        path = tk.filedialog.askopenfilename(
            initialdir = "/",
            title = "Select a File",
            filetypes = (
                ("text files", "*.txt"),
                ('All files', '*.*')
            )
        )

        with open(path) as f:
            contents = f.readlines()
            
        client.sendFile((questions.size() - 1,), contents)

    btnUpload = tk.Button(
        master=window,
        text="Upload",
        command=lambda: sendFile()
    )

    fromEntry.grid(row=1, column=0, padx=10, sticky="ew")
    btnSend.grid(row=1, column=1, pady=10, sticky="ew")
    btnRefresh.grid(row=1, column=2, pady=10, sticky="ew")
    btnUpload.grid(row=1, column=3, pady=10, sticky="ew")
    
    window.rowconfigure(0, minsize=500, weight=1)
    window.rowconfigure(1, minsize=50, weight=0)
    window.columnconfigure(0, minsize=500, weight=1)
    window.columnconfigure(1, minsize=100, weight=0)
    window.columnconfigure(2, minsize=100, weight=0)
    window.columnconfigure(3, minsize=100, weight=0)

    def changeButtonState():
        if button['state'] == "normal":
            button['state'] = "disable"
        else:
            button['state'] = "normal"
            
            client.answers = None
            client.questions = None

            receive.answers = None
            receive.questions = None

            if window:
                window.destroy()

    changeButtonState()

    window.protocol('WM_DELETE_WINDOW', lambda: changeButtonState())


if __name__ == "__main__":
    host = input('Host: ')
    port = int(input('Port (default 1060): ') or "1060")

    main(host, port)