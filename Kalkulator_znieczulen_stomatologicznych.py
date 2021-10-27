import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font

win = tk.Tk()
win.title("Kalkulator znieczuleń")
win['background']='black' #kolor tła GUI

tabControl = ttk.Notebook(win)

tab1 = tk.Frame(tabControl, background='#6666cc')    #zakładka 1
tabControl.add(tab1, text="Lidokaina, Bupiwakaina, Artykaina")

tab2 = tk.Frame(tabControl, background='#ff9900')    #zakładka 2
tabControl.add(tab2, text="Prokaina, Prylokaina, Mepiwakaina")

tabControl.pack(expand=1, fill="both", padx=10, pady=10)

mainFrame1 = tk.LabelFrame(tab1, text = "Oblicz liczbę ampułek", background='#ccccff')
mainFrame1.grid(column=0, row=0,columnspan=3,sticky='W', padx=30,pady=10)

mainFrame2 = tk.LabelFrame(tab2, text = "Oblicz liczbę ampułek", background='#ffcc66')
mainFrame2.grid(column=0, row=0,columnspan=3,sticky='W', padx=70,pady=10)

#pierwsza zakładka
aLabel = tk.Label(mainFrame1, text="Masa ciała pacjenta [kg]", background='#ccccff', fg='#154360', font=('Arial',9,'bold'))
aLabel.grid(column=0, row=1, sticky = tk.W)

spinVar = tk.IntVar()
spinVar.set(50)
wSpinbox = tk.Spinbox(mainFrame1, from_=5, to=200,textvariable=spinVar,width=10)
wSpinbox.grid(column=2,row=1,columnspan=2, sticky=tk.E)

bLabel = tk.Label(mainFrame1, text="Stężenie procentowe produktu [%]", background='#ccccff', fg='#154360', font=('Arial',9,'bold'))
bLabel.grid(column=0, row=2, sticky = tk.W)

spinVar2 = tk.DoubleVar()
spinVar2.set(0)
wSpinbox2 = tk.Spinbox(mainFrame1, from_=0, to=100,textvariable=spinVar2,width=10)
wSpinbox2.grid(column=2,row=2,columnspan=2, sticky=tk.E)

cLabel = tk.Label(mainFrame1, text="Objętość ampułki [ml]", background='#ccccff', fg='#154360', font=('Arial',9,'bold'))
cLabel.grid(column=0, row=3, sticky = tk.W)

spinVar3 = tk.DoubleVar()
spinVar3.set(0)
wSpinbox3 = tk.Spinbox(mainFrame1, from_=0, to=3,textvariable=spinVar3,width=10)
wSpinbox3.grid(column=2,row=3,columnspan=2, sticky=tk.E)

dLabel = tk.Label(mainFrame1, text="Substancja znieczulająca", background='#ccccff', fg='#154360', font=('Arial',9,'bold'))
dLabel.grid(column=0, row=4, columnspan=4, sticky = tk.W)

napis=tk.StringVar()
numberChosen = ttk.Combobox(mainFrame1,width=30,textvariable=napis,state='readonly')
numberChosen['values'] = ('Artykaina z wazokonstryktorem','Artykaina bez wazokonstryktora','Bupiwakaina','Lidokaina z wazokonstryktorem','Lidokaina bez wazokonstryktora')
numberChosen['font']=('Georgia',9)
numberChosen.grid(column=1,row=4,columnspan=3,sticky=tk.E)
numberChosen.current(0)
      
def clickMe():
    if  numberChosen.get()=="Artykaina z wazokonstryktorem": dawka_max = 7
    elif numberChosen.get()=="Artykaina bez wazokonstryktora": dawka_max = 4
    elif numberChosen.get()=="Lidokaina z wazokonstryktorem": dawka_max = 7 
    elif numberChosen.get()=="Lidokaina bez wazokonstryktora": dawka_max = 3
    else: dawka_max = 2

    try: 
        liczba = float(spinVar.get())
        liczba2 = float(spinVar2.get())
        liczba3 = float(spinVar3.get())
        if liczba <= 200 and liczba >=5 and liczba2 <= 100 and liczba3 >=1 and liczba3 <=2:
            print("Podane wartości {}, {}, {}".format(liczba,liczba2,liczba3))
        else:
            raise ValueError
    except (tk.TclError, TypeError): 
        messagebox.showerror('Błąd','Wpisany znak nie jest liczbą/wpisano przecinek zamiast kropki')
    except ValueError:
        messagebox.showerror('Błąd','Podano błędną wartość')
        return

    try:
        ampulki=((spinVar.get()*dawka_max)/(spinVar2.get()/100))/(spinVar3.get()*1000)
        messagebox.showinfo('Info',"Maksymalna liczba ampułek wynosi: "+str(int(ampulki)))
    except ZeroDivisionError:
        messagebox.showerror('Błąd','Dzielenie przez 0. Zmień dane wejściowe.')

