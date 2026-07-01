#!/usr/bin/env python3
"""Wide animated profile card: title / drinking portrait (left) + panels (right) / running forest."""
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageFont, ImageSequence
import os, math
_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets"); os.makedirs(_ASSETS, exist_ok=True)
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
W, H, S = 264, 316, 4
cx = 132          # card center (title + forest runner)
HX = 68           # hero + ruins center (left column)
_SD = os.path.dirname(os.path.abspath(__file__))

# ═══════════════════ EDIT THIS TO MAKE IT YOURS ═══════════════════
NAME     = "GABRIEL URS"
ARSENAL  = [("FRONT", "Vue · TypeScript · Tailwind"),        # (label, value)  — keep ~3 rows
            ("BACK",  "Laravel · PHP · REST"),
            ("INFRA", "Docker · Traefik · CI/CD")]
DUNGEONS = [("vertex",     "CRM multitenant",        ""),     # (name, desc, tag) — keep ~5 rows
            ("bportal",    "intranet corporativa",   ""),
            ("rportal",    "consultoría energética", ""),
            ("kyros-core", "núcleo del sistema",     "WIP"),
            ("is-tax-mod", "módulo fiscal",          "WIP")]
RUN_SPRITE   = "run-east.gif"     # side run cycle (faces right) -> forest runner
DRINK_SPRITE = "drink-south.gif"  # front idle             -> big portrait
# ══════════════════════════════════════════════════════════════════

_rg=Image.open(os.path.join(_SD,"..","sprites",RUN_SPRITE)); _rf=[f.convert("RGBA").copy() for f in ImageSequence.Iterator(_rg)]
_bx=[f.getbbox() for f in _rf]; _ub=(min(b[0] for b in _bx),min(b[1] for b in _bx),max(b[2] for b in _bx),max(b[3] for b in _bx))
RUN=[f.crop(_ub) for f in _rf]
_dg=Image.open(os.path.join(_SD,"..","sprites",DRINK_SPRITE)); _df=[f.convert("RGBA").copy() for f in ImageSequence.Iterator(_dg)]
_du=[f.getbbox() for f in _df]; _dub=(min(b[0] for b in _du),min(b[1] for b in _du),max(b[2] for b in _du),max(b[3] for b in _du))
DRINK=[f.crop(_dub) for f in _df]

MAG=(0xe0,0x48,0x5e); MAG_HI=(0xff,0x86,0x92); CYAN=(0x5f,0xe6,0xd2); TEALG=(0x2e,0xc4,0xa8); GOLD=(0xd8,0xb2,0x64)
CREAM=(0xe8,0xdc,0xba); DIM=(0x22,0x4e,0x52)
R1=(0x16,0x30,0x3c); R2=(0x20,0x3e,0x4a); R3=(0x2a,0x50,0x5a); R4=(0x20,0x38,0x42); R5=(0x2c,0x48,0x4e); R6=(0x10,0x22,0x2c)
BAYER=[[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]]
def clamp(c): return tuple(max(0,min(255,int(v))) for v in c)

# ---- top-down forest palette ----
GRASS=(0x1a,0x40,0x30); GRASS2=(0x15,0x35,0x28); PATHC=(0x43,0x43,0x30); PATH_ST=(0x55,0x52,0x3c)
TRUNK=(0x2e,0x22,0x18); CAN_D=(0x10,0x34,0x24); CAN_M=(0x1c,0x4e,0x36); CAN_L=(0x30,0x72,0x4a); CAN_HL=(0x4e,0x96,0x64)
FSHADOW=(0x0b,0x22,0x19); TUFT=(0x24,0x54,0x3a); FIRE=(0x9f,0xf8,0xe6)
FLOWER=[(0xff,0x6a,0x9a),(0xe6,0xc8,0x54),(0x6f,0xf0,0xda)]; MUSH=(0xc8,0x3a,0x46); MUSH_ST=(0xdc,0xd4,0xbc)
ROCK=(0x38,0x46,0x40); ROCK_L=(0x4c,0x5c,0x52); LEAF=[(0x3a,0x7a,0x54),(0xcc,0x96,0x50)]; DUST=(0x2c,0x3e,0x34)
Y0=200; PATH_Y0=Y0+56; PATH_Y1=Y0+76; FEET=Y0+72
BEHIND_P=80; BEHIND=[(14,Y0+20,9),(46,Y0+38,7),(66,Y0+12,11)]
FRONT_P=96;  FRONT=[(24,Y0+98,15),(70,Y0+106,12)]
LUMPS=[(0,0,1.0),(-0.64,0.10,0.54),(0.64,0.06,0.56),(-0.34,-0.44,0.50),(0.38,-0.42,0.46),
       (0.02,-0.64,0.44),(-0.52,-0.46,0.36),(0.52,-0.44,0.34),(0.24,0.44,0.46),(-0.30,0.42,0.44)]
