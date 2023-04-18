from tkinter import *
import paho.mqtt.client as mqtt
import getmac

class MQTTClient:
    def __init__(self):
        self.arr0 = []
        self.mac = getmac.get_mac_address()
        self.connected_flag = False
        self.bad_connection_flag = False
        broker_address="10.120.0.20"
        connection_topic="home/review"
        self.client = mqtt.Client()
        self.client.username_pw_set(username="ubuntu",password="topology")
        self.client.connect(broker_address)
        self.client.on_publish = self.on_publish
        self.client.on_disconnect = self.on_disconnect
        self.client.on_connect = self.on_connect
        self.client.subscribe(connection_topic)
        self.client.loop_start()

    def on_publish(self, client, userdata, result):             
        print("data published \n")
        pass

    def on_disconnect(self, client, userdata, flags, rc=0):
        m="Disconnected flags"+" result code "+str(rc)
        print(m)
        self.connected_flag = False
        self.client.connect(self.host)

    def sending(self):
        if self.connected_flag== True :
            for i in self.arr0:
                self.client.publish("home/review", str(i) + "&" + self.mac)
            self.arr0.clear() 

    def on_connect(self, client, userdata, flags, rc):
        if rc==0:
            print("connected OK Returned code=",rc)
            self.connected_flag=True #Flag to indicate success
            self.sending()
        else:
            print("Bad connection Returned code=",rc)
            self.bad_connection_flag=True

    def satisfied(self):
        self.arr0.append(1)
        self.sending()
        ThankYouWindow()

    def not_bad(self):
        self.arr0.append(2)
        self.sending()
        ThankYouWindow()
        
    def bad(self):
        self.arr0.append(3)
        self.sending()
        ThankYouWindow()

class FeedbackUI:
    def __init__(self,):
        self.request = MQTTClient()
        self.arr0 = []
        self.root = Tk()
        self.root.geometry("1024x768")
        self.root.title("Feedback Page")
        self.root.config(background="#000000")
        self.root.attributes('-fullscreen', True)
        self.root.config(cursor="none")
        
        self.label_top = Label(
            self.root,
            text='Dear visitor, we care about your opinion! \n How was your experience today?',
            bg='black',
            fg='white',
            font=("Arial", 25)
        )

        self.label_top.place(
            relx=0.5,
            rely=0.0,
            anchor='n'
        )

        self.photo = PhotoImage(file=r"/home/group5/Desktop/Satisfied-1-removebg-preview.png")
        toggleButton1 = Button(
            self.root,
            image=self.photo,
            bg='black',
            highlightthickness=0,
            bd=0,
            command=self.request.satisfied,
            activebackground='#000000'
        )
        toggleButton1.place(x=25, y=150)

        self.photo1 = PhotoImage(file=r"/home/group5/Desktop/notBad-2-removebg-preview.png")
        toggleButton2 = Button(
            self.root,
            image=self.photo1,
            bg='black',
            highlightthickness=0,
            bd=0,
            command=self.request.not_bad,
            activebackground='#000000'
        )
        toggleButton2.place(x=295, y=150)

        self.photo2 = PhotoImage(file=r"/home/group5/Desktop/Unsatisfied-3-removebg-preview.png")
        toggleButton3 = Button(
            self.root,
            image=self.photo2,
            bg='black',
            highlightthickness=0,
            bd=0,
            command=self.request.bad,
            activebackground='#000000'
        )
        toggleButton3.place(x=550, y=150)

        self.root.mainloop()

class ThankYouWindow:
    def __init__(self):
        self.thx = Tk()
        self.thx.geometry("1024x768")
        #self.thx.config(background= "#000000")
        self.thx.config(cursor="none")

        self.label = Label(self.thx,
                                text = 'Thank you for the feedback!', bg= 'black', fg= 'white',font=("Arial", 25))

        self.label.place(relx = 0.5,
                        rely= 0.5,
                        anchor= 'center') 

        self.thx.attributes('-fullscreen', True) 
        #self.thx.after(3000,lambda:self.thx.destroy())

MQTTClient()
FeedbackUI()
