from piper.voice import PiperVoice, SynthesisConfig
import asyncio
from collections import deque
import wave
import io
from pathlib import Path

from pydub import AudioSegment
from pydub.playback import play

def run():
    model_path = Path(__file__).resolve().parents[1] / "en_US-lessac-medium.onnx"
    voice = PiperVoice.load(str(model_path))
    text = [
        "In this article, we will explore how to play sound in Python using some of the most popular audio libraries.",
        "Whether you need to play a simple sound effect or work with complex audio files, these methods will cover your needs.",
        "We'll discuss five different approaches to play sound in Python, using modules like playsound, pydub, tksnack, and more.",
        "You'll also find examples to make implementation easier."
    ]

    audio_queue = deque()
    queue_lock = asyncio.Lock()
    synthesis_done = asyncio.Event()

    async def play_audio_bytes(audio_bytes):
        """Coroutine to play audio from in-memory bytes"""
        
        # Load audio from bytes
        song = AudioSegment.from_wav(io.BytesIO(audio_bytes))
        print('playing sound using pydub')
        play(song)

    async def playback_worker():
        """Background worker that plays audio files from the queue sequentially"""
        while True:
            async with queue_lock:
                if audio_queue:
                    audio_bytes = audio_queue.popleft()
                else:
                    audio_bytes = None
            
            if audio_bytes is not None:
                await play_audio_bytes(audio_bytes)
            elif synthesis_done.is_set():
                break
            else:
                await asyncio.sleep(0.1)

    async def main():
        # Start playback worker
        worker_task = asyncio.create_task(playback_worker())

        syn_config = SynthesisConfig(
            volume=1, 
            length_scale=1.0,  # normal speed
            noise_scale=1,  # more audio variation
            noise_w_scale=1,  # more speaking variation
            normalize_audio=True, # use raw audio from voice
        )
        
        # Synthesize and queue audio files
        for t in text:
            wav_buffer = io.BytesIO()
            with wave.open(wav_buffer, "wb") as wav_file:
                voice.synthesize_wav(t, wav_file, syn_config=syn_config)
            
            async with queue_lock:
                audio_queue.append(wav_buffer.getvalue())
        
        synthesis_done.set()
        await worker_task

    # Run the async main function
    asyncio.run(main())