def tree_td(d,x,y,r):
    x=int(x); y=int(y)
    d.ellipse([x-r,y-1,x+r,y+3],fill=FSHADOW); d.rectangle([x-1,y-int(r*0.7),x+2,y+2],fill=TRUNK)
    d.line([(x+1,y-int(r*0.6)),(x+1,y+1)],fill=(0x1c,0x14,0x0e)); cy=y-int(r*1.35)
    for (ox,oy,rr) in LUMPS:
        R=int(r*rr); d.ellipse([x+int(ox*r)-R,cy+int(oy*r)-R+1,x+int(ox*r)+R,cy+int(oy*r)+R+2],fill=CAN_D)
    for (ox,oy,rr) in LUMPS:
        R=int(r*rr); d.ellipse([x+int(ox*r)-R,cy+int(oy*r)-R,x+int(ox*r)+R,cy+int(oy*r)+R-1],fill=CAN_M)
    for (ox,oy,rr) in LUMPS:
        if oy<0.06:
            R=max(1,int(r*rr*0.52)); hx=x+int(ox*r)-int(R*0.4); hy=cy+int(oy*r)-int(R*0.5)
            d.ellipse([hx-R,hy-R,hx+R,hy+R],fill=CAN_L)
    for (ox,oy) in [(-0.14,-0.58),(-0.4,-0.3),(0.18,-0.46)]: d.point([(x+int(ox*r),cy+int(oy*r))],fill=CAN_HL)

def build_bg():
    img=Image.new("RGB",(W,H)); px=img.load()
    top=(0x14,0x2c,0x38); mid=(0x0a,0x16,0x1e); bot=(0x06,0x0e,0x14)
    for y in range(H):
        t=y/(H-1); g=tuple(top[i]+(mid[i]-top[i])*(t/0.5) for i in range(3)) if t<0.5 else tuple(mid[i]+(bot[i]-mid[i])*((t-0.5)/0.5) for i in range(3))
        for x in range(W):
            dist=math.hypot((x-HX),(y-120)/1.1); k=max(0.0,1-dist/86)
            rad=(0x2e*0.18*k*k,0xc4*0.18*k*k,0xa8*0.18*k*k)
            vd=math.hypot((x-cx)/(W*0.62),(y-H*0.5)/(H*0.62)); vig=max(0.4,1-vd*vd*0.85)
            dth=(BAYER[y&3][x&3]/16.0-0.5)*7; px[x,y]=clamp(tuple((g[i]+rad[i])*vig+dth for i in range(3)))
    return img

def build_ruins():
    mask=Image.new("L",(W,H),0); ImageDraw.Draw(mask).polygon([(HX,54),(HX+62,124),(HX,194),(HX-62,124)],fill=255)
    lay=Image.new("RGBA",(W,H),(0,0,0,0)); hd=ImageDraw.Draw(lay)
    L=[([(10,120),(10,72),(16,68),(22,72),(22,120)],R2),([(6,100),(12,96),(12,116),(6,116)],R6),
       ([(24,150),(24,110),(32,104),(32,150)],R1),([(24,116),(40,98),(46,104),(30,124)],R4),
       ([(34,70),(44,64),(42,84),(34,88)],R2),([(16,66),(24,60),(22,74),(16,76)],R3),
       ([(44,120),(52,110),(56,150),(48,150)],R1),([(30,96),(38,90),(38,102),(30,104)],R5)]
    for (pts,c) in L:
        hd.polygon(pts,fill=c+(255,)); hd.polygon([(2*HX-x,y) for (x,y) in pts],fill=c+(255,))
    hd.line([(HX-12,150),(HX-11,96)],fill=(0x5f,0xe6,0xd2,150))
    lay.putalpha(ImageChops.multiply(lay.getchannel("A"),mask)); return lay
