import asyncio
import io
import re

import edge_tts
import pygame

VOICES = {
    "bn": "bn-IN-TanishaaNeural",
    "en": "en-IN-NeerjaNeural",  # Indian English, fits Bengali speakers well
}

BENGALI = re.compile(r"[\u0980-\u09FF]")


def split_by_language(text: str):
    """Split text into [(lang, chunk), ...]. Spaces/punctuation stick to the current chunk."""
    segments = []
    current_lang = None
    buf = ""

    for ch in text:
        if BENGALI.match(ch):
            lang = "bn"
        elif ch.isalpha():
            lang = "en"
        else:
            lang = None  # space, punctuation: neutral

        if lang is None or current_lang is None or lang == current_lang:
            buf += ch
            if lang and current_lang is None:
                current_lang = lang
        else:
            segments.append((current_lang, buf))
            buf, current_lang = ch, lang

    if buf.strip():
        segments.append((current_lang or "en", buf))
    return segments


async def synth(text, voice):
    """Return MP3 bytes for one chunk."""
    data = io.BytesIO()
    async for chunk in edge_tts.Communicate(text, voice).stream():
        if chunk["type"] == "audio":
            data.write(chunk["data"])
    return data.getvalue()


async def build_audio(text):
    audio = io.BytesIO()
    for lang, chunk in split_by_language(text):
        # skip chunks with no real letters/digits (avoids NoAudioReceived)
        if not any(c.isalnum() for c in chunk):
            continue
        audio.write(await synth(chunk, VOICES[lang]))
    audio.seek(0)
    return audio


async def say(text):
    audio = await build_audio(text)
    pygame.mixer.init()
    pygame.mixer.music.load(audio)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


async def save_audio(text, filename="output.mp3"):
    audio = await build_audio(text)
    with open(filename, "wb") as f:
        f.write(audio.read())
    print(f"Saved as {filename}")


async def main():
    text = "আমি আজ Suno AI Song Download ওয়েবসাইটে গিয়েছিলাম, it was really fast!"
    await say(text)
    await save_audio(text, "mixed.mp3")


asyncio.run(main())
