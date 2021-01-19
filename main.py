from tkinter import *
from tkinter import filedialog, messagebox
import os, time, glob

class main():
    def __init__(self):
        
        self.bg = '#1a1a1a'
        self.fg = '#ffff4d'
        self.tk = Tk()
        self.tk.geometry('800x800')
        self.tk.config(bg=self.bg)
        self.tk.attributes('-fullscreen', True)
        self.tk.bind('<Control_L><t>', lambda event :self.tk.attributes('-fullscreen', 0))
        Label(self.tk, text='Press control+t for \nturn off fullscreen mode.').place(x=self.tk.winfo_screenwidth()-200, y=10)
        self.main = Frame(self.tk, bg=self.bg)

        self.help_img = [PhotoImage(file='img/help_1.png')]

        self.help_win = Toplevel()
        
        self.help_win.attributes('-toolwindow', 1)
        self.help_win.wm_attributes('-topmost',1)
        self.help_win.resizable(width=0, height=0)
        self.help_win.title('HELPER')
        self.help_win.protocol('WM_DELETE_WINDOW', lambda:self.help_win.attributes('-alpha', 0))

        self.h_title = Label(self.help_win, text='', font=('微軟正黑體', 15))
        self.h_title.pack()
        self.h_content = Label(self.help_win, text='', font=('微軟正黑體', 13))
        self.h_content.pack(padx=20, pady=(20, 0))
        self.help_win.attributes('-alpha', 0)

        self.skill_fr = Frame(self.tk, bg='#404040')
        Label(self.skill_fr, text='Skill', font=('微軟正黑體', 18), bg='#404040', fg='white').grid(row=0, column=0, columnspan=2)
        Label(self.skill_fr, text='1. You can right-click on your qf file button, \nand then show the menu.', font=('微軟正黑體', 13), bg='#404040', fg='white').grid(row=1, column=0)
        Label(self.skill_fr, image=self.help_img[0]).grid(row=1, column=1)
        #Label(self.skill_fr, text=), Label(self.skill_fr, image=)
        #Label(self.skill_fr, text="2. You can type a number which is \nbigger than any existing number.").grid(row=2, column=0)
        Label(self.skill_fr, text="2. You can type a number which is \nbigger than any existing number.", bg='#404040', fg='white', font=('微軟正黑體', 13)).grid(row=2, column=0, pady=10)
        Button(self.skill_fr, text='open tutorial video ->', command=lambda:os.startfile(glob.glob('video/*.mp4')[0]), bg=self.bg, fg=self.fg, bd=0, font=('微軟正黑體', 13)).grid(row=2, column=1, pady=10)

        self.help = Menu(self.tk)
        self.tk.config(menu=self.help)
        self.test = Menu(self.help)
        self.help.add_cascade(label='Help', menu=self.test)

        self.test.add_command(label='How to start', command=lambda:self.show_help('How to start', '1.Click "new file" button.\n2.Enter "Name" for your file name.\n3.Aftre enter a question and answer, click "Add" button.\nIf you want to continue, do that again.\nEND: Click "Create"'))    
        self.test.add_command(label='How to update', command=lambda:self.show_help('How to update', '1.Choose a file that you want to update.\n2.Choose  a index that you want to update.\n3.Enter the index, a updated question and answer.\n4.Click "Update" button.\n5.Finally click "save" button.'))
        self.test.add_command(label='What is \".qf\"', command=lambda:self.show_help('What is ".qf"', '"qf", aka question file, can be read and saved by this program.'))
        self.test.add_command(label='\"NO enter, NO change\"?', command=lambda:self.show_help('NO enter, NO change', 'If you only want to change the question \nbut don\'t want to enter the same answer text, \nclick the button that this program won\'t change your answer text. \nIf you don\'t click and the answer input is empty, \nthis program will make your answer text empty.'))
        self.test.add_separator()
        self.test.add_command(label='Skill', command=self.show_skill)

        Label(self.main, text='問鼎中原', font=('', 20)).pack()
        Button(self.main, text='open file', 
            command=lambda: self.open_qf(filedialog.askopenfilename(initialdir=os.path.expanduser("~/Desktop"), title='hello', filetypes=(('qf', '*.qf'), ('all', '*.*')))), 
            bg='#8080ff', fg='black', width=13, height=3, bd=0, font=('微軟正黑體', 13)).pack(side=LEFT, pady=(40, 0), padx=5)
        Button(self.main, text='new file', command=self.new_file, bg='#8080ff', fg='black', width=13, height=3, bd=0, font=('微軟正黑體', 13)).pack(side=LEFT, pady=(40, 0), padx=5)
        Button(self.main, text='update', command=self.update, bg='#8080ff', fg='black', width=13, height=3, bd=0, font=('微軟正黑體', 13)).pack(side=LEFT, pady=(40, 0), padx=5)
        Button(self.tk, text='Back', command=self.back, width=15, height=3, bg=self.bg, fg=self.fg).pack()

        self.file_fr = Frame(self.tk, bg=self.bg)
        self.dir_path = os.path.dirname(os.path.realpath(__file__)) 
        self.qf_files = []
        self.qf_file_name = []
        self.var = IntVar()
        self.var.set(0)
        self.n = 0
        self.row = 0
        self.col = 0
        for root, dirs, files in os.walk(self.dir_path): 
            for file in files:  
                
                if file.endswith('.qf'):
                    self.qf_files.append(root+'\\'+file)
                    vars(self)[f'r{self.n}'] = Radiobutton(self.file_fr, text=file, command=self.open_qf, variable=self.var, value=self.n, 
                                                            indicatoron=0, bg='#66ff66', fg='black', bd=0, font=('微軟正黑體', 15), 
                                                            width=11, height=3, justify='left', wraplength=100)
                    eval(f'self.r{self.n}').grid(row=self.row, column=self.col, padx=6, pady=6)
                    eval(f'self.r{self.n}').bind("<Button-3>", lambda event, path=root+'\\'+file: self.show_small_menu(event, path))
                    self.n += 1
                    self.var.set(self.n)

                    self.qf_file_name.append(file)
                    self.col += 1
                    if self.col % 5 == 0:
                        self.row += 1
                        self.col = 0

        self.m = Menu(self.tk, tearoff = 0, font=('微軟正黑體', 13)) 
        self.m.add_command(label ="Update", command=lambda: self.update(True)) 
        self.m.add_separator()
        self.m.add_separator()
        self.m.add_command(label ="Delete", command=self.delete_qf) 

        self.main.pack(pady=50)
        self.file_fr.pack()
        self.tk.focus_force()
        self.tk.mainloop()
          
    def show_small_menu(self, event, path):

        self.path = path
            
        try: 
            self.m.tk_popup(event.x_root, event.y_root) 
        finally: 
            self.m.grab_release()

    def delete_qf(self):
        os.remove(self.path)
        self.refresh()

    def show_help(self, title, content):
        self.h_title.config(text=title)
        self.h_content.config(text=content)
        self.help_win.attributes('-alpha', 1)
    def show_skill(self):
        self.back()
        self.main.pack_forget()
        self.file_fr.pack_forget()

        self.skill_fr.pack(pady=(50, 0))


    def refresh(self):

        #print(len(self.qf_files))
        for i in range(0, len(self.qf_files)):
            eval(f'self.r{i}').destroy() # all delete

        self.row = 0
        self.col = 0
        self.qf_files = []
        self.qf_file_name = []
        self.n = 0

        for root, dirs, files in os.walk(self.dir_path): 
            for file in files:  
        
                if file.endswith('.qf'): 
                    self.qf_files.append(root+'\\'+file)
                    vars(self)[f'r{self.n}'] = Radiobutton(self.file_fr, text=file, command=self.open_qf, variable=self.var, value=self.n, 
                                                            indicatoron=0, bg='#66ff66', fg='black', bd=0, font=('微軟正黑體', 15), width=11, height=3, justify='left', wraplength=100)
                    eval(f'self.r{self.n}').grid(row=self.row, column=self.col, padx=6, pady=6)
                    eval(f'self.r{self.n}').bind("<Button-3>", lambda event, path=root+'\\'+file: self.show_small_menu(event, path))
                    self.n += 1
                    self.var.set(self.n)
                    self.qf_file_name.append(file)
                    self.col += 1
	
                    if self.col % 5 == 0:
                        self.row += 1
                        self.col = 0
                

    def new_file(self):
        
        self.data = []
        self.main.pack_forget()
        self.file_fr.pack_forget()
        self.new_file_fr = Frame(self.tk, bg=self.bg)
        Label(self.new_file_fr, text='Name: ', bg=self.bg, fg=self.fg, font=('微軟正黑體', 25)).grid(row=0, column=0, pady=(50, 10), sticky=W)
        self.new_name = Entry(self.new_file_fr, font=('微軟正黑體', 16), bg='#66ccff', bd=0)
        self.new_name.grid(row=0, column=1, pady=(50, 10), ipadx=5, ipady=5)

        Label(self.new_file_fr, text='Question: ', bg=self.bg, fg=self.fg, font=('微軟正黑體', 25)).grid(row=1, column=0, pady=(40, 0), sticky=W)
        self.que = Entry(self.new_file_fr, font=('微軟正黑體', 16), bd=0, bg='#66ccff')
        self.que.grid(row=1, column=1, pady=(40, 0), ipadx=5, ipady=5)

        Label(self.new_file_fr, text='Answer: ', bg=self.bg, fg=self.fg, font=('微軟正黑體', 25)).grid(row=2, column=0, pady=5, sticky=W)
        self.ans = Entry(self.new_file_fr, font=('微軟正黑體', 16), bd=0, bg='#66ccff')
        self.ans.grid(row=2, column=1, pady=5, ipadx=5, ipady=5)

        Button(self.new_file_fr, text='Add', command=self.add, bg=self.bg, fg=self.fg, font=('微軟正黑體', 18)).grid(row=3, column=0, pady=(40, 0), sticky=S)
        Button(self.new_file_fr, text='Create', command=self.create, bg=self.bg, fg=self.fg, font=('微軟正黑體', 18)).grid(row=3, column=1, pady=(20, 0), sticky=S)
        
        self.new_file_fr.pack(pady=(50, 0))

    def add(self):
        self.line = []
        self.line.append(self.que.get())
        self.line.append(self.ans.get())
        self.data.append(self.line)

        self.que.delete(0, END)
        self.ans.delete(0, END)


    def create(self):
        """
        self.file = open("test.qf", "w", )
        self.file.write("hello world")
        self.file.close()"""
        self.new_file_fr.pack_forget()
        self.new_file_name = self.new_name.get()

        with open(f"{self.new_file_name}.qf", "w", encoding='utf-8') as f:
            f.write(str(self.data))
        try:
            os.rename(f"{self.new_file_name}.qf", f"que_file/{self.new_file_name}.qf")
        except FileExistsError:
            messagebox.showinfo('ERROR', f'\"{self.new_file_name}.qf\" is existing.')
            os.remove(f'{self.new_file_name}.qf')
            self.refresh()

        self.back()
        
        """os.chdir("c://")
        for file in glob.glob("*.qf"):
            print(file)"""

    def open_qf(self, is_other=None):
        self.main.pack_forget()
        self.file_fr.pack_forget()
        self.testing = Frame(self.tk, bg=self.bg)
        self.v_get = self.var.get()
        try:
            self.open_path = self.qf_files[self.v_get].replace('\\', '/') if not is_other else is_other

            Label(self.testing, text=self.open_path.split('/')[-1][:-3], font=('微軟正黑體', 40), bg=self.bg, 
                fg=self.fg, justify='left', wraplength=400).pack(side=LEFT, padx=(100, 100))
            if not is_other:
                eval(f"self.r{self.v_get}").deselect()

            self.testing.pack(side=LEFT)

            self.canvas=Canvas(self.testing, bd=0, height=500, width=700, bg=self.bg, highlightthickness=0)
            self.test_frame=Frame(self.canvas, bd=0, bg=self.bg, width=200)
            self.myscrollbar=Scrollbar(self.testing,command=self.canvas.yview, width=30)
            self.myscrollbar.set(0, 0)
            self.canvas.configure(yscrollcommand=self.myscrollbar.set)
            self.myscrollbar.pack(side="right", fill="y", padx=0)
            self.canvas.pack(expand=1, fill='both')#grid(row=1, column=0, columnspan=2)
            self.canvas.create_window((0,0),window=self.test_frame, width=500)
            self.test_frame.bind("<Configure>",self.myfunction)
            

            with open(self.open_path, 'r', encoding='utf-8') as f:
                self.n = 0
                self.var.set(0)
                self.r = 1
                for que, ans in eval(f.read()):

                    vars(self)[f'q{self.n}'] = Radiobutton(

                        self.test_frame, text=que, command=self.show_ans, variable=self.var, value=self.n, 
                        indicatoron=0, bg=self.bg, fg='white', 
                        font=('微軟正黑體', 17), bd=0
                        
                        )

                    vars(self)[f"a{self.n}"] = Label(self.test_frame, text=ans, fg=self.bg, 
                        font=('微軟正黑體', 17), bg=self.bg, justify='left', wraplength=300)
                    Label(self.test_frame, text=str(self.n+1), bg=self.bg, fg='#ff99ff', font=('微軟正黑體', 17)).grid(row=self.r,column=0, padx=(50, 10), pady=(100, 0))

                    eval(f'self.q{self.n}').grid(row=self.r, column=1, pady=10, padx=(70, 70), sticky=W, ipadx=5, ipady=5)
                    eval(f'self.a{self.n}').grid(row=self.r+1, column=1, pady=(10, 50), padx=(100, 0), sticky=W)
                    
                    self.n += 1
                    self.r += 2

            try:
                eval('self.q0').deselect()
            except:
                pass
        except:
            messagebox.showerror('ERROR', 'Please choose a file!\nClick \"back\" button can back.')


    def update(self, is_other=None):
        try:
            self.filename = filedialog.askopenfilename(initialdir=os.path.expanduser('que_file'), title='hello', filetypes=(('qf', '*.qf'), ('all', '*.*'))) if not is_other else self.path
            
            self.main.pack_forget()
            self.file_fr.pack_forget()
            self.update_fr = Frame(self.tk, bg=self.bg)
            self.reset = LabelFrame(self.update_fr, bg=self.bg, text='update', fg=self.fg, font=('微軟正黑體', 17))

            self.title = Label(self.update_fr, text=self.filename.replace('\\', '/').split('/')[-1][:-3], bg=self.bg, fg=self.fg, font=('微軟正黑體', 40))
            self.title.pack()
            # =========== main code =============
            
            with open(self.filename, 'r', encoding='utf-8') as f:

                self.canvas=Canvas(self.update_fr, bd=0, height=500, width=700, bg=self.bg, highlightthickness=0)
                self.test_frame=Frame(self.canvas, bd=0, bg=self.bg, width=200)
                self.myscrollbar=Scrollbar(self.update_fr,command=self.canvas.yview, width=30)
                self.myscrollbar.set(0, 0)
                self.canvas.configure(yscrollcommand=self.myscrollbar.set)

                self.canvas.pack(expand=1, fill='both', side=LEFT)
                self.myscrollbar.pack(side=LEFT, fill="y")
                #grid(row=1, column=0, columnspan=2)
                self.canvas.create_window((0,0),window=self.test_frame, width=500)
                self.test_frame.bind("<Configure>",self.myfunction)
                        
                        
                        
                self.n = 0                
                self.var.set(0)                
                self.r = 0
                for que, ans in eval(f.read()):

                    vars(self)[f'q{self.n}'] = Radiobutton(

                            self.test_frame, text=que, command=self.show_ans, variable=self.var, value=self.n, 
                            indicatoron=0, bg=self.bg, fg='white', 
                            font=('微軟正黑體', 17), bd=0
                                        
                            )
                    vars(self)[f"a{self.n}"] = Label(self.test_frame, text=ans, fg=self.bg, font=('微軟正黑體', 17), bg=self.bg, justify='left', wraplength=400)
                    vars(self)[f"i{self.n}"] = Label(self.test_frame, text=str(self.n+1), bg=self.bg, fg='#ff99ff', font=('微軟正黑體', 17))
                    eval(f'self.q{self.n}').grid(row=self.r, column=1, pady=10, padx=(0, 100), sticky=W, ipadx=5, ipady=5)
                    eval(f'self.a{self.n}').grid(row=self.r+1, column=1, pady=(10, 50), padx=(80, 0), sticky=W)
                    eval(f"self.i{self.n}").grid(row=self.r,column=0, padx=(50, 80), pady=(100, 0))
                    eval(f'self.a{self.n}').config(fg='#6699ff', bg='black')
                                    
                    self.n += 1
                    self.r += 2

                try:
                    eval('self.q0').deselect()
                except:
                    pass
                    # ===== reset UI======
                self.nonechange = BooleanVar()
                self.nonechange.set(True)
                    
                Label(self.reset, text='Index: ', bg=self.bg, font=('微軟正黑體', 19), fg='white').grid(row=0, column=0)
                self.change_index = Entry(self.reset, width=7)
                Label(self.reset, text='Que: ', bg=self.bg, font=('微軟正黑體', 19), fg='white').grid(row=1, column=0)
                self.change_que = Entry(self.reset)
                Label(self.reset, text='Ans: ', bg=self.bg, font=('微軟正黑體', 19), fg='white').grid(row=2, column=0)
                self.change_ans = Entry(self.reset)
                Checkbutton(self.reset, text='NO enter, NO change.', variable=self.nonechange, 
                    bg=self.bg, fg='#cc66ff', font=('微軟正黑體', 17), selectcolor='black').grid(row=3, column=0, columnspan=2)
                Label(self.reset, text='File name', bg=self.bg, fg='white', font=('微軟正黑體', 19)).grid(row=4, column=0)
                self.change_name = Entry(self.reset)
                self.change_name.insert(0, self.filename.replace('\\', '/').split('/')[-1][:-3])

                Button(self.reset, text='Update', font=('微軟正黑體', 19), command=self.change).grid(row=5, column=0, columnspan=2) 
                Button(self.reset, text='DELETE', command=self.del_index, bd=0, bg='red', fg='white').grid(row=0, column=2)

                self.change_index.grid(row=0, column=1, sticky=W)
                self.change_que.grid(row=1, column=1, sticky=W)
                self.change_ans.grid(row=2, column=1, sticky=W)
                self.change_name.grid(row=4, column=1, sticky=W)

                    # ===============

                # =========== main code =============

                self.reset.pack(side=TOP, ipadx=15, ipady=15, padx=(70, 0))
                Button(self.update_fr, text='Save', font=('Arial', 30), width=10, height=20, 
                    bd=0, bg='#476b6b', fg='white', command=self.save_update).pack(side=TOP, pady=(80, 40))
                self.update_fr.pack()
        except FileNotFoundError:
            messagebox.showerror('ERROR', 'Please choose a file!\nClick \"back\" button can back.')
        

    def change(self):
        self.c_index = int(self.change_index.get())
        self.c_que = self.change_que.get()
        self.c_ans = self.change_ans.get()
        try:
            
            if self.nonechange.get() == False: # 空白變空白
                eval(f'self.q{self.c_index-1}').config(text=self.c_que)
                eval(f'self.a{self.c_index-1}').config(text=self.c_ans)

            else: # 空白沒事
                eval(f'self.q{self.c_index-1}').config(text=self.c_que if self.c_que != '' else eval(f'self.q{self.c_index-1}')['text'])
                eval(f'self.a{self.c_index-1}').config(text=self.c_ans if self.c_ans != '' else eval(f'self.a{self.c_index-1}')['text'])

        except ValueError:
            messagebox.showerror('ERROR', 'Please enter a NUMBER.')
        except:
            #messagebox.showerror('ERROR', 'Please enter an index which exists.')
            vars(self)[f'q{self.n}'] = Radiobutton(

                    self.test_frame, text=self.c_que, command=self.show_ans, variable=self.var, value=self.n, 
                    indicatoron=0, bg=self.bg, fg='white', 
                    font=('微軟正黑體', 17), bd=0
                                        
                    )
            vars(self)[f"a{self.n}"] = Label(self.test_frame, text=self.c_ans, fg=self.bg, font=('微軟正黑體', 17), bg=self.bg, justify='left', wraplength=400)
            vars(self)[f"i{self.n}"] = Label(self.test_frame, text=str(self.n+1), bg=self.bg, fg='#ff99ff', font=('微軟正黑體', 17))
            eval(f'self.q{self.n}').grid(row=self.r, column=1, pady=10, padx=(0, 100), sticky=W, ipadx=5, ipady=5)
            eval(f'self.a{self.n}').grid(row=self.r+1, column=1, pady=(10, 50), padx=(80, 0), sticky=W)
            eval(f"self.i{self.n}").grid(row=self.r, column=0, padx=(50, 80), pady=(100, 0))
            eval(f'self.a{self.n}').config(fg='#6699ff', bg='black')
            self.n += 1
            self.r += 1

        self.title.config(text=self.change_name.get())

    def save_update(self):
        self.k = []
        for i in range(0, self.n):
            try:
                self.k.append([eval(f'self.q{i}')['text'], eval(f'self.a{i}')['text']])
            except:
                pass
        #print(str([q, a for n in range(0, self.n) for q in ]), end=", ")

        self.new_path = self.change_name.get().join(self.filename.rsplit(self.filename.split('\\')[-1][:-3], 1))
        os.rename(self.filename, self.new_path)

        with open(self.new_path, 'w', encoding='utf-8') as f:
            f.write(str(self.k))
        self.update_fr.pack_forget()
        self.refresh()
        self.main.pack(pady=50)
        self.file_fr.pack()


    def myfunction(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))       

    def back(self):
        try:
            self.new_file_fr.pack_forget()
        except:
            pass
        try:
            self.testing.pack_forget()
        except:
            pass
        try:
            self.update_fr.pack_forget()
        except:
            pass
        try:
            self.skill_fr.pack_forget()
        except:
            pass
        self.refresh()

        self.main.pack(pady=50)
        self.file_fr.pack()

    def show_ans(self):
        self.v_get = self.var.get()
        eval(f'self.q{self.v_get}').deselect()
        eval(f'self.a{self.v_get}').config(fg='#6699ff', bg='black')

    def del_index(self):
        self.c_index = self.change_index.get()
        try:
            eval(f'self.q{int(self.c_index)-1}').destroy()
            eval(f'self.i{int(self.c_index)-1}').destroy()
            eval(f'self.a{int(self.c_index)-1}').destroy()
        except:
            messagebox.showerror('', 'Please type a number')

        for index in range(int(self.c_index), self.n):
            eval(f'self.i{index}').config(text=str(int(eval(f'self.i{index}')["text"])-1))
            eval(f'self.q{index}').config(text=eval(f'self.q{index}')["text"])
            eval(f'self.a{index}').config(text=eval(f'self.a{index}')["text"])

        self.k = []
        for i in range(0, self.n):
            try:
                self.k.append([eval(f'self.q{i}')['text'], eval(f'self.a{i}')['text']])
            except:
                pass


main()
