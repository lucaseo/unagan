import os
import librosa
from pydub import AudioSegment
import argparse



def process_one(items):
    filename, audio_path, output_dir, subclip_duration = items

    in_fp = os.path.join(audio_path, '{}.wav'.format(filename))
    print(in_fp)

    if not os.path.exists(in_fp):
        assert False, 'Not exists'


    duration = librosa.get_duration(filename=in_fp)

    num_subclips = int(duration // subclip_duration)

    try:
        song = AudioSegment.from_mp3(in_fp)

    except Exception:
        assert False, 'Error in loading'

    for ii in range(num_subclips):
        start = ii * subclip_duration
        end = (ii+1) * subclip_duration
        print(filename, start, end)

        output_fp = os.path.join(output_dir, '{}_{}_{}.mp3'.format(filename, start, end))
        if os.path.exists(output_fp):
            print('Done before')
            continue

        subclip = song[start * 1000 : end * 1000]
        subclip.export(output_fp, format='mp3')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--audio_path', default='./data/', type=str)

    args = parser.parse_args()

    output_dir = './training_data/clips/'
    subclip_duration = 10
    sr = 22050
    ext = '.wav'

    num_samples = int(round(subclip_duration * sr))
    os.makedirs(output_dir, exist_ok=True)

    list_ = []
    filenames = [fn.replace(ext, '') for fn in os.listdir(args.audio_path)]
    for fn in filenames:
        list_.append((
            fn,
            args.audio_path,
            output_dir,
            subclip_duration,
        ))

    for items in list_:
        process_one(items)