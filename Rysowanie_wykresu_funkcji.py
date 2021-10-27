import math
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import messagebox
from tkinter import Entry
from tkinter import Frame

win = tk.Tk()
win.title("Rysowanie wykresu")

tabControl = ttk.Notebook(win)

tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text="Funkcje trygonometryczne")

tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text="Wykres wielomianu")

tabControl.pack(expand=1, fill="both", padx=10, pady=10)

#pierwsza zakładka - f.trygonometryczne
mainFrame1 = ttk.LabelFrame(tab1, text = "Podaj granice wykresu i krok")
mainFrame1.grid(column=0, row=0,columnspan=3,sticky='W', padx=10,pady=10)

mainFrame2 = ttk.LabelFrame(tab1, text = "Wybierz funkcję, której wykres ma zostać narysowany")
mainFrame2.grid(column=0, row=4,columnspan=3,sticky='W')

Label1=tk.Label(mainFrame1,text='Podaj xmin')
Label1.grid(column=0, row=1,sticky=tk.W)
dolnagranica = tk.DoubleVar()
okno1=tk.Entry(mainFrame1,width=20, textvariable=dolnagranica)
okno1.grid(column=2,row=1,sticky=tk.E)

Label2=tk.Label(mainFrame1,text='Podaj xmax')
Label2.grid(column=0,row=2,sticky=tk.W)
gornagranica = tk.DoubleVar()
okno2=tk.Entry(mainFrame1,width=20, textvariable=gornagranica)
okno2.grid(column=2,row=2,sticky=tk.E)

Label3=tk.Label(mainFrame1,text='Podaj krok')
Label3.grid(column=0,row=3,sticky=tk.W)
krok= tk.DoubleVar()
okno3=tk.Entry(mainFrame1,width=20, textvariable=krok)
okno3.grid(column=2,row=3,sticky=tk.E)

f_trygonom = ['sin(x)','cos(x)','tg(x)','ctg(x)']
var=tk.IntVar()
for col in range(4):
    R=tk.Radiobutton(mainFrame2,text=f_trygonom[col],variable=var,value=[col])
    R.pack(anchor = 'w')

class series: #klasa będzie przechowywała punkty wykresu
    def __init__(self, **cnf):   #__init__ - tworzy konstruktor
                                #**cnf - parametry, np. czcionka, linia, w formie słownika do rozpakowania
        self.cnf=cnf            #self. - atrybut w klasie
        self.X, self.Y = [],[]
        self.xmin, self.xmax, self.ymin, self.ymax = None, None, None, None
        self.n = 0  #liczba punktów na wykresie
    def add_point(self, xi, yi):    #dodawanie punktów do wykresu
        self.X.append(xi)           #X są zdefiniowane jako lista, więc dodajemy przez append
        self.Y.append(yi)
        self.n =+ 1
        if self.xmin == None or self.xmin>xi: #sprawdzenie, czy dobrze się wyświetlają wartości(podstawienie nowej wartości w odpowienim miejscu listy)
            self.xmin=xi
        if self.ymin == None or self.ymin>yi: 
            self.ymin=yi
        if self.xmax == None or self.xmax<xi: 
            self.xmax=xi
        if self.ymax == None or self.ymax<yi: 
            self.ymax=yi
    def get_range(self):
        return self.xmin, self.ymin, self.xmax, self.ymax 
          

class wykres:
    def __init__(self,kanwa,*coords):    #*coords - parametry współrzędnych w formie listy
        self.kanwa = kanwa
        self.xemin, self.yemin, self.xemax, self.yemax = coords #min i max wykresu
        self.width = self.xemax-self.xemin  #szerokość wykresu
        self.height = self.yemax-self.yemin #wysokość wykresu
        self.series = []
    def add_series(self,**cnf): #dodawanie serii do wykresu
        self.series.append(series(**cnf))

    def draw(self):
        self.kanwa.delete(tk.ALL) #czyści płótno - usuwa wszystko, co było wcześniej narysowane
        kanwa.create_rectangle(self.xemin,self.yemin,self.xemax,self.yemax, fill="white")     

        xmin,ymin,xmax,ymax = self.get_range()

        try:      #pułapka, żeby nie dzielić przez 0
            skala_x=self.width/(xmax-xmin)
            skala_y=self.height/(ymax-ymin)
        except ZeroDivisionError:
            return

        for s in self.series: #nowe wartości, po przeskalowaniu
            Xe=[self.xemin+(xi-xmin)*skala_x for xi in s.X] #idziemy po wektorze x i do elementu z xemin dodajemy element z wektora (xi-xmin) i mnożymy razy skalę, żeby się zmieściło w oknie
            Ye=[self.yemin+(ymax-yi)*skala_y for yi in s.Y]

        self.kanwa.create_line(tuple(zip(Xe,Ye)),s.cnf) #zip wrzuci do krotki wszystkie wartości x i y 
        

    def get_range(self):
        xmin,ymin,xmax,ymax=self.series[0].get_range()
        for s in self.series:
            x1,y1,x2,y2=s.get_range()
            if xmin>x1: xmin=x1
            if ymin>y1: ymin=y1
            if xmax<x2: xmax=x2
            if ymax<y2: ymax=y2
        return xmin,ymin,xmax,ymax

    def __getitem__(self,i):
        return self.series[i]

