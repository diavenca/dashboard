# Librerías para el manejo de directorios
import sqlite3
from pathlib import Path

def conectarse():
    BASE_DIR = Path.cwd()
    return sqlite3.connect(f"{BASE_DIR / 'data/in/diavenca'}")


def desconectarse(conn):
    conn.commit()
    conn.close()

def ejecutar_consulta(query, conn, varios=True):
    cur = conn.cursor()
    cur.execute(query)

    if varios:
        return cur.fetchall()
    else: 
        return cur.fetchone()

def ejecutar(query, conn):
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
