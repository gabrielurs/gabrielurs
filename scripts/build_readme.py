#!/usr/bin/env python3
"""Cohesive HLD poster+UI, animated. Humanoid masked drifter + atmosphere + HUD panels."""
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps, ImageFont, ImageSequence
import os, math
_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(_ASSETS, exist_ok=True)
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
W, H, S = 160, 446, 4
cx = 80
_SD = os.path.dirname(os.path.abspath(__file__))
# ---- top-down forest band (matches the 3/4 character perspective) ----
Y0=322                                                   # band top (below the RUINS panel)
GRASS=(0x1a,0x40,0x30); GRASS2=(0x15,0x35,0x28); PATHC=(0x43,0x43,0x30); PATH_ST=(0x55,0x52,0x3c)
TRUNK=(0x2e,0x22,0x18); CAN_D=(0x10,0x34,0x24); CAN_M=(0x1c,0x4e,0x36); CAN_L=(0x30,0x72,0x4a); CAN_HL=(0x4e,0x96,0x64)
FSHADOW=(0x0b,0x22,0x19); TUFT=(0x24,0x54,0x3a); FIRE=(0x9f,0xf8,0xe6)
PATH_Y0=Y0+60; PATH_Y1=Y0+82; FEET=Y0+78
BEHIND_P=80; BEHIND=[(14,Y0+22,9),(46,Y0+42,7),(66,Y0+14,11)]     # (x,y,r) far, above path
FRONT_P=96;  FRONT=[(24,Y0+104,15),(70,Y0+112,12)]               # near, below path (drawn in front)
LUMPS=[(0,0,1.0),(-0.64,0.10,0.54),(0.64,0.06,0.56),(-0.34,-0.44,0.50),(0.38,-0.42,0.46),
       (0.02,-0.64,0.44),(-0.52,-0.46,0.36),(0.52,-0.44,0.34),(0.24,0.44,0.46),(-0.30,0.42,0.44)]
def tree_td(d,x,y,r):
    x=int(x); y=int(y)
    d.ellipse([x-r,y-1,x+r,y+3],fill=FSHADOW)                     # ground shadow
    d.rectangle([x-1,y-int(r*0.7),x+2,y+2],fill=TRUNK)            # trunk (3/4)
    d.line([(x+1,y-int(r*0.6)),(x+1,y+1)],fill=(0x1c,0x14,0x0e))
    cy=y-int(r*1.35)                                              # canopy above trunk
    for (ox,oy,rr) in LUMPS:
        R=int(r*rr); d.ellipse([x+int(ox*r)-R,cy+int(oy*r)-R+1,x+int(ox*r)+R,cy+int(oy*r)+R+2],fill=CAN_D)
    for (ox,oy,rr) in LUMPS:
        R=int(r*rr); d.ellipse([x+int(ox*r)-R,cy+int(oy*r)-R,x+int(ox*r)+R,cy+int(oy*r)+R-1],fill=CAN_M)
    for (ox,oy,rr) in LUMPS:
        if oy<0.06:
            R=max(1,int(r*rr*0.52)); hx=x+int(ox*r)-int(R*0.4); hy=cy+int(oy*r)-int(R*0.5)
            d.ellipse([hx-R,hy-R,hx+R,hy+R],fill=CAN_L)
    for (ox,oy) in [(-0.14,-0.58),(-0.4,-0.3),(0.18,-0.46)]:
        d.point([(x+int(ox*r),cy+int(oy*r))],fill=CAN_HL)
# --- running character: 6-frame east (right-facing) cycle ---
_rg=Image.open(os.path.join(_SD,"..","sprites","run-east.gif"))
_rf=[f.convert("RGBA").copy() for f in ImageSequence.Iterator(_rg)]
_bx=[f.getbbox() for f in _rf]
_ub=(min(b[0] for b in _bx),min(b[1] for b in _bx),max(b[2] for b in _bx),max(b[3] for b in _bx))
RUN=[f.crop(_ub) for f in _rf]
# --- chill idle: character drinking (front) — used for the big portrait ---
_dg=Image.open(os.path.join(_SD,"..","sprites","drink-south.gif"))
_df=[f.convert("RGBA").copy() for f in ImageSequence.Iterator(_dg)]
_du=[f.getbbox() for f in _df]
_dub=(min(b[0] for b in _du),min(b[1] for b in _du),max(b[2] for b in _du),max(b[3] for b in _du))
DRINK=[f.crop(_dub) for f in _df]

