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

# ===== biome band (forest -> desert -> snow), local coords 0..BH =====
BH=H-Y0; LP0=PATH_Y0-Y0; LP1=PATH_Y1-Y0
BEHIND_L=[(14,20,9),(46,38,7),(66,12,11)]; FRONT_L=[(24,98,15),(70,106,12)]
def lerp(a,b,t): return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))
def cactus(d,x,y,r):
    x=int(x);y=int(y); h=int(r*2.3); col=(0x2e,0x6e,0x3e); dk=(0x1c,0x4a,0x2c); hi=(0x4a,0x92,0x52)
    d.ellipse([x-4,y-1,x+4,y+2],fill=(0x18,0x12,0x0c))
    d.rectangle([x-2,y-h,x+2,y],fill=col); d.line([(x-2,y-h+2),(x-2,y)],fill=dk); d.line([(x+2,y-h+2),(x+2,y)],fill=hi)
    d.rectangle([x-6,y-int(h*0.6),x-2,y-int(h*0.5)],fill=col); d.rectangle([x-6,y-int(h*0.6),x-4,y-int(h*0.32)],fill=col)
    d.rectangle([x+2,y-int(h*0.72),x+6,y-int(h*0.62)],fill=col); d.rectangle([x+4,y-int(h*0.72),x+6,y-int(h*0.42)],fill=col)
    d.line([(x,y-h+1),(x,y-h+4)],fill=hi)
