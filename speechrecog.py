import speech_recognition as sr  

# get audio from the microphone                                                                       
r = sr.Recognizer()                                                                                   
with sr.Microphone() as source:                                                                       
    print("Speak:")                                                                                   
    audio = r.listen(source)   
str1 = "password"

try:
    str2 =  r.recognize_google(audio)
    print("You said " + r.recognize_google(audio))
    if str2 == str1:
        print("Fuck yeah biatch")
except sr.UnknownValueError:
    print("Could not understand audio")
except sr.RequestError as e:
    print("Could not request results; {0}".format(e))
