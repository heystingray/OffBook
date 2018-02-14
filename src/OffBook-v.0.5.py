from tkinter import *
import os, shutil, glob
import pyaudio, wave, winsound
import time
import random
import ttk


class OffBook():

    #what the app does when first opened
    def __init__(self,master):

        self.build_widgets(master)  #first builds windows

        self.tk = master    #reference for the Tk instance


    #function to open a scene by selecting it's directory
    def open(self):
        os.chdir(r'C:\OffBook\Scenes')

        self.scene=filedialog.askdirectory(title='Open Scene',
                                           parent=self.tk,
                                           mustexist=True)

        os.chdir(self.scene)

        self.tk.title('OffBook- '+ os.path.basename(self.scene))

        self.refresh()

    #creates prompt to name new scene, scene created once user presses OK button
    def new(self):

        self.new_prompt=Toplevel(self.tk)
        self.new_prompt.title('New')

        new_label=Label(self.new_prompt,
                        text='Name of new scene:')
        new_label.pack(side=TOP)

        self.new_entry=Entry(self.new_prompt)
        self.new_entry.pack(side=TOP, fill=X)

        new_button=Button(self.new_prompt,
                          text='OK',
                          command=self.create_new)
        new_button.pack(side=TOP)

        self.new_prompt.focus()

    #creates a new, empty scene and it's corresponding directory
    def create_new(self):

        if self.new_entry.get()!='':

            os.chdir(r'C:\OffBook\Scenes')

            os.mkdir(self.new_entry.get())

            os.chdir(self.new_entry.get())

            self.scene=self.new_entry.get()

            self.tk.title('Offbook-'+self.new_entry.get())

            self.refresh()

            self.new_prompt.destroy()

    #function to build app window with tkinter
    def build_widgets(self,master):

        master.title('OffBook')



        #menu
        menubar=Menu(master)

        menubar.add_command(label='New',command=self.new)
        menubar.add_command(label='Open', command=self.open)
        menubar.add_command(label='Import', command=self.get_characters)

        master.config(menu=menubar)

        #frame for practice menu on left side
        self.practice_menu=LabelFrame(master,
                                      text='Practice',
                                      padx=10,
                                      pady=10)
        self.practice_menu.pack(fill=BOTH, side=LEFT,)

        #role frame
        role_f= Frame(self.practice_menu)
        role_f.pack(side=TOP,
                    pady=10,
                    expand=1)

        #'Role:' label
        role_l= Label(role_f, text='Role:')
        role_l.pack(side=LEFT)

        #role selection combobox
        self.rolevar = StringVar()
        role_combobox = ttk.Combobox(role_f, textvariable=self.rolevar)

        role_combobox.pack(side=LEFT)

        self.character_options=[]

        #'from the top' button
        self.from_the_top_button= Button(self.practice_menu,
                                  text='FROM \nTHE TOP',
                                  height=6,
                                  width=40,
                                  bg='green',
                                  fg='white',
                                    command=self.from_the_top)
        self.from_the_top_button.pack(side=TOP,
                               fill=Y,
                               expand=1)

        #'from selected' button
        self.from_selected_button= Button(self.practice_menu,
                                  text='FROM \nSELECTED',
                                  height=6,
                                  width=40,
                                   bg='green',
                                  fg='white',
                                          command=self.from_selected)
        self.from_selected_button.pack(side=TOP,
                                fill=Y,
                                pady=50,
                                expand=1)

        #'random cues' button
        self.random_cues_button= Button(self.practice_menu,
                                 text='RANDOM \nCUES',
                                 height=6,
                                 width=40,
                                 bg='purple',
                                  fg='white',
                                        command=self.random_cues)
        self.random_cues_button.pack(side=TOP,
                              fill=Y,
                              expand=1)

        #paned window to hold script and bottom part
        self.base=PanedWindow(master,
                         orient=VERTICAL,
                         sashrelief=SUNKEN)

        self.base.pack(fill=BOTH, expand=1, side=LEFT)

        #script frame
        script_f= Frame(self.base)
        self.base.add(script_f)

        #listbox to become script
        self.script = Listbox(script_f,
                              width=120,
                              height=20,
                              activestyle=DOTBOX,)
        self.script.pack(side=LEFT, fill=BOTH, expand=1)

        #script scrollbar
        script_scrollbar= Scrollbar(script_f,
                                    command=self.script.yview)
        script_scrollbar.pack(side=LEFT,
                              fill=Y,
                              )
        self.script.config(yscrollcommand=script_scrollbar.set)

        #second paned window to hold bottom part
        self.bottombase=Frame(self.base)
        self.base.add(self.bottombase)

        #frame for line input
        self.line_input= Frame(self.bottombase)
        self.line_input.pack(side=LEFT, fill=BOTH, expand=1)

        self.line_input_top= Frame(self.line_input)
        self.line_input_top.pack(side=TOP, fill=X)

        self.line_input_bottom= Frame(self.line_input)
        self.line_input_bottom.pack(side=TOP,
                                 fill=BOTH,
                                 expand=1)

        #"Speaker:" label
        speaker_l= Label(self.line_input_top, text='Speaker:')
        speaker_l.pack(side=LEFT)

        #speaker entry

        self.speaker_entry= Entry(self.line_input_top,
                                  width=30,
                                  )
        self.speaker_entry.pack(side=LEFT, fill=X, expand=1)

        #enter button
        self.enter_button=Button(self.line_input_top,
                                 text='Enter',
                                 bg='green',
                                 fg='white',
                                 command=self.enter_line)

        self.enter_button.pack(side=LEFT)

        #new line text holder
        self.line_text= Text(self.line_input_bottom,
                             width=50,
                             height=10)
        self.line_text.pack(side=LEFT, fill=BOTH, expand=1)


        #new line text scrollbar
        line_text_scrollbar= Scrollbar(self.line_input_bottom,
                                    command=self.line_text.yview)
        line_text_scrollbar.pack(side=LEFT,
                              fill=Y,
                              )
        self.line_text.config(yscrollcommand=line_text_scrollbar.set)


        #frame for control buttons
        self.controlboard= Frame(self.bottombase)
        self.controlboard.pack(side=LEFT,
                               )

        self.audio_options= LabelFrame(self.controlboard,
                                    text='Audio')
        self.audio_options.pack(side=TOP)

        self.line_options= LabelFrame(self.controlboard,
                                    text='Options')
        self.line_options.pack(side=TOP)

        #audio buttons
        self.var=IntVar()
        self.record_button=Checkbutton(self.audio_options,
                                   text="Record",
                                   fg='red',
                                   variable=self.var,
                                   command=self.record,
                                   indicatoron=False)
        self.record_button.pack(side=LEFT)

        self.play_button=Button(self.audio_options, text='Play',
                                command=self.play)
        self.play_button.pack(side=LEFT)

        self.clear_button=Button(self.audio_options, text='Clear',
                                 command=self.clear)
        self.clear_button.pack(side=LEFT)

        #option buttons

        self.line_down_button=Button(self.line_options, text='Line Down',
                                     command=self.line_down)
        self.line_down_button.pack(side=LEFT)

        self.line_up_button=Button(self.line_options, text='Line Up',
                                   command=self.line_up)
        self.line_up_button.pack(side=LEFT)

        self.edit_button=Button(self.line_options, text='Edit',
                                command=self.edit)
        self.edit_button.pack(side=LEFT)

        self.delete_button=Button(self.line_options, text='Delete',
                                  command=self.delete_line)
        self.delete_button.pack(side=LEFT)


    #this function was built to practice manipulating pathnames to open files, not actually used in any app functions
    def print_scene_list(self):


        self.line_list= ['Line0','Line1']



        for line in self.line_list:

            speaker_path=line+r'\speaker.txt'

            speaker=open(speaker_path)

            text_path=line+r'\text.txt'

            text=open(text_path)

            for line in  speaker:
                print(line)

            for line in text:
                print(line)

    #function called to update representation of lines in listbox to match the file directory of the scene, called when opening scene and after lines are added, edited, or removed
    def refresh(self):
        self.script.delete(0,END)

        for num in range(1000):

            line='Line'+str(num)

            if os.path.exists(line):
                speaker_path=line+r'\speaker.txt'

                speaker_f=open(speaker_path)

                text_path=line+r'\text.txt'

                text_f=open(text_path)

                for speaker in speaker_f:
                    entry=speaker+': '

                for text in text_f:
                    entry+=text

                self.script.insert(END,entry)

                speaker_f.close()
                text_f.close()
                #print(entry)









    #adds new line to end of script by taking from speaker and text inputs
    def enter_line(self):


        speaker=self.speaker_entry.get()
        text=self.line_text.get(0.0,END)


        place='Line'+str((self.script.index(END)))

        if not os.path.exists(place):
            os.mkdir(place)

        speaker_f=open(place+r'\speaker.txt', 'w')

        speaker_f.write(speaker)

        speaker_f.close()

        text_f=open(place+r'\text.txt', 'w')

        text_f.write(text)

        text_f.close()

        self.speaker_entry.delete(0,END)

        self.line_text.delete(0.0, END)

        self.refresh()


    #deletes selected line from script
    def delete_line(self):
        place='Line'+str(self.script.index(ACTIVE))
        place2='Line'+str(self.script.index(ACTIVE)+1)
        if os.path.exists(place):
            shutil.rmtree(place)

            for num in range(self.script.index(ACTIVE), 1000):          #this loop renames the files to new numerical order after line is removed
                if os.path.exists('Line'+str(num)):
                    os.rename('Line'+str(num), 'Line'+str(num-1))

            self.refresh()
        else:
            print(place, 'does not exist')

    #callback to record audio data
    def callback(self, in_data, frame_count, time_info, status):

        self.frames.append(in_data) #records audio data to list

        return (in_data, pyaudio.paContinue)



    #function called every time record button is pressed
    def record(self):

        place='Line'+str((self.script.index(ACTIVE)))

        #when turned on, it begins the stream
        if self.var.get()==1:

            #put line in text box
            self.line_text.delete(0.0,END)


            text_path=place+r'\text.txt'

            text_f=open(text_path)

            for text in text_f:
                self.line_text.insert(END, text)

            text_f.close()

            #begin recording
            self.p=pyaudio.PyAudio()

            self.frames= []

            self.stream=self.p.open(format=pyaudio.paInt16,
                                    channels=2,
                                    rate=44100,
                                    input=True,
                                    frames_per_buffer=1024,
                                    stream_callback=self.callback)










        #when turned off, it ends the stream, then records audio data from the 'frames' list to a WAVE file
        elif self.var.get()==0 and self.stream.is_active()==True:

            self.line_text.delete(0.0,END)

            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()

            wf = wave.open(place+r'/audio.wav', 'wb')
            wf.setnchannels(2)
            wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.frames))
            wf.close()



        else:

            print('did nothing')

    #plays audio file connected to selected line
    def play(self):

        place='Line'+str((self.script.index(ACTIVE)))

        CHUNK = 1024

        wf = wave.open(place+r'\audio.wav', 'rb')
        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(CHUNK)

        while data != '':
            stream.write(data)
            data = wf.readframes(CHUNK)

        stream.stop_stream()
        stream.close()
        wf.close()

        p.terminate()

    #deletes audio file from selected line
    def clear(self):

        place='Line'+str((self.script.index(ACTIVE)))

        os.remove(place+r'\audio.wav')

    #changes new line input into an edit input, signified by changing of enter button to blue
    def edit(self):

        place='Line'+str((self.script.index(ACTIVE)))
        self.edit_place=place

        if os.path.exists(place):
            self.enter_button.config(bg='blue', command=self.enter_edit)    #changes enter button command and color

            #puts speaker in speaker box
            self.speaker_entry.delete(0,END)

            speaker_path=place+r'\speaker.txt'

            speaker_f=open(speaker_path)

            for speaker in speaker_f:
                self.speaker_entry.insert(0,speaker)

            speaker_f.close()

            #puts line in text box
            self.line_text.delete(0.0,END)

            text_path=place+r'\text.txt'

            text_f=open(text_path)

            for text in text_f:
                self.line_text.insert(END, text)

            text_f.close()

    #function of blue enter button, basically same as normal enter function but entered into the place of the line chosen to be edited
    def enter_edit(self):
        place=self.edit_place

        speaker=self.speaker_entry.get()
        text=self.line_text.get(0.0,END)

        speaker_f=open(place+r'\speaker.txt', 'w')

        speaker_f.write(speaker)

        speaker_f.close()

        text_f=open(place+r'\text.txt', 'w')

        text_f.write(text)

        text_f.close()

        self.speaker_entry.delete(0,END)

        self.line_text.delete(0.0, END)

        self.refresh()

        self.enter_button.config(bg='green', command=self.enter_line)

    #moves selected line down in position relative to other lines once
    def line_down(self):
        anchor=(self.script.index(ANCHOR))
        place='Line'+str(anchor)
        goal='Line'+str(anchor+1)

        if not os.path.exists(goal):
             return

        os.rename(goal,'dummy')
        os.rename(place, goal)
        os.rename('dummy', place)

        self.refresh()

        self.script.select_anchor(anchor+1)

    #moves selected line up in position relative to other lines once
    def line_up(self):
        anchor=(self.script.index(ANCHOR))
        place='Line'+str(anchor)
        goal='Line'+str(anchor-1)

        if not os.path.exists(goal):
             return

        os.rename(goal,'dummy')
        os.rename(place, goal)
        os.rename('dummy', place)

        self.refresh()

        self.script.select_anchor(anchor-1)

    #function called to create the practice window used for all three modes of practice
    def create_practice_window(self):

        self.practice= Toplevel(self.tk)

        self.practice.title(self.scene)

        line_display= Frame(self.practice)
        line_display.pack(side=TOP, fill=BOTH, expand=1)

        #speaker display
        self.current_role= StringVar()
        self.speaker_display= Label(line_display,
                                    textvariable=self.current_role)
        self.speaker_display.pack(side=TOP)

        #text display
        text_frame= Frame(line_display)
        text_frame.pack(side=TOP, fill=BOTH, expand=1)

        self.text_display= Text(text_frame,
                                relief=RAISED)
        self.text_display.pack(side=LEFT, fill=BOTH, expand=1)

        #scrollbar
        text_display_scrollbar= Scrollbar(text_frame,
                                            command=self.text_display.yview)
        text_display_scrollbar.pack(side=LEFT,
                              fill=Y,)

        self.text_display.config(yscrollcommand=text_display_scrollbar.set)

        #practice buttons
        practice_buttons= Frame(self.practice)
        practice_buttons.pack(side=TOP, fill=X)

        #next button
        self.next_button= Button(practice_buttons,
                                 text='Next',
                                 command=self.next)
        self.next_button.pack(side=RIGHT)

        #back button
        self.back_button= Button(practice_buttons,
                                 text='Back',
                                 command=self.back)
        self.back_button.pack(side=RIGHT)

        #replay button
        self.replay_button= Button(practice_buttons,
                                   text='Replay',
                                   command=self.replay)

        #mute button
        self.mute_state= StringVar()
        self.mute_state.set('off')
        self.mute_button= Checkbutton(practice_buttons,
                                      text='Mute',
                                      variable=self.mute_state,
                                      onvalue='on',
                                      offvalue='off',
                                      indicatoron=False)
        self.mute_button.pack(side=RIGHT)

        #replay button
        self.replay_button= Button(practice_buttons,
                                   text='Replay',
                                   command=self.replay)
        self.replay_button.pack(side=RIGHT)


    #practice mode that starts at beginning of the script
    def from_the_top(self):

        self.create_practice_window()

        self.text_display.config(state=NORMAL)
        self.text_display.delete(0.0,END)

        self.line_place=0

        speaker_f=open(r'Line0\speaker.txt')
        text_f=open(r'Line0\text.txt')

        for line in speaker_f:
            self.current_role.set(line)

        for line in text_f:
            self.text_display.insert(END,line)

        speaker_f.close
        text_f.close
        self.text_display.config(state=DISABLED)

        self.audio_place=0

        self.tk.after(500, self.replay)

        self.practice.focus()

        self.next_button.config(command=self.next)

        self.back_button.config(state=NORMAL,
                                command=self.back)

    #practice mode that starts at the selected line within the script
    def from_selected(self):

        self.create_practice_window()

        self.text_display.config(state=NORMAL)
        self.text_display.delete(0.0,END)

        self.line_place=self.script.index(ACTIVE)

        speaker_path='Line'+str(self.line_place)+r'\speaker.txt'
        text_path='Line'+str(self.line_place)+r'\text.txt'

        speaker_f=open(speaker_path)
        text_f=open(text_path)

        for line in speaker_f:
            self.current_role.set(line)

        for line in text_f:
            self.text_display.insert(END,line)

        speaker_f.close
        text_f.close
        self.text_display.config(state=DISABLED)

        self.audio_place=self.script.index(ACTIVE)

        self.tk.after(500, self.replay)

        self.practice.focus()

        self.next_button.config(command=self.next)

        self.back_button.config(state=NORMAL,
                                command=self.back)

    #practice mode which gives the user random lines that come before the specified role's lines, then allows them to check if they got their line correct
    def random_cues(self):

        if self.role_entry.get()!='':

            self.create_practice_window()

            self.text_display.config(state=NORMAL)
            self.text_display.delete(0.0,END)

            self.cues=[]

            for num in range(1,1000):

                line='Line'+str(num)

                if os.path.exists(line):

                    speaker_f=open(line+r'\speaker.txt')

                    if self.role_entry.get()==speaker_f.read():

                        self.cues.append(num-1)
                        print(self.cues)

                    speaker_f.close()

            choice=random.choice(self.cues)
            self.cues.remove(choice)

            speaker_path='Line'+str(choice)+r'\speaker.txt'
            text_path='Line'+str(choice)+r'\text.txt'

            speaker_f=open(speaker_path)
            text_f=open(text_path)

            for line in speaker_f:
                self.current_role.set(line)

            for line in text_f:
                self.text_display.insert(END,line)

            speaker_f.close
            text_f.close
            self.text_display.config(state=DISABLED)

            self.audio_place=choice

            self.tk.after(500, self.replay)

            self.practice.focus()

            self.line_place=choice

            self.next_button.config(command=self.next_aftercue)

            self.back_button.config(state=DISABLED)

    #function of next button, puts next line into display and plays audio if not muted
    def next(self):
        if os.path.exists('Line'+str(self.line_place+1)):

            self.text_display.config(state=NORMAL)
            self.text_display.delete(0.0,END)

            self.line_place+=1

            speaker_path='Line'+str(self.line_place)+r'\speaker.txt'
            text_path='Line'+str(self.line_place)+r'\text.txt'

            speaker_f=open(speaker_path)
            text_f=open(text_path)

            for line in speaker_f:
                self.current_role.set(line)

            for line in text_f:
                self.text_display.insert(END,line)

            speaker_f.close
            text_f.close
            self.text_display.config(state=DISABLED)

            self.audio_place+=1

            if self.mute_state.get()=='off' and self.role_entry.get()!=self.current_role.get():
                self.tk.after(500, self.replay)

    #function used for random, identical to normal next except it changes button function to next_random
    def next_aftercue(self):
        if os.path.exists('Line'+str(self.line_place+1)):

            self.text_display.config(state=NORMAL)
            self.text_display.delete(0.0,END)

            self.line_place+=1

            speaker_path='Line'+str(self.line_place)+r'\speaker.txt'
            text_path='Line'+str(self.line_place)+r'\text.txt'

            speaker_f=open(speaker_path)
            text_f=open(text_path)

            for line in speaker_f:
                self.current_role.set(line)

            for line in text_f:
                self.text_display.insert(END,line)

            speaker_f.close
            text_f.close
            self.text_display.config(state=DISABLED)

            self.audio_place+=1

            if self.mute_state.get()=='off' and self.role_entry.get()!=self.current_role.get():
                self.tk.after(500, self.replay)

            self.next_button.config(command=self.next_random)

            self.back_button.config(state=NORMAL,
                                    command=self.back_aftercue)

    #function used for random, displays another random cue instead of the next line in order
    def next_random(self):
        self.text_display.config(state=NORMAL)
        self.text_display.delete(0.0,END)

        choice=random.choice(self.cues)
        self.cues.remove(choice)

        speaker_path='Line'+str(choice)+r'\speaker.txt'
        text_path='Line'+str(choice)+r'\text.txt'

        speaker_f=open(speaker_path)
        text_f=open(text_path)

        for line in speaker_f:
            self.current_role.set(line)

        for line in text_f:
            self.text_display.insert(END,line)

        speaker_f.close
        text_f.close
        self.text_display.config(state=DISABLED)

        self.audio_place=choice

        if self.mute_state.get()=='off' and self.role_entry.get()!=self.current_role.get():
            self.tk.after(500, self.replay)

        self.where_you_were= self.line_place

        self.line_place=choice

        self.next_button.config(command=self.next_aftercue)

        self.back_button.config(state=DISABLED)

    #function to go back a line, in random mode the button for it is sometimes disabled
    def back(self):
        if os.path.exists('Line'+str(self.line_place-1)):

            self.text_display.config(state=NORMAL)
            self.text_display.delete(0.0,END)

            self.line_place-=1

            speaker_path='Line'+str(self.line_place)+r'\speaker.txt'
            text_path='Line'+str(self.line_place)+r'\text.txt'

            speaker_f=open(speaker_path)
            text_f=open(text_path)

            for line in speaker_f:
                self.current_role.set(line)

            for line in text_f:
                self.text_display.insert(END,line)

            speaker_f.close
            text_f.close
            self.text_display.config(state=DISABLED)

            self.audio_place-=1

            if self.mute_state.get()=='off' and self.role_entry.get()!=self.current_role.get():
                self.tk.after(500, self.replay)

    #used for random, identical to back but changes button functions
    def back_aftercue(self):
        if os.path.exists('Line'+str(self.line_place-1)):

            self.text_display.config(state=NORMAL)
            self.text_display.delete(0.0,END)

            self.line_place-=1

            speaker_path='Line'+str(self.line_place)+r'\speaker.txt'
            text_path='Line'+str(self.line_place)+r'\text.txt'

            speaker_f=open(speaker_path)
            text_f=open(text_path)

            for line in speaker_f:
                self.current_role.set(line)

            for line in text_f:
                self.text_display.insert(END,line)

            speaker_f.close
            text_f.close
            self.text_display.config(state=DISABLED)

            self.audio_place-=1

            if self.mute_state.get()=='off' and self.role_entry.get()!=self.current_role.get():
                self.tk.after(500, self.replay)

            self.back_button.config(state=DISABLED)
            self.next_button.config(command=self.next_aftercue)

    #function to replay the audio recorded for displayed line
    def replay(self):
        place='Line'+str(self.audio_place)

        CHUNK = 1024

        wf = wave.open(place+r'\audio.wav', 'rb')
        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(CHUNK)

        while data != '':
            stream.write(data)
            data = wf.readframes(CHUNK)

        stream.stop_stream()
        stream.close()
        wf.close()

        p.terminate()

    #first step of import process, makes window to allow user to input character names for script to be imported
    def get_characters(self):

        self.get_char_window= Toplevel(self.tk)

        label=Label(self.get_char_window,
                    text= 'Enter character names:')
        label.pack(side=TOP)

        c_frame= Frame(self.get_char_window)
        c_frame.pack(side=TOP)

        self.character_listbox=Listbox(c_frame)
        self.character_listbox.pack(side=LEFT)

        scrollbar= Scrollbar(c_frame,
                             command=self.character_listbox.yview)

        scrollbar.pack(side=LEFT,
                        fill=Y,)

        self.character_listbox.config(yscrollcommand=scrollbar.set)

        character_input_frame=Frame(self.get_char_window)
        character_input_frame.pack(side=TOP)

        self.character_entry=Entry(character_input_frame)
        self.character_entry.pack(side=LEFT)

        character_enter=Button(character_input_frame,
                               text='Enter',
                               command=self.add_character)
        character_enter.pack(side=LEFT)

        character_entry_done_button= Button(self.get_char_window,
                                            text='Done',
                                            command=self.import_script)
        character_entry_done_button.pack(side=TOP)

        self.characters=[]

    #adds character's name to the list
    def add_character(self):

        addition=self.character_entry.get()+'\n'

        if addition not in self.characters:
            self.characters.append(addition)

            self.character_listbox.insert(END, addition)

        self.character_entry.delete(0,END)

    #goes through text file and generates lines for application automatically using given character names
    def import_script(self):

        self.get_char_window.destroy()

        #print(self.characters)

        line_place=(-1)

        script_f= filedialog.askopenfile(title='Select Script to Import',
                                           parent=self.tk,
                                           filetypes=[('text files', '.txt')])
        started=False

        for line in script_f:

            if line in self.characters:

                    if started:
                        os.chdir('..')

                    line_place+=1

                    os.mkdir('Line'+str(line_place))

                    os.chdir('Line'+str(line_place))

                    speaker_f=open('speaker.txt', 'w')

                    line=line.replace('\n','')

                    speaker_f.write(line)

                    speaker_f.close()

                    started=True


            elif started:

                text_f=open('text.txt', 'a')

                text_f.write(line)

                text_f.close()



        os.chdir('..')

        script_f.close()

        self.refresh()








master=Tk()

app=OffBook(master)

master.mainloop()