RUINS=build_ruins()

def hud_panel(d,x0,y0,x1,y1,cut=6):
    pts=[(x0+cut,y0),(x1-cut,y0),(x1,y0+cut),(x1,y1-cut),(x1-cut,y1),(x0+cut,y1),(x0,y1-cut),(x0,y0+cut)]
    d.polygon(pts,fill=(0x0c,0x1a,0x20),outline=DIM)
    for (a,b) in [(x0+cut,y0),(x1-cut,y0),(x1-cut,y1),(x0+cut,y1)]: d.point([(a,b)],fill=CYAN)

def build_base():
    img=build_bg(); d=ImageDraw.Draw(img)   # clean portrait backdrop (no ruins clutter)
    def dia(x,y,r,c): d.polygon([(x,y-r),(x+r,y),(x,y+r),(x-r,y)],fill=c)
    d.rectangle([4,4,W-5,H-5],outline=DIM)
    for (X,Y) in [(4,4),(W-5,4),(4,H-5),(W-5,H-5)]: dia(X,Y,2,CYAN)
    hud_panel(d,136,54,256,116); hud_panel(d,136,124,256,196)
    # forest band: grass field + dirt path (static)
    d.line([(16,Y0),(W-16,Y0)],fill=DIM)
    for y in range(Y0+2,H-5):
        f=(y-Y0)/(H-Y0); g=tuple(int(GRASS2[i]+(GRASS[i]-GRASS2[i])*f) for i in range(3))
        for x in range(6,W-6):
            dth=int((BAYER[y&3][x&3]/16-0.5)*7); img.putpixel((x,y),tuple(max(0,min(255,c+dth)) for c in g))
    d.rectangle([6,PATH_Y0,W-6,PATH_Y1],fill=PATHC)
    return img
BASE=build_base()

