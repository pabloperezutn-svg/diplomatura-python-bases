import sqlite3
import psycopg2

# Config PostgreSQL
pg_config = {
    'user': '<username>',
    'password': '<password>',
    'dbname': 'library',
}

db_sqlite = 'library.db'

def obtener_estructura_sqlite(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablas = cursor.fetchall()

    estructura = {}

    for tabla in tablas:
        nombre_tabla = tabla[0]

        cursor.execute(f"PRAGMA table_info({nombre_tabla});")
        columnas = cursor.fetchall()

        estructura[nombre_tabla] = columnas

    conn.close()
    return estructura

def convertir_tipo_sqlite_a_postgres(tipo_sqlite):
    tipo = tipo_sqlite.upper()
    if "INT" in tipo:
        return "INTEGER"
    elif "CHAR" in tipo or "CLOB" in tipo or "TEXT" in tipo:
        return "TEXT"
    elif "BLOB" in tipo:
        return "BYTEA"
    elif "REAL" in tipo or "FLOA" in tipo or "DOUB" in tipo:
        return "REAL"
    elif "NUMERIC" in tipo or "DECIMAL" in tipo:
        return "NUMERIC"
    elif tipo == "":
        return "TEXT"
    else:
        return tipo

def crear_tablas_postgres(estructura, pg_config):
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user=pg_config['user'],
        password=pg_config['password'],
        dbname=pg_config['dbname']
    )
    cursor = conn.cursor()

    for tabla, columnas in estructura.items():
        campos_sql = []
        pk_cols = []

        for col in columnas:
            cid, name, tipo, notnull, dflt_value, pk = col
            tipo_pg = convertir_tipo_sqlite_a_postgres(tipo)
            campo = f'"{name}" {tipo_pg}'

            if notnull:
                campo += " NOT NULL"
            if dflt_value is not None:
                campo += f" DEFAULT {dflt_value}"
            campos_sql.append(campo)

            if pk:
                pk_cols.append(name)

        pk_sql = ""
        if pk_cols:
            pk_sql = f", PRIMARY KEY ({', '.join(pk_cols)})"

        sql = f'CREATE TABLE IF NOT EXISTS "{tabla}" ({", ".join(campos_sql)}{pk_sql});'

        cursor.execute(sql)

    conn.commit()
    cursor.close()
    conn.close()

def exportar_datos_sqlite_a_postgres(db_sqlite, pg_config, estructura):
    conn_sqlite = sqlite3.connect(db_sqlite)
    cursor_sqlite = conn_sqlite.cursor()

    conn_pg = psycopg2.connect(
        host="localhost",
        port=5432,
        user=pg_config['user'],
        password=pg_config['password'],
        dbname=pg_config['dbname']
    )
    cursor_pg = conn_pg.cursor()

    for tabla, columnas in estructura.items():
        # Obtener nombres de columnas para hacer INSERT
        nombres_columnas = [col[1] for col in columnas]

        cursor_sqlite.execute(f'SELECT * FROM "{tabla}";')
        filas = cursor_sqlite.fetchall()

        if not filas:
            print(f"No hay datos para insertar en la tabla '{tabla}'")
            continue

        # Construir consulta insert con placeholders
        columnas_str = ', '.join(f'"{col}"' for col in nombres_columnas)
        placeholders = ', '.join(['%s'] * len(nombres_columnas))
        sql_insert = f'INSERT INTO "{tabla}" ({columnas_str}) VALUES ({placeholders})'

        # Insertar filas en PostgreSQL
        cursor_pg.executemany(sql_insert, filas)
        print(f"Insertados {len(filas)} registros en '{tabla}'")

    conn_pg.commit()

    cursor_sqlite.close()
    conn_sqlite.close()
    cursor_pg.close()
    conn_pg.close()

# Ejecutar todo el proceso
estructura = obtener_estructura_sqlite(db_sqlite)
crear_tablas_postgres(estructura, pg_config)
exportar_datos_sqlite_a_postgres(db_sqlite, pg_config, estructura)
