#!/bin/bash
# uso: narr.sh RATE  -> gera b00..bNN.wav aparados e imprime métricas
S=/tmp/claude-0/-home-user-claude-ash/2e6d7256-5f7a-57a7-8571-616b4a481510/scratchpad
. $S/vsenv/bin/activate; export SSL_CERT_FILE=/root/.ccr/ca-bundle.crt
RATE=$1; cd $S/narr
python3 -c "
import json;B=json.load(open('$S/frames/beats.json'))
for i,b in enumerate(B): open('b%02d.txt'%i,'w').write(b['s'])
"
for f in b*.txt; do n=${f%.txt}
  edge-tts --proxy "$HTTPS_PROXY" --voice pt-BR-AntonioNeural --rate=$RATE -f $f --write-media $n.mp3 2>/dev/null
  ffmpeg -loglevel error -y -i $n.mp3 -af "silenceremove=start_periods=1:start_threshold=-45dB:stop_periods=-1:stop_duration=0.09:stop_threshold=-45dB:stop_silence=0.13,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse" -ar 48000 -ac 1 $n.wav
done
python3 - <<'P'
import glob,subprocess
tw=tt=0
for w in sorted(glob.glob('b*.wav')):
  d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',w]))
  n=len(open(w[:-4]+'.txt').read().split());tw+=n;tt+=d
  print(w,n,'pal',round(d,2),'s',round(n/d,2),'p/s')
print('TOTAL',tw,'pal',round(tt,1),'s',round(tw/tt,2),'p/s')
P
