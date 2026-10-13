"""Distinct vector motion studies based on each project's actual purpose.

Scenes illustrate workflows; they do not represent measurements or product UI.
"""

import html
import math

MINT = "#2effbf"
PURPLE = "#b9a7ff"
WHITE = "#d5e1ed"
DIM = "#3c5064"


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
    p = rect(18, 17, 268, 182, rx=18) + rect(18, 17, 268, 29, "#1a2636", rx=12)
    p += label(38, 37, "FREN / COMMUNITY GAMES", 12, PURPLE)
    p += rect(38, 60, 126, 29, "#243348", "none", 12) + label(50, 80, "/play with fren", 14)
    p += '<g class="fren-reply">' + rect(86, 105, 181, 40, "#12362d", "#2c6657", 12) + label(101, 130, "Your next round is ready.", 13, MINT) + '</g>'
    for i in range(3): p += dot(46+i*14, 167, 3, PURPLE, f'class="fren-typing" style="animation-delay:-{i*.35}s"')
    p += '<g class="fren-dice">' + rect(226, 157, 44, 44, "#202239", PURPLE, 9)
    for x,y in [(237,168),(259,168),(248,179),(237,190),(259,190)]: p += dot(x,y,2,PURPLE)
    p += '</g>'
    return scene(p, '.fren-reply{animation:frenReply 8s infinite}.fren-typing{animation:frenTyping 1.6s infinite}.fren-dice{transform-box:fill-box;transform-origin:center;animation:frenDice 8s infinite}@keyframes frenReply{0%,18%,95%,100%{opacity:0;transform:translateY(12px)}30%,82%{opacity:1;transform:translateY(0)}}@keyframes frenTyping{0%,100%{opacity:.25}50%{opacity:1}}@keyframes frenDice{0%,38%,100%{transform:rotate(0)}48%{transform:rotate(-12deg)}58%{transform:rotate(12deg)}68%,85%{transform:rotate(0)}}')


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
    p = rect(18,22,85,116,"#16253b",DIM,5)+rect(116,22,86,75,"#282239",DIM,5)+rect(216,22,86,116,"#143327",DIM,5)+rect(116,108,86,91,"#153035",DIM,5)
    p += dot(60,64,23,PURPLE)+path('M25 123 53 86 95 123',MINT,fill='#27564a')
    p += path('M129 78C135 27 179 91 190 43',PURPLE,'class="art-paint"',width=7)
    p += '<g class="art-tile">'+path('M228 124 234 66 268 42 288 89 256 130',MINT,fill='#275548')+'</g>'
    p += path('M132 183 150 127 187 166 171 183',PURPLE,fill='#423b60')
    p += label(23,224,'GALLERY / CREATE / PUBLISH',12,PURPLE)
    return scene(p,'.art-paint{stroke-dasharray:130;animation:artPaint 8s ease-in-out infinite}.art-tile{transform-box:fill-box;transform-origin:center;animation:artTile 8s ease-in-out infinite}@keyframes artPaint{0%,100%{stroke-dashoffset:130;opacity:.2}65%,85%{stroke-dashoffset:0;opacity:1}}@keyframes artTile{0%,100%{transform:rotate(0)}50%{transform:rotate(-5deg)}}')


def notifyme():
    p=rect(99,12,119,209,'#121c2b',DIM,20)+rect(136,20,45,6,'#354255','none',3)
    p+=label(126,51,'NotifyMe',14,WHITE)
    for i,word in enumerate(['Job complete','Callback ready','History synced']):
        y=70+i*42
        p+='<g class="notify-toast" style="animation-delay:-'+str(i*2)+'s">'+rect(109,y,99,32,'#19372f','#36584e',8)+dot(119,y+16,3,MINT)+label(130,y+20,word,10)+'</g>'
    p+=path('M46 107H84M78 101 84 107 78 113',PURPLE,'class="notify-send"')+label(26,137,'API',15,PURPLE)
    p+=dot(159,203,3,WHITE)
    return scene(p,'.notify-toast{animation:notifyToast 8s infinite}.notify-send{animation:notifySend 8s infinite}@keyframes notifyToast{0%,12%,100%{opacity:0;transform:translateY(-13px)}25%,88%{opacity:1;transform:translateY(0)}}@keyframes notifySend{0%,100%{opacity:.3;transform:translateX(0)}45%{opacity:1;transform:translateX(9px)}}')


