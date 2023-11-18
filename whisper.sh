if [ "$#" -ge 1 ]; then
    ffmpeg -i "$1" -ar 16000 -ac 1 -c:a pcm_s16le -f wav - 2>/dev/null
else
    cat
fi | (
    cd $(dirname -- "$0")/whisperX
    . ./venv/bin/activate
    whisperx --model large-v2 --align_model WAV2VEC2_ASR_LARGE_LV60K_960H --compute_type int8 --language en --output_format tsv - >/dev/null 2>/dev/null
    tail -n+2 ./-.tsv
    rm ./-.tsv
)
