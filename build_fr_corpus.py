#!/usr/bin/env python3
"""Build the KS3–KS4 French lists from the five year-group workbooks, with
lesson titles taken from FRENCH OVERVIEW 2026-2027 MTPs.xlsx.

The French workbooks come in three shapes, and a word is often allocated to
several lessons at once, so each of those lessons gets it: a list is exactly
what the workbook says that lesson teaches.

Output: data/index.js (the contents page) and one file per lesson in
data/lists/ — the same layout as the Spanish site, so both are edited the
same way.
"""
import json, os, re, unicodedata
from collections import OrderedDict, defaultdict
import openpyxl

SRC = "/mnt/user-data/uploads/KS3 & KS4 French"
MTP = "/root/.claude/uploads/d94fa504-7d80-503f-af76-da936ab863dc/fe1047ac-FRENCH_OVERVIEW_2026-2027_MTPs.xlsx"
OUT = "/home/claude/work/KS3-KS4-French-Vocabulary-training"

YEARS = OrderedDict([
    ("Y7",  dict(file="Y7_FR_Vocabulary_by_Lesson_v2.xlsx",  name="Year 7")),
    ("Y8",  dict(file="Y8_FR_Vocabulary_by_Lesson_v2.xlsx",  name="Year 8")),
    ("Y9",  dict(file="Y9_FR_Vocabulary_by_Lesson_v2.xlsx",  name="Year 9")),
    ("Y10", dict(file="Y10_FR_Vocabulary_by_Lesson_v2.xlsx", name="Year 10")),
    ("Y11", dict(file="Y11_FR_Vocabulary_by_Lesson_v2.xlsx", name="Year 11")),
])

# Unit names as the KS3–KS4 curriculum progression sheet gives them.
UNIT_NAMES = {
    "Y7":  {"1": "Moi et ma famille — my family",
            "2": "Ma maison et ma ville — my home and town",
            "3": "Mon collège — my school"},
    "Y8":  {"4": "Le temps libre — free time",
            "5": "Les voyages — travel",
            "6": "Les métiers — careers"},
    "Y9":  {"7": "Les modes de vie — lifestyles",
            "8": "Les problèmes — problems and the environment",
            "9": "La technologie — technology"},
    "Y10": {"1": "Les médias et la technologie — media, gaming, music, TV and film",
            "2": "La famille et les amis — family, friends and relationships",
            "3": "La santé et l'égalité — sport, well-being, food and equality",
            "4": "Le collège et l'avenir — school and future opportunities"},
    "Y11": {"5": "Les voyages et le tourisme — travel, tourism and accommodation",
            "6": "Ma ville et l'environnement — transport, shopping, town and the environment"},
}
COMMON_NAME = "Les mots courants — high-frequency words used all year"
EXTRA_NAME  = "Vocabulaire supplémentaire — extra words, not yet placed in a lesson"

def word_id(word, width=4):
    h = 0x811c9dc5
    for ch in unicodedata.normalize("NFD", word.strip().lower()):
        h ^= ord(ch) & 0xFF
        h = (h * 0x01000193) & 0xFFFFFFFF
    return format(h, "08x")[:width]

def norm(s):
    return re.sub(r"\s+", " ", str(s or "").replace("\xa0", " ")).strip()

def split_variants(cell):
    out = []
    for part in re.split(r"[;；]", str(cell or "")):
        part = norm(part)
        if part and part not in out:
            out.append(part)
    return out

