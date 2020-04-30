from textHelpers import get_hansard, text_operations
from cloner import VoiceCloner
import librosa
import numpy as np

import os

DATE = "2020-04-22"
vc = VoiceCloner()


def chunks(arr, n):
    n = max(1, n)
    return (arr[i:i+n] for i in range(0, len(arr), n))


statements = get_hansard.GetHansard(date=DATE, members=[4007, 4514])
changed_statements = text_operations.replace_words(statements)

if not os.path.exists("output/" + DATE):
    os.mkdir("output/" + DATE)

file_no = 0
for statement in changed_statements:
    if os.path.exists("reference_audio/%s.wav" % statement[0]):
        words = statement[1].split(" ")
        wavs = []
        word_chunks = chunks(words, 25)
        last_chunk = ""
        for chunk in word_chunks:
            if len(chunk) < 15:
                chunk = last_chunk + chunk
                wavs.pop()
            chunk_text = " ".join(chunk)
            new_wav = vc.gen_audio("reference_audio/%s.wav" % statement[0], chunk_text)
            wavs.append(new_wav)
            last_chunk = chunk
        fpath = "output/%s/output_%02d.wav" % (DATE, file_no)
        file_no += 1
        generated_wav = np.concatenate(wavs)
        librosa.output.write_wav(fpath, generated_wav.astype(np.float32),  vc.synthesizer.sample_rate)
        print("\nSaved output as %s\n\n" % fpath)


