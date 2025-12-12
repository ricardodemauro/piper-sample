import numpy as np
import subprocess
from piper.voice import PiperVoice
import asyncio
from collections import deque
import wave
import uuid
import os
import time
from pathlib import Path

from pydub import AudioSegment
from pydub.playback import play

def run():
    model_path = Path(__file__).resolve().parents[1] / "en_US-lessac-medium.onnx"
    voice = PiperVoice.load(str(model_path))
    text = [
        "The Piper repository includes a variety of pre-trained voice models sorted by language that you can use in your projects.",
        "These models determine how the synthesized speech will sound, in other words, each model is a different \"voice\" you can use with Piper.",
        "You can also create your own voice model using the Piper Recording Studio, a web application that you can run locally to generate a Piper dataset by recording clips with your voice.",
        "However, make sure to have a decent graphics card on your device, or training your model could be a very slow task.",
        "For more information on the process of creating a model for Piper, look at this article from Sam Howell."
    ]

    audio_queue = deque()
    queue_lock = asyncio.Lock()
    synthesis_done = asyncio.Event()

    async def play_audio_file(filepath):
        """Coroutine to play a single WAV file using aplay"""
        
        # for playing wav file
        song = AudioSegment.from_wav(filepath)
        print('playing sound using  pydub')
        play(song)
        
        # Clean up the file after playing
        os.remove(filepath)

    async def playback_worker():
        """Background worker that plays audio files from the queue sequentially"""
        while True:
            async with queue_lock:
                if audio_queue:
                    filepath = audio_queue.popleft()
                else:
                    filepath = None
            
            if filepath is not None:
                await play_audio_file(filepath)
            elif synthesis_done.is_set():
                break
            else:
                await asyncio.sleep(0.1)

    async def main():
        # Start playback worker
        worker_task = asyncio.create_task(playback_worker())
        
        # Synthesize and queue audio files
        for t in text:
            filename = f"audio_{uuid.uuid4().hex}.wav"
            with wave.open(filename, "wb") as wav_file:
                voice.synthesize_wav(t, wav_file)
            
            async with queue_lock:
                audio_queue.append(filename)
        
        synthesis_done.set()
        await worker_task

    # Run the async main function
    asyncio.run(main())
