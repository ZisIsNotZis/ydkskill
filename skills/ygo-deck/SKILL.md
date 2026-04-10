---
name: ygo-deck
description: Build, analyze, compare, and optimize Yu-Gi-Oh (OCG) decks using data-driven methodology. Use when asked to build a Yu-Gi-Oh deck, review a deck, compare two decks, check ban list compliance, discuss Yu-Gi-Oh strategy, or analyze card synergies.
allowedTools:
  - read_file
  - write_file
  - run_shell_command
  - grep_search
  - glob
  - task
  - web_search
  - web_fetch
---

# Yu-Gi-Oh Deck Building

## Prerequisites

**Required files** (all under project root):
- `cards.cdb` — card database (SQLite)
- `lflist.conf` — ban/limit list
- `strings.conf` — setcode name mapping
- `pack/` — deck timestamp data (optional, for ydkshow date display)

**Scripts** (under this skill directory):
- `scripts/ydkshow.py` — consensus statistics from deck databases
- `scripts/ydkcheck.py` — quantitative deck checker (8 check sections)

**If required files not found:** Ask user for their YGOPro root directory or project root. The paths may differ on different installations.

## Step 0: Identify Deck Type & Gather References

### 0.1 Gather local references
Search for existing ydk files matching the target archetype. YDK files can live at:
- `deck/*.ydk` — non-categorized (most common for users)
- `deck/*/*.ydk` — categorized by archetype/year

Search by both:
- **Filename**: Use `glob` with patterns like `**/*<name>*.ydk` and `**/*天气*.ydk` — user ydk filenames are often information-rich (e.g. `2024-tearlaments-pearl-solitaire-destruction.ydk`)
- **Content**: Use `grep_search` to find ydk files containing known card IDs of the archetype

### 0.2 Gather online references
Whether or not local references are found, search online for:
- Recent tournament results and top-cut decklists for the archetype
- Meta tier ranking and matchup data
- Recent ban list impacts on the archetype
- Community discussions (Reddit, Yugioh! Duel Links subreddit, Team APS, Master Duel Meta, etc.)

Use `web_search` with queries like:
- `<archetype> deck 2024 2025 tournament`
- `<archetype> top cut decklist`
- `<archetype> master duel guide` (for digital versions)
- `<archetype> ocg meta` (for physical Japanese meta)
- `<archetype> tcg meta` (for physical Western meta)

### 0.3 Classify the deck
From references gathered, classify the archetype's playstyle:
- **Control**: Many continuous spells/traps, impedance from field effects (weather, Eldlich)
- **Combo/Expand**: Many archetype monsters and extra deck, impedance from extra negates (Orcust, Swordsoul)
- **OTK**: Long search chains, fixed end field, hand trap escort (Kushaque, Tearlaments)

Read `[references/workflow.md](references/workflow.md)` for full classification criteria.

## Step 1: Determine Core

### 1.1 Query card database
Use `sqlite3 cards.cdb` to query all cards belonging to the target series by setcode. If setcode is unknown, search by card name pattern.

### 1.2 Analyze consensus (if local decks exist)
Run `scripts/ydkshow.py` on the collected reference decks:
```bash
python scripts/ydkshow.py deck/26*<name>*/
# or specific ydk files
python scripts/ydkshow.py deck/tearlaments*.ydk
```

Interpret output:
- **mean≥2.0, q90=3**: Cross-variant core, must include
- **mean 1.5-2.0, q90=3**: Core (some variants run 2), almost must include
- **mean 1.0-1.5, q90=2-3**: Important support, choose based on environment
- **mean 0.5-1.0, q90=1-2**: Optional support, understand before choosing
- **mean<0.5, q90=0-1**: Personal preference, exclude unless justified
- **stddev≥1.0**: Multi-axis coexistence signal
- **q75≥3 but mean<1.0**: Some variants run full but others run zero

