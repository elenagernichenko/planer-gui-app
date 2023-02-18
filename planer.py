from tkinter import *
from tkcalendar import *
from test import Scrollable
import datetime
import pickle

class Planer:
    def __init__(self):
        self.tasks = 'E:/python/project/tasks.pickle'
        self.tasks_bydate = 'E:/python/project/tasks_bydate.pickle'
        self.file_wdate = 'E:/python/project/file_wdate.pickle'
        self.file_done = 'E:/python/project/file_done.pickle'
        self.root = Tk()
        self.root.title('To Do')
        self.root.resizable(False, False)
        self.now = datetime.datetime.now()
        
        self.r = 999
        self.on = 999
        self.tasks_arr = []
        self.tasks_arr_bydate = []
        self.time = []
        self.tasks_done = []
        
        self.values = {}
        
        self.root.update_idletasks()
        self.s = self.root.geometry()
        self.s = self.s.split('+')
        self.s = self.s[0].split('x')
        self.width_root = int(self.s[0])
        self.height_root = int(self.s[1])
        
        self.w = self.root.winfo_screenwidth()
        self.h = self.root.winfo_screenheight()
        self.w = self.w // 2
        self.h = self.h // 2 
        self.w = self.w - self.width_root // 2
        self.h = self.h - self.height_root // 2
        self.root.geometry('+{}+{}'.format(self.w, self.h))
        
        self.lab1 = Label(text='Hello, dear...enter your name!')
        self.ent_name = Entry()

        self.but_calendar = Button(text='Calendar', width=40, height=5, command=self.calendar_view)
        self.but_day = Button(text='My day', width=40, height=5, command=self.myday_view)
        self.but_task = Button(text='Tasks', width=40, height=5, command=self.tasks_view)
        self.but_done = Button(text='Done', width=40, height=5, command=self.done_view)
        
        self.lab1.grid(sticky=N+S+W+E)
        self.ent_name.grid(row=1, column=0)
        self.but_calendar.grid(row=2, column=0, padx=20, pady=10)
        self.but_day.grid(row=3, column=0, padx=20, pady=5)
        self.but_task.grid(row=4, column=0, padx=20, pady=5)
        self.but_done.grid(row=5, column=0, padx=20, pady=10)

        self.ent_name.bind('<Return>', self.change_name)


    def change_name(self, event):
        name = self.ent_name.get()
        self.lab1['text'] = 'Hello, dear {}'.format(name)
        self.ent_name.grid_forget()
        
    def calendar_view(self):
        self.window1 = Toplevel()
        self.window1.geometry('610x300-0+0')
        
        self.cal = Calendar(self.window1, date_pattern='y-mm-dd',
                            showweeknumbers=False, background='#ce897b', foreground='#fbd2d7',
                            disabledbackground='#e4a199')

        self.ent_add = Entry(self.window1, width=80)
        self.but_add = Button(self.window1, text='Add task', width=20)
        
        self.cal.pack(pady=10, padx=10, fill='both', expand=True, side=TOP)
        self.ent_add.pack(pady=10, padx=10,side=LEFT)
        self.but_add.pack(pady=10, padx=10,side=LEFT)

        self.ent_add.bind('<Return>', self.add_fromcalendar)
        self.but_add.bind('<Button-1>', self.add_fromcalendar)

    def myday_view(self):
        self.window2 = Toplevel()
        self.frame2 = Frame(self.window2)

        self.window2.resizable(False, False)
        self.window2.geometry('610x320+0+0')

        self.lab = Label(self.window2, text='{}'.format(self.now.strftime('%Y-%m-%d')))
        self.ent_add1 = Entry(self.window2, width=70)
        self.but_add1 = Button(self.window2, text='New task', width=10)
        self.but_add1.bind("<Button-1>", self.add_task)
        self.lab.grid(row=0, column=0, padx=10)
        self.ent_add1.grid(column=1, row=0)
        self.but_add1.grid(column=2, row=0)
        
        self.frame2.grid(column=0, row=1, columnspan=3)
        self.scrollable_body = Scrollable(self.frame2)
        self.load_t()

        
    def tasks_view(self):
        self.window3 = Toplevel()
        self.frame3 = Frame(self.window3)
        self.window3.resizable(False, False)
        self.window3.geometry('610x300+0-0')


        self.lab2 = Label(self.window3, text='Tasks by date:')

        self.lab2.grid(row=0, column=0, padx=10)

        self.frame3.grid(column=0, row=1, columnspan=3)
        self.scrollable_body2 = Scrollable(self.frame3)
        self.load_t_bytime()
        

    def done_view(self):
        self.window4 = Toplevel()
        self.frame4 = Frame(self.window4)
        self.window4.resizable(False, False)
        self.window4.geometry('610x300-0-0')

        self.lab3 = Label(self.window4, text='Completed tasks:')

        self.lab3.grid(row=0, column=0, padx=10)
        self.frame4.grid(column=0, row=1, columnspan=3)

        self.scrollable_body3 = Scrollable(self.frame4)
        self.load_done()

    def add_task(self, event):
        task = self.ent_add1.get()
        self.tasks_arr.append(task)
        pickle.dump(self.tasks_arr, open(self.tasks, 'wb'))
        self.ent_add1.delete(0, END)
        self.var = IntVar()
        while self.r > 0:
            self.task_added = Checkbutton(self.scrollable_body, text=task, variable=self.var, offvalue=0, onvalue=self.on, relief=GROOVE, width=80,
                                          wraplength=540, height=3,
                                          anchor=W)
            self.task_added.grid(row=self.r, column=0, columnspan=3)
            self.task_added.bind('<Button-1>', self.move_indone)
            self.r -= 1

            task_and_time = [task, self.now.strftime('%Y-%m-%d')]
            self.values[self.on] = task_and_time

            self.on -= 1
            break
        self.scrollable_body.update()
        
    def add_fromcalendar(self, event):
        selected_date = self.cal.get_date()
        task_CAL = self.ent_add.get()
        self.ent_add.delete(0, END)
        
        self.tasks_arr_bydate.append(task_CAL)
        pickle.dump(self.tasks_arr_bydate, open(self.tasks_bydate, 'wb'))

        self.time.append(selected_date)
        pickle.dump(self.time, open(self.file_wdate, 'wb'))
        
        self.var = IntVar()
        while self.r > 0:
            if selected_date == self.now.strftime('%Y-%m-%d'):
                self.tasks_arr.append(task_CAL)
                pickle.dump(self.tasks_arr, open(self.tasks, 'wb')) 
                self.task_added = Checkbutton(self.scrollable_body, text=task_CAL, variable=self.var, offvalue=0, onvalue=self.on, relief=GROOVE,
                                              width=80, wraplength=540, height=3,
                                              anchor=W)
                self.task_added.bind('<Button-1>', self.move_indone)
                self.task_added.grid(row=self.r, column=0, columnspan=3)
                task_and_time = [task_CAL, selected_date]
                self.values[self.on] = task_and_time
                self.on -= 1

                self.task_added.widget = task_CAL
                self.scrollable_body.update()

                
                self.task_added = Checkbutton(self.scrollable_body2, text='{} \n {}'.format(task_CAL, selected_date), variable=self.var, offvalue=0,
                                              onvalue=self.on,
                                              relief=GROOVE, width=80, wraplength=540, height=3, anchor=W)
                self.task_added.grid(row=self.r, column=0, columnspan=3)
                self.task_added.bind('<Button-1>', self.move_indone)
                self.r -= 1
                
                task_and_time = [task_CAL, selected_date]
                self.values[self.on] = task_and_time
                
                self.on -= 1
                self.scrollable_body2.update()
                break
            
            else:
                self.task_added = Checkbutton(self.scrollable_body2, text='{} \n {}'.format(task_CAL, selected_date), variable=self.var, offvalue=0,
                                              onvalue=self.on,
                                              relief=GROOVE, width=80, wraplength=540, height=3,anchor=W)
                self.task_added.bind('<Button-1>', self.move_indone)
                self.task_added.grid(row=self.r, column=0, columnspan=3)
                
                self.r -= 1
                
                task_and_time = [task_CAL, selected_date]
                self.values[self.on] = task_and_time
                
                self.on -= 1
                self.scrollable_body2.update()
                break
            
    def load_t(self):
        try:
            f = open(self.tasks, 'rb')
        except FileNotFoundError:
            return
        self.tasks_arr = pickle.load(f)
        
        self.var = IntVar()
        for task in self.tasks_arr:
            self.task_added = Checkbutton(self.scrollable_body, text=task, variable=self.var, offvalue=0, onvalue=self.on, relief=GROOVE, width=80,
                                          wraplength=540, height=3,
                                          anchor=W)
            self.task_added.bind('<Button-1>', self.move_indone)
            self.task_added.grid(row=self.r, column=0, columnspan=3)
            
            self.r -= 1
            task_and_time = [task, self.now.strftime('%Y-%m-%d')]
            self.values[self.on] = task_and_time
            self.on -= 1
        self.scrollable_body.update()
        
    def load_t_bytime(self):
        try:
            file = open(self.tasks_bydate, 'rb')
            file_time = open(self.file_wdate, 'rb')
        except FileNotFoundError:
            return
        self.tasks_arr_bydate = pickle.load(file)
        self.time = pickle.load(file_time)
        
        self.var = IntVar()
        i = 0
        for task in self.tasks_arr_bydate:
            self.task_added = Checkbutton(self.scrollable_body2, text='{} \n {}'.format(task, self.time[i]), variable=self.var, offvalue=0,
                                          onvalue=self.on, relief=GROOVE,
                                          width=80, wraplength=540, height=3, anchor=W)
            self.task_added.bind('<Button-1>', self.move_indone)
            self.task_added.grid(row=self.r, column=0, columnspan=3)
            self.r -= 1
            task_and_time = [task, self.time[i]]
            self.values[self.on] = task_and_time
            self.on -= 1
            i += 1
        self.scrollable_body2.update()
        
    def load_done(self):
        try:
            file = open(self.file_done, 'rb')
        except FileNotFoundError:
            return
        self.tasks_done = pickle.load(file)

        k = 0
        for task in self.tasks_done:
            self.task_done = Label(self.scrollable_body3, text=task, relief=GROOVE, width=80, wraplength=540, height=3, anchor=W)
            self.task_done.grid(row=self.r, column=0, columnspan=3)
            self.r -= 1
            k += 1
        self.scrollable_body3.update()
            
    def move_indone(self, event):
        for value, task_name in self.values.items():

            self.tasks_done.append(task_name)
            pickle.dump(self.tasks_done, open(self.file_done, 'wb'))

            if event.widget['onvalue'] == value:

                if task_name[0] in self.tasks_arr and task_name[0] in self.tasks_arr_bydate:
                    event.widget.grid_forget()
                    self.tasks_arr_bydate.remove(task_name[0])
                    pickle.dump(self.tasks_arr_bydate, open(self.tasks_bydate, 'wb'))

                    self.tasks_arr.remove(task_name[0])
                    pickle.dump(self.tasks_arr_bydate, open(self.tasks, 'wb'))

                elif task_name[0] in self.tasks_arr_bydate:
                    event.widget.grid_forget()
                    self.tasks_arr_bydate.remove(task_name[0])
                    pickle.dump(self.tasks_arr_bydate, open(self.tasks_bydate, 'wb'))
                    
                elif task_name[0] in self.tasks_arr:
                    event.widget.grid_forget()
                    self.tasks_arr.remove(task_name[0])
                    pickle.dump(self.tasks_arr_bydate, open(self.tasks, 'wb'))
                    
                self.task_done = Label(self.scrollable_body3, text='{} \n {}'.format(task_name[0], task_name[1]), relief=GROOVE, width=80, wraplength=540, height=3, anchor=W)
                self.task_done.grid(row=self.r, column=0, columnspan=3)
                self.r -= 1
                self.scrollable_body3.update()

                
planer = Planer()
planer.root.mainloop()