def host():
    p=label(24,27,'BUILD → DEPLOY → LIVE',14,MINT)+rect(22,59,76,88,rx=8)+label(38,87,'</>',27,PURPLE)
    p+=path('M36 104H82M36 116H66',DIM)+rect(207,55,87,126,rx=8)
    for i in range(3): p+=rect(221,70+i*28,59,19,'#15283a',DIM,4)+dot(269,79+i*28,2,MINT)
    p+=path('M105 103H197',DIM)
    p+='<g class="host-bundle">'+rect(108,91,22,24,'#234d42',MINT,4)+path('M114 99H123M114 105H120',MINT)+'</g>'
    p+='<g class="host-live">'+dot(251,202,12,'#123b2e')+path('M246 202 250 206 257 197',MINT)+label(211,227,'LIVE RELEASE',11,MINT)+'</g>'
    return scene(p,'.host-bundle{animation:hostBundle 8s ease-in-out infinite}.host-live{animation:hostLive 8s infinite}@keyframes hostBundle{0%,10%{transform:translateX(0);opacity:0}20%{opacity:1}65%,85%{transform:translateX(78px);opacity:1}95%,100%{transform:translateX(78px);opacity:0}}@keyframes hostLive{0%,60%,100%{opacity:.25}72%,90%{opacity:1}}')


def rlpinn():
    p=rect(15,35,93,52,'#26233c',PURPLE,12)+label(36,66,'RL POLICY',14,PURPLE)+rect(209,111,94,54,'#16332b',MINT,12)+label(224,143,'PINN',23,MINT)
    p+=path('M112 62H260V106',DIM)+path('M209 141H64V91',DIM)
    p+=dot(137,62,5,PURPLE,'class="rl-action"')+dot(172,141,4,MINT,'class="rl-feedback"')
    p+=label(157,45,'ACTION',11,PURPLE)+label(71,168,'RESIDUAL / REWARD',11,MINT)
    p+=path('M22 215H139M22 215V182',DIM)+path('M30 201 51 207 72 189 94 193 128 182',PURPLE,'class="rl-reward"')
    return scene(p,'.rl-action{animation:rlAction 8s linear infinite}.rl-feedback{animation:rlFeedback 8s linear infinite}.rl-reward{stroke-dasharray:125;animation:rlReward 8s infinite}@keyframes rlAction{0%{transform:translate(0,0);opacity:0}10%{opacity:1}50%{transform:translate(123px,0);opacity:1}70%{transform:translate(123px,42px);opacity:1}90%,100%{transform:translate(123px,42px);opacity:0}}@keyframes rlFeedback{0%,20%,100%{opacity:0;transform:translate(0,0)}30%{opacity:1}70%{transform:translate(-108px,0);opacity:1}90%{transform:translate(-108px,-47px);opacity:0}}@keyframes rlReward{0%,100%{stroke-dashoffset:125}80%{stroke-dashoffset:0}}')


def slidenext():
    p='<g class="slide-back">'+rect(64,31,214,151,'#25243b',PURPLE,10)+label(83,64,'02 / STORY',15,PURPLE)+'</g>'
    p+='<g class="slide-front">'+rect(36,57,214,151,'#102b29',MINT,10)+label(58,92,'01 / OUTLINE',15,MINT)+rect(58,112,147,8,'#446b66','none',3)+rect(58,133,112,8,'#385553','none',3)+path('M60 175H169',MINT)+'</g>'
    return scene(p,'.slide-back{transform-box:fill-box;transform-origin:center;animation:slideBack 8s ease-in-out infinite}.slide-front{animation:slideFront 8s ease-in-out infinite}@keyframes slideBack{0%,100%{transform:rotate(5deg)}50%{transform:rotate(-2deg)}}@keyframes slideFront{0%,100%{transform:translate(0,0)}50%{transform:translate(-10px,9px)}}')


def watermark():
    p=rect(28,21,225,176,'#1c293c',DIM,8)+dot(84,72,25,'#8275b5')+path('M42 183 119 96 167 155 202 119 241 183',MINT,fill='#225949')
    p+='<g class="watermark-stamp" transform="rotate(-20 150 113)">'+rect(67,96,166,34,'#0d1520',PURPLE,3)+label(81,118,'WATERMARK',20,PURPLE)+'</g>'
    p+=rect(254,160,44,39,'#13362f',MINT,7)+path('M265 159V150A11 11 0 0 1 287 150V159',MINT)+dot(276,179,3,MINT)
    return scene(p,'.watermark-stamp{animation:watermarkStamp 8s ease-in-out infinite}@keyframes watermarkStamp{0%,10%,100%{opacity:0}35%,85%{opacity:.95}}')