# ─────────────────────────────────────────────── lesson titles from the MTP
def mtp_titles():
    """(year, unit, lesson) -> title, from the three MTP layouts."""
    wb = openpyxl.load_workbook(MTP, data_only=True, read_only=True)
    t = {}

    # Y7: the sheet restarts its numbering each term — U1L1…U1L11 in Autumn 1,
    # then U1L1…U1L9 again in Autumn 2 — while the vocabulary workbook numbers
    # Unit 1 straight through to L16. So the rows are taken in sheet order and
    # renumbered 1..N per unit. Spring and Summer (Units 2 and 3) are not
    # written yet, so those lists keep their code as their name until they are.
    ws = wb["Y7 MTP NEW "]
    seq = defaultdict(list)
    for r in ws.iter_rows(values_only=True):
        cells = [norm(v) for v in (r or [])]
        for i, c in enumerate(cells):
            m = re.fullmatch(r"U(\d+)\s*L(\d+)", c, re.I)
            if not m:
                continue
            nxt = next((x for x in cells[i + 1:] if x), "")
            if nxt and not re.fullmatch(r"(?:skip if required|fast feedback.*)", nxt, re.I):
                seq[m.group(1)].append(nxt)
            break
    for unit, titles in seq.items():
        for i, title in enumerate(titles, 1):
            t[("Y7", unit, i)] = title

    # Y8 and Y9 carry their titles in the vocabulary workbook itself.

    # Y10: a unit heading that changes down the sheet, then 'lesson # | name'
    ws = wb["Y10 MTP"]
    cur = None
    for r in ws.iter_rows(values_only=True):
        a = norm(r[0] if r else "")
        b = norm(r[1] if r and len(r) > 1 else "")
        c = norm(r[2] if r and len(r) > 2 else "")
        if a:
            m = re.search(r"Unit\s*(\d+(?:\.\d+)?)", a)
            if m:
                cur = m.group(1)
        if cur and b.isdigit() and c and c.lower() != "lesson name":
            t[("Y10", cur, int(b))] = c

    # Y11: 'title | Unit 5 | lesson #', numbered straight through the unit
    ws = wb["Y11 MTP"]
    for r in ws.iter_rows(values_only=True):
        title = norm(r[0] if r else "")
        unit = norm(r[1] if r and len(r) > 1 else "")
        num = norm(r[2] if r and len(r) > 2 else "")
        m = re.search(r"Unit\s*(\d+)", unit)
        if title and m and num.isdigit():
            t[("Y11", m.group(1), int(num))] = title
    wb.close()
    return t

TITLES = mtp_titles()

def title_for(year, unit, sub, lesson, offsets):
    """Try the sub-unit key, then the major-unit key, then the sub-unit's
    offset into a unit the MTP numbers straight through (Y11 does)."""
    if lesson is None:
        return None
    if sub:
        v = TITLES.get((year, f"{unit}.{sub}", lesson))
        if v: return v
    v = TITLES.get((year, unit, lesson))
    if v and not sub: return v
    if sub:
        off = offsets.get((year, unit, sub), 0)
        v = TITLES.get((year, unit, lesson + off))
        if v: return v
    return v if v else None

# ─────────────────────────────────────────────── token parsing
def parse_token(tok):
    """'U2.3 L3' -> ('2','3',3) · 'U4 L2#2' -> ('4',None,2) · 'Common' -> COMMON"""
    tok = norm(tok)
    if not tok:
        return None
    if tok.lower().startswith("common"):
        return ("C", None, None)
    if tok.lower().startswith("unassigned"):
        return ("X", None, None)
    m = re.search(r"U\s*(\d+)(?:\.(\d+))?", tok, re.I)
    ml = re.search(r"\bL\s*(\d+)", tok, re.I)
    if not m:
        return None
    return (m.group(1), m.group(2), int(ml.group(1)) if ml else None)

def clean_title(raw):
    """Y8/Y9 keep a title after the code: 'U4 L1 — Unit 4 Lesson 1 Role Models — …'"""
    t = norm(raw)
    t = re.sub(r"^U\s*\d+(?:\.\d+)?\s*L[\d\s&.]*", "", t, flags=re.I)
    t = re.sub(r"^[—\-–:\s]+", "", t)
    for _ in range(3):
        before = t
        t = re.sub(r'^"?\s*Y\d+\s*FR\s*,?\s*', "", t, flags=re.I)
        t = re.sub(r"^Unit\s*\d+\s*(?:Lesson\s*\d+)?\s*[—\-–:]?\s*", "", t, flags=re.I)
        t = re.sub(r"^U\s*\d+(?:\.\d+)?\s*L[\d\s&.]*[—\-–:]?\s*", "", t, flags=re.I)
        t = t.strip(' "—-–:')
        if t == before:
            break
    return t or norm(raw)

