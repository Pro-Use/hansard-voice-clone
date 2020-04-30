from encoder.params_model import model_embedding_size as speaker_embedding_size
from utils.argutils import print_args
from synthesizer.inference import Synthesizer
from encoder import inference as encoder
from vocoder import inference as vocoder
from pathlib import Path
import numpy as np
import librosa
import traceback


class VoiceCloner:
    def __init__(self):
        # Info & args
        enc_model_fpath = Path("encoder/saved_models/pretrained.pt")

        syn_model_dir = Path("synthesizer/saved_models/logs-pretrained/")
        voc_model_fpath = Path("vocoder/saved_models/pretrained/pretrained.pt")
        low_mem = False

        ## Load the models one by one.
        print("Preparing the encoder, the synthesizer and the vocoder...")
        encoder.load_model(enc_model_fpath)
        self.synthesizer = Synthesizer(syn_model_dir.joinpath("taco_pretrained"), low_mem=low_mem)
        vocoder.load_model(voc_model_fpath)

    def gen_audio(self, ref_audio, text):
        try:
            in_fpath = Path(ref_audio.replace("\"", "").replace("\'", ""))

            ## Computing the embedding
            # First, we load the wav using the function that the speaker encoder provides. This is
            # important: there is preprocessing that must be applied.

            # The following two methods are equivalent:
            # - Directly load from the filepath:
            # preprocessed_wav = encoder.preprocess_wav(in_fpath)
            # - If the wav is already loaded:
            original_wav, sampling_rate = librosa.load(in_fpath, sr=None)
            preprocessed_wav = encoder.preprocess_wav(original_wav, sampling_rate)
            print("Loaded file succesfully, rate=%s" % sampling_rate)

            # Then we derive the embedding. There are many functions and parameters that the
            # speaker encoder interfaces. These are mostly for in-depth research. You will typically
            # only use this function (with its default parameters):
            embed = encoder.embed_utterance(preprocessed_wav)
            print("Created the embedding")

            ## Generating the spectrogram
            # The synthesizer works in batch, so you need to put your data in a list or numpy array
            texts = [text]
            embeds = [embed]
            # If you know what the attention layer alignments are, you can retrieve them here by
            # passing return_alignments=True
            specs = self.synthesizer.synthesize_spectrograms(texts, embeds)
            spec = specs[0]
            print("Created the mel spectrogram")

            ## Generating the waveform
            print("Synthesizing the waveform:")
            # Synthesizing the waveform is fairly straightforward. Remember that the longer the
            # spectrogram, the more time-efficient the vocoder.
            generated_wav = vocoder.infer_waveform(spec)

            ## Post-generation
            # There's a bug with sounddevice that makes the audio cut one second earlier, so we
            # pad it.
            # generated_wav = np.pad(generated_wav, (0, self.synthesizer.sample_rate), mode="constant")
            print("\n samples = %s @ %s" % (len(generated_wav), self.synthesizer.sample_rate))

            return generated_wav

        except Exception as e:
            traceback.print_exc()
            print("Caught exception: %s" % repr(e))
            print("Restarting\n")