def frenshop():
    p=path('M23 65H45L66 152H240L264 82H54',PURPLE,width=3)+dot(90,179,13,PURPLE)+dot(224,179,13,PURPLE)
    p+='<g class="shop-drop">'+rect(108,38,89,74,'#24352f',MINT,12)+path('M131 51V42A22 22 0 0 1 175 42V51',MINT)+label(124,87,'FREN',21,MINT)+'</g>'
    p+=label(45,216,'PREMIUM / COMMUNITY',13,PURPLE)
    return scene(p,'.shop-drop{animation:shopDrop 8s cubic-bezier(.4,0,.2,1) infinite}@keyframes shopDrop{0%,100%{transform:translateY(-14px);opacity:.25}40%,76%{transform:translateY(34px);opacity:1}}')


def tree():
    p=path('M159 60V105M59 139V105H259V139M99 187V163H219V187',DIM,width=2)
    p+=rect(124,14,70,48,'#253041',PURPLE,14)+dot(159,32,7,PURPLE)+path('M145 51Q159 36 173 51',PURPLE)
    for i,(x,y) in enumerate([(28,138),(228,138),(128,111),(69,187),(189,187)]):
        p+='<g class="tree-branch" style="animation-delay:-'+str(i*1.1)+'s">'+rect(x,y,62,30,'#15332b',MINT,10)+dot(x+13,y+15,4,MINT)+path(f'M{x+25} {y+15}H{x+48}',DIM)+'</g>'
    return scene(p,'.tree-branch{animation:treeBranch 8s ease-in-out infinite}@keyframes treeBranch{0%,14%,100%{opacity:.2;transform:translateY(-6px)}35%,78%{opacity:1;transform:translateY(0)}}')


def zinging():
    p=rect(111,74,94,64,'#1c293a',PURPLE,20)+label(123,112,'AGENT',20,PURPLE)
    points=[(56,34,'CODE'),(257,36,'TOOLS'),(256,188,'MEMORY'),(45,191,'TRANSLATE')]
    for i,(x,y,word) in enumerate(points):
        p+=path(f'M158 106Q{x} 106 {x} {y}',DIM)
        p+=rect(x-36,y-15,72,30,'#122921',MINT,8)+label(x,y+4,word,10,MINT,'text-anchor="middle"')
        p+=dot(158,106,4,MINT,f'class="zing-route-{i}"')
    css=''
    for i,(x,y,_) in enumerate(points):
        css+=f'.zing-route-{i}'+'{animation:zingRoute'+str(i)+' 8s '+str(i*1.2)+'s infinite}@keyframes zingRoute'+str(i)+'{0%,100%{transform:translate(0,0);opacity:0}20%{opacity:1}65%{transform:translate('+str(x-158)+'px,'+str(y-106)+'px);opacity:1}90%{transform:translate('+str(x-158)+'px,'+str(y-106)+'px);opacity:0}}'
    return scene(p,css)


def url():
    p=rect(16,33,172,39,'#23243a',PURPLE,11)+label(29,58,'tenor / giphy / klipy',12,PURPLE)+path('M99 82V122H207',DIM)
    p+=rect(197,89,103,112,'#123128',MINT,12)+path('M233 114 233 168 270 141Z',MINT,fill='#2effbf')
    p+=label(23,180,'LINK → MEDIA URL',14,MINT)
    p+=dot(99,92,5,PURPLE,'class="url-resolve"')+rect(204,94,89,101,'none',MINT,8,'class="url-result"')
    return scene(p,'.url-resolve{animation:urlResolve 8s linear infinite}.url-result{animation:urlResult 8s infinite}@keyframes urlResolve{0%,100%{opacity:0;transform:translate(0,0)}15%{opacity:1}40%{transform:translate(0,30px)}65%,80%{transform:translate(107px,30px);opacity:1}95%{transform:translate(107px,30px);opacity:0}}@keyframes urlResult{0%,50%,100%{opacity:.15}65%,90%{opacity:1}}')


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