oblicz = tk.Button(mainFrame1, text="Oblicz",command = clickMe, background='#ff6666', activebackground='#cc0000', fg='#7B241C')
oblicz['font']=('Arial',11,'bold')
oblicz.grid(column = 0, row=6, columnspan=4, sticky=tk.E+tk.W)

#druga zakładka
aaLabel = tk.Label(mainFrame2, text="Znieczulenie z dodatkiem wazokonstryktorów?", background='#ffcc66', fg='#641E16', font=('Arial',9,'italic'))
aaLabel.grid(column=0, row=1, sticky = tk.W)

radVar2 = tk.IntVar()
curRad2 = tk.Radiobutton(mainFrame2, text="nie", variable=radVar2, value=0, width=1, background='#ffcc66')
curRad2.grid(column=3,row=1,columnspan=2, sticky=tk.E)
curRad2 = tk.Radiobutton(mainFrame2, text="tak", variable=radVar2, value=1, width=1, background='#ffcc66')
curRad2.grid(column=4,row=1, columnspan=2, sticky=tk.E)

bbLabel = tk.Label(mainFrame2, text="Stężenie procentowe produktu [%]", background='#ffcc66', fg='#641E16', font=('Arial',9,'italic'))
bbLabel.grid(column=0, row=2, sticky = tk.W)

spinVar4 = tk.DoubleVar()
spinVar4.set(0)
wSpinbox4 = tk.Spinbox(mainFrame2, from_=0, to=100,textvariable=spinVar4,width=10)
wSpinbox4.grid(column=4,row=2,columnspan=2, sticky=tk.E)

ccLabel = tk.Label(mainFrame2, text="Objętość ampułki [ml]", background='#ffcc66', fg='#641E16', font=('Arial',9,'italic'))
ccLabel.grid(column=0, row=3, sticky = tk.W)

spinVar5 = tk.DoubleVar()
spinVar5.set(0)
wSpinbox5 = tk.Spinbox(mainFrame2, from_=0, to=3,textvariable=spinVar5,width=10)
wSpinbox5.grid(column=4,row=3,columnspan=2, sticky=tk.E)

ddLabel = tk.Label(mainFrame2, text="Substancja znieczulająca", background='#ffcc66', fg='#641E16', font=('Arial',9,'italic'))
ddLabel.grid(column=0, row=4, columnspan=4, sticky = tk.W)

napis2=tk.StringVar()
numberChosen2 = ttk.Combobox(mainFrame2,width=12,textvariable=napis2,state='readonly')
numberChosen2['values'] = ('Mepiwakaina','Prokaina','Prylokaina')
numberChosen2['font']=('Georgia',9)
numberChosen2.grid(column=3,row=4,columnspan=3,sticky=tk.E+tk.W)
numberChosen2.current(0)

def clickMe2():
    if radVar2.get()==1 and numberChosen2.get()=="Mepiwakaina": dawka_max2 = 500
    elif radVar2.get() ==0 and numberChosen2.get()=="Mepiwakaina": dawka_max2 = 400
    elif numberChosen2.get()=="Prokaina": dawka_max2 = 500
    else: dawka_max2 = 400
    
    try: 
        liczba4 = float(spinVar4.get())
        liczba5 = float(spinVar5.get())
        if liczba4 <= 100 and  liczba5 >=1 and liczba5 <=2:
            print("Podane wartości {}, {}".format(liczba4,liczba5))
        else:
            raise ValueError
    except (tk.TclError, TypeError): 
        messagebox.showerror('Błąd','Wpisany znak nie jest liczbą/wpisano przecinek zamiast kropki')
    except ValueError:
        messagebox.showerror('Błąd','Podano błędną wartość')
        return

    try:
        ampulki2=((dawka_max2/(spinVar4.get()/100))/(spinVar5.get()*100))
        messagebox.showinfo('Info',"Maksymalna liczba ampułek wynosi: "+str(int(ampulki2)))
    except ZeroDivisionError:
        messagebox.showerror('Błąd','Dzielenie przez 0. Zmień dane wejściowe.')

oblicz2 = tk.Button(mainFrame2,text="Oblicz",command = clickMe2, background='#99cc66', activebackground='#215E21', fg='#0B5345')
oblicz2['font']=('Arial',11,'bold')
oblicz2.grid(column=0, row=6, columnspan=6, sticky = tk.E+tk.W)


win.mainloop()