def snowpine(d,x,y,r):
    x=int(x);y=int(y); sz=int(r*2.4); d.ellipse([x-sz//2,y-1,x+sz//2,y+3],fill=(0x18,0x24,0x30))
    d.rectangle([x-1,y-int(sz*0.16),x+2,y],fill=(0x2e,0x26,0x20)); top=y-sz
    for k in range(4):
        f=k/3.0; ty=top+int(sz*0.62*f); by=top+int(sz*(0.62*f+0.44)); w=int(sz*(0.16+0.20*f))
        d.polygon([(x,ty),(x-w,by),(x+w,by)],fill=(0x26,0x4c,0x42))            # green tier
        my=ty+int((by-ty)*0.52); mw=max(1,int(w*0.66))
        d.polygon([(x,ty),(x-mw,my),(x+mw,my)],fill=(0xe6,0xf0,0xf6))          # snow only on the top part
        d.point([(x-w+1,by-2),(x+w-2,by-2)],fill=(0xcc,0xda,0xe6))
def barrel(d,x,y):                                                            # small round cactus
    d.ellipse([x-4,y+1,x+4,y+3],fill=(0x2a,0x1e,0x12)); d.ellipse([x-3,y-5,x+3,y+2],fill=(0x38,0x76,0x46))
    d.line([(x-1,y-4),(x-1,y+1)],fill=(0x22,0x50,0x32)); d.line([(x+1,y-4),(x+1,y+1)],fill=(0x22,0x50,0x32)); d.point([(x,y-5)],fill=(0xff,0xd0,0x60))
def band(biome,t):
    if biome=='forest': g0,g1,pth,edg=(0x1a,0x40,0x30),(0x12,0x2e,0x22),(0x3a,0x3e,0x2c),TUFT
    elif biome=='desert': g0,g1,pth,edg=(0x70,0x5a,0x3e),(0x50,0x3e,0x2a),(0x62,0x4c,0x32),(0x6a,0x54,0x3c)
    else: g0,g1,pth,edg=(0x6c,0x7a,0x88),(0x50,0x5e,0x6e),(0x60,0x6e,0x7c),(0x88,0x96,0xa2)
    back=Image.new("RGB",(W,BH)); px=back.load()
    for y in range(BH):
        base=lerp(g0,g1,y/BH)
        for x in range(W):
            dth=int((BAYER[y&3][x&3]/16-0.5)*4); px[x,y]=clamp((base[0]+dth,base[1]+dth,base[2]+dth))
    d=ImageDraw.Draw(back); d.rectangle([6,LP0,W-6,LP1],fill=pth)
    front=Image.new("RGBA",(W,BH),(0,0,0,0)); fd=ImageDraw.Draw(front); tau=2*math.pi*t
    def tiled(p,fn):
        off=t*p
        for i in range(-1,W//p+2): fn(i*p-off)
    def plant(dd,x,y,r):
        if biome=='forest': tree_td(dd,x,y,r)
        elif biome=='desert': cactus(dd,x,y,r)
        else: snowpine(dd,x,y,r)
    def edges(bx):
        gx=int(bx); d.line([(gx,LP0),(gx+1,LP0-2),(gx+2,LP0)],fill=edg); d.line([(gx+4,LP1),(gx+5,LP1+2),(gx+6,LP1)],fill=edg)
    tiled(11,edges)
    def sb(bx):                                                # back scenery
        gx=int(bx)
        if biome=='forest':
            for (fx,fy,fc) in [(20,14,FLOWER[0]),(56,40,FLOWER[2])]: d.point([(gx+fx,fy)],fill=fc)
            d.rectangle([gx+40,30,gx+41,33],fill=MUSH_ST); d.ellipse([gx+38,27,gx+43,30],fill=MUSH)
        elif biome=='desert':
            d.line([(gx+20,40),(gx+21,35),(gx+23,40)],fill=(0x4e,0x40,0x2c)); d.line([(gx+22,39),(gx+24,36)],fill=(0x4e,0x40,0x2c)); barrel(d,gx+56,41)
        else:
            d.polygon([(gx+20,32),(gx+22,27),(gx+24,32)],fill=(0xc4,0xd4,0xe2)); d.ellipse([gx+50,39,gx+58,43],fill=(0x94,0xa4,0xb2))
    tiled(88,sb)
    tiled(80,lambda bx:[plant(d,bx+ox,oy,r) for (ox,oy,r) in sorted(BEHIND_L,key=lambda e:e[1])])
    if biome=='forest':
        for (a,b,ph) in [(40,30,0.0),(214,22,0.5),(150,44,0.3)]:
            yy=b+round(3*math.sin(tau+ph*6.28)); d.point([(a,yy)],fill=FIRE)
        for (lx,ph,ci) in [(24,0.0,0),(150,0.6,1),(210,0.15,0)]:
            pr=(t+ph)%1.0; yy=4+int(pr*(BH-8)); xx=lx+int(7*math.sin(pr*9.4)); d.point([(xx,yy),(xx+1,yy)],fill=LEAF[ci])
    elif biome=='desert':
        for (sy,ph) in [(18,0.0),(58,0.4),(98,0.7)]:
            sx=int((t*3+ph)%1.0*W); d.line([(sx,sy),(sx+7,sy)],fill=(0x9c,0x86,0x60))
    else:
        for (lx,ph) in [(20,0.0),(70,0.3),(130,0.6),(190,0.2),(240,0.8)]:
            pr=(t+ph)%1.0; yy=int(pr*BH); xx=lx+int(9*math.sin(pr*6.28+ph*6)); d.point([(xx,yy),(xx+1,yy+1)],fill=(0xf0,0xf6,0xfa))
    # ---- FRONT layer (drawn OVER the runner for depth) ----
    tiled(96,lambda bx:[plant(fd,bx+ox,oy,r) for (ox,oy,r) in sorted(FRONT_L,key=lambda e:e[1])])
    def sf(bx):
        gx=int(bx)
        if biome=='forest':
            fd.ellipse([gx+15,94,gx+21,97],fill=ROCK)
            for (fx,fy,fc) in [(50,104,FLOWER[0]),(51,106,FLOWER[1])]: fd.point([(gx+fx,fy)],fill=fc)
            tree_td(fd,gx+72,106,6)
        elif biome=='desert':
            fd.ellipse([gx+14,96,gx+22,99],fill=(0x4a,0x3a,0x28)); barrel(fd,gx+52,105)
        else:
            fd.ellipse([gx+10,99,gx+28,107],fill=(0xda,0xe4,0xec)); fd.ellipse([gx+13,101,gx+23,106],fill=(0xf2,0xf8,0xfc)); snowpine(fd,gx+58,108,7)
    tiled(100,sf)
    return back,front
BIOMES=['forest','desert','snow']; TW=0.16
def band_at(t):
    ph=t*3.0; bi=int(ph)%3; fr=ph-int(ph)
    if fr>1-TW:
        bl=(fr-(1-TW))/TW; ba,fa=band(BIOMES[bi],t); bb,fb=band(BIOMES[(bi+1)%3],t)
        return Image.blend(ba,bb,bl),Image.blend(fa,fb,bl)
    return band(BIOMES[bi],t)

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
    d.line([(16,Y0),(W-16,Y0)],fill=DIM)   # band is drawn per-frame (biomes)
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
    g=[(HX,124,30,TEALG,0.16),(cx,24,34,(0xd0,0x50,0x64),0.11)]
    for (X,Y) in [(4,4),(W-5,4),(4,H-5),(W-5,H-5)]: g.append((X,Y,4,(69,230,204),0.55))
    return g

def frame(t,S):
    scene=BASE.copy(); d=ImageDraw.Draw(scene); tau=2*math.pi*t
    for (a,b,c) in [(18,88,CYAN),(120,92,MAG_HI)]:   # sparkles above the portrait
        d.polygon([(a,b-1),(a+1,b),(a,b+1),(a-1,b)],fill=c)
    # ===== biome band: back / runner / front (front plants overlap the runner) =====
    back,front=band_at(t); scene.paste(back,(0,Y0))
    d.line([(16,Y0),(W-16,Y0)],fill=DIM)
    if int(t*12)%6 in (1,4): d.ellipse([cx-16,FEET-1,cx-11,FEET+2],fill=DUST)   # footfall dust
    d.ellipse([cx-8,FEET-2,cx+8,FEET+3],fill=FSHADOW)
    cf=RUN[int(t*12)%len(RUN)]; scene.paste(cf,(cx-cf.width//2,FEET-cf.height+1),cf)
    scene.paste(front,(0,Y0),front)   # foreground plants over the runner (depth)
    d.rectangle([4,4,W-5,H-5],outline=DIM)
    big=scene.resize((W*S,H*S),Image.NEAREST)
    gl=Image.new("RGB",big.size,(0,0,0)); gd=ImageDraw.Draw(gl)
    for (gx,gy,gr,gc,gi) in frame_glows(t):
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