app = tk.Tk()
app.withdraw()
app.title("Wykres")
kanwa = tk.Canvas(app,width=800,height=600)
kanwa.pack()
W=wykres(kanwa, 50,50,800-50,600-50) #gdzie ma się rysować wykres; ograniczony po 50 pxl z każdej strony
W.add_series(fill='blue',width=3)
i=0
app.withdraw() #ukrywa okno z kanwą, żeby wyświetlało się dopiero po przyciśnięciu przycisku rysuj

def clickMe():
    def rysuj():
        app.deiconify() #wyświetla okno z kanwą
        global i
        x=xmin+i*dx #wyznaczane kolejnych punktów na wykresie zależne od wart. min oraz kroku
        y=fun(x)
        W[0].add_point(x,y)
        W.draw()
        i += 1
        if xmin+i*dx>xmax: return
        app.after(20,rysuj)

    def fun(x):
        try:
            if var.get() == 0:return math.sin(x)    #wykres funkcji sin(x)
            elif var.get() == 1:return math.cos(x)  #wykres funkcji cos(x)
            elif var.get() == 2:return math.tan(x)  #wykres funkcji tg(x)
            else: return (1/math.tan(x))            #wykres funkcji ctg(x)
        except ZeroDivisionError:
            messagebox.showerror('Błąd','Błędny zakres x')
    
    try: 
        xmin = float(dolnagranica.get())
        xmax = float(gornagranica.get())
        dx = float(krok.get())
        if dx>0 and xmin<xmax:
            print(xmin,xmax,dx)
            rysuj()
        else:
            raise ValueError
    except (tk.TclError,TypeError): 
        messagebox.showerror('Błąd','Wpisany znak nie jest liczbą')
    except ValueError:
        messagebox.showerror('Błąd','Podane dane są nieprawidłowe. Krok musi być >0, a xmin<xmax')

    app.deiconify() 
    app.mainloop()


def zamykanie():
    app.quit()
    win.quit()

#przyciski
rysuj_button1 = ttk.Button(mainFrame2,text="Rysuj",command = clickMe)
rysuj_button1.pack( side='left')
wyczysc_button1 = ttk.Button(mainFrame2,text="Wyjdź",command = zamykanie)
wyczysc_button1.pack( side='left')

#druga zakładka - wielomian
mainFrame3 = ttk.LabelFrame(tab2, text = "Podaj granice wykresu i krok")
mainFrame3.grid(column=0, row=0,columnspan=3,sticky='W', padx=10,pady=10)

Label4=tk.Label(mainFrame3,text='Podaj xmin')
Label4.grid(column=0, row=1,sticky=tk.W)
dolnagranica2 = tk.DoubleVar()
okno4=tk.Entry(mainFrame3,width=20, textvariable=dolnagranica2)
okno4.grid(column=2,row=1,sticky=tk.E)

Label5=tk.Label(mainFrame3,text='Podaj xmax')
Label5.grid(column=0,row=2,sticky=tk.W)
gornagranica2 = tk.DoubleVar()
okno5=tk.Entry(mainFrame3,width=20, textvariable=gornagranica2)
okno5.grid(column=2,row=2,sticky=tk.E)

Label6=tk.Label(mainFrame3,text='Podaj krok')
Label6.grid(column=0,row=3,sticky=tk.W)
krok2 = tk.DoubleVar()
okno6=tk.Entry(mainFrame3,width=20, textvariable=krok2)
okno6.grid(column=2,row=3,sticky=tk.E)

Label7=tk.Label(mainFrame3,text='Wpisz równanie wielomianu')
Label7.grid(column=0,row=4,sticky=tk.W)
wielomian = tk.StringVar()
okno7=tk.Entry(mainFrame3,width=20, textvariable=wielomian)
okno7.grid(column=2,row=4,sticky=tk.E)

def clickMe2():
    def rysuj():
        app.deiconify() #wyświetla okno z kanwą
        global i
        x=xmin+i*dx #wyznaczane kolejnych punktów na wykresie zależne od wart. min oraz kroku
        y=fun(x)
        W[0].add_point(x,y)
        W.draw()
        i += 1
        if xmin+i*dx>xmax: return
        app.after(20,rysuj)

    def fun(x):
        rownanie=wielomian.get()
        try:
            return eval(rownanie)
        except SyntaxError:
            messagebox.showerror('Błąd','Błąd składni. Popraw równanie')

    try: 
        xmin = float(dolnagranica2.get())
        xmax = float(gornagranica2.get())
        dx = float(krok2.get())
        if dx>0 and xmin<xmax:
            print(xmin,xmax,dx)
            rysuj()
        else:
            raise ValueError
    except (tk.TclError,TypeError): 
        messagebox.showerror('Błąd','Wpisany znak nie jest liczbą')
    except ValueError:
        messagebox.showerror('Błąd','Podane dane są nieprawidłowe. Krok musi być >0, a xmin<xmax')

def zamykanie2():
    app.quit()
    win.quit()

#przyciski
rysuj_button2 = ttk.Button(mainFrame3,text="Rysuj",command = clickMe2)
rysuj_button2.grid(column=2,row=5,sticky=tk.W)
wyczysc_button2 = ttk.Button(mainFrame3,text="Wyjdź",command = zamykanie2)
wyczysc_button2.grid(column=2,row=6,sticky=tk.W)

win.mainloop()




