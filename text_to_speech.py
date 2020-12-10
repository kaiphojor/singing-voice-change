import boto3
from pydub import AudioSegment
import os
import pydub
import subprocess
import json
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from xml.etree import ElementTree

def generate_voice():
    polly_client = boto3.Session(
        aws_access_key_id='AKIAJSNUEM4XXIJU4WSQ',
        aws_secret_access_key='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',
        region_name='ap-northeast-2').client('polly')
    # 경로수정 필요
    pydub.AudioSegment.converter = "./tts_storage/ffmpeg/bin/ffmpeg.exe"
    with open("./tts_storage/text/tts_script.txt", encoding='utf-8') as file_in:
        data = []
        text_ = ''
        for line in file_in:

            text_ += line
            print("## TTS script:",line)
        data.append(text_)
    for i in range(0, len(data)):
        response = polly_client.synthesize_speech(VoiceId='Seoyeon',
                                                  OutputFormat='mp3',
                                                  Text=data[i] + ' .')

        file = open('./tts_storage/sound/seoyeon_{}.mp3'.format(i), 'wb')
        file.write(response['AudioStream'].read())
        file.close()

        src = "./tts_storage/sound/seoyeon_{}.mp3".format(i)
        dst = "./text_conversion/data/test/tts.wav".format(i)
        subprocess.call(['ffmpeg', '-i', 'seoyeon_{}.mp3'.format(i), '-c', 'pcm_u8', 'tts.wav'.format(i)])

        sound = AudioSegment.from_mp3(src)
        sound.export(dst, format="wav", parameters=["-c:a", "pcm_u8"])
        os.remove("./tts_storage/sound/seoyeon_{}.mp3".format(i))

    ############# AZURE #######################
    # rate = "-3.0%"
    # pitch = "low"
    # speech_config = SpeechConfig(subscription="259174701e154db59bdd1e8af77a6423", region="eastus")
    # synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    # pydub.AudioSegment.converter = "./tts_storage/ffmpeg/bin/ffmpeg.exe"
    # with open('./tts_storage/text/tts_script.txt', encoding='utf-8') as file_in:
    #     text = ""
    #     for line in file_in:
    #         text += line
    #     # print("## TTS script:",text)
    #
    #     root = ElementTree.fromstring(
    #         '<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US"><voice name="ko-KR-HeamiRUS"><prosody rate="{}" pitch="{}">{}</prosody></voice></speak>'.format(
    #             rate, pitch, text))
    #     xml_script = ElementTree.ElementTree()
    #     ElementTree.dump(root)
    #     xml_script._setroot(root)
    #     xml_script.write('ssml.xml')
    #
    #     ssml_string = open("./ssml.xml", "r", encoding='utf-8').read()
    #     result = synthesizer.speak_ssml_async(ssml_string).get()
    #     stream = AudioDataStream(result)
    #     stream.save_to_wav_file("./tts_storage/sound/tts.wav")
    #
    #     src = "./tts_storage/sound/tts.wav"
    #     dst = "./text_conversion/data/test/tts.wav"
    #     subprocess.call(['ffmpeg', '-i', 'tts.wav', '-c', 'pcm_u8', 'tts.wav'])
    #
    #     sound = AudioSegment.from_wav(src)
    #     sound.export(dst, format="wav", parameters=["-c:a", "pcm_u8"])
    #     os.remove("./tts_storage/sound/tts.wav")