def draw_ui(big):
    dd=ImageDraw.Draw(big)
    def F(s,bold=True): return ImageFont.truetype(FB if bold else FR,s)
    def dia(x,y,r,c): dd.polygon([(x,y-r),(x+r,y),(x,y+r),(x-r,y)],fill=c)
    def center(text,y,size,fill,sp):
        f=F(size); w=sum(dd.textlength(c,font=f)+sp for c in text)-sp; x=(W*S-w)/2
        for ch in text: dd.text((x,y),ch,font=f,fill=fill); x+=dd.textlength(ch,font=f)+sp
    center(NAME,42,42,(0xf2,0xea,0xd2),4)
    ry=112; dd.line([(300,ry),(W*S-300,ry)],fill=(0x2a,0x6c,0x64),width=2)
    for X in (300,W*S//2,W*S-300): dia(X,ry,5,CYAN)
    ax=600   # content shifted right so the block is centered in the panels
    dia(ax-18,264,7,MAG); dd.text((ax,246),"ARSENAL",font=F(25),fill=CREAM)
    y=302
    for lab,val in ARSENAL:
        dd.text((ax,y),lab,font=F(18),fill=CYAN); dd.text((ax+150,y+1),val,font=F(16,False),fill=CREAM); y+=48
    dia(ax-18,528,7,MAG); dd.text((ax,510),"DUNGEONS",font=F(25),fill=CREAM)
    y=562
    for name,desc,tag in DUNGEONS:
        dd.text((ax,y),name,font=F(17),fill=CYAN); dd.text((ax+150,y+1),desc,font=F(15,False),fill=(0xbe,0xd2,0xc6))
        if tag: dd.text((ax+340,y+2),tag,font=F(13),fill=GOLD)
        y+=43

def frame_glows(t):
    tau=2*math.pi*t; g=[(HX,124,30,TEALG,0.16),(cx,24,34,(0xd0,0x50,0x64),0.11)]
    for (a,b,ph) in [(40,Y0+30,0.0),(214,Y0+22,0.5),(150,Y0+44,0.3),(232,Y0+36,0.8)]:
        g.append((a,b,3,FIRE,0.5+0.3*math.sin(tau*2+ph*6.28)))
    for (X,Y) in [(4,4),(W-5,4),(4,H-5),(W-5,H-5)]: g.append((X,Y,4,(69,230,204),0.55))
    return g

def frame(t,S):
    scene=BASE.copy(); d=ImageDraw.Draw(scene); tau=2*math.pi*t; dyn=[]
    for (a,b,c) in [(18,88,CYAN),(120,92,MAG_HI)]:   # sparkles above the portrait
        d.polygon([(a,b-1),(a+1,b),(a,b+1),(a-1,b)],fill=c)
    # ===== top-down forest (full width; runner faces right, world scrolls left) =====
    def tiled(p,fn):
        off=t*p
        for i in range(-1, W//p+2): fn(i*p-off)
    def path_edge(bx):
        gx=int(bx); d.line([(gx,PATH_Y0),(gx+1,PATH_Y0-2),(gx+2,PATH_Y0)],fill=TUFT); d.line([(gx+4,PATH_Y1),(gx+5,PATH_Y1+2),(gx+6,PATH_Y1)],fill=TUFT)
    tiled(11,path_edge)
    def path_st(bx):
        gx=int(bx); d.ellipse([gx,PATH_Y0+8,gx+2,PATH_Y0+10],fill=PATH_ST); d.point([(gx+14,PATH_Y1-5)],fill=PATH_ST)
    tiled(30,path_st)
    def tufts(bx):
        gx=int(bx); d.line([(gx,Y0+12),(gx+1,Y0+9),(gx+2,Y0+12)],fill=TUFT); d.line([(gx+7,Y0+48),(gx+8,Y0+46),(gx+9,Y0+48)],fill=TUFT)
    tiled(18,tufts)
    def scen_b(bx):                                   # flowers + mushroom above the path
        gx=int(bx)
        for (fx,fy,fc) in [(20,Y0+14,FLOWER[0]),(21,Y0+16,FLOWER[1]),(56,Y0+40,FLOWER[2])]: d.point([(gx+fx,fy)],fill=fc)
        d.rectangle([gx+40,Y0+30,gx+41,Y0+33],fill=MUSH_ST); d.ellipse([gx+38,Y0+27,gx+43,Y0+30],fill=MUSH); d.point([(gx+39,Y0+28)],fill=(0xf0,0xe8,0xd8))
    tiled(88,scen_b)
    def behind(bx):
        for (ox,oy,r) in sorted(BEHIND,key=lambda e:e[1]): tree_td(d,bx+ox,oy,r)
    tiled(BEHIND_P,behind)
    def shrine(bx):                                   # glowing monolith landmark (scrolls past)
        x=int(bx+40); base=Y0+44
        d.rectangle([x-6,base,x+7,base+3],fill=(0x12,0x2c,0x32))
        d.polygon([(x-4,base),(x-3,base-30),(x+1,base-34),(x+4,base-30),(x+5,base)],fill=(0x1a,0x38,0x40))
        d.polygon([(x+1,base-34),(x+4,base-30),(x+2,base-32)],fill=(0x2a,0x50,0x56))
        d.line([(x,base-6),(x+1,base-18),(x,base-28)],fill=(0x6f,0xf0,0xe0))
        dyn.append((x,base-16,9,(69,230,204),0.55+0.3*math.sin(tau*1.5)))
    tiled(176,shrine)
    def campfire(bx):                                 # cozy fire (warm accent, flickers)
        x=int(bx+50); y=Y0+50
        d.line([(x-5,y),(x+5,y)],fill=(0x3a,0x28,0x1c)); d.line([(x-4,y-1),(x+3,y-1)],fill=(0x24,0x18,0x10))
        fl=int(2*math.sin(tau*6))
        d.polygon([(x,y-10-fl),(x-3,y-2),(x+3,y-2)],fill=(0xff,0x7a,0x2a)); d.polygon([(x,y-6-fl),(x-2,y-2),(x+2,y-2)],fill=(0xff,0xd0,0x5a))
        dyn.append((x,y-5,11,(255,150,60),0.6+0.3*math.sin(tau*6)))
    tiled(220,campfire)
    for (a,b,ph) in [(40,Y0+30,0.0),(214,Y0+22,0.5),(150,Y0+44,0.3),(232,Y0+36,0.8)]:
        yy=b+round(3*math.sin(tau+ph*6.28)); d.point([(a,yy)],fill=FIRE)
    if int(t*12)%6 in (1,4): d.ellipse([cx-16,FEET-1,cx-11,FEET+2],fill=DUST)   # footfall dust
    d.ellipse([cx-8,FEET-2,cx+8,FEET+3],fill=FSHADOW)
    cf=RUN[int(t*12)%len(RUN)]; scene.paste(cf,(cx-cf.width//2,FEET-cf.height+1),cf)
    def front(bx):
        for (ox,oy,r) in sorted(FRONT,key=lambda e:e[1]): tree_td(d,bx+ox,oy,r)
    tiled(FRONT_P,front)
    def pond(bx):                                    # pond with animated shimmer (scrolls past)
        x=int(bx+30); y=Y0+96
        d.ellipse([x-14,y-5,x+14,y+5],fill=(0x14,0x30,0x3c)); d.ellipse([x-14,y-5,x+14,y+5],outline=(0x2a,0x58,0x54))
        sh=int(3*math.sin(tau*2))
        d.line([(x-6+sh,y-1),(x+2+sh,y-1)],fill=(0x4a,0x9a,0x90)); d.line([(x-3-sh,y+2),(x+5-sh,y+2)],fill=(0x36,0x74,0x70))
        d.ellipse([x+8,y-3,x+11,y-1],fill=(0x1e,0x50,0x36))
    tiled(200,pond)
    def crystals(bx):                                # HLD crystal cluster (glows)
        x=int(bx+40); y=Y0+94
        for (dx,h,col) in [(-4,9,(0xe0,0x48,0x8e)),(2,14,(0x5f,0xe6,0xd2)),(6,7,(0xa0,0x6a,0xe0))]:
            d.polygon([(x+dx,y-h),(x+dx-2,y),(x+dx+2,y)],fill=col)
        dyn.append((x+2,y-8,8,(120,220,220),0.5+0.3*math.sin(tau*2)))
    tiled(190,crystals)
    def scen_f(bx):                                  # rock + flowers + bush in the foreground
        gx=int(bx)
        d.ellipse([gx+15,Y0+94,gx+21,Y0+97],fill=ROCK); d.line([(gx+16,Y0+94),(gx+19,Y0+94)],fill=ROCK_L)
        for (fx,fy,fc) in [(50,Y0+104,FLOWER[0]),(51,Y0+106,FLOWER[1])]: d.point([(gx+fx,fy)],fill=fc)
        tree_td(d,gx+72,Y0+106,6)
    tiled(100,scen_f)
    bandh=H-Y0-6                                      # falling leaves (seamless drift)
    for (lx,ph,ci) in [(24,0.0,0),(96,0.35,1),(150,0.6,0),(210,0.15,1),(244,0.8,0)]:
        prog=(t+ph)%1.0; yy=Y0+4+int(prog*bandh); xx=lx+int(7*math.sin(prog*9.4+ph*6))
        d.point([(xx,yy),(xx+1,yy),(xx,yy+1)],fill=LEAF[ci])
    d.rectangle([4,4,W-5,H-5],outline=DIM)
    big=scene.resize((W*S,H*S),Image.NEAREST)
    gl=Image.new("RGB",big.size,(0,0,0)); gd=ImageDraw.Draw(gl)
    for (gx,gy,gr,gc,gi) in frame_glows(t)+dyn:
        GX,GY,GR=gx*S,gy*S,gr*S; gd.ellipse([GX-GR,GY-GR,GX+GR,GY+GR],fill=tuple(int(min(255,c*gi)) for c in gc))
    big=ImageChops.screen(big,gl.filter(ImageFilter.GaussianBlur(radius=S*2.5)))
    # drinking portrait (left column, chill loop)
    hf=DRINK[int(t*6)%len(DRINK)]; sp=hf.resize((hf.width*11,hf.height*11),Image.NEAREST)
    big.paste(sp,(HX*S-sp.width//2, 500-sp.height//2),sp)   # centered with the panels block
    draw_ui(big); return big

frame(0.0,4).save(_ASSETS+"/readme.png"); print("still")
N=24; frames=[frame(i/N,4) for i in range(N)]
pal=frames[0].quantize(colors=100,method=Image.MEDIANCUT)
fp=[f.quantize(palette=pal,dither=Image.Dither.NONE) for f in frames]
fp[0].save(_ASSETS+"/readme.gif",save_all=True,append_images=fp[1:],duration=60,loop=0,optimize=True,disposal=1)
print("gif",N)
