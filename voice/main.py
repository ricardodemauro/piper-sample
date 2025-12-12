import wave
from piper import PiperVoice, SynthesisConfig

def run():

    BAKE_CAKE = """Today it's time for a good basic recipe: a delicious vanilla cake. There are already quite a few cake recipes on the site, but a tasty basic cake recipe was still missing.

While I always eagerly use a basic recipe and then give it a different twist each time.

I use this recipe regularly when I'm baking cupcakes or cakes. It's also been used several times for the baking books I've created.

If you ask me, this is the most delicious cake recipe you can make. So it's high time to share it with you!"""

    voice = PiperVoice.load("/home/radmin/projects/piper-sample/en_US-lessac-medium.onnx")

    syn_config = SynthesisConfig(
        volume=0.5,  # half as loud
        length_scale=1.0,  # slower
        noise_scale=1.0,  # more audio variation
        noise_w_scale=1.0,  # more speaking variation
        normalize_audio=False, # use raw audio from voice
    )

    with wave.open("test.wav", "wb") as wav_file:
        voice.synthesize_wav(BAKE_CAKE, wav_file, syn_config=syn_config)
        