# ─────────────────────────────────────────────── readers
def read_year(year, path):
    """Returns rows of {fr, en, tokens:[(unit,sub,lesson)], title_hint}."""
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    ws = wb["Full List"]
    rows = [list(r) for r in ws.iter_rows(values_only=True)]
    hdr = [norm(v).lower() for v in rows[0]]
    def col(*names):
        for i, h in enumerate(hdr):
            if any(h.startswith(nme) for nme in names):
                return i
        return None
    fi, ei = col("french"), col("english")
    ai = col("allocated")
    ui, li = col("unit"), col("lesson")
    out = []
    for r in rows[1:]:
        if fi is None or ei is None or not r:
            continue
        fr, en = norm(r[fi] if fi < len(r) else ""), norm(r[ei] if ei < len(r) else "")
        if not fr or not en:
            continue
        toks, hint = [], ""
        if ai is not None and ai < len(r):
            for piece in str(r[ai] or "").split(","):
                t = parse_token(piece)
                if t: toks.append(t)
        elif li is not None and li < len(r):
            raw = norm(r[li])
            t = parse_token(raw)
            if t: toks.append(t)
            hint = clean_title(raw)
            if t and t[0] == "X":
                hint = ""
        if not toks:
            toks = [("X", None, None)]
        out.append(dict(fr=fr, en=en, tokens=toks, hint=hint))
    wb.close()
    return out

