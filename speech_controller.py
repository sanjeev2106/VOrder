from speaker_training import Trainer
from tkinter import Tk, Label, Button
import speech_recognition as sr
import threading
import os
import speech

training_text = '''\n
Banarsidas Chandiwala Institute of Information Technology 
was established in 1999 to run Three-Year Master of Computer Application programme. 
The Institute is affiliated with Guru Gobind Singh Indraprastha University, Delhi 
for awarding the degree and is approved by the 
All India Council of Technical Education, Ministry of HRD, Government of India.
The Institute is established under the aegis of Sri Banarsidas Chandiwala Sewa Smarak Trust Society, 
a charitable Society working in the field of health and education since 1952. 
'''

class Speech_Controller:
    user_input = None
    runnnigStatus = False
    modelPath = r'C:/VOrder/sys/speaker_model'
    audioPath = r'C:/VOrder/sys/speaker_model/audio_clip'
    modelCounter  = None
    trainingIsGoingOn = True

    def __init__(self, master):
        self.master = master
        self.master.iconbitmap(r'E:\python_project\icon.ico')
        if not os.path.exists(Speech_Controller.audioPath):
            os.makedirs(Speech_Controller.audioPath)

        w = 260  # width for the Tk root
        h = 50  # height for the Tk root
        # get screen width and height
        ws = self.master.winfo_screenwidth()  # width of the screen
        hs = self.master.winfo_screenheight()  # height of the screen
        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 28) - (h / 2)
        # set the dimensions of the screen and where it is placed
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.button = Button(master, text="Start Lisetning", width=17, state = "active", height=3, command=self.changeStatus)
        self.button.pack(side="left")
        self.buttonTrn = Button(master, text="Start Training", width=18, state = "active", height=3, command=self.startTrainSpeaker)
        self.buttonTrn.pack(side="right")
        self.master.resizable(width=False, height=False)
        self.myThread = threading.Thread(target=self.recordAudio)
        self.myThread.start()

    def startTrainSpeaker(self):
        if Speech_Controller.runnnigStatus:
            Speech_Controller.runnnigStatus = False
            self.master.title('Off')
            self.button.config(text='Start Listening')
        dirs = [d for d in os.listdir(Speech_Controller.modelPath) if
                os.path.isdir(os.path.join(Speech_Controller.modelPath, d))]
        Speech_Controller.modelCounter = len(dirs)
        if Speech_Controller.modelCounter == 1:
            Speech_Controller.modelCounter = 1
        else:
            Speech_Controller.modelCounter = int(dirs[-2])+1
            #Speech_Controller.modelCounter += 1
        self.button.config(state='disabled')
        self.buttonTrn.config(state='disabled')
        self.trainingThread = threading.Thread(target=self.trainSpeaker)
        self.trainingThread.start()

    def trainSpeaker(self):
        print("Have you done Speaker Training...?(y/n): ")
        speech.say("Have you done Speaker Training?")
        trainedAlready = raw_input()
        while not trainedAlready == 'y' or not trainedAlready == 'n':
            if trainedAlready == 'n':
                print'Please enter name of the Trainer: '
                speech.say("Please enter name of the Trainer")
                trainerName = raw_input()
                path = os.path.join(Speech_Controller.modelPath + '/' + str(Speech_Controller.modelCounter) + '/' + trainerName)   #path................
                if not os.path.exists(path):
                    os.makedirs(path)
                break
            elif trainedAlready == 'y': # not completed this module
                break
            else:
                print"Please reply only 'y' or 'n': "
                trainedAlready = raw_input()

        global training_text
        print training_text
        print'Please read-out the above paragraph to create your speaker model'
        speech.say('Please read-out the above paragraph to create your speaker model')

        i = 0;
        while True:
            i += 1
            saveAaudioPath = os.path.join(Speech_Controller.audioPath+'/audio' +str(i)+'.wav')
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source)
            data = None
            try:
                data = r.recognize_google(audio)
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print"Check your internet connection..."
            if data is not None:
                with open(saveAaudioPath, "wb") as f:
                    f.write(audio.get_wav_data())
            if data and 'since 1952' in data:
                #self.button.config(state='normal')
                #self.buttonTrn.config(state='normal')
                print'Training is completed\nPlease wait untill prepared speaker model....'
                speech.say('Training is completed\nPlease wait untill prepared speaker model')
                try:
                    self.trainingThread._Thread__stop()
                    #print'thread stopped'
                except:
                    print'Error to stop the thread'
                trainerOB = Trainer()
                trainerOB.createModel(path+'/')
                self.button.config(state='normal')
                self.buttonTrn.config(state='normal')
                break

    def changeStatus(self):
        if not Speech_Controller.runnnigStatus:
            Speech_Controller.runnnigStatus = True
            self.master.title('Listening...')
            self.button.config(text='Stop')
        else:
            Speech_Controller.runnnigStatus = False
            self.master.title('Off')
            self.button.config(text='Start Listening')
            #try:
                #self.myThread._Thread__stop()
                #print 'Waiting to stop..'
                #time.sleep(3)
                #print 'Stopped'
                #print Speech_Controller.myThread.isAlive()
                # except:
            #    print 'Error to stop'

    def recordAudio(self):
        while True:
            if Speech_Controller.runnnigStatus:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    audio = r.listen(source)
                try:
                    if Speech_Controller.runnnigStatus:
                        Speech_Controller.user_input = r.recognize_google(audio)
                        print"You: " + Speech_Controller.user_input
                except sr.UnknownValueError:
                    pass
                    #Speech_Controller.user_input = self.recordAudio()
                except sr.RequestError as e:
                    print"Check your internet connection..."
                    speech.say("Check your internet connection")
#if __name__ == '__main__':
   # root = Tk()
   # window = Speech_Controller(root)
    #root.mainloop()