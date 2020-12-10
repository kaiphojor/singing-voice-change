import pyaudio # Soundcard audio I/O access library
import wave # Python 3 module for reading / writing simple .wav files
#import voice_conversion.test as vc


def speech_voice_conv():
    FORMAT = pyaudio.paInt16 # data type formate
    CHANNELS = 1 # Adjust to your number of channels
    RATE = 24000 # Sample Rate
    CHUNK = 1024 # Block Size
    RECORD_SECONDS = 10 # Record time
    WAVE_OUTPUT_FILENAME = "./voice_conversion/data/test/voice.wav"

    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    print("recording...")
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finished recording")


    stream.stop_stream()
    stream.close()
    audio.terminate()

    # wav convert
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    # voice conversing
    #vc.test()
    print("######### Converting Done ########")

