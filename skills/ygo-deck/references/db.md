# cards.cdb 数据库

## 表结构
- `datas`: id, alias, setcode, type, level, race, attribute, atk, def
- `texts`: id, name, desc

## Type位掩码 (见script/constant.lua)
- TYPE_MONSTER=0x1, TYPE_SPELL=0x2, TYPE_TRAP=0x4
- TYPE_EFFECT=0x20, TYPE_TUNER=0x1000
- TYPE_FUSION=0x40, TYPE_SYNCHRO=0x2000, TYPE_XYZ=0x800000, TYPE_LINK=0x4000000
- 额外怪兽判定: `type & 0x4802040 > 0`

## Setcode
- 64位整数, 4×16位字段: `(setcode >> N*16) & 0xFFFF`
- 字段含义: 系列名, 子字段1, 子字段2, 子字段3
- 常见: 烙印=1154, 相剑=1254, 自奏=1168, 深渊之兽=1234, 珠泪=1232

## 常用查询
```sql
-- 查卡名
SELECT d.id, d.alias, d.setcode, d.type, d.level FROM datas d JOIN texts t ON d.id=t.id WHERE t.name='卡名';
-- 查系列(检查setcode 4个16位)
SELECT d.id, t.name, d.type, d.level FROM datas d JOIN texts t ON d.id=t.id WHERE (d.setcode&0xFFFF=1154 OR (d.setcode>>16)&0xFFFF=1154 OR (d.setcode>>32)&0xFFFF=1154 OR (d.setcode>>48)&0xFFFF=1154) AND NOT d.alias;
-- 查额外怪兽
SELECT id, name FROM texts WHERE id IN (SELECT id FROM datas WHERE type & 0x4802040 > 0);
```
