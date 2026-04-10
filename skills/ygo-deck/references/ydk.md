# YDK文件与ydkshow工具

## YDK格式
- `#main` → 主卡组卡片id(每行一个)
- `#extra` → 额外卡组卡片id
- `!side` → 副卡组(可选)
- 仅含数字id, 无卡名
- 文件位置: `deck/*.ydk`(未分类, 最常见) 或 `deck/*/*.ydk`(按系列/年份分类)

## ydkshow用法
```bash
# 无参数 = 帮助
python scripts/ydkshow.py

# 单卡组统计 (直接输出该卡组所有卡, 带完整信息)
python scripts/ydkshow.py deck/天气.ydk

# 多卡组共识 (显示mean/stddev/quantiles)
python scripts/ydkshow.py deck/26*天气*/
python scripts/ydkshow.py deck/*tearlament*.ydk
N=50 python scripts/ydkshow.py deck/26*天气*/   # 只显示top 50

# 按卡ID查卡
python scripts/ydkshow.py 14558127
# 输出: 灰流丽 14558127lim2 2017-01-14 效果 3·炎·不死 0/1800 <效果文本>

# 按关键词查卡 (所有匹配卡片)
python scripts/ydkshow.py 灰流丽
python scripts/ydkshow.py 天气 天使
# 输出所有包含关键词的完整卡片信息
```

## 输出格式
`mean±stddev q1-9=q10...q90 卡名(系列) id→alias lim 日期 类型 星级·属性·种族 攻/守 效果`

## 关键列
- mean: 平均携带量(多卡组时), 单卡组时=实际数量
- stddev: 标准差, 高(≥1.0)=多轴共存
- q1-9: quantiles 0.1~0.9, q10=0说明10%不带, q90=3说明90%带3张
- 系列: 卡片所属系列(setcode翻译, 不一定出现在卡名中)
- id: 卡片密码
- →alias: 别名id (≠0且与id差>10时=同名不同效果)
- lim: lim0=禁用, lim1=限1, lim2=限2, 无=不限
- 日期: 卡片发行/收录日期 (从pack/目录推导)
- 类型: 怪兽/魔法/陷阱 + 子类型(效果/永续/反击等)
- 星级·属性·种族 攻/守: 怪兽参数

## 阈值解读
- mean≥2.0且q90=3: 跨变体核心, 必带
- mean 1.5-2.0且q90=3: 核心, 几乎必带
- mean 1.0-1.5且q90=2-3: 重要支援
- mean 0.5-1.0且q90=1-2: 可选支援
- mean<0.5且q90=0-1: 个人偏好
- stddev≥1.0: 多轴共存信号

## 解析辅助
- 额外怪兽判定: `type & 0x4802040 > 0`
- YDK文件内容仅为数字id, 需查cards.cdb获取卡名和效果
