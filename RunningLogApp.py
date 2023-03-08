import tkinter as tk
import tkinter.ttk as ttk
from tkcalendar import Calendar
from RunData import RunLog
import datetime
from functools import partial
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class AddRunWin:

    dateList = ''

    def __init__(self, log):
        def submit():
            day = int(self.dateList[1])
            month = int(self.dateList[0])
            year = int('20' + self.dateList[2])
            date = datetime.date(year, month, day)
            distance = float(distanceEntry.get())
            time = timeEntry.get()
            hours = int(time[:2])
            if hours < 10:
                hours = int('0' + str(hours))
            minutes = int(time[3:5])
            seconds = int(time[-2:])
            notes = str(notesEntry.get("1.0", 'end-1c'))

            RunLog.addRun(
                log, date, year, month, day, distance, hours, minutes, seconds, notes)

            addRunWindow.destroy()

        def set_date():
            date = cal.get_date()
            self.dateList = re.split('/', date)
            dateLabel.config(text=date)

        addRunWindow = tk.Tk()
        addRunWindow.title("Add a Run")

        addRunWindowStyle = ttk.Style(addRunWindow)
        addRunWindowStyle.theme_use('default')
        addRunWindowStyle.configure('run.TLabel', font=('Comic Sans MS', 40),
                                    foreground='#E1E1E5', background='#36417B')
        addRunWindowStyle.configure('run.TButton', font=('Comic Sans MS', 40))
        addRunWindowStyle.configure(
            'run.TEntry', foreground='white', fieldbackground='black')
        addRunWindowStyle.configure('run.TFrame', background='#36417B')

        addRunWindowFrame = ttk.Frame(addRunWindow, style='run.TFrame')
        addRunWindowFrame.pack(expand=True, fill='both')

        addRunWindow.title("Add a Run")
        addRunWindow.geometry('800x1200')

        titleLabel = ttk.Label(addRunWindowFrame, text='Add a New Run',
                               style='run.TLabel', font=('Comic Sans MS', 50))
        titleLabel.pack()

        cal = Calendar(addRunWindowFrame, selectmode='day', year=main.currentYear,
                       month=main.currentMonth, day=main.currentDay, font='Arial 25', style="BW.TLabel")
        cal.pack()

        setDateFrame = ttk.Frame(addRunWindowFrame, style='run.TFrame')
        setDateFrame.pack()
        dateButton = ttk.Button(setDateFrame, text='Set Date', style='run.TButton',
                                command=set_date)
        dateButton.grid(row=0, column=0)
        dateLabel = ttk.Label(setDateFrame, text='', style='run.TLabel')
        dateLabel.grid(row=0, column=1)
        distanceLabel = ttk.Label(
            addRunWindowFrame, text="Distance: ", style='run.TLabel')
        distanceLabel.pack()
        distanceEntry = ttk.Entry(
            addRunWindowFrame, text="", style='run.TEntry', font=('Comic Sans MS', 50))
        distanceEntry.pack()
        timeLabel = ttk.Label(addRunWindowFrame, text="Time: (hr:min:sec  00:00:00)",
                              style='run.TLabel')
        timeLabel.pack()
        timeEntry = ttk.Entry(addRunWindowFrame, text="",
                              style='run.TEntry', font=('Comic Sans MS', 50))
        timeEntry.insert(0, '00:00:00')
        timeEntry.pack()
        notesLabel = ttk.Label(addRunWindowFrame, text="Notes:",
                               style='run.TLabel')
        notesLabel.pack()
        notesEntry = tk.Text(addRunWindowFrame, font=('Comic Sans MS', 20),
                             foreground='white', width=100, height=6)
        notesEntry.pack()
        submitButton = ttk.Button(addRunWindowFrame, text="Submit",
                                  style='run.TButton', command=submit)
        submitButton.pack()

        addRunWindow.mainloop()


class main:

    currentDate = str(datetime.date.today())
    currentDay = int(currentDate[-2:])
    currentMonth = int(currentDate[5:7])
    currentYear = int(currentDate[:4])

    def __init__(self, master):
        def plot():
            fig = plt.Figure(figsize=(4, 4), dpi=80)
            ax = fig.add_subplot(111)
            chart_type = FigureCanvasTkAgg(fig, mainFrame)
            chart_type.get_tk_widget().grid(row=2, column=0)
            df = RunLog.getGraphData(log)
            df = df[['Date', 'Distance']]
            df.set_index('Date')
            df.plot(kind='bar', legend=True, ax=ax)
            ax.set_title('Title here')

        self.master = master
        log = RunLog()
        master.protocol('WM_DELETE_WINDOW', lambda: main.on_closing(self, log))

        master.geometry("800x800")
        master.title("Running Log")
        master.configure(background="#36417B")

        style.configure('my.TButton', font=('Comic Sans MS', 40), padding=10)
        style.configure('my.TEntry', font=('Comic Sans MS', 50))
        style.configure('my.TLabel', font=('Comic Sans MS', 40),
                        foreground='#E1E1E5', background='#36417B')
        style.configure('my.TFrame', background='#36417B')
        style.configure('stats.TButton', font=('Comic Sans MS', 20))

        mainFrame = ttk.Frame(master, style='my.TFrame')
        mainFrame.pack()

        headerLabel = ttk.Label(
            mainFrame, text='Running Log', style='my.TLabel')
        headerLabel.grid(row=0, column=0)
        addRunBut = ttk.Button(mainFrame, text="Add Run", style='my.TButton',
                               command=partial(AddRunWin, log))
        addRunBut.grid(row=1, column=0, pady=25)
        plot()
        statsHeaderLabel = ttk.Label(mainFrame, text='Statistics', style='my.TLabel',
                                     font=('Comic Sans MS', 30))
        statsHeaderLabel.grid(row=3, column=0, pady=10)
        statsButtonsFrame = ttk.Frame(mainFrame, style='my.TFrame')
        statsButtonsFrame.grid(row=4, column=0, pady=5)
        statsWkButton = ttk.Button(
            statsButtonsFrame, text='Week', style='stats.TButton')
        statsWkButton.grid(row=0, column=0, padx=10)
        statsMonthButton = ttk.Button(
            statsButtonsFrame, text='Month', style='stats.TButton')
        statsMonthButton.grid(row=0, column=1, padx=10)
        statsOverallButton = ttk.Button(
            statsButtonsFrame, text='Overall', style='stats.TButton')
        statsOverallButton.grid(row=0, column=2, padx=10)
        statsFrame = ttk.Frame(mainFrame, style='my.TFrame')
        statsFrame.grid(row=5, column=0, pady=10)

        RunLog.setOverallStats(log)

        distLabel = ttk.Label(statsFrame, text='test', style='my.TLabel')
        distLabel.grid(row=0, column=0)

    def on_closing(self, log):
        log.saveToFile()


root = tk.Tk()
style = ttk.Style(root)
style.theme_use('default')
main(root)

root.mainloop()
