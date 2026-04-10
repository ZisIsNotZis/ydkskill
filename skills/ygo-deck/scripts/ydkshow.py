#!/bin/env python
from statistics import stdev, quantiles
from sqlite3 import connect
from sys import argv
from glob import glob
from os import getenv, listdir
from functools import reduce
from collections import Counter, defaultdict
from datetime import date
TYPE = ' 魔法 陷阱  通常 效果 融合 仪式  灵魂 同盟 二重 调整 同调   速攻 永续 装备 场地 反击 反转 卡通 超量 灵摆  连接'.split(' ')
RACE = '战士 魔法师 天使 恶魔 不死 机械 水 炎 岩石 鸟兽 植物 昆虫 雷 龙 兽 兽战士 恐龙 鱼 海龙 爬虫类 念动力 幻神兽 创造神 幻龙 电子界 幻想魔'.split()
ATT = '地水炎风光暗神'
LINK = '↙↓↘←-→↖↑↗'
YGOROOT = getenv('YGOROOT', '.')
LF = {i: j for i in open(f'{YGOROOT}/lflist.conf').read().split('\n\n')[0].split('\n')if i[0]not in '#!'for i, j in [map(int, i.split()[:2])]}
SET = {int(i, 16): j for i in open(f'{YGOROOT}/strings.conf').read().split('setname ')[1:]for i, j in [i.split()[:2]]}
DATE = {int(j): date.fromisoformat(i.split()[0].replace('misc.ydk', '01-01'))for i in listdir(f'{YGOROOT}/pack')for j in open(f'{YGOROOT}/pack/{i}')if j.strip().isdigit()}
CARD = {i: f'{name}{f'({_})'if (_ := '|'.join(i for i in range(0, 64, 16)for i in [SET.get(set >> i & 0xffff, '')]if i not in name))else ''} {i}{f'→{alias}'if alias else ''}{f'lim{LF[alias or i]}'if (alias or i) in LF else ''} {DATE.get(i, DATE.get(alias, ''))} {''.join(TYPE[i]for i in range(27)if type & 1 << i)}{lv >> 24 if type & 0x1000000 else ''}{''.join(LINK[i]for i in range(9)if type & 0x4000000 and Def & 1 << i)} {f'{lv & 15}·{ATT[att.bit_length()-1]}·{RACE[race.bit_length()-1]} {'?'if atk < 0 else atk}/{'?'if Def < 0 else '-'if type & 0x4000000 else Def} 'if type & 1 else ''}{desc.replace('\r', '').replace('\n', '').strip()}'for i, alias, name, type, set, att, race, lv, atk, Def, desc in connect(f'{YGOROOT}/cards.cdb').execute('select datas.id,alias,name,type,setcode,attribute,race,level,atk,def,desc from datas join texts on datas.id=texts.id')}
if len(argv) < 2:
    print('''(YGOROOT=. N=300) ydkshow.py <file>.ydk|<ydkfolder>/...
    Show decks and statistics between them (top N cards) in a super information-dense human readable form
ydkshow.py <cardid>|<pattern>...
    Show cards that match id or ALL pattern in a super information-dense human readable form''')
elif argv[1].endswith('.ydk') or argv[1].endswith('/'):
    N = int(getenv('N', 300))
    argv = [i for i in argv[1:]for i in (glob(f'{i}**/*.ydk', recursive=True)if i.endswith('/')else [i])]
    print(*(f'{sum(j)/len(argv):.2f}±{stdev(j.extend((0,)*(len(argv)-len(j))) or j*2):.2f} q1-9={','.join('%d' % i for i in quantiles(j*2, n=10))} {CARD.get(i, i)}'for i, j in sorted(reduce(lambda a, b: [a[i].append(b)for i, b in b.items()] and a, (Counter(int(i)for i in open(i, 'rb').read().split()if i.isdigit())for i in argv), defaultdict(list)).items(), key=lambda i: -sum(i[1]))[:N]), sep='\n')
else:
    print(*(CARD.get(int(i), i)for i in argv[1:]if i.isdigit()), sep='\n')
    if argv := [i for i in argv[1:]if not i.isdigit()]:
        print(*(i for i in CARD.values()if all(j in i for j in argv)), sep='\n')
