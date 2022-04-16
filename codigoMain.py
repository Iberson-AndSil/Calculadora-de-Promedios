from cProfile import label
from hashlib import new
from lib2to3.pytree import convert
from tkinter import BOTH, RIGHT, Button, Variable, messagebox
from typing import Text
from numpy import insert

from pyparsing import StringStart
from claseCursos import cursos
import sqlite3
from cgitb import text
from pickle import FRAME
import tkinter as tk
from tkinter import CENTER, ttk
from tkinter import Frame, StringVar
import re

#Creando ventana principal y agregando algunos atributos...
ventanaPrincipal = tk.Tk()
ventanaPrincipal.title("Promedios :)")
ventanaPrincipal.geometry('300x400')
ventanaPrincipal.resizable(0,0)

#Conectando a la base de datos local...
conex = sqlite3.connect("BasedeDatos.db")
Cr = conex.cursor()


#Creando base de datos con sus respectivos atributos
Cr.execute("""CREATE TABLE IF NOT EXISTS cursos(
            codigo VARCHAR(4) PRIMARY KEY,
            nombre VARCHAR2(20) NOT NULL,
            horas VARCHAR(2) NOT NULL
            )""")
conex.commit()

#Funcion para guardar cursos y sus atributos...
def guardaCurso():

    #Agrego primer frame 
    PestañaGuardaCurso = Frame()
    PestañaGuardaCurso.pack()
    PestañaGuardaCurso.config(bg="white")
    PestañaGuardaCurso.config(width="300", height="375")
    PestañaGuardaCurso.place(x=0, y=25)

    def is_valid_char(char):
        return char in "0123456789."

    validatecommand = PestañaGuardaCurso.register(is_valid_char)

    lblMuestratexto = tk.Label(text="Datos del Curso")
    lblMuestratexto.place(x=100, y=60)

    #Agrego un codigo opcional que aun no esta guardado en la bd
    Cr.execute("select codigo from cursos")
    ids = Cr.fetchall()
    contador = len(ids)
    contador=contador+1

    #Solicita Codigo del curso
    lblCodigo = tk.Label(text="Código: ")
    lblCodigo.place(x=40, y=120)

    #Restrinigir el ingreso de datos...
    entry_text = StringVar()
    edtCodigo = tk.Entry(textvariable=entry_text, validate="key", validatecommand=(validatecommand, "%S")  ,justify=CENTER)
    edtCodigo.insert(0, contador)
    edtCodigo.place(x=120, y=120)
    def limitador(entry_text):
        if len(entry_text.get()) > 0:
            entry_text.set(entry_text.get()[:2])

    entry_text.trace("w", lambda *args: limitador(entry_text))

    #Solicita nombre del curso
    lblNombre = tk.Label(text="Nombre: ")
    lblNombre.place(x=40, y=150)
    edtNombre = tk.Entry(justify=CENTER)
    edtNombre.place(x=120, y=150)

    #solicita horas semanales
    lblHoras = tk.Label(text="Horas:")
    lblHoras.place(x=40, y=180)

    #Restringir el ingreso de datos
    entry_text1 = StringVar()
    edtHoras = tk.Entry(textvariable=entry_text1, validate="key", validatecommand=(validatecommand, "%S"), justify=CENTER)
    edtHoras.place(x=120, y=180)
    def limitador(entry_text1):
        if len(entry_text1.get()) > 0:
            entry_text1.set(entry_text1.get()[:2])

    entry_text1.trace("w", lambda *args: limitador(entry_text1))
    
    #Funcion de guardado
    def registerBd():

        #Creando variables compatibles para agregar a  la bd
        c = edtCodigo.get()
        n = edtNombre.get()
        h = edtHoras.get()

        if n != "":
       
            cursone = cursos(c, n, h)
            Cr.execute("INSERT INTO cursos VALUES(?, ?, ?)",
                    (cursone.codigo, cursone.nombre, cursone.horas))    
            conex.commit()
        
        #Limpiando las cajas de entrada...
        edtCodigo.delete(0, "end")
        edtNombre.delete(0, "end")
        edtHoras.delete(0, "end")
        
    #Boton para guardar registros
    btnGuardarenBD = tk.Button(text="Registrar", command=registerBd)
    btnGuardarenBD.place(x=120, y=210)

    def mostrarRegistros():

        #Solicitando todos los ids a mi bd...
        Cr.execute("select codigo from cursos")
        vcur = Cr.fetchall() #Almacenando en vcur...

        #Almacenando en un txt con fines de compatibilidad...
        fle = open("element.txt", "w")
        fle.write(str(vcur))
        fle.close

        with open("element.txt","r") as fle:
            for linea in fle:
                descomprimir = linea

        #Algoritmo para descomprimir la lista e igualar los ids...
        s = [str(s) for s in re.findall(r'-?\d+\.?\d*', descomprimir)]
        var = str(" ".join(s))

        #Creando Listbox
        cuadroText = tk.Listbox(PestañaGuardaCurso)
        scrollbar = tk.Scrollbar(cuadroText) 
        scrollbar.pack(side = RIGHT, fill = BOTH) 

        Str_value = var
        for index in range ( len ( Str_value ) ):
            varia = Str_value[index]

            Cr.execute("SELECT codigo FROM cursos WHERE codigo=?",(varia,))
            cursc = str(Cr.fetchone())
            newCurs = cursc+"          "
            Cr.execute("SELECT nombre FROM cursos WHERE codigo=?",(varia,))
            cursn = str(Cr.fetchone())
            newCurs = newCurs+cursn+"          "
            Cr.execute("SELECT horas FROM cursos WHERE codigo=?",(varia,))
            cursh = str(Cr.fetchone())
            newCurs = newCurs+cursh+""

            c = False
            for i in newCurs:
                if i.isalpha():
                    c = True

            if c == True:
                cuadroText.insert(0,newCurs)
            newCurs = ""

        cuadroText.place(x=25, y=220, width="250", height="100")
        cuadroText.config(yscrollcommand = scrollbar.set) 
        scrollbar.config(command = cuadroText.yview) 
        
    btnCargarRegistros = tk.Button(text="Acualiza/Muestra", command=mostrarRegistros)
    btnCargarRegistros.place(x=190, y=210)
    
    entry = StringVar()
    edtGuardaCodigo = tk.Entry(textvariable=entry,validate="key", validatecommand=(validatecommand, "%S") ,justify=CENTER)
    edtGuardaCodigo.place(x=135, y=355, width="40", height="25")
    def limitador(entry):
        if len(entry.get()) > 0:
            entry.set(entry.get()[:2])

    entry.trace("w", lambda *args: limitador(entry))

    def EliminaRegistro():
        messagebox.showinfo(message="Acualzar tabla.", title="Registro Elimado")
        guardaCodigo = edtGuardaCodigo.get()
        Cr.execute("delete from cursos where codigo=?",(guardaCodigo,))
        conex.commit()

    btnBorrarRegistro = tk.Button(text="Eliminar/Codigo:", command=EliminaRegistro)
    btnBorrarRegistro.place(x=30, y=355)

