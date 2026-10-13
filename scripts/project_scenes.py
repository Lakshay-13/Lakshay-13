"""Distinct vector motion studies based on each project's actual purpose.

Scenes illustrate workflows; they do not represent measurements or product UI.
"""

import html
import math
import base64
from pathlib import Path

MINT = "#2effbf"
PURPLE = "#b9a7ff"
WHITE = "#d5e1ed"
DIM = "#3c5064"


def logo(filename, x, y, width, height):
    binary = (Path(__file__).resolve().parents[1] / "assets" / filename).read_bytes()
    encoded = base64.b64encode(binary).decode()
    return f'<image x="{x}" y="{y}" width="{width}" height="{height}" href="data:image/png;base64,{encoded}" preserveAspectRatio="xMidYMid meet"/>'


def rect(x, y, w, h, fill="#101b29", stroke=DIM, rx=10, attrs=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" {attrs}/>'


def path(d, color=MINT, attrs="", fill="none", width=2):
    return f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {attrs}/>'


def dot(x, y, r=4, color=MINT, attrs=""):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" {attrs}/>'


def label(x, y, value, size=13, color=WHITE, attrs=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" style="fill:{color}" {attrs}>{html.escape(value)}</text>'


def scene(content, css):
    return f'<style>{css}</style><g data-project-scene="true">{content}</g>'


def fren():
    p = '<defs><clipPath id="fren-emblem"><circle cx="160" cy="112" r="47"/></clipPath></defs>'
    p += '<ellipse cx="160" cy="112" rx="94" ry="88" fill="url(#purple-glow)"/>'
    p += path('M160 48V61M113 112H76V163M207 112H249V163', '#485968', width=1.3)
    p += '<circle class="fren-halo" cx="160" cy="112" r="53" fill="none" stroke="#b9a7ff" stroke-width="1.2"/>'
    p += '<g clip-path="url(#fren-emblem)">'+logo('logos/fren.png',106,58,108,108)+'</g>'
    p += rect(109,13,102,33,'#1b2035','#4d476c',9)+label(160,35,'Games',14,PURPLE,'text-anchor="middle"')
    p += rect(13,165,124,37,'#11292a','#2d5050',9)+label(75,189,'AI utilities',14,MINT,'text-anchor="middle"')
    p += rect(181,165,134,37,'#172235','#43516c',9)+label(248,189,'Moderation',14,WHITE,'text-anchor="middle"')
    p += dot(160,52,2.5,PURPLE,'class="fren-game-signal"')
    p += dot(94,112,2.5,MINT,'class="fren-ai-signal"')
    p += dot(228,112,2.5,PURPLE,'class="fren-mod-signal"')
    return scene(p, '.fren-halo{animation:frenHalo 4s ease-in-out infinite}.fren-game-signal{animation:frenGame 4s infinite}.fren-ai-signal{animation:frenAI 4s infinite}.fren-mod-signal{animation:frenMod 4s infinite}@keyframes frenHalo{0%,100%{opacity:.3}50%{opacity:.85}}@keyframes frenGame{0%,100%{transform:translateY(0);opacity:.2}60%{transform:translateY(9px);opacity:1}}@keyframes frenAI{0%,100%{transform:translate(0,0);opacity:.25}40%{transform:translate(-18px,0);opacity:1}80%{transform:translate(-18px,43px);opacity:.3}}@keyframes frenMod{0%,100%{transform:translate(0,0);opacity:.25}45%{transform:translate(21px,0);opacity:1}80%{transform:translate(21px,43px);opacity:.3}}')


def pinnhub():
    p = label(24,24,"PHYSICS-INFORMED SOLUTIONS",12,PURPLE)
    for row in range(7):
        points=[]
        for col in range(29):
            x=34+col*8+row*3; y=80+row*15+12*math.sin(col*.23+row*.45)
            points.append(f'{x:.1f},{y:.1f}')
        p += f'<polyline points="{" ".join(points)}" fill="none" stroke="{MINT if row%2==0 else PURPLE}" stroke-width="1.4" class="pinn-field" style="animation-delay:-{row*.5}s"/>'
    p += path('M28 196H290M28 196V58',DIM) + label(235,216,'x, t → u',15,MINT)
    for x,y in [(60,84),(110,135),(178,101),(229,170)]: p+=dot(x,y,3,WHITE,'class="pinn-point"')
    return scene(p,'.pinn-field{animation:pinnField 8s ease-in-out infinite}.pinn-point{animation:pinnPoint 4s infinite}@keyframes pinnField{0%,100%{opacity:.35;transform:translateY(0)}50%{opacity:.95;transform:translateY(-8px)}}@keyframes pinnPoint{0%,100%{opacity:.4}50%{opacity:1}}')


def artgridx():
    p=rect(154,25,147,178,'#101824','#344251',12)
    p+=label(169,49,'ARTIST STUDIO',10,'#b4c2cd')
    p+=rect(169,61,59,68,'#1a3439','#34535a',5)+rect(237,61,49,42,'#28233c','#49425c',5)+rect(237,111,49,43,'#19342c','#315849',5)
    p+=path('M177 119V73H220M246 72H278M246 79H272M246 86H276', '#5f8287', width=1)
    p+='<g class="art-layout">'+rect(177,78,16,33,'#294f4a','none',3)+rect(198,78,22,18,'#65548d','none',3)+rect(198,101,22,10,'#344358','none',2)+'</g>'
    p+=path('M245 145L254 120 266 139 277 125',PURPLE,width=1.4)
    p+=label(169,149,'Templates',12,WHITE)+label(169,176,'Domains · Analytics',11,'#a5bbc6')
    p+='<rect class="art-frame" x="169" y="61" width="59" height="68" rx="5" fill="none" stroke="#2effbf" stroke-width="1.4"/>'
    p='<ellipse cx="160" cy="119" rx="109" ry="105" fill="url(#purple-glow)"/><g transform="translate(-95 -5) scale(1.12)">'+p+'</g>'
    return scene(p,'.art-frame{stroke-dasharray:64 190;animation:artFrame 8s linear infinite}.art-layout{animation:artLayout 8s ease-in-out infinite}@keyframes artFrame{to{stroke-dashoffset:-254}}@keyframes artLayout{0%,100%{opacity:.55}45%,70%{opacity:1}}')


def notifyme():
    p=rect(99,12,119,209,'#121c2b',DIM,20)+rect(136,20,45,6,'#354255','none',3)
    p+=label(126,51,'NotifyMe',14,WHITE)
    for i,word in enumerate(['Job complete','Callback ready','History synced']):
        y=70+i*42
        p+='<g class="notify-toast" style="animation-delay:-'+str(i*2)+'s">'+rect(109,y,99,32,'#19372f','#36584e',8)+dot(119,y+16,3,MINT)+label(130,y+20,word,10)+'</g>'
    p+=label(13,112,'API',15,PURPLE)+path('M46 107H84M78 101 84 107 78 113',PURPLE,'class="notify-send"')
    p+=dot(159,203,3,WHITE)
    return scene(p,'.notify-toast{animation:notifyToast 8s infinite}.notify-send{animation:notifySend 8s infinite}@keyframes notifyToast{0%,12%,100%{opacity:0;transform:translateY(-13px)}25%,88%{opacity:1;transform:translateY(0)}}@keyframes notifySend{0%,100%{opacity:.3;transform:translateX(0)}45%{opacity:1;transform:translateX(9px)}}')


def host():
    p=rect(23,39,126,138,'#122133',DIM,10)
    p+=rect(36,55,100,57,'#1b3542','none',6)+dot(61,72,8,PURPLE)+path('M44 102 70 82 86 96 106 78 128 103',MINT)
    p+=path('M40 130H121M40 143H104M40 156H113','#91a8bd',width=2)
    p+=path('M157 108H182M175 101 182 108 175 115',DIM)
    p+=path('M211 138H285A19 19 0 0 0 286 100A32 32 0 0 0 224 87A26 26 0 0 0 211 138Z',MINT,fill='#143329',width=1.8)
    p+='<g class="host-upload">'+path('M247 124V96M237 106 247 96 257 106',MINT,width=2.5)+'</g>'
    p+=rect(204,157,91,32,'#142133',DIM,7)
    p+='<g transform="translate(236 160) scale(1.08)" fill="none" stroke="#b9a7ff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7 .2l3-3a5 5 0 0 0-7-7l-1.7 1.7M14 11a5 5 0 0 0-7-.2l-3 3a5 5 0 0 0 7 7l1.7-1.7"/></g>'
    p+=label(34,211,'FILES',12,WHITE)+label(215,211,'SHARE LINKS',12,MINT)
    return scene(p,'.host-upload{animation:hostUpload 4s ease-in-out infinite}@keyframes hostUpload{0%,100%{transform:translateY(5px);opacity:.4}50%{transform:translateY(-4px);opacity:1}}')


def rlpinn():
    p=label(18,26,'ADAPTIVE PINN TRAINING',12,WHITE)+rect(18,47,168,126,'#101b28','#35485a',4)
    for row in range(5):p+=path(f'M30 {64+row*22}H173','#253748',width=.7)
    for col in range(7):p+=path(f'M{31+col*23} 58V163','#253748',width=.7)
    p+=path('M30 146C59 151 75 72 103 88S144 156 173 75',PURPLE,width=1.4)
    for i,(x,y) in enumerate([(40,119),(63,103),(87,87),(110,108),(139,122),(160,99)]):
        p+=dot(x,y,3.5,MINT,f'class="rl-sample" style="animation-delay:-{i*.6}s"')
    p+=rect(228,67,73,34,'#172237','#62708c',4)+label(242,89,'POLICY',12,PURPLE)
    p+=path('M229 81H207V107H189M195 103 189 107 195 111',PURPLE,width=1.3)
    p+=path('M189 147H265V106M261 113 265 106 269 113',MINT,width=1.3)
    p+=label(215,57,'ACTION',9,PURPLE)+label(226,169,'STATE',9,MINT)
    p+=label(29,191,'Residual field / adaptive sampling',11,'#a8b8c9')
    return scene(p,'.rl-sample{animation:rlSample 4s ease-in-out infinite}@keyframes rlSample{0%,100%{opacity:.25}50%{opacity:1}}')


def slidenext():
    p='<g class="slide-back">'+rect(64,31,214,151,'#25243b',PURPLE,10)+label(83,64,'02 / STORY',15,PURPLE)+'</g>'
    p+='<g class="slide-front">'+rect(36,57,214,151,'#102b29',MINT,10)+label(58,92,'01 / OUTLINE',15,MINT)+rect(58,112,147,8,'#446b66','none',3)+rect(58,133,112,8,'#385553','none',3)+path('M60 175H169',MINT)+'</g>'
    return scene(p,'.slide-back{transform-box:fill-box;transform-origin:center;animation:slideBack 8s ease-in-out infinite}.slide-front{animation:slideFront 8s ease-in-out infinite}@keyframes slideBack{0%,100%{transform:rotate(5deg)}50%{transform:rotate(-2deg)}}@keyframes slideFront{0%,100%{transform:translate(0,0)}50%{transform:translate(-10px,9px)}}')


def watermark():
    p='<ellipse cx="160" cy="122" rx="111" ry="92" fill="url(#purple-glow)"/>'
    p+='<g class="watermark-brand">'+logo('logos/watermark.png',45,25,230,170)+'</g>'
    return scene(p,'.watermark-brand{animation:watermarkBrand 8s ease-in-out infinite}@keyframes watermarkBrand{0%,100%{transform:translateY(0)}15%{transform:translateY(-8px)}32%{transform:translateY(5px)}42%,85%{transform:translateY(0)}}')


def frenshop():
    outline='M27 42H293Q307 42 307 56V104C289 104 289 132 307 132V180Q307 194 293 194H27Q13 194 13 180V132C31 132 31 104 13 104V56Q13 42 27 42Z'
    p='<defs><clipPath id="shop-pass-clip"><path d="'+outline+'"/></clipPath><linearGradient id="shop-foil"><stop stop-color="#2effbf" stop-opacity="0"/><stop offset=".5" stop-color="#b9a7ff" stop-opacity=".16"/><stop offset="1" stop-color="#2effbf" stop-opacity="0"/></linearGradient></defs>'
    p+='<ellipse cx="163" cy="122" rx="141" ry="102" fill="url(#purple-glow)"/>'
    p+=path(outline,'#74668e',fill='#141d30',width=1.3)
    p+='<g clip-path="url(#shop-pass-clip)"><g class="shop-foil"><path d="M-60 42H10L76 194H6Z" fill="url(#shop-foil)"/></g></g>'
    p+=path('M230 57V179','#625678','stroke-dasharray="2 7"',width=1)
    p+=label(35,68,'DIGITAL / COMMUNITY',10,'#a9b4ca')
    p+=label(35,100,'FREN SHOP',23,WHITE)
    p+=label(35,128,'Premium passes',14,PURPLE)
    p+=label(35,160,'Upgrades & collectibles',11,'#b1bfce')
    p+=logo('logos/frenshop.png',242,66,55,55)
    p+=label(269,146,'DIGITAL',9,MINT,'text-anchor="middle"')+label(269,161,'PERKS',9,MINT,'text-anchor="middle"')
    p+=path('M37 179H104',MINT,'class="shop-pass-accent"',width=1.7)
    return scene(p,'.shop-foil{animation:shopFoil 8s linear infinite}.shop-pass-accent{animation:shopAccent 4s ease-in-out infinite}@keyframes shopFoil{0%{transform:translateX(40px);opacity:.6}85%{transform:translateX(365px);opacity:.6}100%{transform:translateX(365px);opacity:0}}@keyframes shopAccent{0%,100%{opacity:.35}50%{opacity:.85}}')


def tree():
    p=path('M159 60V105M59 139V105H259V139M99 187V163H219V187',DIM,width=2)
    p+=rect(124,14,70,48,'#253041',PURPLE,14)+dot(159,32,7,PURPLE)+path('M145 51Q159 36 173 51',PURPLE)
    for i,(x,y) in enumerate([(28,138),(228,138),(128,111),(69,187),(189,187)]):
        p+='<g class="tree-branch" style="animation-delay:-'+str(i*1.1)+'s">'+rect(x,y,62,30,'#15332b',MINT,10)+dot(x+13,y+15,4,MINT)+path(f'M{x+25} {y+15}H{x+48}',DIM)+'</g>'
    return scene(p,'.tree-branch{animation:treeBranch 8s ease-in-out infinite}@keyframes treeBranch{0%,14%,100%{opacity:.2;transform:translateY(-6px)}35%,78%{opacity:1;transform:translateY(0)}}')


def zinging():
    p='<g class="zing-brand">'+logo('logos/zinging.png',8,33,174,174)+'</g>'
    routes=['M158 70H183V62H195','M179 121H195','M158 174H183V180H195']
    for i,(y,word) in enumerate([(46,'Chat'),(105,'Translate'),(164,'Memory')]):
        p+=path(routes[i],'#5fab66','class="zing-trace"',width=1.3)
        p+='<g class="zing-capability" style="animation-delay:-'+str(i*1.2)+'s">'+rect(194,y,111,33,'#143425','#31553a',7)+dot(208,y+16,2.5,'#b5f55f')+label(220,y+21,word,14,'#d1f0c5')+'</g>'
    return scene(p,'.zing-brand{animation:zingBrand 4s ease-in-out infinite}.zing-trace{stroke-dasharray:4 11;animation:zingTrace 4s linear infinite}.zing-capability{animation:zingCapability 4s ease-in-out infinite}@keyframes zingBrand{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}@keyframes zingTrace{to{stroke-dashoffset:-60}}@keyframes zingCapability{0%,100%{opacity:.65}50%{opacity:1}}')


def url():
    p=label(160,25,'Tenor · Pinterest · Giphy · KLIPY',12,'#b5c2ce','text-anchor="middle"')
    p+=rect(19,52,113,114,'#142032','#42516b',9)
    for x in (32,41,50):p+=dot(x,65,1.7,'#8495a9')
    p+=path('M30 78H120','#35455c',width=1)
    p+='<g transform="translate(56 89) scale(1.5)" fill="none" stroke="#b9a7ff" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7 .2l3-3a5 5 0 0 0-7-7l-1.7 1.7M14 11a5 5 0 0 0-7-.2l-3 3a5 5 0 0 0 7 7l1.7-1.7"/></g>'
    p+=path('M40 143H111',PURPLE,width=1.4)
    p+=path('M141 109H193M185 102 193 109 185 116','#75899d',width=1.5)
    p+=dot(145,109,2.5,MINT,'class="url-transfer"')
    p+=path('M209 52H278L296 70V166H209Z',MINT,fill='#122c2a',width=1.4)+path('M278 52V70H296','#69a997',width=1.2)
    p+=rect(221,85,63,43,'#193c36','#42695e',5)+dot(235,97,4,'#86bfb0')
    p+=path('M225 122 241 108 255 122 269 111 280 121',MINT,width=1.5)
    p+=path('M221 145H281','#719f91',width=1.2)
    p+=path('M223 125H282',MINT,'class="url-media-scan"',width=1.2)
    p+=label(76,194,'Page URL',13,WHITE,'text-anchor="middle"')+label(252,194,'Direct media URL',12,MINT,'text-anchor="middle"')
    return scene(p,'.url-transfer{animation:urlTransfer 4s linear infinite}.url-media-scan{animation:urlMediaScan 4s ease-in-out infinite}@keyframes urlTransfer{0%{transform:translateX(0);opacity:.5}75%{transform:translateX(46px);opacity:1}100%{transform:translateX(46px);opacity:0}}@keyframes urlMediaScan{0%,100%{transform:translateY(0);opacity:.2}50%{transform:translateY(-35px);opacity:.7}}')


def rags():
    p=label(26,25,'RETRIEVE → GROUND → ANSWER',12,MINT)
    for i in range(3):
        x=22+i*27;y=42+i*24
        p+=rect(x,y,88,97,'#172438',DIM,7)
        for j in range(3): p+=path(f'M{x+13} {y+21+j*17}H{x+70}',DIM)
    p+=rect(76,109,62,7,'#2effbf','none',2,'class="rag-match"')
    p+=path('M159 103H185M178 96 185 103 178 110',PURPLE)+rect(193,65,105,134,'#20283c',PURPLE,12)
    p+=label(204,91,'ANSWER',12,PURPLE)
    for i,w in enumerate([71,60,76,42]): p+=rect(206,110+i*18,w,5,'#779996','none',2,f'class="rag-answer" style="animation-delay:-{i*.7}s"')
    return scene(p,'.rag-match{animation:ragMatch 8s infinite}.rag-answer{transform-box:fill-box;transform-origin:left;animation:ragAnswer 8s infinite}@keyframes ragMatch{0%,100%{opacity:.15}30%,60%{opacity:1}}@keyframes ragAnswer{0%,24%,100%{transform:scaleX(.05);opacity:.15}65%,88%{transform:scaleX(1);opacity:1}}')


def variable_stars():
    p=label(22,23,'GAIA DR3 / PERIODIC VARIABLES',11,PURPLE)
    for i,(x,y,r) in enumerate([(61,66,5),(119,48,3),(209,78,6),(271,43,4)]):
        p+=dot(x,y,r,WHITE,f'class="star-flux" style="animation-delay:-{i*1.4}s"')+path(f'M{x-9} {y}H{x+9}M{x} {y-9}V{y+9}',PURPLE,width=.8)
    p+=path('M23 194H296M23 194V109',DIM)
    points=' '.join(f'{x},{154-26*math.sin((x-24)*.063):.1f}' for x in range(24,298,4))
    p+=f'<polyline points="{points}" fill="none" stroke="{PURPLE}" stroke-width="2.5"/>'
    p+=path('M26 110V194',MINT,'class="star-observation"',width=1.5)+label(184,221,'LIGHT CURVE',13,PURPLE)
    return scene(p,'.star-flux{transform-box:fill-box;transform-origin:center;animation:starFlux 8s infinite}.star-observation{animation:starObservation 8s linear infinite}@keyframes starFlux{0%,100%{opacity:.2;transform:scale(.7)}40%,60%{opacity:1;transform:scale(1.2)}}@keyframes starObservation{0%{transform:translateX(0);opacity:.2}10%,90%{opacity:1}100%{transform:translateX(269px);opacity:.2}}')


def notes():
    p=rect(128,23,169,184,'#1c2534',DIM,10)+path('M153 38V193',PURPLE)
    for i in range(4):
        y=64+i*33
        p+=dot(169,y,3,MINT)+path(f'M183 {y}H{274-i*10}',MINT,f'class="notes-ink" style="animation-delay:-{i*.8}s"')
    p+=path('M18 108 29 108 35 82 42 138 49 66 56 148 62 93 68 117 75 80 82 133 88 108H108',PURPLE,'class="notes-audio"')
    p+=label(22,173,'AUDIO',13,PURPLE)+label(162,224,'STRUCTURED NOTES',12,MINT)
    return scene(p,'.notes-ink{stroke-dasharray:100;animation:notesInk 8s infinite}.notes-audio{animation:notesAudio 8s ease-in-out infinite}@keyframes notesInk{0%,20%,100%{stroke-dashoffset:100;opacity:.2}65%,88%{stroke-dashoffset:0;opacity:1}}@keyframes notesAudio{0%,100%{opacity:.25}30%,60%{opacity:1}}')


def customer():
    p=label(22,23,'CHURN / APPETENCY / UPSELL',12,MINT)
    for i,(x,y,color) in enumerate([(81,85,PURPLE),(237,89,MINT),(167,172,'#8caad7')]):
        p+=f'<ellipse cx="{x}" cy="{y}" rx="48" ry="34" fill="{color}" fill-opacity=".055" stroke="{color}" stroke-opacity=".4"/>'
        for j in range(7):
            angle=j*2.4;dx=math.cos(angle)*(12+j*3);dy=math.sin(angle)*(8+j*2)
            p+=dot(round(x+dx,1),round(y+dy,1),3,color,f'class="customer-segment" style="animation-delay:-{i+j*.3}s"')
        p+=path(f'M{x-7} {y}H{x+7}M{x} {y-7}V{y+7}',color,width=1.4)
    return scene(p,'.customer-segment{animation:customerSegment 8s ease-in-out infinite}@keyframes customerSegment{0%,100%{opacity:.2;transform:translateY(5px)}45%,65%{opacity:1;transform:translateY(0)}}')


def music():
    p=f'<circle cx="112" cy="115" r="80" fill="#182030" stroke="{DIM}"/>'
    p+='<g class="music-record">'
    for radius in [69,58,47]: p+=f'<circle cx="112" cy="115" r="{radius}" fill="none" stroke="#34405b"/>'
    p+=path('M112 41V87M112 143V189',PURPLE,width=7)+dot(112,115,27,PURPLE)+dot(112,115,4,'#111a29')+'</g>'
    p+=path('M228 39H254V118L188 154',MINT,width=5)+rect(174,147,25,14,'#26745d',MINT,3)
    p+=label(210,202,'GENRE',15,MINT)+label(38,218,'AUDIO FEATURES',12,PURPLE)
    return scene(p,'.music-record{transform-origin:112px 115px;animation:musicRecord 8s linear infinite}@keyframes musicRecord{to{transform:rotate(360deg)}}')


def code_image():
    p=rect(19,24,194,134,'#112439',DIM,10)+label(35,49,'CODE',12,MINT)
    for i,(word,color) in enumerate([('def render(code):',PURPLE),('  image = draw(code)',MINT),('  return image',WHITE)]): p+=label(35,78+i*25,word,12,color)
    p+=path('M179 123H238V146',DIM)+rect(161,149,136,69,'#26334d',PURPLE,8)
    for i,w in enumerate([87,103,67]): p+=rect(178,164+i*14,w,4,'#acb4d2','none',1)
    p+=rect(208,23,3,135,'#2effbf','none',0,'class="code-capture"')
    p+=rect(159,147,140,73,'none',MINT,10,'class="code-export"')
    return scene(p,'.code-capture{animation:codeCapture 8s infinite}.code-export{animation:codeExport 8s infinite}@keyframes codeCapture{0%,100%{opacity:0;transform:translateX(-189px)}10%{opacity:.5}65%{transform:translateX(0);opacity:.5}85%{transform:translateX(0);opacity:0}}@keyframes codeExport{0%,50%,100%{opacity:.1}65%,85%{opacity:1}}')


def morph():
    p=label(20,24,'GRAPH A → MORPHING GIF → GRAPH B',10,PURPLE)+path('M30 194H295M30 194V50',DIM)
    a='M42 163C83 160 101 70 137 93S215 172 283 70'
    b='M42 74C88 83 104 159 137 140S225 61 283 157'
    p+=path(a,'#485266',width=1)+path(b,'#485266',width=1)+path(a,PURPLE,'class="graph-morph"',width=3)
    p+=label(155,220,'INTERPOLATE',12,PURPLE)
    return scene(p,'.graph-morph{animation:graphMorph 8s ease-in-out infinite}@keyframes graphMorph{0%,100%{d:path("'+a+'")}50%{d:path("'+b+'")}}')


def transcribe():
    p=rect(17,20,286,190,'#162337',DIM,12)+rect(17,20,286,27,'#2a3344','none',10)
    for i,color in enumerate(['#b7889a','#bbaa80','#83b79f']): p+=dot(33+i*13,34,3,color)
    p+=label(191,39,'LOCAL / API',10,PURPLE)
    p+=path('M37 84 48 84 53 73 59 98 65 66 71 99 78 78 83 87 89 84H281',PURPLE)
    p+=label(37,123,'AUDIO + VIDEO',12,PURPLE)
    p+=rect(33,143,253,42,'#0c1929','none',8)+label(44,168,'Speech becomes a transcript.',14,MINT)
    p+=rect(43,148,232,32,'#0c1929','none',0,'class="transcript-reveal"')
    return scene(p,'.transcript-reveal{animation:transcriptReveal 8s steps(28,end) infinite}@keyframes transcriptReveal{0%,100%{transform:translateX(0);width:232px}75%,90%{transform:translateX(232px);width:0}}')


def grid():
    p=label(24,23,'TRIANGULAR TESSELLATION',12,MINT)
    for row in range(4):
        for col in range(7):
            x=25+col*37;y=44+row*39
            points=f'{x},{y+36} {x+18},{y} {x+36},{y+36}'
            color=MINT if (row+col)%2==0 else PURPLE
            p+=f'<polygon points="{points}" fill="{color}" fill-opacity=".25" stroke="{color}" stroke-opacity=".55" class="grid-tile" style="animation-delay:-{row*.7+col*.4}s"/>'
    p+=label(95,226,'COLOR / PATTERN / EXPORT',11,PURPLE)
    return scene(p,'.grid-tile{animation:gridTile 8s ease-in-out infinite}@keyframes gridTile{0%,100%{fill-opacity:.08}45%,65%{fill-opacity:.7}}')


SCENES = {"fren": fren, "pinnhub": pinnhub, "artgridx": artgridx,
          "notifyme": notifyme, "host": host, "rlpinn": rlpinn,
          "slidenext": slidenext, "watermark": watermark, "frenshop": frenshop,
          "tree": tree, "zinging": zinging, "url": url, "rags": rags,
          "variable-stars": variable_stars, "notes": notes, "customer": customer,
          "music": music, "code-image": code_image, "morph": morph,
          "transcribe": transcribe, "grid": grid}


def render(project_id):
    return SCENES[project_id]()