### 1.3 If no local references found or references are outdated
Heavily rely on online search results from Step 0.2:
- Extract core cards from online decklists
- Cross-reference multiple sources for consensus
- Note regional differences (OCG vs TCG may differ due to ban list)
- Check if the archetype is competitive or casual

### 1.4 Verify each core card
For every card with mean≥1.0, verify it actually belongs to target series (setcode match). Non-series high-mean cards = combo partners, not core.

**Pass criteria**:
- ≥4 distinct cards from target series with mean≥2.0 and q90=3
- All series cards listed then filtered
- ≥1 extra deck summon point confirmed

Read `[references/db.md](references/db.md)` for database schema and queries.

## Step 2: Build Main Deck (40-44 cards)

### 2.1 Card selection
**Ratio**: Core 12-18 | Hand traps 9-12 | Generic support 3-6 | Generic removal 2-4

Sources for each category:
- **Core**: From Step 1, all confirmed series cards
- **Hand traps**: From `[references/handtrap.md](references/handtrap.md)` — cards that activate from HAND during OPPONENT'S TURN to INTERFERE
- **Generic support**: From `[references/support.md](references/support.md)` — generic search/mill/draw/summon
- **Generic removal**: From `[references/gentrap.md](references/gentrap.md)`, `[references/countertrap.md](references/countertrap.md)`

### 2.2 Compliance checks during construction
- Same-name ≤3 (respecting lim column: lim0=0, lim1≤1, lim2≤2)
- Check lim from ydkshow output or `lflist.conf`
- Hand traps ≥9
- Core ≥12
- No cards with mean<0.5 without strategic justification

### 2.3 Validate card usability
For each card, verify:
- It can actually be activated/used in this deck's context
- Cost/material requirements are satisfiable
- No conflicts with other cards (e.g., Dimension Shifter vs Foolish Burial)

Read `[references/rules.md](references/rules.md)` for construction rules including alias handling.

## Step 3: Build Extra Deck (12-15 cards)

### 3.1 Card selection
**Ratio**: Fusion/Synchro/XYZ 5-8 | Link-1/2 boards 3-5 | Link-3+ finishers 2-4 | Generic removal 1-2

Generic extra deck monsters: `[references/genericextra.md](references/genericextra.md)`

### 3.2 Verification
- Every extra monster must be summonable by main deck
- Verify summon conditions: Fusion needs fusion spell, Synchro needs tuner, XYZ needs same-level monsters, Link needs enough material types
- ≥1 Link-1 or Link-2 board
- ≥2 boss monsters
- Extra = 12-15 cards (minimum 12, understand why if reference runs <15)

## Step 4: Quantitative Verification

Run the full deck check:
```bash
python scripts/ydkcheck.py deck.ydk --section=all
```

**Must pass (0 ERRORs)**:
- **basic**: Main 40-60, Extra 0-15, recommended 40-44/12-15
- **duplicates**: Same-name ≤3 (with alias handling)
- **lflist**: All cards respect ban list (lim0=0, lim1≤1, lim2≤2)
- **start**: T1 cumulative start rate ≥80% (N_SAMPLES=500)
- **quality**: Score ≥60 (competitive level)

**Allowed warnings** (with explanation):
- **types**: Type ratio deviation with strategic reason
- **extra**: Summonability flagged but human-verified summonable
- **usability**: Cost warning acknowledged and addressed

If any check fails, fix the specific issue and re-run.

Read `[references/metrics.md](references/metrics.md)` for threshold definitions and quality scoring formula.

## Step 5: Compare with References

### 5.1 Calculate match rate
- Open 5-10 reference variants (local + online)
- Identify unique cards (non-core, non-series cards)
- Calculate: common unique cards / total unique cards × 100%
- ≥50% = acceptable

### 5.2 Analyze differences
For every card that differs between your build and references:
- Why does the reference run card A?
- Why did I choose card B?
- Which is better for the current environment?
- Can I justify my choice?