#Funcion para registrar notas
def RegistraNotas():

    #Agrego segundo frame
    PestañaRegistraNotas = Frame()
    PestañaRegistraNotas.pack()
    PestañaRegistraNotas.config(bg="white")
    PestañaRegistraNotas.config(width="300", height="375")
    PestañaRegistraNotas.place(x=0, y=25)

    def is_valid_char(char):
        return char in "0123456789."

    validatecommand = PestañaRegistraNotas.register(is_valid_char)

    #Solicitando id del curso... 
    lblBuscarxID = tk.Label(text="ID del curso:")
    lblBuscarxID.place(x=20, y=50)

    #Capturando dato...
    entry_text = StringVar()
    edtGuardaID = tk.Entry(textvariable=entry_text, validate="key", validatecommand=(validatecommand, "%S")  ,justify=CENTER)
    edtGuardaID.place(x=100, y=50)
    def limitador(entry_text):
        if len(entry_text.get()) > 0:
            entry_text.set(entry_text.get()[:2])

    entry_text.trace("w", lambda *args: limitador(entry_text))

    #Funcion para buscar el id en la bd
    def BuscaID():
        
        #Solicitando todos los ids a mi bd...
        Cr.execute("select codigo from cursos")
        curs = Cr.fetchall() #Almacenando en curs...

        #Almacenando en un txt con fines de compatibilidad...
        fl = open("element.txt", "w")
        fl.write(str(curs))
        fl.close

        with open("element.txt","r") as fl:
            for linea in fl:
                descomprimir = linea

        #Algoritmo para descomprimir la lista e igualar los ids...
        s = [str(s) for s in re.findall(r'-?\d+\.?\d*', descomprimir)]
        var = str(" ".join(s))

        boll = False
        Str_value = var
        for index in range ( len ( Str_value ) ):
            if Str_value[index] == edtGuardaID.get():
                # messagebox.showinfo(message="si existe", title="Título")
                boll = True

        if boll == True:

            PestañaOperaciones=tk.Frame()
            PestañaOperaciones.pack()
            PestañaOperaciones.config(bg="white")
            PestañaOperaciones.config(width="300", height="320")
            PestañaOperaciones.place(x=0, y=80)

            Variable = edtGuardaID.get()
                
            Cr.execute("select nombre from cursos where codigo=?", (Variable,))
            nombreCurso = Cr.fetchone()

            MostrarCurso = tk.Label(text=nombreCurso)
            MostrarCurso.place(x=120, y=100)

            lblMedioCurso = tk.Label(text="Medio curso:  ")
            lblMedioCurso.place(x=10, y=150)

            entrada1 = StringVar()
            edtGuardaNotaMedioCurso = tk.Entry(textvariable=entrada1, validate="key", validatecommand=(validatecommand, "%S"), justify=CENTER)
            edtGuardaNotaMedioCurso.place(x=90, y=150)
            def limitador(entrada1):
                if len(entrada1.get()) > 0:
                    entrada1.set(entrada1.get()[:4])

            entrada1.trace("w", lambda *args: limitador(entrada1))

            lblPorcentajeMedioCurso = tk.Label(text="%")
            lblPorcentajeMedioCurso.place(x=220, y=150)

            #*****************************************************
            ent1=StringVar()
            entPorcMedioCurso = tk.Entry(textvariable=ent1, validate="key", validatecommand=(validatecommand, "%S") ,justify=CENTER)
            entPorcMedioCurso.place(x=240, y=150, width="50", height="20")
            def limitador(ent1):
                if len(ent1.get()) > 0:
                    ent1.set(ent1.get()[:2])

            ent1.trace("w", lambda *args: limitador(ent1))
            
            lblExamenFinal = tk.Label(text="Examen final:")
            lblExamenFinal.place(x=10, y=180)
               
            entrada2 = StringVar()
            edtGuardaNotaFinal = tk.Entry(textvariable=entrada2, validate="key", validatecommand=(validatecommand, "%S") ,justify=CENTER)
            edtGuardaNotaFinal.place(x=90, y=180)
            def limitador(entrada2):
                if len(entrada2.get()) > 0:
                    entrada2.set(entrada2.get()[:4])

            entrada2.trace("w", lambda *args: limitador(entrada2))

            lblPorcentajeFinal = tk.Label(text="%")
            lblPorcentajeFinal.place(x=220, y=180)

            #*****************************************************
            ent2=StringVar()
            entPorcFinal = tk.Entry(textvariable=ent2, validate="key", validatecommand=(validatecommand, "%S"), justify=CENTER)
            entPorcFinal.place(x=240, y=180, width="50", height="20")
            def limitador(ent2):
                if len(ent2.get()) > 0:
                    ent2.set(ent2.get()[:2])

            ent2.trace("w", lambda *args: limitador(ent2))

            lblPracticas = tk.Label(text="Practicas:")
            lblPracticas.place(x=10, y=210)

            edtGuardaNotasPracticas = tk.Entry(justify=CENTER)
            edtGuardaNotasPracticas.place(x=90, y=210)

            def MostrarPromedio():
                #Algoritmo para calcular el promedio de las practicas
                try:
                    cadena = edtGuardaNotasPracticas.get()
                    extraeEntero = ""
                    numeroextraido = ""
                    cadena = cadena + " "
                    contador = 0
                    sumaPracticas = 0
                    for i in cadena:
                        extraeEntero = extraeEntero + i
                    if i == " ":
                        contador += 1
                        numeroextraido = float(extraeEntero)
                        extraeEntero = ""
                        sumaPracticas += numeroextraido
                except ValueError:
                    print("0")

                #Datos de examenes...
                PromedioPracticas = sumaPracticas/contador
                MedioCurso = float(edtGuardaNotaMedioCurso.get())
                ExamenFinal = float(edtGuardaNotaFinal.get())

                #Datos de los porcentajes...
                porcMedioCurso = int(entPorcMedioCurso.get())
                porcFinal = int(entPorcFinal.get())
                porcPracticas = 100 - porcMedioCurso - porcFinal

                #Operacion...
                Promedio = ((porcMedioCurso/100)*MedioCurso)+((porcFinal/100)*ExamenFinal)+((porcPracticas/100)*PromedioPracticas)

                convert = str(Promedio)
                lblMuestra = tk.Label(text=convert)
                lblMuestra.place(x=150, y=250)

            btnMostrar = tk.Button(text="Promedio:", command=MostrarPromedio)
            btnMostrar.place(x=55, y=250)
        
    btBuscaID = tk.Button(text="Buscar", command=BuscaID) 
    btBuscaID.place(x=230, y=47)

#Boton para guardar curso
btnGuardarCursos = tk.Button(text="Guarda Curso", command=guardaCurso)
btnGuardarCursos.place(x=0, y=0, width="150", height="26")

#Boton para registrar notas
btnRegistrarNotas = tk.Button(text="Registra Notas", command=RegistraNotas)
btnRegistrarNotas.place(x=150, y=0, width="150", height="26")

# conex.close()
ventanaPrincipal.mainloop()