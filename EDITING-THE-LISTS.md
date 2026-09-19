# Le Lexique · KS3 & KS4 French — how the lists work

Live site → https://artmemry.github.io/KS3-KS4-French-Vocabulary-training/

6,182 list items across 232 lists, Years 7 to 11, built from the five
`Y*_FR_Vocabulary_by_Lesson_v2.xlsx` workbooks with lesson names from
*FRENCH OVERVIEW 2026-2027 MTPs.xlsx*. Everything runs in the browser: no
login, no server, no data leaving the student's device.

## One list, one file

Each lesson is its own file, so you can change a list without touching
anything else:

    data/lists/Y8U4.3.js        Year 8, Unit 4, third list

Open it on GitHub, click the pencil, edit, commit. That is the whole job —
there is nothing to rebuild and nothing to upload alongside it.

    BBA.list("Y8U4.3", [
      ["aller", "to go"],
      ["je vais", "I go;I am going"],
      ["le parc;un parc", "the park;a park;park"]
    ]);

One pair per line. A semicolon separates forms that are interchangeable:
everything before the first semicolon is what the student is shown, and the
rest are accepted as correct. So `"le parc;un parc"` prompts with *le parc*,
and `"the park;a park;park"` accepts any of the three.

**You can add, delete and reorder freely.** A word's place in a student's
progress is tied to its French, not to its position in the file, so
inserting a word at the top does not disturb anything below it. Changing a
word's English keeps its history; changing its French starts it afresh,
which is right, because it is then a different word.

## Adding a whole new list

Two steps. Add `data/lists/<id>.js` in the format above, then add one line to
`data/index.js` in the right unit:

    {"l": "Y8U4.15", "t": "L15 · Les sports d'hiver", "n": 18}

`n` is only a hint for the contents page; the list itself is the truth and
corrects it as soon as a student opens it.

## The contents page

`data/index.js` holds every year, unit and lesson title. It is what the home
page and the Progress tab read, which is why neither has to download 232
files — a list is fetched only when a student opens it.

To change a lesson's **title**, or a unit's name, edit `data/index.js`.

## Rebuilding from the workbooks

`build_fr_corpus.py` regenerates `data/index.js` and every file in
`data/lists/` from the five workbooks and the MTP. It overwrites hand edits,
so use it when the workbooks are the newer source, not as routine
maintenance.

## What the teacher sees

Codes begin `LEXKSFR2.` and are read by the one dashboard at
`artmemry.github.io/A-Level-French-BBA/teacher.html`, where KS3–KS4 French
has its own section and the roster can be filtered by year group. Set the
week's task there — pick the site, the class, tick the lists, copy the link,
post it in that class's channel.

## Three things worth knowing

**A word can belong to several lessons.** The workbooks allocate many words
to more than one lesson — in Year 10, 322 words are allocated to four each.
Each of those lessons gets the word, because a list should be exactly what
that lesson teaches. The consequence is that the site's totals count *list
items*, not unique words: 6,182 items from about 4,600 distinct words. A
student who meets *aller* again in Unit 3 practises it again there, which is
spacing rather than duplication.

**Years 7 to 9 start in the easier direction.** Français → Anglais is the
default for KS3 and the mix for KS4, which is what the GCSE asks for. A
student can change it on the lesson screen either way.

**Moving up in September.** A task link names its class. On a new device it
simply sets it. On a device already set to another year — the same student a
year later — the link does not move them silently; it offers: *This task was
set for Y9. You are down as Y8.* One tap moves them up.

## Where the lesson names came from, and what is still missing

| Year | Names from |
|---|---|
| Y7 Unit 1 | `Y7 MTP NEW` |
| Y7 Units 2 and 3 | **not written yet** — those 28 lists are named by their code (`L1`, `L2`…) until the Spring and Summer MTP exists |
| Y8, Y9 | the vocabulary workbooks themselves, which carry the lesson name beside the code |
| Y10 | `Y10 MTP`, keyed on sub-unit and lesson number |
| Y11 | `Y11 MTP`. The MTP numbers Unit 5 straight through 1–13 while the vocabulary uses U5.1 and U5.2, so U5.2 was offset onto lessons 7 onwards — worth a glance to confirm it lines up |

**One judgement to check.** The Y7 MTP restarts its numbering each term —
`U1L1`…`U1L11` in Autumn 1, then `U1L1`…`U1L9` again in Autumn 2 — while the
vocabulary workbook numbers Unit 1 straight through to L16. The two runs were
therefore joined end to end, so vocabulary `U1 L12` is Autumn 2's first
lesson. If the workbook meant the Autumn 2 numbering instead, say so and it
is a one-line change in `build_fr_corpus.py`.

Two other things the build reports: 261 rows were the same French word twice
in one list and were kept once, and Years 8 and 9 have 210 words the
workbooks mark *Unassigned*, which sit in a *Vocabulaire supplémentaire* unit
for that year rather than being dropped. Move any of them into a real lesson
by cutting the line from `data/lists/Y8UX.*.js` into the lesson's own file.
