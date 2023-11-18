This was my attempt to catch up on the 2022-2023 AI tools which have come out recently, based on "transformers".

[ ] Transcribe D&D audio as a test
[ ] TranscribeAudio() function for library

[ ] Say() function for library
[ ] Chat() function for library using HuggingFace
[ ] Chat(continue=conversation) function for library using HuggingFace
[ ] Draw() function for library using StableDiffusion (return PIL object)
[ ] Listen() function for library

My goal is to write a python library, so that I can write command like (or the equivalent with async/await):

    # Speech transcription, using whisper/whisperx
    annotated_text = TranscribeAudio("audio.mp3")

    # Talking to LLMs, which respond to text with text. Uses HuggingFace
    reply, conversation = Chat("What is a healthy, tasty meal to eat for dinner?", engine="LLaMA-2") # GPT-3 not supported

    # Speech synthesis
    Say(reply)
    Say(reply, as="Jerry Seinfeld")

    # Human language translation, using LLMs again
    auf_deutsch = Translate(reply, "German")
    print(auf_deutch)
    Say(auf_deutsch)

    # Creating pictures, using stable diffusion
    picture = Draw("a sarcastic cat, in a simple cartoon style")
    picture.show()
    picture.save("cat.jpg")
    
    # Wait for a spoken command
    annotated_prompt = Listen()

## Install whisperx

```
yay -S python310
```

```
git clone https://github.com/m-bain/whisperX
cd whisperX
virtualenv -p python3.10 venv
. ./venv/bin/activate
pip install -r requirements.txt
pip install -e .
```
