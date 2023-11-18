cd $(dirname -- "$0")/whisperX
. ./venv/bin/activate
whisperx --model large-v2 --align_model WAV2VEC2_ASR_LARGE_LV60K_960H --compute_type int8 --language en --output_format tsv - >/dev/null 2>/dev/null
cat ./-.tsv
rm ./-.tsv
