import requests
from datetime import datetime  
from datetime import timedelta  
from datetime import date
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry  
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

app=tk.Tk()
app.title("Kursy walut")
mainFrame1 = tk.LabelFrame(app, text = "Wybierz walutę i datę")
mainFrame1.grid(column=0, row=0,columnspan=3,sticky='W', padx=10,pady=10)

Label1 = ttk.Label(mainFrame1, text="Waluta")
Label1.grid(column=0, row=1, columnspan=1, sticky = tk.W)
WALUTA=tk.StringVar()
numberChosen = ttk.Combobox(mainFrame1,width=30,textvariable=WALUTA,state='readonly')
numberChosen['values'] = ('USD','CHF','EUR','GBP','RUB','CZK','DKK','HUF','NOK','SEK','CAD','JPY','CNY')
numberChosen.grid(column=3,row=1,columnspan=1,sticky=tk.E)
numberChosen.current(0)

Label2=ttk.Label(mainFrame1,text="Data początkowa")
Label2.grid(column=0,row=2,sticky=tk.W)
DATA1 = DateEntry(mainFrame1, width=12, background='darkblue',foreground='white', borderwidth=2)
DATA1.grid(column=1, row=2,columnspan=3,sticky=tk.E)
 
Label3=ttk.Label(mainFrame1,text="Data końcowa")
Label3.grid(column=0,row=3,sticky=tk.W)
DATA2 = DateEntry(mainFrame1, width=12, background='darkblue',foreground='white', borderwidth=2)
DATA2.grid(column=1, row=3,columnspan=3,sticky=tk.E)

ADRES_API = 'http://api.nbp.pl/api/exchangerates/rates/{rate}/{code}/{startDate}/{endDate}/'

def ClickMe():
    data1=DATA1.get()
    print(data1)
    data2=DATA2.get()
    print(data2)
    dt=data1.split('.')
    data1_1 = date(year=int(dt[2]), month=int(dt[1]), day=int(dt[0]))
    print(data1_1)
    dt2=data2.split('.')
    data2_1 = date(year=int(dt2[2]), month=int(dt2[1]), day=int(dt2[0]))
    print(data2_1)
    while True:
        adres = ADRES_API.replace('{rate}', 'A').replace('{code}',numberChosen.get()).replace('{startDate}', data1_1.isoformat()).replace('{endDate}',data2_1.isoformat())
        print(adres)
        r = requests.get(adres)
        if data1_1 > date.today() or data2_1 > date.today():
            messagebox.showerror('Błąd', 'Wybrano datę z przyszłości. Serwer nie posiada dla niej danych')
        if data1_1 < date(2002,1,1):
            messagebox.showerror('Błąd','Serwer nie posiada danych sprzed 2002 roku')
        if data1_1 > data2_1:
            messagebox.showerror('Błąd', 'Data początkowa nie może być późniejsza niż data końcowa')
        break
         
    kurs = []
    daty = []
    rates = r.json()['rates']
    for r in rates:
        kurs.append(r['mid'])
        daty.append(r['effectiveDate'])
 
    print(kurs)
    print(daty)

  
    if len(kurs) >= 2:
        fig = Figure(figsize=(12, 5), facecolor='white')

        axis = fig.add_subplot(111)

        xValues = daty
        yValues = kurs

        axis.plot(xValues, yValues, 'go--')

        axis.set_xticklabels(daty,rotation=30, fontsize='small')
        axis.set_xlabel('Daty')
        axis.set_ylabel('Kurs waluty {}'.format(WALUTA.get()))

        axis.grid(linestyle='dashed') 

        def _destroyWindow():
            root.quit()
            root.destroy()

        root = tk.Tk()
        root.withdraw()
        root.protocol('WM_DELETE_WINDOW', _destroyWindow)

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        root.update()
        root.deiconify()
        root.mainloop()

    else:
        messagebox.showerror('Błąd', 'Wybrano za krótki przedział dat. Wymagane są daty obejmujące co najmniej dwa dni robocze')

    
sprawdz = ttk.Button(mainFrame1,text="Rysuj wykes kursu waluty", command=ClickMe)
sprawdz.grid(row=4, columnspan=5, sticky = tk.E+tk.W)

app.mainloop()
                
    
