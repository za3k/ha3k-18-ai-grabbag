import asyncio
import collections
import os
import subprocess
import sys
import tempfile

import typing
from typing import Literal, Tuple, IO, AnyStr, Union, Optional, Any

ChatEngine = Literal["LLaMA-2"]
Language = str
ConversationToken = str
AnnotatedText = collections.namedtuple("AnnotatedText", ["start", "end", "text"])
Image = Any # Will correct later

DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

def tmpfile(b):
    # Can't just use io.BytesIO because subprocess wants a fileno
    f = tempfile.TemporaryFile() 
    f.write(b)
    f.seek(0)
    return f

async def TranscribeAudio(file: Union[str, IO[AnyStr]]) -> list[AnnotatedText]:
    if isinstance(file, str):
        with open(file, "r") as f:
            return await TranscribeAudio(f)

    text = subprocess.check_output(os.path.join(DIR, "whisper.sh"), stdin=file, stderr=subprocess.DEVNULL).decode('utf8').strip()

    ret: list[AnnotatedText] = []
    for line in text.split("\n"):
        start, end, text = line.split("\t")
        ret.append(AnnotatedText(int(start), int(end), text))
    return ret

async def Chat(prompt: str, conversation: Optional[ConversationToken]=None, reply_length=1000, engine: ChatEngine="LLaMA-2") -> Tuple[str, ConversationToken]:
    llama_dir = os.path.join(DIR, "llama.cpp")
    LLAMA_PROMPT = """[INST] <<SYS>>\nYou are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.\n<</SYS>>\n{prompt}[/INST] """
    LLAMA_PROMPT = """[INST]{prompt}[/INST]\n\n"""
    prompt = (conversation or "") + LLAMA_PROMPT.format(prompt=prompt)

    command = ["./main",
        "-m", "models/llama-2-7b-chat.Q4_K_M.gguf",
        "--verbose-prompt",
        "-n", str(reply_length),
        "-p", prompt,
        "-ngl", "4000",
    ]
    conversation = subprocess.check_output(command, stderr=subprocess.DEVNULL, cwd=llama_dir).decode("utf8").strip()
    reply = conversation.removeprefix(prompt).strip()
    return reply, conversation

async def Say(text: str, language=None) -> None:
    subprocess.check_output("speak", input=text.encode("utf8"), stderr=subprocess.DEVNULL)

async def SaySound(text: str, language=None) -> IO[AnyStr]:
    return tmpfile(subprocess.check_output(["speak", "--stdout"], input=text.encode("utf8"), stderr=subprocess.DEVNULL))

async def Translate(text: str, to_language: Language="en", from_language: Optional[Language]=None) -> str:
    # return translated_text
    return text

async def Draw(prompt) -> Image:
    pass
    # Return PIL object with show() and save(filename) methods
    return None
    
async def Listen() -> list[AnnotatedText]:
    return []

async def main():
    if False:
        print("Speech test start.")
        await Say("Testing testing, 1 2 3")
        test_audio = await SaySound("Testing testing, 1 2 3")
        print("Speech test done.")

        print("Speech recognition test start.")
        jfk_text = await TranscribeAudio("sample/jfk.wav")
        print("  ", jfk_text[0].text)

        re_transcribed = await TranscribeAudio(test_audio)
        print("  ", re_transcribed[0].text)
        print("Speech recognition test end.")
    if False:
        print("LLM chat test start.")
        reply, convo = await Chat("Explain the single most important difference between London and Moscow.")
        print(reply)
        reply, convo = await Chat("Okay, say one more cool thing about each city.", convo)
        print(reply)
        print("LLM chat test end.")
        print("LLM translation test start.")
        reply, convo = await Chat("Translate the following into conversational German. Please do not add any prefaces, helpful greetings, or notes. The English phrase is: I am going to the bus station. Could you take care of my cat while I am gone today? \n\n What is the German translation?")
        print(reply)
        print("LLM translation test end.")


if __name__ == "__main__":
    asyncio.run(main())
