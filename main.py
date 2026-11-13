import asyncio
import io
import edge_tts
import pygame


async def say(text: str, voice="en-US-AriaNeural"):
    # Stream audio directly into memory
    communicate = edge_tts.Communicate(text, voice)
    audio_stream = io.BytesIO()

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_stream.write(chunk["data"])

    audio_stream.seek(0)  # Rewind the memory stream to the beginning

    # Play the audio from memory
    pygame.mixer.init()
    pygame.mixer.music.load(audio_stream)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


async def save_audio(text, filename="output.mp3", voice="en-US-AriaNeural"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filename)
    print(f"Saved successfully as {filename}")


# Test it out
# asyncio.run(
#     say("Hello! I am speaking directly from memory without using the os module.")
# )

text = "Visit Our Website: www.SunoAiSongDownload.Online"

text = "সন্ধেবেলা সে বাড়ির পেছনের লেবুর বাগানে ঘুরত, কিন্তু একটাও জোনাকি তার হাতে ধরা দিত না"
text = "আমি আজ Suno AI Song Download ওয়েবসাইটে গিয়েছিলাম, it was really fast!"


voice_agent = "en-IN-NeerjaExpressiveNeural"
# voice_agent = "bg-BG-BorislavNeural"
# voice_agent = "bn-IN-TanishaaNeural"

asyncio.run(
    say(
        text,
        voice=voice_agent,
    )
)


asyncio.run(save_audio("Hello! This is saved directly as an MP3 file.", "my_voice.mp3"))
