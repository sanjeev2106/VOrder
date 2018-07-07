#------------Importing libraries or modules--------------------
import speech_controller
from speech_controller import *
from Tkinter import *
import Tkinter as tk
import os.path
#import speech
import speech_recognition as sr
import threading
import re
##########################################################
def Main():
# ------------------------Editor Window-----------------------------
    ROOT = Tk()
    ROOT.title("VOrder")
    ROOT.iconbitmap(r'E:\python_project\icon.ico')
    ROOT.attributes('-alpha', 0.9)
    txt = Text(ROOT, bg='Dark Slate Gray', fg='white')
    vsb = tk.Scrollbar(orient="vertical", command=txt.yview)
    txt.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    txt.pack(side="left", fill="both", expand=True)
    menu = Menu(ROOT)
    ROOT.config(menu=menu)

    filemenu = Menu(menu)
    menu.add_cascade(label="File", menu=filemenu)

    editmenu = Menu(menu)
    menu.add_cascade(label="Edit", menu=editmenu)

    helpmenu = Menu(menu)
    menu.add_cascade(label="Help", menu=helpmenu)

    aboutmenu = Menu(menu)
    menu.add_cascade(label="About", menu=aboutmenu)

    w = 760  # width for the Tk root
    h = 370  # height for the Tk root

    # get screen width and height
    ws = ROOT.winfo_screenwidth()  # width of the screen
    hs = ROOT.winfo_screenheight()  # height of the screen
    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (w / 2)
    y = (hs / 2.9) - (h / 2)

    # set the dimensions of the screen and where it is placed
    ROOT.geometry('%dx%d+%d+%d' % (w, h, x, y))
####################################################################

    APP = App(ROOT, txt) # creating object of class or calling class constructor

# toplevel window for voice controller
    win = tk.Toplevel(ROOT)
    win.title("Off")
    win.attributes('-alpha', 0.9)
    Speech_Controller(win)
###################################################################

    ROOT.mainloop() # loop to show editor window
    ROOT.destroy()  # To destroy all window
###################################################################

class App(threading.Thread):
#-------Class Variables declaration and Initialization------------
    loop_active = True
    fileSaved = True
    isTempFile = True
    fname = None
    fst_st_pos = None
    scnd_ed_pos = None
    copiedText = None
    current_text = None
    textSelected = False
    checkTempFile = r'C:/VOrder/sys/temp.txt'
    myPath = r'C:/VOrder'
    tempFilePath = r'C:/VOrder/sys'
######################################################################
#-------------Checking and creating defalt path for file location------------------
    if not os.path.exists(tempFilePath):
        os.makedirs(tempFilePath)
#######################################################################
#----constructor of the 'App' class, used for initialization and start the run function----------
    def __init__(self, tk_root, w):
        #print("thread ", threading._get_ident())
        #self.ui_queue = Queue()
        self.txt = w
        self.root = tk_root

        threading.Thread.__init__(self)
        self.start()

        #print("thread ", threading._get_ident())

###########################################################################
#----function to check, is the user was unable to save last file before closing of application-------
    def checkTempFileExistence(self):
        if os.path.exists(App.checkTempFile):
            print"You are unable to save last file, do you want to retrive?"
            #speech.say("You are unable to save last file, do you want to retrive?")
            while True:
                if Speech_Controller.user_input:
                    if Speech_Controller.user_input == 'yes':
                        Speech_Controller.user_input = None
                        file = open(App.checkTempFile,'r')
                        if file is not None:
                            contents = file.read()
                            self.txt.insert('1.0', contents)
                            file.close()
                            App.fileSaved = False
                            break
                    elif Speech_Controller.user_input == 'no':
                        Speech_Controller.user_input = None
                        os.remove(App.checkTempFile)
                        break
                    else:
                        if 'yes' or 'no' not in Speech_Controller.user_input:
                            print 'Reply yes or no'
                        #speech.say('Reply yes, or no')
                        Speech_Controller.user_input = None
