import asyncio
import io
import edge_tts


async def say(text: str, voice: str = "en-US-AriaNeural"):
    import pygame

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


async def save_audio(
    text,
    filename="output.mp3",
    voice="en-US-AriaNeural",
    rate="+0%",
    volume="+0%",
    pitch="+0Hz",
):
    communicate = edge_tts.Communicate(
        text,
        voice,
        rate=rate,
        volume=volume,
        pitch=pitch,
    )
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
voice_agent = "bn-IN-TanishaaNeural"

# asyncio.run(
#     say(
#         text,
#         voice=voice_agent,
#     )
# )


# asyncio.run(save_audio(text, "my_voice.mp3"))


async def main():
    # for now i want to use single voice here not separat of language

    text = "আমি আজ Suno AI Song Download ওয়েবসাইটে গিয়েছিলাম, it was really fast!"

    text = """
এক টুকরো রোদ

ছোট্ট একটা গ্রাম ‘নন্দনপুর’। সেখানে থাকত ছোট্ট একটা ছেলে, নাম তার রতন। বয়স মোটে আট বছর। রতনের খুব শখ ছিল একটা জোনাকি পোকা ধরার। রোজ সন্ধেবেলা সে বাড়ির পেছনের লেবুর বাগানে ঘুরত, কিন্তু একটাও জোনাকি তার হাতে ধরা দিত না।
একদিন খুব বৃষ্টি হলো। বিকেলবেলা বৃষ্টি থামার পর রতন বারান্দায় এসে দাঁড়াল। দেখল, ভিজে ঘাসের ওপর একটা ছোট্ট হলুদ প্রজাপতি বসে আছে, যার ডানায় বৃষ্টির ফোঁটা মুক্তোর মতো চকচক করছে।
রতন আস্তে করে এগিয়ে গিয়ে তার হাতটা বাড়িয়ে দিল। প্রজাপতিটা উড়ল না, বরং উড়ে এসে রতনের ছোট্ট আঙুলের ডগায় বসল। রতনের মনে হলো, সে যেন আকাশের এক টুকরো রোদ নিজের হাতে পেয়ে গেছে।
সেদিন রাতে ঘুমাতে যাওয়ার সময় রতন তার মাকে বলল, "মা, আজ আমি রোদ ধরেছিলাম।"
মা হেসে মাথায় হাত বুলিয়ে বললেন, "রোদ কি আর ধরা যায় সোনা? ও তো সবার জন্য।"
রতন মনে মনে ভাবল— সবার জন্য হলেও, আজ কিছুক্ষণ তো ও শুধু আমারই ছিল!
"""
    await save_audio(
        text,
        "mixed.mp3",
        voice=voice_agent,
        rate="+20%",  # faster
        volume="+50%",  # louder
        pitch="+50Hz",
    )


asyncio.run(main())