MAG=(0xe0,0x48,0x5e); MAG_HI=(0xff,0x86,0x92); MAG_DK=(0x8a,0x26,0x36)   # crimson (scarf)
PUR=(0x6a,0x40,0xa8); PUR_DK=(0x35,0x1e,0x60); PUR_LT=(0x9a,0x74,0xd8)
LAV=(0xa6,0x8c,0xe6); LAV_DK=(0x6f,0x54,0xb0); LAV_HI=(0xc6,0xb2,0xf2)
ROBE=(0x22,0x13,0x3e); ROBE_D=(0x16,0x0c,0x2a)
MASKW=(0xee,0xe8,0xd8); MASK_SH=(0xcf,0xc6,0xb0)
CYAN=(0x5f,0xe6,0xd2); EYE=(0xff,0x2d,0x8a); TEALG=(0x2e,0xc4,0xa8); GOLD=(0xd8,0xb2,0x64)
R1=(0x16,0x30,0x3c); R2=(0x20,0x3e,0x4a); R3=(0x2a,0x50,0x5a)
R4=(0x20,0x38,0x42); R5=(0x2c,0x48,0x4e); R6=(0x10,0x22,0x2c)
CREAM=(0xe8,0xdc,0xba); DIM=(0x22,0x4e,0x52)
CLOAK=(0x33,0x20,0x5c); CLOAK_D=(0x1f,0x12,0x3c); CLOAK_L=(0x46,0x2e,0x78); FACE=(0x0e,0x0a,0x1e)
BAYER=[[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]]
def clamp(c): return tuple(max(0,min(255,int(v))) for v in c)

def build_bg():
    img=Image.new("RGB",(W,H)); px=img.load()
    top=(0x14,0x2c,0x38); mid=(0x0a,0x16,0x1e); bot=(0x06,0x0e,0x14)
    for y in range(H):
        t=y/(H-1)
        g=tuple(top[i]+(mid[i]-top[i])*(t/0.5) for i in range(3)) if t<0.5 else tuple(mid[i]+(bot[i]-mid[i])*((t-0.5)/0.5) for i in range(3))
        for x in range(W):
            dist=math.hypot((x-cx),(y-104)/1.15); k=max(0.0,1-dist/78)
            rad=(0x2e*0.18*k*k,0xc4*0.18*k*k,0xa8*0.18*k*k)
            vd=math.hypot((x-cx)/(W*0.62),(y-H*0.5)/(H*0.62)); vig=max(0.35,1-vd*vd*0.9)
            dth=(BAYER[y&3][x&3]/16.0-0.5)*7
            px[x,y]=clamp(tuple((g[i]+rad[i])*vig+dth for i in range(3)))
    return img