##################################################################################
#/\/\/\//\/\/\/\/\/\//\/\//\//\/\/\/\/\//\/\/\/\\//\/\/\/\\//\\/\//\/\/\\//\/\
##    def recordAudio(self):
##        print 'Listening...'
##        r = sr.Recognizer()
##        with sr.Microphone() as source:
##            audio = r.listen(source)     
##        data = None
##        try:
##            data = r.recognize_google(audio)
##            print"You: " + data
##        except sr.UnknownValueError:
##            #print"unable understanding"
##            data = self.recordAudio()
##        except sr.RequestError as e:
##            print"Check your internet connection..."
##            speech.say("Check your internet connection")
##        finally:
##            while data is None:
##                data = self.recordAudio()
##            return data
#/\/\/\/\/\/\/\/\//\\/\/\/\/\/\/\/\/\//\/\\///\/\/\/\\//\/\\/\//\/\/\/\/\/\
#########################################################################
#----------function to open the existing file------------------------
    def open_file(self):
        Speech_Controller.user_input = None
        if App.fileSaved:
            App.fname = None
            myPath = r'C:/VOrder'
            print("Tell me name of the file to be open..")
            #speech.say("Tell me name of the file to be open..")
            #App.fname = Speech_Controller.user_input
            while not App.fname:
                App.fname = Speech_Controller.user_input
            Speech_Controller.user_input = None
            try:
                path = os.path.join(myPath+'/'+App.fname+'.txt')
                file = open(path,'r')
                if file is not None:
                    contents = file.read()
                    self.txt.delete('1.0', END)
                    self.txt.insert('1.0', contents)
                    file.close()
                    self.deselect_text()
                    print(App.fname+".txt file has opened")
                    #speech.say(App.fname+".txt file has opened")
                    #App.currrentFname = App.fname

                    Speech_Controller.user_input = None
            except (OSError, IOError) as e:
                print("File '"+App.fname+"' not found")
                #speech.say("File '"+App.fname+"' not found")

        if not App.fileSaved:
            data = self.txt.get('1.0', END + '-1c')
            if data:
                print("File is not saved, Do you want to save??(yes/no)...")
                #speech.say("File is not saved, Do you want to save??")
                while True:
                    if Speech_Controller.user_input:
                        cnf = Speech_Controller.user_input
                        Speech_Controller.user_input = None
                        if cnf == 'yes':
                            self.save_file()
                            self.open_file()
                            break
                        elif cnf == 'no':
                            if os.path.exists(App.checkTempFile):
                                os.remove(App.checkTempFile)
                            App.fileSaved = True
                            self.open_file()
                            break
                        else:
                            print 'Reply me yes or no'
                            #speech.say('Reply me yes, or no')
            else:
                App.fileSaved = True
                self.open_file()
##############################################################################
#-------function to close the application------------------------------
    def close_file(self):
        if App.fileSaved:
            App.loop_active = False
            self.root.update()
            if os.path.exists(App.checkTempFile):
                os.remove(App.checkTempFile)
            self.root.quit()
            
        if not App.fileSaved:
            data = self.txt.get('1.0', END + '-1c')
            if data:
                print("File is not saved, Do you want to save??(yes/no)...")
                #speech.say("File is not saved, Do you want to save??")
                while True:
                    if Speech_Controller.user_input:
                        cnf = Speech_Controller.user_input
                        Speech_Controller.user_input = None
                        if cnf == 'yes':
                            self.save_file()
                            self.close_file()
                            break
                        elif cnf == 'no':
                            App.fileSaved = True
                            self.close_file()
                            break
                        else:
                            print 'Reply me yes or no'
                            #speech.say('Reply me yes, or no')
            else:
                App.fileSaved = True
                self.close_file()