Read `[references/compare.md](references/compare.md)` for comparison methodology.

### 5.3 Online validation
Compare your build against online top-cut lists:
- Does your build match current meta direction?
- Are there tech choices you missed?
- Side deck options (if applicable)?

## Output Format

When building a deck, output must include:

### Deck List
```
#main
<card_id> × <count>  <card_name>  [role: core|handtrap|support|removal]
...
#extra
<card_id> × <count>  <card_name>  [role: boss|board|removal]
```

### Build Summary
- Step 0 result: Deck type classification with evidence
- Step 1 result: Core cards identified (N cards, X from setcode Y)
- Step 2 result: Main deck composition by category
- Step 3 result: Extra deck composition by type
- Step 4 result: ydkcheck.py output summary
- Step 5 result: Reference match rate and difference analysis

## Quick Commands

### Card lookup
```bash
# By ID (full card info with effect text)
python scripts/ydkshow.py <card_id>

# By keyword (all matching cards)
python scripts/ydkshow.py <keyword1> <keyword2>

# No args = help text
python scripts/ydkshow.py
```

### Deck statistics
```bash
# Single deck
python scripts/ydkshow.py deck.ydk

# Multiple decks (consensus)
python scripts/ydkshow.py deck/*<name>*.ydk
python scripts/ydkshow.py deck/26*<name>*/
```

### Deck check
```bash
# Full check
python scripts/ydkcheck.py deck.ydk --section=all

# Specific sections
python scripts/ydkcheck.py deck.ydk --section=basic     # counts
python scripts/ydkcheck.py deck.ydk --section=lflist    # ban list
python scripts/ydkcheck.py deck.ydk --section=start     # T0/T1 start rate
python scripts/ydkcheck.py deck.ydk --section=quality   # quality score
python scripts/ydkcheck.py deck.ydk --section=extra     # extra summonability
python scripts/ydkcheck.py deck.ydk --section=usability # card usability
```

### Database queries
```bash
# Card by name
sqlite3 cards.cdb "select d.id,t.name,d.type,d.setcode from datas d join texts t on d.id=t.id where t.name='CardName'"

# Cards by setcode (weather=265 example)
sqlite3 cards.cdb "select d.id,t.name,d.type from datas d join texts t on d.id=t.id where d.setcode&0xFFFF=265"

# Extra deck monsters
sqlite3 cards.cdb "select d.id,t.name from datas d join texts t on d.id=t.id where d.type & 0x4802040 > 0"
```

## Key Definitions

### Hand Trap (手坑)
Card that activates from **HAND** during **OPPONENT'S TURN** to **INTERFERE** (negate/destroy/banish/stop/draw-pressure). All 3 required: from hand + opponent turn + interference. Excludes: pure self-summon, pure searchers.

### Generic Support
Cards for **YOUR OWN** resource management (search/mill/draw/summon). Generic = no specific series restriction.

### Trap (陷阱)
Trap cards that **INTERFERE** from the **FIELD**. Excludes self-benefit cards (recursion/search).

### Counter (反击)
Counter traps or quick-play spells that **NEGATE/COUNTER** opponent actions.

### NHT (Non-Handtrap Interference)
Monsters that **INTERFERE** from the **FIELD**. Excludes pure searchers/extenders.

## Important Notes

- **Always query the card database** — never guess card IDs, names, or effects
- **Always verify ban list** (lim column) before including any card
- **A card can appear in multiple catalogs** if it meets multiple definitions (e.g., 无限泡影 qualifies as both hand trap AND generic trap)
- **Online sources are equally important as local references** — the meta evolves, and local data may be outdated
- **User's ydk filenames are often rich in information** — parse them for archetype, strategy, tier, and date
- **When local data is sparse, lean heavily on web search** for current meta, tournament results, and community consensus
- **Script paths are relative to this skill directory**: `.qwen/skills/ygo-deck/scripts/`
