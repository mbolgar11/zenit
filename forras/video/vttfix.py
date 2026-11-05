import re,sys
def fix(p):
    s=open(p,encoding='utf8').read(); blocks=s.strip().split('\n\n'); head=blocks[0]; cues=[]
    for b in blocks[1:]:
        L=b.split('\n'); m=re.match(r'(\S+) --> (\S+)',L[1]); cues.append([L[0],m.group(1),m.group(2),'\n'.join(L[2:])])
    sec=lambda t:int(t[:2])*3600+int(t[3:5])*60+float(t[6:])
    ts=lambda t:f"{int(t//3600):02d}:{int(t%3600//60):02d}:{t%60:06.3f}"
    for i in range(len(cues)-1):
        if sec(cues[i][2])>sec(cues[i+1][1])-0.05: cues[i][2]=ts(sec(cues[i+1][1])-0.05)
    open(p,'w',encoding='utf8').write(head+'\n\n'+'\n\n'.join(f"{c[0]}\n{c[1]} --> {c[2]}\n{c[3]}" for c in cues)+'\n')
for p in sys.argv[1:]: fix(p)
