#!/usr/bin/env python3
"""
Placement engine: takes content JSON where each question has
  {"q":..., "correct":"<text>", "wrongs":[t1,t2,t3,t4], "comment":..., "numeric":bool?}
and assigns A-E positions using a per-file balanced, deterministic shuffle
(seeded by topic number) so that:
  - each letter appears ~2x per 10-question file (pattern covers all 5 twice),
  - no letter 3x consecutive,
  - wrong-answer order is shuffled per question.

Outputs the final questions.json consumed by build_xlsx.py / qa_check.py.
"""
import sys, json, random

# Balanced correct-letter pattern for a 10-question file: each letter twice,
# arranged so no 3-in-a-row and good visual spread.
BASE_PATTERN = ["A", "C", "E", "B", "D", "B", "D", "A", "C", "E"]

def place(data):
    out = {}
    for topic, qs in sorted(data.items()):
        seed = int(topic)
        rng = random.Random(seed)
        n = len(qs)
        # build pattern of length n: repeat BASE and lightly shuffle in blocks
        pattern = []
        letters_cycle = ["A", "B", "C", "D", "E"]
        # construct counts as even as possible
        base = (BASE_PATTERN * ((n // 10) + 1))[:n]
        pattern = base[:]
        # deterministic local shuffle that preserves no-3-in-row
        def ok(p):
            for i in range(len(p) - 2):
                if p[i] == p[i+1] == p[i+2]:
                    return False
            return True
        for _ in range(200):
            cand = pattern[:]
            rng.shuffle(cand)
            if ok(cand):
                pattern = cand
                break
        rows = []
        for i, q in enumerate(qs):
            correct_letter = pattern[i]
            wrongs = q["wrongs"][:]
            rng.shuffle(wrongs)
            cells = {}
            wi = 0
            for L in "ABCDE":
                if L == correct_letter:
                    cells[L] = q["correct"]
                else:
                    cells[L] = wrongs[wi]; wi += 1
            row = {"q": q["q"], **cells, "correct": correct_letter,
                   "comment": q["comment"]}
            if q.get("numeric"):
                row["numeric"] = True
            rows.append(row)
        out[topic] = rows
    return out

def main():
    with open(sys.argv[1], encoding="utf-8") as f:
        data = json.load(f)
    out = place(data)
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"placed {sum(len(v) for v in out.values())} questions into {sys.argv[2]}")

if __name__ == "__main__":
    main()