#################################################################################
#--------function to save the file on hard-disk--------------------------------
    def save_file(self):
        Speech_Controller.user_input = None
        if App.fname:
            data = self.txt.get('1.0', END + '-1c')

            path = os.path.join(App.myPath + '/' + App.fname + '.txt')

            file = open(path,'w')
            file.write(data)
            file.close()
            App.fileSaved = True  
                
        elif App.fname is None:
            print("Tell me name to save this file..")
            #speech.say("Tell me name to save this file..")
            while not App.fname:
                App.fname = Speech_Controller.user_input
            Speech_Controller.user_input = None
            data = self.txt.get('1.0', END + '-1c')
            path = os.path.join(App.myPath+'/'+App.fname+'.txt')
            if not os.path.exists(path):
                file = open(path,'w')
                file.write(data)
                file.close()                
            else:
                print"File "+App.fname+".txt already exists, Do you want to replace?"
                #speech.say("File "+App.fname+".txt already exists, Do you want to replace?")
                while True:
                    if Speech_Controller.user_input:
                        ans = Speech_Controller.user_input
                        Speech_Controller.user_input = None
                        if ans == "yes":
                            file = open(path,'w')
                            file.write(data)
                            file.close()
                            break
                        elif ans == 'no':
                            App.fname = None
                            self.save_file()
                            break
                        else:
                            print 'Reply me yes or no'
                            #speech.say('Reply me yes, or no')
            App.fileSaved = True

            if os.path.exists(App.checkTempFile):
                os.remove(App.checkTempFile)

        else:
            print("failed to save..")
            #speech.say("failed to save..")
#################################################################################
#-------function which helps user to know all the commands of it---------------------
    def help_box(self):
        commands = ''' The following are commands of the VOrder.
             NEW, To open new empty file.
             OPEN, To open an existing file.
             SAVE, To save the file.
             CLOSE, To close the opened file.
             FIND, To search or find any text.
             SELECT, To select some text.
             SELECT ALL, To select the all text.
             DESELECT, To unselect the selected text.
             DELETE, To delete the selected text or current written text.
             COPY, To copy the selected text.
             CUT, To cut the selected text.
             PASTE, To paste the cut or copied text.
             CLEAR, To delete all contents of editor.
             READ, To listen the written text.
             ABOUT, To know abot editor.
             HELP, To know the commands of VOrder.
'''
        
        print'''
                  Command     |     Operation
                 ----------------------------------------------------
                  NEW         |     For new empty file
                  OPEN        |     To open an existing file
                  SAVE        |     To save the content of file
                  CLOSE       |     To close the open file
                  FIND        |     To search or find a word
                  SELECT      |     To select the group of words
                  SELECT ALL  |     To select entire text
                  DESELECT    |     To unselect the selected words
                  DELETE      |     To delete the selected text or
                              |     current written text.
                  COPY        |     To copy the selected text
                  CUT         |     To cut the selected text
                  PASTE       |     To paste the copy/cut text
                  CLEAR       |     To delete all contents of editor
                  REPLACE     |     To replace a word with other
                  ABOUT       |     To know abot editor

                  NOTE: 'VOrder' open initially with writing mode,
                         Speek to write anything.
        '''
        #speech.say(commands)
###################################################################################
#------function of small description about VOrder-------------------------------
    def about(self):
        about = '''
                'VOrder' is a editor with normal operations
                (like: open, save, close, find, delete, copy, cut, paste).
                'VOrder' is based on SPEECH RECOGNITION SYSTEM, control by
                 Human voice.                
    '''
        print(about)
        #speech.say(about)
####################################################################################
#------------function to open new file--------------------------------------------
    def new_file(self):
        Speech_Controller.user_input = None
        if App.fileSaved:
            self.txt.delete('1.0', END)
            self.deselect_text()
            App.fname = None
            print('Untitled new file opened')
        if not App.fileSaved:
            data = self.txt.get('1.0', END + '-1c')
            if data:
                print("File is not saved! Do you want to save??(yes/no)...")
                #speech.say("File is not saved! Do you want to save??")
                while True:
                    if Speech_Controller.user_input:
                        cnf = Speech_Controller.user_input
                        Speech_Controller.user_input = None
                        if cnf == 'yes':
                            self.save_file()
                            self.new_file()
                            break
                        elif cnf == 'no':
                            if os.path.exists(App.checkTempFile):
                                os.remove(App.checkTempFile)
                            App.fileSaved = True
                            self.new_file()
                            break
                        else:
                            print 'Reply me yes or no'
                            #speech.say('Reply me yes, or no')
            else:
                App.fileSaved = True
                self.new_file()