# ─────────────────────────────────────────────── build
def main():
    groups = OrderedDict()      # (year, unitkey) -> OrderedDict(lesson_no -> {title, rows})
    untitled = 0
    for year, meta in YEARS.items():
        rows = read_year(year, os.path.join(SRC, meta["file"]))

        # how many lessons each sub-unit has, so a sub-unit can be offset into a
        # unit the MTP numbers straight through
        span = defaultdict(int)
        for row in rows:
            for (u, sub, l) in row["tokens"]:
                if sub and l:
                    span[(year, u, sub)] = max(span[(year, u, sub)], l)
        offsets = {}
        for (y, u) in {(y, u) for (y, u, _s) in span}:
            run = 0
            for sub in sorted({s for (yy, uu, s) in span if yy == y and uu == u}, key=int):
                offsets[(y, u, sub)] = run
                run += span[(y, u, sub)]

        for row in rows:
            for (u, sub, l) in row["tokens"]:
                key = (year, u)
                g = groups.setdefault(key, OrderedDict())
                lnum = l if l is not None else 0
                slot = (sub or "", lnum)
                if slot not in g:
                    if u == "C":
                        title = COMMON_NAME
                    elif u == "X":
                        title = EXTRA_NAME
                    else:
                        title = title_for(year, u, sub, l, offsets) or row["hint"] or ""
                        if not title:
                            title = f"U{u}{'.'+sub if sub else ''} L{l}" if l else f"U{u}"
                            untitled += 1
                    g[slot] = dict(title=title, rows=[])
                elif row["hint"] and not g[slot]["title"]:
                    g[slot]["title"] = row["hint"]
                g[slot]["rows"].append(row)

    # ─────────── emit
    lists_dir = os.path.join(OUT, "data", "lists")
    os.makedirs(lists_dir, exist_ok=True)
    for f in os.listdir(lists_dir):
        if f.endswith(".js"):
            os.remove(os.path.join(lists_dir, f))

    manifest_units, CHUNK, stats = OrderedDict(), 30, defaultdict(int)
    for (year, u), slots in groups.items():
        meta = YEARS[year]
        uid = f"{year}U{u}"
        if u == "C":
            unit_label = f"{meta['name']} · {COMMON_NAME}"
        elif u == "X":
            unit_label = f"{meta['name']} · {EXTRA_NAME}"
        else:
            unit_label = (f"{meta['name']} · Unité {u} — "
                          + UNIT_NAMES.get(year, {}).get(u, f"Unité {u}"))

        # order the lessons, and break the big bucket units into lists of 30
        ordered = sorted(slots.items(), key=lambda kv: (kv[0][0] or "", kv[0][1]))
        emitted = []
        if u in ("C", "X"):
            allrows = [r for _k, v in ordered for r in v["rows"]]
            for i in range(0, len(allrows), CHUNK):
                nm = i // CHUNK + 1
                label = (COMMON_NAME if u == "C" else EXTRA_NAME).split(" — ")[0]
                emitted.append((f"{uid}.{nm}", f"{label} {nm}", allrows[i:i + CHUNK]))
        else:
            for i, ((sub, lnum), v) in enumerate(ordered, 1):
                tag = f"{u}.{sub} L{lnum}" if sub else f"L{lnum}"
                title = v["title"] or ""
                # a lesson the MTP does not name yet keeps its code, once
                if re.fullmatch(r"U?\d+(?:\.\d+)?\s*L\d+", title, re.I):
                    title = ""
                if title and not title.startswith(tag):
                    title = f"{tag} · {title}"
                emitted.append((f"{uid}.{i}", title or tag, v["rows"]))

        for lesson_id, title, rws in emitted:
            lines, used = [], set()
            seen_here = set()
            for row in rws:
                fr, en = split_variants(row["fr"]), split_variants(row["en"])
                if not fr or not en:
                    continue
                sig = fr[0].lower()
                if sig in seen_here:            # the same word twice in one list
                    stats["duplicate in list"] += 1
                    continue
                seen_here.add(sig)
                key = word_id(fr[0])
                if key in used:
                    key = word_id(fr[0], 6)
                    stats["id widened"] += 1
                used.add(key)
                lines.append("  [%s, %s]" % (json.dumps(";".join(fr), ensure_ascii=False),
                                             json.dumps(";".join(en), ensure_ascii=False)))
            if not lines:
                continue
            body = (
                "/* %s — %s\n"
                "   %s\n"
                '   One pair per line: ["French", "English"]. Separate interchangeable\n'
                '   forms with a semicolon — "le garçon;un garçon" / "the boy;a boy;boy".\n'
                "   Add, remove or reorder freely: a word keeps its place in a student's\n"
                "   progress as long as its French stays the same. */\n"
                "BBA.list(%s, [\n%s\n]);\n"
            ) % (lesson_id, title.replace("*/", ""), unit_label.replace("*/", ""),
                 json.dumps(lesson_id), ",\n".join(lines))
            with open(os.path.join(lists_dir, lesson_id + ".js"), "w",
                      encoding="utf-8", newline="\n") as f:
                f.write(body)
            mu = manifest_units.setdefault(uid, OrderedDict(
                [("u", uid), ("y", year), ("name", unit_label), ("lessons", [])]))
            mu["lessons"].append(OrderedDict([("l", lesson_id), ("t", title), ("n", len(lines))]))
            stats["items"] += len(lines)

    # units in year order, real units before Common and Extra
    def ukey(uid):
        y = re.match(r"(Y\d+)U(.+)", uid)
        yr = list(YEARS).index(y.group(1))
        u = y.group(2)
        return (yr, 98 if u == "C" else 99 if u == "X" else int(u))
    ordered_units = [manifest_units[k] for k in sorted(manifest_units, key=ukey)]

    manifest = OrderedDict([
        ("years", [OrderedDict([("y", y), ("name", m["name"])]) for y, m in YEARS.items()]),
        ("units", ordered_units)])
    with open(os.path.join(OUT, "data", "index.js"), "w", encoding="utf-8", newline="\n") as f:
        f.write(
            "/* The contents page: every year, unit and lesson, with the number of words\n"
            "   each list holds. The site reads this to draw the home page and the progress\n"
            "   tab; the lists themselves load one at a time, from data/lists/.\n"
            "\n"
            "   Editing an existing list: change data/lists/<lesson>.js only. The count below\n"
            "   is a hint and corrects itself once the list loads.\n"
            "   Adding a new list: add the file, then one line here in the right unit.\n"
            "   Generated by build_fr_corpus.py, which rewrites both. */\n"
            "window.BBA_INDEX = " + json.dumps(manifest, ensure_ascii=False, indent=1) + ";\n")

    nl = sum(len(u["lessons"]) for u in ordered_units)
    print(f"{stats['items']} list items · {nl} lessons · {len(ordered_units)} units")
    for u in ordered_units:
        print(f"   {u['u']:7s} {len(u['lessons']):3d} lists {sum(l['n'] for l in u['lessons']):5d} items   {u['name'][:70]}")
    print("lessons with no MTP title:", untitled, "| other:", dict(stats))

main()
