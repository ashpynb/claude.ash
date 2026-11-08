import sys,json,time,torch,soundfile as sf
sys.path.insert(0,'/home/user/MakramAli20/freeElevenlabs')
from omnivoice.models.omnivoice import OmniVoice
jobs=json.load(open(sys.argv[1]))
m=OmniVoice.from_pretrained('k2-fsa/OmniVoice',device_map='cpu',dtype=torch.float32)
for j in jobs:
    t=time.time()
    a=m.generate(text=j['text'],language='pt',instruct=j.get('instruct'),duration=j.get('duration'),speed=j.get('speed',1.0),num_step=j.get('steps',32))
    w=a[0].squeeze().float().cpu().numpy()
    sf.write(j['out'],w,m.sampling_rate)
    print(j['out'],round(len(w)/m.sampling_rate,2),'s, took',round(time.time()-t,1),flush=True)
