# # from django.shortcuts import render

# # # Create your views here.
# import speech_recognition as sr
# from transformers import pipeline
# from rest_framework import status 
# from pydub import AudioSegment 
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# import io

# @api_view(["GET"])
# def home(request):
#     return Response({"message": "Doctor-Patient Backend Running ✅"})


# # @api_view(["POST"])
# # def voice_to_text(request):
# #     try:
# #         audio_file = request.FILES['audio']
        
# #         recognizer = sr.Recognizer()
# #         with sr.AudioFile(audio_file) as source:
# #             audio = recognizer.record(source)
# #             text = recognizer.recognize_google(audio)

# #         # Optional NLP: For now, just returning the recognized text
# #         return Response({"text": text})

# #     except Exception as e:
# #         return Response({"error": str(e)})



# # Load HuggingFace pipeline (medical chatbot)
# chatbot = pipeline("text-generation", model="microsoft/DialoGPT-medium")

# @api_view(['POST'])
# def voice_to_text(request):
#     audio_file = request.FILES.get('audio')
#     recognizer = sr.Recognizer()

#     with sr.AudioFile(audio_file) as source:
#         audio_data = recognizer.record(source)

#     try:
#         # Step 1: Convert voice to text
#         user_text = recognizer.recognize_google(audio_data)
#         print("User said:", user_text)

#         # Step 2: Get response from medical chatbot
#         doctor_reply = chatbot(f"You are a doctor. A patient says: {user_text}", max_length=100)[0]['generated_text']

#         return Response({'text': doctor_reply})

#     except sr.UnknownValueError:
#         return Response({'text': 'Could not understand audio'}, status=400)
#     except Exception as e:
#         return Response({'text': str(e)}, status=500)


























# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# import speech_recognition as sr
# from pydub import AudioSegment
# import io

# @api_view(['POST'])
# def voice_to_text(request):
#     try:
#         audio_file = request.FILES['audio']
        
#         # Convert the uploaded file to WAV using pydub
#         audio = AudioSegment.from_file(audio_file)
#         wav_io = io.BytesIO()
#         audio.export(wav_io, format='wav')
#         wav_io.seek(0)
#         print("audio tak aa gye he backend me ")

#         recognizer = sr.Recognizer()
#         with sr.AudioFile(wav_io) as source:
#             audio_data = recognizer.record(source)
#             text = recognizer.recognize_google(audio_data)

#         return Response({'text': text})

#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import speech_recognition as sr
from pydub import AudioSegment
import traceback
import io 
import pyttsx3
from gtts import gTTS
import os
from django.conf import settings

doctor_advice = {
    "headache": {
        "advice": "It seems like you are suffering from a headache. I recommend taking pain relievers like Paracetamol and drinking plenty of water. If it persists, consult a doctor.",
        "medicines": ["Paracetamol", "Ibuprofen"]
    },
    "fever": {
        "advice": "It looks like you have a fever. You should rest, stay hydrated, and take fever-reducing medicines like Paracetamol. If symptoms worsen, visit a doctor.Anything else ",
        "medicines": ["Paracetamol", "Ibuprofen"]
    },
    "cough": {
        "advice": "It seems like you have a cough. You may want to try some over-the-counter medicines like Cough Syrup. Also, make sure to rest and drink warm fluids.",
        "medicines": ["Cough Syrup", "Honey Lemon Tea"]
    }
}



# def speak_advice(advice_text):
#     """Function to convert text to speech with a different driver"""
#     engine = pyttsx3.init()  
#     engine.say(advice_text)
#     engine.runAndWait()
# def speak_advice(advice_text):
#     """Function to convert text to speech using gTTS"""
#     tts = gTTS(text=advice_text, lang='en')
#     audio_path = "media/audio/advice.mp3"
#     tts.save("advice.mp3")
#     os.system("mpg321 advice.mp3")  # Play the speech using mpg321 or another media player

# def speak_advice(advice_text):
#     """Convert advice text to speech and save it as MP3 in media/audio/"""

#     # Define path
#     audio_folder = os.path.join(settings.MEDIA_ROOT, 'audio')
#     os.makedirs(audio_folder, exist_ok=True)  # ✅ This creates the folder if it doesn't exist

#     # Full file path
#     audio_path = os.path.join(audio_folder, 'advice.mp3')

#     # Init and save audio
#     engine = pyttsx3.init()
#     engine.save_to_file(advice_text, audio_path)
#     engine.runAndWait()


def speak_advice(advice_text):
    # Folder path
    audio_folder = os.path.join(settings.MEDIA_ROOT, 'audio')
    os.makedirs(audio_folder, exist_ok=True)

    # File path
    audio_path = os.path.join(audio_folder, 'advice.mp3')

    # Generate and save audio
    tts = gTTS(text=advice_text, lang='en')
    tts.save(audio_path)

    # Return relative URL
    return '/media/audio/advice.mp3'







@api_view(['POST'])
def voice_to_text(request):
    try:
        audio_file = request.FILES.get('audio')

        if not audio_file:
            return Response({'error': 'No audio file received'}, status=400)

        print("🔊 Audio received:", audio_file.content_type)

        # Convert webm to wav
        audio = AudioSegment.from_file(audio_file, format="webm")
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)
        

        # Use SpeechRecognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_io) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)

        try:
            text = recognizer.recognize_google(audio_data)
        except UnknownValueError:
            return Response({'text': "Sorry, couldn't understand the audio. Try again."}, status=200)

        # return Response({'text': text})

            # Analyzing the text and providing doctor-like advice
        symptom = None
        for key in doctor_advice:
            if key in text.lower():  # Simple keyword matching
                symptom = key
                break

        if symptom:
            advice = doctor_advice[symptom]["advice"]
            medicines = doctor_advice[symptom]["medicines"]
            response_text = f"Advice: {advice}\nMedicines: {', '.join(medicines)}"
        else:
            response_text = "Sorry, I couldn't understand your symptoms. Please try again."

        speak_advice(response_text)

        # Text-to-Speech: Convert advice into speech (Optional)
        # You can use a library like pyttsx3 to convert text into speech
        # But for now, we’ll just send the response text

        return Response({'text': response_text})





    except Exception as e:
        print("❌ INTERNAL ERROR:")
        traceback.print_exc()  # This prints full error trace
        return Response({'error': str(e)}, status=500)