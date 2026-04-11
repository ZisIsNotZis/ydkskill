#!/bin/env python
from statistics import stdev, quantiles
from sqlite3 import connect
from sys import argv
from glob import glob
from os import getenv, listdir
from functools import reduce
from collections import Counter, defaultdict
from datetime import date
TYPE = '怪兽 魔法 陷阱  通常 效果 融合 仪式 陷怪 灵魂 同盟 二重 调整 同调 衍生  速攻 永续 装备 场地 反击 反转 卡通 超量 灵摆 特招 连接'.split(' ')
RACE = '战士 魔法师 天使 恶魔 不死 机械 水 炎 岩石 鸟兽 植物 昆虫 雷 龙 兽 兽战士 恐龙 鱼 海龙 爬虫类 念动力 幻神兽 创造神 幻龙 电子界 幻想魔'.split()
ATT = '地水炎风光暗神'
LINK = '↙↓↘← →↖↑↗'
CAT = '魔陷破坏 怪兽破坏 卡片除外 送去墓地 返回手卡 返回卡组 手卡破坏 卡组破坏 抽卡辅助 卡组检索 卡片回收 表示形式 控制权 攻守变化 穿刺伤害 多次攻击 攻击限制 直接攻击 特殊召唤 衍生物 种族相关 属性相关 LP伤害 LP回复 破坏耐性 效果耐性 指示物 幸运 融合相关 同调相关 超量相关 效果无效'.split()
YGOROOT = getenv('YGOROOT', '.')
LF = {i: j for i in open(f'{YGOROOT}/lflist.conf').read().split('\n\n')[0].split('\n')if i[0]not in '#!'for i, j in [map(int, i.split()[:2])]}
SET = {int(i, 16): j.split('|') for i in open(f'{YGOROOT}/strings.conf').read().split('setname ')[1:]for i, j in [i.split()[:2]]}
SET = {i:'|'.join(set(k for j,k in SET.items()if i&0xfff==j&0xfff and i&j==j for k in k))for i in SET}
DATE = {int(j): date.fromisoformat(i.split()[0].replace('misc.ydk', '01-01'))for i in listdir(f'{YGOROOT}/pack')for j in open(f'{YGOROOT}/pack/{i}')if j.strip().isdigit()}
CARD = {i: f'{name}{f'({_})'if (_:='|'.join(SET[set >> i & 0xffff]for i in range(0,64,16)if set>>i))else ''} {i}{f'→{alias}'if alias else''}{f'lim{_}'if(_:=LF.get(alias or i,3))!=3 else''} {DATE.get(i,DATE.get(alias,''))} {''.join(j for i,j in enumerate(TYPE)if type&1<<i)}{lv >> 24 if type & 0x1000000 else ''}{''.join(LINK[i]for i in range(9)if type & 0x4000000 and Def & 1 << i)}{f'({_})'if(_:='|'.join(j for i,j in enumerate(CAT)if category%0x100000000&1<<i))else''} {f'{'连接'if type&0x4000000 else''}{lv & 15}{'阶'if type&0x800000 else'星'}·{ATT[att.bit_length()-1]}属性·{RACE[race.bit_length()-1]}族 {'?'if atk < 0 else atk}/{'?'if Def < 0 else '-'if type & 0x4000000 else Def} 'if type & 0x101 else ''}{desc.replace('\r', '').replace('\n', '').strip()}'for i, alias, name, type, set, att, race, lv, atk, Def, category, desc in connect(f'{YGOROOT}/cards.cdb').execute('select datas.id,alias,name,type,setcode,attribute,race,level,atk,def,category,desc from datas join texts on datas.id=texts.id')}
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
        print(*sorted(i for i in CARD.values()if all(j in i for j in argv)), sep='\n')