def build_ruins():
    mask=Image.new("L",(W,H),0)
    ImageDraw.Draw(mask).polygon([(cx,42),(150,116),(cx,192),(10,116)],fill=255)
    half=Image.new("RGBA",(W,H),(0,0,0,0)); hd=ImageDraw.Draw(half)
    L=[([(16,156),(16,84),(23,78),(31,84),(31,156)],R2),([(23,78),(31,84),(27,80)],R3),
       ([(8,136),(16,124),(16,156),(8,156)],R1),([(8,100),(16,96),(16,120),(8,120)],R6),
       ([(34,154),(34,108),(44,100),(44,154)],R1),([(33,114),(52,94),(59,102),(39,124)],R4),
       ([(37,142),(56,132),(54,156),(37,158)],R6),([(46,70),(59,64),(56,86),(46,90)],R2),
       ([(24,68),(34,62),(32,78),(24,80)],R3),([(50,154),(68,154),(68,166),(54,168)],R2),
       ([(56,120),(66,108),(70,154),(60,154)],R1),([(40,96),(49,90),(49,104),(40,106)],R5),
       ([(61,76),(67,72),(67,154),(61,154)],R1),([(70,122),(75,114),(75,154),(70,154)],R2)]
    for (p,c) in L: hd.polygon(p,fill=c+(255,))
    hd.line([(16,84),(23,78)],fill=(0x4c,0x9c,0x8c,255)); hd.line([(23,78),(31,84)],fill=(0x4c,0x9c,0x8c,255))
    hd.line([(23,84),(23,150)],fill=(0x5f,0xe6,0xd2,150))
    ruins=Image.alpha_composite(half,ImageOps.mirror(half))
    ruins.putalpha(ImageChops.multiply(ruins.getchannel("A"),mask))
    far=ruins.resize((int(W*0.9),int(H*0.9))).convert("RGBA")
    faro=Image.new("RGBA",(W,H),(0,0,0,0)); faro.paste(far,(int(W*0.05),int(H*0.03)),far)
    faro.putalpha(faro.getchannel("A").point(lambda a:a//3))
    out=Image.alpha_composite(Image.alpha_composite(Image.new("RGBA",(W,H),(0,0,0,0)),faro),ruins)
    return out
RUINS=build_ruins()

def hud_panel(d,x0,y0,x1,y1,cut=6):
    pts=[(x0+cut,y0),(x1-cut,y0),(x1,y0+cut),(x1,y1-cut),(x1-cut,y1),(x0+cut,y1),(x0,y1-cut),(x0,y0+cut)]
    d.polygon(pts,fill=(0x0c,0x1a,0x20),outline=DIM)
    for (a,b) in [(x0+cut,y0),(x1-cut,y0),(x1-cut,y1),(x0+cut,y1)]: d.point([(a,b)],fill=CYAN)

def build_base():
    img=build_bg(); img.paste(RUINS,(0,0),RUINS)
    d=ImageDraw.Draw(img)
    def dia(x,y,r,c): d.polygon([(x,y-r),(x+r,y),(x,y+r),(x-r,y)],fill=c)
    # (the real character sprite is composited in frame(), not drawn here)
    # --- outer frame + panels ---
    d.rectangle([4,4,W-5,H-5],outline=DIM)
    for (X,Y) in [(4,4),(W-5,4),(4,H-5),(W-5,H-5)]: dia(X,Y,2,CYAN)
    hud_panel(d,9,199,W-10,245); hud_panel(d,9,251,W-10,313)
    # --- forest band: static ground ---
    d.line([(16,Y0),(W-16,Y0)],fill=DIM)
    for y in range(Y0+2,H-5):                                # top-down grass field
        f=(y-Y0)/(H-Y0); g=tuple(int(GRASS2[i]+(GRASS[i]-GRASS2[i])*f) for i in range(3))
        for x in range(6,W-6):
            dth=int((BAYER[y&3][x&3]/16-0.5)*7); img.putpixel((x,y),tuple(max(0,min(255,c+dth)) for c in g))
    d.rectangle([6,PATH_Y0,W-6,PATH_Y1],fill=PATHC)          # dirt path the runner follows
    return img
BASE=build_base()

def draw_ui(big):
    dd=ImageDraw.Draw(big)
    def F(s,bold=True): return ImageFont.truetype(FB if bold else FR,s)
    def dia(x,y,r,c): dd.polygon([(x,y-r),(x+r,y),(x,y+r),(x-r,y)],fill=c)
    def center(text,y,size,fill,sp):
        f=F(size); w=sum(dd.textlength(c,font=f)+sp for c in text)-sp; x=(W*S-w)/2
        for ch in text: dd.text((x,y),ch,font=f,fill=fill); x+=dd.textlength(ch,font=f)+sp
    center("GABRIEL URS",64,48,(0xf2,0xea,0xd2),4)
    ry=150; dd.line([(150,ry),(W*S-150,ry)],fill=(0x2a,0x6c,0x64),width=2)
    for X in (150,W*S//2,W*S-150): dia(X,ry,5,CYAN)
    LM=64
    dia(LM-8,824,7,MAG); dd.text((LM+12,806),"ARSENAL",font=F(25),fill=CREAM)
    y=850
    for lab,val in [("FRONT","Vue · TypeScript · Tailwind"),("BACK","Laravel · PHP · REST"),("INFRA","Docker · Traefik · CI/CD")]:
        dd.text((LM,y),lab,font=F(19),fill=CYAN); dd.text((LM+165,y+1),val,font=F(18,False),fill=CREAM); y+=37
    dia(LM-8,1032,7,MAG); dd.text((LM+12,1014),"DUNGEONS",font=F(25),fill=CREAM)
    y=1058
    for name,desc,tag in [("vertex","CRM multitenant",""),("bportal","intranet corporativa",""),("rportal","consultoría energética",""),("kyros-core","núcleo del sistema","WIP"),("is-tax-mod","módulo fiscal","WIP")]:
        dd.text((LM,y),name,font=F(18),fill=CYAN); dd.text((LM+180,y+1),desc,font=F(17,False),fill=(0xbe,0xd2,0xc6))
        if tag:
            fw=F(14); dd.text(((W-10)*S-16-dd.textlength(tag,font=fw),y+2),tag,font=fw,fill=GOLD)
        y+=36

def frame_glows(t):
    tau=2*math.pi*t; g=[]
    g+=[(cx,100,28,TEALG,0.16),(cx,20,34,(0xd0,0x50,0x64),0.11)]   # teal seat glow + warm title glow
    for (a,b,ph) in [(30,Y0+42,0.0),(120,Y0+32,0.5),(96,Y0+52,0.3),(140,Y0+46,0.8)]:   # fireflies
        g.append((a,b,3,(0x9f,0xf8,0xe6),0.5+0.3*math.sin(tau*2+ph*6.28)))
    for (X,Y) in [(4,4),(W-5,4),(4,H-5),(W-5,H-5)]: g.append((X,Y,4,(69,230,204),0.55))
    return g

def frame(t,S):
    scene=BASE.copy(); d=ImageDraw.Draw(scene); tau=2*math.pi*t
    # ===== forest band (west sprite running left, world scrolls right) =====
    # ===== top-down forest scene (scrolls left; runner faces right) =====
    def tiled(p,fn):
        off=t*p
        for i in range(-1, W//p+2): fn(i*p-off)
    def path_edge(bx):                                          # grass tufts on the path edges
        gx=int(bx)
        d.line([(gx,PATH_Y0),(gx+1,PATH_Y0-2),(gx+2,PATH_Y0)],fill=TUFT)
        d.line([(gx+4,PATH_Y1),(gx+5,PATH_Y1+2),(gx+6,PATH_Y1)],fill=TUFT)
    tiled(11,path_edge)
    def path_st(bx):                                            # path stones
        gx=int(bx); d.ellipse([gx,PATH_Y0+8,gx+2,PATH_Y0+10],fill=PATH_ST); d.point([(gx+14,PATH_Y1-5)],fill=PATH_ST)
    tiled(30,path_st)
    def tufts(bx):                                              # grass tufts on the field
        gx=int(bx); d.line([(gx,Y0+12),(gx+1,Y0+9),(gx+2,Y0+12)],fill=TUFT); d.line([(gx+7,Y0+50),(gx+8,Y0+48),(gx+9,Y0+50)],fill=TUFT)
    tiled(18,tufts)
    def behind(bx):                                             # trees above the path (far)
        for (ox,oy,r) in sorted(BEHIND,key=lambda e:e[1]): tree_td(d,bx+ox,oy,r)
    tiled(BEHIND_P,behind)
    for (a,b,ph) in [(30,Y0+42,0.0),(120,Y0+32,0.5),(96,Y0+52,0.3),(140,Y0+46,0.8)]:   # fireflies
        yy=b+round(3*math.sin(tau+ph*6.28)); d.point([(a,yy)],fill=FIRE)
    d.ellipse([cx-8,FEET-2,cx+8,FEET+3],fill=FSHADOW)           # runner shadow
    cf=RUN[int(t*12)%len(RUN)]; scene.paste(cf,(cx-cf.width//2,FEET-cf.height+1),cf)
    def front(bx):                                              # trees below the path (near, in front)
        for (ox,oy,r) in sorted(FRONT,key=lambda e:e[1]): tree_td(d,bx+ox,oy,r)
    tiled(FRONT_P,front)
    d.rectangle([4,4,W-5,H-5],outline=DIM)
    for (a,b,c) in [(30,110,CYAN),(128,120,MAG_HI),(24,170,CYAN),(132,175,MAG_HI),(46,60,CYAN),(112,64,MAG_HI)]:
        d.polygon([(a,b-1),(a+1,b),(a,b+1),(a-1,b)],fill=c)     # static (upper card frozen for small GIF)
    big=scene.resize((W*S,H*S),Image.NEAREST)
    gl=Image.new("RGB",big.size,(0,0,0)); gd=ImageDraw.Draw(gl)
    for (gx,gy,gr,gc,gi) in frame_glows(t):
        GX,GY,GR=gx*S,gy*S,gr*S
        gd.ellipse([GX-GR,GY-GR,GX+GR,GY+GR],fill=tuple(int(min(255,c*gi)) for c in gc))
    big=ImageChops.screen(big,gl.filter(ImageFilter.GaussianBlur(radius=S*2.5)))
    # --- composite the real character sprite (idle bob) ---
    fscale=9
    hf=DRINK[int(t*6)%len(DRINK)]                     # slow chill drinking loop
    sp=hf.resize((hf.width*fscale,hf.height*fscale),Image.NEAREST)
    big.paste(sp,((big.width-sp.width)//2,235),sp)
    draw_ui(big); return big

frame(0.0,4).save(_ASSETS+"/readme.png"); print("still")
N=24; frames=[frame(i/N,4) for i in range(N)]
pal=frames[0].quantize(colors=88,method=Image.MEDIANCUT)
fp=[f.quantize(palette=pal,dither=Image.Dither.NONE) for f in frames]
fp[0].save(_ASSETS+"/readme.gif",save_all=True,append_images=fp[1:],duration=60,loop=0,optimize=True,disposal=1)
print("gif",N)
