import asyncio
import collections
import subprocess
import tempfile

import typing
from typing import Literal, Tuple, IO, AnyStr, Union, Optional, Any

ChatEngine = Literal["LLaMA-2"]
Language = str
ConversationToken = str
AnnotatedText = collections.namedtuple("AnnotatedText", ["start", "end", "text"])
Image = Any # Will correct later

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

    text = subprocess.check_output("~/ha3k-18-ai-grabbag/whisper.sh", shell=True, stdin=file, stderr=subprocess.DEVNULL).decode('utf8').strip()

    ret: list[AnnotatedText] = []
    for line in text.split("\n")[1:]:
        start, end, text = line.split("\t")
        ret.append(AnnotatedText(int(start), int(end), text))
    return ret

async def Chat(prompt: str, conversation: Optional[ConversationToken], engine: ChatEngine="LLaMA-2") -> Tuple[str, ConversationToken]:
    pass
    #return reply, conversation
    return "", ""

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

if __name__ == "__main__":
    asyncio.run(main())