#################################################################################
#-------------function to replace any text to another--------------------------
    def replace(self):
        Speech_Controller.user_input = None
        data = self.txt.get('1.0', END+'-1c')
        from_word = to_word = None
        if data:
            print"say word to be replace"
            #speech.say("say word to be replace")
            while not to_word:
                to_word = Speech_Controller.user_input
            Speech_Controller.user_input = None
            if to_word in data:
                print"say word by which "+to_word+" is replace"
                #speech.say("say word by which "+to_word+" is replace")
                while not from_word:
                    from_word = Speech_Controller.user_input
                Speech_Controller.user_input = None
                data = data.replace(to_word,from_word)
                self.txt.delete('1.0', END)
                self.txt.insert(END, data)
                App.fileSaved = False
                self.fileUpdater()
                print(to_word+" is replaced by "+from_word)
                #speech.say(to_word+" is replaced by "+from_word)
            else:
                print"Sorry! "+to_word+" is not found"
                #speech.say("Sorry! "+to_word+" is not found")
        else:
            print"sorry! file is empty"
            #speech.say("sorry! file is empty")
##############################################################################
    def selectAll(self):
        Speech_Controller.user_input = None
        data = self.txt.get('1.0', END+'-1c')
        if data:
            self.txt.tag_add("start", '1.0', '1.' + END)
            self.txt.tag_config("start", background="Light Blue", foreground="black")
            App.fst_st_pos = 0
            App.scnd_ed_pos = len(data)
            App.textSelected = True
        else:
            print"Sorry! file is empty, nothing to select"
            #speech.say("Sorry! file is empty, nothing to select")
##################################################################################
#-------------helping function for 'select' and 'find' the text-------------------
    def get_pos(self, w, name):
        word = w
        funName = name
        cnf = None
        data = self.txt.get('1.0', END + '-1c')
        if re.search(word, data, re.IGNORECASE):            
            starts = ([x.start() for x in re.finditer(word, data, re.IGNORECASE)])
            ends = ([x.end() for x in re.finditer(word, data, re.IGNORECASE)])            
            i=0
            s_pos = starts[i]
            e_pos = ends[i]                
            try:
                while(i <= len(starts)):
                    #Speech_Controller.user_input = None
                    cnf = None
                    if funName is None:
                        self.txt.tag_add("start", '1.' + str(s_pos), "1." + str(e_pos))
                        self.txt.tag_config("start", background="Light Blue", foreground="black")
                    if funName == "select":
                        self.txt.tag_add("start", '1.' + str(App.fst_st_pos), "1." + str(e_pos))
                        self.txt.tag_config("start", background="Light Blue", foreground="black")
                    if len(starts) == 1:
                        cnf = 'ok'
                    if len(starts) > 1:  
                        print("say 'ok' if you got word else 'next'")
                        #speech.say("say 'ok' if you got word else 'next'")
                        while not cnf:
                            cnf = Speech_Controller.user_input
                        Speech_Controller.user_input = None
                    if cnf == "next":
                        i += 1
                        data = data.replace(word,word)
                        self.txt.delete('1.0', END)
                        self.txt.insert(END, data)
                        s_pos = starts[i]
                        e_pos = ends[i]
                        Speech_Controller.user_input = None
                    if cnf == "ok":
                        return s_pos, e_pos
                else:
                    if funName == "select":
                        self.txt.tag_add("start", '1.' + str(App.fst_st_pos), "1." + str(e_pos))
                        self.txt.tag_config("start", background="Light Blue", foreground="white")
                        print("No more matches found...") 
                        #speech.say("No more matches found...")
                        return starts[i-1], ends[i-1]
                    if funName is None:
                        print("No more matches found...") 
                        #speech.say("No more matches found...")
                        return None, None
            except IndexError as e: 
                if funName == "select":
                    self.txt.tag_add("start", '1.' + str(App.fst_st_pos), "1." + str(e_pos))
                    self.txt.tag_config("start", background="Light Blue", foreground="white")
                    print("No more matches found...") 
                    #speech.say("No more matches found...")
                    return starts[i-1], ends[i-1]
                if funName is None:
                    print("No more matches found...") 
                    #speech.say("No more matches found...")
                    return None, None
        else:
            print("No matches found for '"+word+"'")
            #speech.say("No matches found for '"+word+"'")
            return None, None
