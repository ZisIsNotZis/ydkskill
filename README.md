# ygo-deck — Yu-Gi-Oh! Deck Building Skill for Qwen Code / Claude Code

Data-driven Yu-Gi-Oh! (OCG) deck building, analysis, and optimization. Build competitive decks using consensus from historical deck databases, verify with quantitative checks, and compare against the current meta.

> **Works with both Qwen Code and Claude Code.** Uses the same `SKILL.md` format.

## Quickstart

### 1. Install the Skill

**For Qwen Code:**
```bash
# Clone this repo
git clone https://github.com/ZisIsNotZis/ydkskill.git
# Copy the skill to your project skills
cp -r ydkskill/skills/ygo-deck /your/project/.qwen/skills/ygo-deck
```

**For Claude Code:**
```bash
git clone https://github.com/ZisIsNotZis/ydkskill.git
cp -r ydkskill/skills/ygo-deck ~/.claude/skills/ygo-deck
```

### 2. Prerequisites

The skill requires a YGOPro installation or card database:

| File | Description | Where to find |
|------|-------------|---------------|
| `cards.cdb` | Card database (SQLite) | Any YGOPro client `cards.cdb` |
| `lflist.conf` | Ban/limit list | YGOPro client or [ygopro-lflist](https://github.com/Fluorohydride/ygopro) |
| `strings.conf` | Setcode name mappings | YGOPro client |
| `pack/` *(optional)* | Card release dates | YGOPro client |

If you don't have a YGOPro client, download one from [Fluorohydride/ygopro](https://github.com/Fluorohydride/ygopro) or set the `YGOROOT` environment variable to your YGOPro directory:

```bash
export YGOROOT=/path/to/your/ygopro
```

### 3. Use It

Start Qwen Code / Claude Code in your project directory and ask:

- _"帮我组一套刻魔混沌卡组"_ — Build a deck from scratch
- _"Check this deck for ban list compliance"_ — Verify a `.ydk` file
- _"Compare these two decklists"_ — Analyze differences
- _"What's the current meta for this archetype?"_ — Online meta research

## What This Skill Does

### 5-Step Deck Building Workflow
1. **Identify** deck type (control/combo/OTK) via consensus analysis + online meta
2. **Determine core** cards from database queries + historical deck data
3. **Build main deck** (40-44) with hand trap / support / removal ratios
4. **Build extra deck** (12-15) with summonability verification
5. **Verify & compare** against references with quantitative scoring

### Built-in Tools

| Tool | Purpose |
|------|---------|
| `scripts/ydkshow.py` | Card lookup + deck consensus statistics |
| `scripts/ydkcheck.py` | 8-section quantitative deck checker |

### Card Catalogs (16 reference files)
- Hand traps, field-interference monsters, traps, counters, support, generic extras
- Mini engines, ban list rules, database schema, combat strategy
- Comparison methodology, quality metrics, lessons learned

## Usage Examples

### Look up a card by ID
```bash
python scripts/ydkshow.py 14558127
# 灰流丽 14558127lim2 2017-01-14 效果 3·炎·不死 0/1800 ...
```

### Search cards by keyword
```bash
python scripts/ydkshow.py 天气 天使
# Returns all cards matching both keywords
```

### Analyze deck consensus
```bash
N=50 python scripts/ydkshow.py deck/26*刻魔*/
# mean±stddev q1-9=... for each card across all matching decks
```

### Full deck verification
```bash
python scripts/ydkcheck.py mydeck.ydk --section=all
# Checks: counts, duplicates, ban list, T0/T1 start rate, quality score, etc.
```

## Project Structure

```
skills/ygo-deck/
├── SKILL.md                  # Main skill instructions (entry point)
├── references/               # Knowledge base (loaded on demand)
│   ├── rules.md              # Deck construction rules
│   ├── workflow.md           # 5-step build workflow
│   ├── compare.md            # Deck comparison methodology
│   ├── metrics.md            # Quality scoring, T0/T1 thresholds
│   ├── combat.md             # First/second turn strategy
│   ├── lessons.md            # Categorized build-phase lessons
│   ├── handtrap.md           # Hand-activated disruption cards
│   ├── nht.md                # Field-interference monsters
│   ├── gentrap.md            # Field-activated trap cards
│   ├── countertrap.md        # Counter traps & quick-play
│   ├── support.md            # Generic support cards
│   ├── genericextra.md       # Generic extra deck monsters
│   ├── engines.md            # Mini engine directory
│   ├── db.md                 # cards.cdb schema & queries
│   ├── lflist.md             # Ban list format
│   └── ydk.md                # YDK parsing & ydkshow usage
└── scripts/
    ├── ydkcheck.py            # Quantitative deck checker (8 sections)
    └── ydkshow.py             # Card lookup & consensus statistics
```

## License

[MIT](LICENSE)

## Credits

- Card database: [Fluorohydride/ygopro](https://github.com/Fluorohydride/ygopro)
- Deck consensus analysis from historical YGOPro deck collections
- Card descriptions from `cards.cdb` / `strings.conf` / `lflist.conf`
