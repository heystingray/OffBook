from tkinter import *
import pyaudio
import wave



class app():

    def __init__(self, master):


        frame= Frame(master)
        frame.pack()

        

        #the record button
        self.var=IntVar()
        self.recbutton=Checkbutton(frame,
                                   text="Record",
                                   fg='red',
                                   variable=self.var,
                                   command=self.record,
                                   indicatoron=False)
        
        self.recbutton.pack(side=LEFT)

        #the play button
        self.playbutton=Button(
            frame, text='Play', fg='green', command=self.play)
        self.playbutton.pack(side=LEFT)


    def callback(self, in_data, frame_count, time_info, status):
        
        self.frames.append(in_data)

        return (in_data, pyaudio.paContinue) 
        
        
            
        
    def record(self):
        
        if self.var.get()==1:

            self.p=pyaudio.PyAudio()

            self.frames= []
            
            self.stream=self.p.open(format=pyaudio.paInt16,
                                    channels=2,
                                    rate=44100,
                                    input=True,
                                    frames_per_buffer=1024,
                                    stream_callback=self.callback)

            

            

            print('stream made')

            
           
                

        elif self.var.get()==0 and self.stream.is_active()==True:
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()
            
            wf = wave.open('test.wav', 'wb')
            wf.setnchannels(2)
            wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.frames))
            wf.close()

            print('done')

        else:

            print('did nothing')
            

        
                
    def play(self):
        CHUNK = 1024

        wf = wave.open('test.wav', 'rb')
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

        p.terminate()

        print('played')

root= Tk()

App=app(root)

root.mainloop()