######################################################################
#-------------function to select the text--------------------------------
    def select(self):
        Speech_Controller.user_input = None
        data = self.txt.get('1.0', END + '-1c')

        if data:
            print("Tell me starting word...")
            word = None
            #speech.say("Tell me starting word")
            while not word:
                word = Speech_Controller.user_input
            Speech_Controller.user_input = None
            self.deselect_text()
            App.fst_st_pos, fst_ed_pos = self.get_pos(word, None)
            if App.fst_st_pos is not None:
                print("Tell me ending word...")
                word = None
                #speech.say("Tell me ending word")
                while not word:
                    word = Speech_Controller.user_input
                Speech_Controller.user_input = None
                scnd_st_pos, App.scnd_ed_pos = self.get_pos(word, "select")
                App.textSelected = True
        if data is None:
            print("File is empty...")
            #speech.say("File is empty...")
#######################################################################################
#--------------function to delete selected text or current written text--------------------
    def delete_text(self):
        data = self.txt.get('1.0', END + '-1c')
        if App.scnd_ed_pos is None:
            if App.current_text is not None:
                dataLen = len(data) - App.current_text
                data = data[ : dataLen]
                self.txt.delete('1.0', END)
                self.txt.insert(END, data)
                App.current_text = None
            else:
                print"There is no selected text, first select the text to delete!"
                #speech.say("There is no selected text, first select the text to delete!")
        if App.scnd_ed_pos is not None:
            data = data[:App.fst_st_pos] + data[(App.scnd_ed_pos + 1):]
            self.txt.delete('1.0', END)
            self.txt.insert('1.0', data)
            print"Selected text are deleted"
            #speech.say("Selected text are deleted")
            App.scnd_ed_pos = None
            App.fst_st_pos = None
        self.fileUpdater()
########################################################################
#--------function to copy selected text----------------------------------
    def copy_text(self):
        if App.scnd_ed_pos is None:
            print"There is no selected text, first select the text to copy!"
            #speech.say("There is no selected text, first select the text to copy!")
        if App.scnd_ed_pos is not None:
            data = self.txt.get('1.0', END + '-1c')
            App.copiedText = data[App.fst_st_pos:(App.scnd_ed_pos + 1)]
            print"Selected text are copied !"
            #speech.say("Selected text are copied !")
########################################################################
#----------function to paste the copied or cutted text----------------
    def paste_text(self):
        Speech_Controller.user_input = None
        if App.copiedText is not None:
            data = self.txt.get('1.0', END + '-1c')
            speek = '''Say 'START' to paste at starting position,
            Else tell me that word after you have to paste!'''
            if data:
                print speek
                #speech.say(speek)
                word = None
                while word is None:
                    word = Speech_Controller.user_input
                Speech_Controller.user_input = None
                self.deselect_text()
                if word == 'start':
                    self.txt.insert('1.0', App.copiedText)
                else:
                    sp,ep = self.get_pos(word,None)
                    if ep:
                        self.txt.insert('1.' + str(ep), ' ' + App.copiedText)
            else:
                self.txt.insert('1.0', App.copiedText)
            self.fileUpdater()
            App.current_text = len(App.copiedText)
        else:
            print"There is no copied text, First copy the text"
            #speech.say("There is no copied text, First copy the text")
#########################################################################
#---------function to cut the selected text----------------------------------
    def cut_text(self):
        if App.scnd_ed_pos is None:
            print"There is no selected text, first select the text to cut!"
            #speech.say("There is no selected text, first select the text to cut!")
        if App.scnd_ed_pos is not None:
            data = self.txt.get('1.0', END + '-1c')
            App.copiedText = data[(App.fst_st_pos):(App.scnd_ed_pos+1)]
            data = data[:(App.fst_st_pos)] + data[(App.scnd_ed_pos+1):]
            self.txt.delete('1.0', END)
            self.txt.insert('1.0', data)
            self.fileUpdater()
            print"Selected text are cutted !"
            #speech.say("Selected text are cutted !")
