import pyaudio
import wave

#creates instance of PyAudio
p = pyaudio.PyAudio()

#open a stream
stream = p.open(format=pyaudio.paInt16,
                channels=2,
                rate=44100,
                input=True,
                frames_per_buffer=1024)

frames=[]


for i in range(0, int(44100 / 1024 * 3)):
    data = stream.read(1024)
    frames.append(data)
    



#while stream.is_active():
    #data= stream.read(1024)
    #frames.append(data)

stream.stop_stream()
stream.close()
p.terminate()
