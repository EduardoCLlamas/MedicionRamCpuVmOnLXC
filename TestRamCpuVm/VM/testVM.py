# Recuperación de datos del sistema (RAM,CPU,Virtual Memory)
#Autor: Eduardo Cebrero Llamas UAM-Cuajimalpa
import sqlite3
import time 
import datetime
import random
import psutil 
from subprocess import PIPE, Popen, call
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import re

def CreateTables(c):
  c.execute('CREATE TABLE IF NOT EXISTS ProcessMemory(tiempo REAL, dateData TEXT, valor REAL)')
  c.execute('CREATE TABLE IF NOT EXISTS ProcessVirtual(tiempo REAL, dateData TEXT, valor REAL)')
  c.execute('CREATE TABLE IF NOT EXISTS ProcessCpu(tiempo REAL, dateData TEXT, valor REAL)')

def MemoryDataEntry(c, conn, tiempo, dateData, valor):
	c.execute("INSERT INTO ProcessMemory(tiempo, dateData, valor) VALUES(?, ?, ?)", (tiempo, dateData, valor))
	conn.commit()

def VirtualDataEntry(c, conn, tiempo, dateData, valor):
	c.execute("INSERT INTO ProcessVirtual(tiempo, dateData, valor) VALUES(?, ?, ?)", (tiempo, dateData, valor))
	conn.commit()

def CpuDataEntry(c, conn, tiempo, dateData, valor):
	c.execute("INSERT INTO ProcessCpu(tiempo, dateData, valor) VALUES(?, ?, ?)", (tiempo, dateData, valor))
	conn.commit()

def Transf(cadena):
	for i in range(0,len(cadena)):
		cadena[i] = re.sub("\D","",cadena[i])



def SplitElements(cadena):
	lista = cadena.split(",") #se fragmenta
	for i in range(0,len(lista)):
		lista[i] = lista[i][:len(lista[i])-1] #se elimina el último caracter

	return lista #se regresa la lista


def Carga(c,conn):
	memVirt = str(psutil.virtual_memory())
	memProc = psutil.Process()
	memFis = str(memProc.memory_info())
	cpu = str(psutil.cpu_percent())
	lista = SplitElements(memVirt)# memoria activa
	lista2 = SplitElements(memFis)
	Transf(lista)
	Transf(lista2)
	tiempo = time.time()
	fecha = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
	MemoryDataEntry(c,conn,tiempo,fecha,str(float(lista2[0])/1024))
	VirtualDataEntry(c,conn,tiempo,fecha,lista[2])
	CpuDataEntry(c,conn,tiempo,fecha,cpu)


def PlotData(c):
	
	dates = []
	values = []
	dates2 = []
	values2 = []
	dates3 = []
	values3 = []
	c.execute("SELECT tiempo,valor FROM ProcessCpu")
	for row in c.fetchall():
		dates.append(row[0])
		values.append(row[1])
	c.execute("SELECT tiempo,valor FROM ProcessMemory")
	for row in c.fetchall():
		dates2.append(row[0])
		values2.append(row[1])
	c.execute("SELECT tiempo,valor FROM ProcessVirtual")
	for row in c.fetchall():
		dates3.append(row[0])
		values3.append(row[1])
	plt.figure()
	ax1 = plt.subplot2grid((2,1),(0,0), colspan = 3)
	ax2 = plt.subplot2grid((2,1),(1,0), colspan = 2)
	ax1.plot(dates, values,label = "Uso de CPU", marker = "p", color = "r")
	ax1.plot(dates3, values3,label = "Uso de Memoria Virtual", linestyle = ":", marker = "o", color = "b")	
	ax2.plot(dates2, values2,label = "Uso de RAM", linestyle = "--", marker = "D", color = "g")	
	ax1.set_ylabel("Porcentaje(%)")
	ax2.set_ylabel("MegaBytes")
	ax1.legend()
	ax2.legend()
	ax1.grid()
	ax2.grid()
	plt.xlabel("Segundos")
	plt.suptitle("Rendimiento del Sistema")
	plt.savefig('sistema.pdf')
	plt.show()
	
def PruebaVM():
	call(["echo", "Deleting files"])
	call(["rm", "Process.db"])
	call(["ls", "-l"])
	call(["clear"])
	conn = sqlite3.connect('Process.db')
	c = conn.cursor()
	CreateTables(c)
	lxc =""
	for i in range(10):
		lxc = "ubu-lxc"
		lxc += str(random.randrange(1,5))
		call(["lxc-start", "-n", lxc])
		lxc = "ubu-lxc"
		lxc += str(random.randrange(1,5))
		call(["lxc-stop", "-n", lxc])
		Carga(c,conn)
		time.sleep(0.10)
	PlotData(c)
	c.close()
	conn.close()

def PruebaLXCHard():
	call(["echo", "Deleting files"])
	call(["rm", "Process.db"])
	call(["ls", "-l"])
	call(["clear"])
	conn = sqlite3.connect('Process.db')
	c = conn.cursor()
	CreateTables(c)
	lxc = ""
	for i in range(60):
		lxc = "ubu-lxc"
		lxc += str(random.randrange(1,5))
		call(["lxc-start", "-n", lxc])
		lxc = "ubu-lxc"
		lxc += str(random.randrange(1,5))
		call(["lxc-stop", "-n", lxc])
		call(["sh","test.sh"])
		Carga(c,conn)
		time.sleep(1)
	PlotData(c)
	c.close()
	conn.close()

def PruebaLXC():
	call(["echo", "Deleting files"])
	call(["rm", "Process.db"])
	call(["ls", "-l"])
	call(["clear"])
	conn = sqlite3.connect('Process.db')
	c = conn.cursor()
	CreateTables(c)
	call(["sh","test.sh"])
	for i in range(60):
		Carga(c,conn)
		time.sleep(1)
	PlotData(c)
	c.close()
	conn.close()

def main():
	#PruebaVM()
	PruebaLXCHard()
	#PruebaLXC()

main()

		