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
from concurrent.futures import ThreadPoolExecutor

from pydub import AudioSegment
from pydub.playback import play

def run():
    model_path = Path(__file__).resolve().parents[1] / "en_US-lessac-medium.onnx"
    voice = PiperVoice.load(str(model_path))

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

    async def input_worker(loop, executor):
        """Background worker that reads keyboard input and queues synthesis tasks"""
        print("Enter text to synthesize (press Enter to send, type 'quit' to exit):")
        while True:
            # Run input in executor thread to avoid blocking the event loop
            text = await loop.run_in_executor(executor, input, "> ")
            
            if text.lower() == 'quit':
                synthesis_done.set()
                break
            
            if text.strip():
                filename = f"audio_{uuid.uuid4().hex}.wav"
                with wave.open(filename, "wb") as wav_file:
                    voice.synthesize_wav(text, wav_file)
                
                async with queue_lock:
                    audio_queue.append(filename)

    async def main():
        # Create a thread pool executor for blocking input
        executor = ThreadPoolExecutor(max_workers=1)
        loop = asyncio.get_event_loop()
        
        # Start playback worker and input worker as concurrent tasks
        playback_task = asyncio.create_task(playback_worker())
        input_task = asyncio.create_task(input_worker(loop, executor))
        
        # Wait for both workers to complete
        await asyncio.gather(playback_task, input_task)
        executor.shutdown(wait=True)

    # Run the async main function
    asyncio.run(main())
