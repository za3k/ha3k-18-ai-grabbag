This was my attempt to catch up on the 2022-2023 AI tools which have come out recently, based on "transformers".

If you install CUDA, all of the below will run significantly faster.

- [ ] Draw() function for library using StableDiffusion (return PIL object, or file path)
- [ ] Translate() function for translation

My goal is to write a python library, so that I can write commands like (or the equivalent with async/await):

```
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

# Wait for a spoken command (not done)
annotated_prompt = Listen()
```

## Install espeak-ng (speech synthesis)

```
pacman -S espeak-ng
```

## Install whisperx (speech recognition)

```
yay -S python310
```

```
git clone https://github.com/m-bain/whisperX
cd whisperX
virtualenv -p python3.10 venv
. venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Install llama.cpp (chat, translation)

```
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
wget --directory-prefix models -c https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf
```

## Install Stable Diffusion WebUI (images)

(not done)