############################################################
#--------function to desect the all selected text-------------
    def deselect_text(self):
        data = self.txt.get('1.0', END + '-1c')
        self.txt.delete('1.0', END)
        self.txt.insert(END,data)
        App.textSelected = False
        App.fst_st_pos = None
        App.scnd_ed_pos = None
##########################################################
#---------function to find or search text in file---------------
    def find_text(self):
        Speech_Controller.user_input = None
        data = self.txt.get('1.0', END+'-1c')
        if data:
            print("Tell me word to find...")
            word = None
            #speech.say("Tell me word to find...")
            while word is None:
                word = Speech_Controller.user_input
            Speech_Controller.user_input = None
            self.deselect_text()
            sp,ep = self.get_pos(word, None)
        if data is None:
            print("File is empty...")
            #speech.say("File is empty...")
###########################################################
#-----------Function to update the file---------------------
    def fileUpdater(self):
        data = self.txt.get('1.0', END + '-1c')
        if App.fname is None:
            file = open(App.checkTempFile,'w')
            file.write(data)
            file.close()
            App.fileSaved = False
        else:
            self.save_file()
#############################################################
#----function to write text to editor----------------------
    def textWrite(self, user_input):
        if App.textSelected:
            self.deselect_text()
            self.txt.insert(END,user_input+" ")
        else:    
            self.txt.insert(END,user_input+" ")
        App.current_text = len(user_input+" ")
        self.fileUpdater()
        #self.root.update.title(App.fname)
###########################################################

    def run(self):
        #print("thread ", threading._get_ident())

        self.checkTempFileExistence()
##        print 'Tell me something'
##        print"Say 'help' anytime to view all the commands..."
##        speech.say("say 'help' anytime to view the all commands")
##        self.help_box()
##        threading.MainThread.ROOT.title('hii')
        while App.loop_active:
            if Speech_Controller.user_input:
                #print"Tell me something..."
                #speech.say("Tell me something...")
                #user_input = self.recordAudio()

                if Speech_Controller.user_input == "open":
                    Speech_Controller.user_input = None
                    self.open_file()

                elif Speech_Controller.user_input == "find":
                    self.find_text()

                elif Speech_Controller.user_input == "close":
                    self.close_file()

                elif Speech_Controller.user_input == "save":
                    self.save_file()
                    print("File saved successfully as '" + App.fname + ".txt'")
                    #speech.say("File saved successfully as '"+App.fname+".txt'")

                elif Speech_Controller.user_input == "help":
                    self.help_box()

                elif Speech_Controller.user_input == "about":
                    self.about()

                elif Speech_Controller.user_input == "clear":
                    self.txt.delete('1.0', END)
                    self.fileUpdater()

                elif Speech_Controller.user_input == 'new':
                    self.new_file()

                elif Speech_Controller.user_input == 'read':
                    data = self.txt.get('1.0', END+'-1c')
                    #if data:
                        #speech.say(data)
                    #else:
                        #speech.say("sorry file is empty")

                elif Speech_Controller.user_input == 'select':
                    self.select()

                elif Speech_Controller.user_input == 'select all':
                    self.selectAll()

                elif Speech_Controller.user_input == 'deselect':
                    self.deselect_text()

                elif Speech_Controller.user_input == 'replace':
                    self.replace()

                elif Speech_Controller.user_input == 'delete':
                    self.delete_text()

                elif Speech_Controller.user_input == 'copy':
                    self.copy_text()

                elif Speech_Controller.user_input == 'paste':
                    self.paste_text()

                elif Speech_Controller.user_input == 'cut':
                    self.cut_text()

                else:
                    self.textWrite(Speech_Controller.user_input)

                Speech_Controller.user_input = None

#--------Starts the programm--------
if __name__ == '__main__':
    Main()
#----------------------------