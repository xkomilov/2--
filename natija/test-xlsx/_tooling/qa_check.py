#!/usr/bin/env python3
"""
QA checker for the question JSON. Enforces task rules and prints flags.

Rules checked:
4. Letter balance per file and overall; no letter 3x consecutive (correct col).
   Also wrong-answer order mixed (we check correct letter distribution).
5. Length: correct answer not >10% longer than longest wrong (hard flag >30%).
6. Wrong-answer templating:
   - at most 1 wrong answer starting with Faqat/Hech/Umuman/Barcha per question;
   - not 3+ wrong answers starting with the same word (unless correct starts same).
   - numeric/formula questions exempt (marked by "numeric": true).
7. (manual) all options grammatically fit — not auto-checkable.
8. correct is a valid letter and comment starts with "To'g'ri javob:".
"""
import sys, json, re, os
from collections import Counter

START_WORDS = ("faqat", "hech", "umuman", "barcha")

def first_word(s):
    s = s.strip().lower()
    m = re.match(r"[a-zа-яёʼ'`’]+", s)
    return m.group(0) if m else s.split()[0] if s.split() else ""

def check(data):
    flags = []
    overall = Counter()
    long_flagged = 0
    total_q = 0
    per_file_letters = {}

    for topic, rows in sorted(data.items()):
        letters = [r["correct"] for r in rows]
        per_file_letters[topic] = Counter(letters)
        overall.update(letters)
        total_q += len(rows)

        # 3-in-a-row
        for i in range(len(letters) - 2):
            if letters[i] == letters[i+1] == letters[i+2]:
                flags.append(f"[{topic}] 3x ketma-ket harf '{letters[i]}' savol {i+1}-{i+3}")

        # per-file balance: each letter should appear; spread check
        c = per_file_letters[topic]
        n = len(rows)
        # expect roughly n/5 each; flag if any letter 0 or any > ceil(n/5)+1 strongly
        for L in "ABCDE":
            if c.get(L, 0) == 0:
                flags.append(f"[{topic}] '{L}' harfi umuman ishlatilmagan ({dict(c)})")
        mx = max(c.values()); mn = min(c.get(L,0) for L in "ABCDE")
        if mx - mn > 2:
            flags.append(f"[{topic}] harf muvozanati nomutanosib: {dict(c)}")

        for i, r in enumerate(rows, start=1):
            qid = f"{topic} S{i}"
            # 8: correct valid + comment format
            if r["correct"] not in "ABCDE":
                flags.append(f"[{qid}] Correct noto'g'ri: {r['correct']!r}")
            if not r["comment"].strip().startswith("To'g'ri javob:"):
                flags.append(f"[{qid}] Comment formati noto'g'ri")
            # correct text must match the option it points to
            corr_text = r[r["correct"]]
            # comment must start with "To'g'ri javob: <corr_text>"
            if not r["comment"].startswith("To'g'ri javob: " + corr_text):
                flags.append(f"[{qid}] Comment matni to'g'ri javob bilan mos emas")
            # comment should contain the correct answer text (loose check)
            # 5: length ratio
            correct_len = len(corr_text)
            wrong_lens = [len(r[L]) for L in "ABCDE" if L != r["correct"]]
            max_wrong = max(wrong_lens) if wrong_lens else 0
            if max_wrong > 0:
                ratio = correct_len / max_wrong
                if ratio > 1.30:
                    flags.append(f"[{qid}] to'g'ri javob >30% uzun (nisbat {ratio:.2f}) "
                                 f"corr={correct_len} maxwrong={max_wrong}")
                    long_flagged += 1
                elif ratio > 1.10:
                    flags.append(f"[{qid}] to'g'ri javob >10% uzun (nisbat {ratio:.2f})")
                    long_flagged += 1
            # 6: wrong-answer templating (skip numeric)
            if not r.get("numeric"):
                wrongs = [r[L] for L in "ABCDE" if L != r["correct"]]
                sw = sum(1 for w in wrongs if first_word(w) in START_WORDS)
                if sw > 1:
                    flags.append(f"[{qid}] {sw} ta noto'g'ri javob Faqat/Hech/Umuman/Barcha bilan boshlanadi")
                # same first word 3+
                fw = Counter(first_word(w) for w in wrongs)
                corr_fw = first_word(corr_text)
                for w, cnt in fw.items():
                    if cnt >= 3 and w != corr_fw:
                        flags.append(f"[{qid}] {cnt} ta noto'g'ri javob '{w}' bilan boshlanadi")

    return flags, overall, long_flagged, total_q, per_file_letters

def main():
    with open(sys.argv[1], encoding="utf-8") as f:
        data = json.load(f)
    flags, overall, long_flagged, total_q, per_file = check(data)
    print("=== QA HISOBOT ===")
    print(f"Fayllar: {len(data)}  |  Jami savollar: {total_q}")
    print(f"Harf taqsimoti (umumiy): {dict(sorted(overall.items()))}")
    tot = sum(overall.values())
    if tot:
        pct = {k: f"{v/tot*100:.1f}%" for k, v in sorted(overall.items())}
        print(f"Foizda: {pct}")
    print(f">10% uzun to'g'ri javoblar: {long_flagged} / {total_q} "
          f"({long_flagged/total_q*100:.1f}%)" if total_q else "")
    print(f"\nBayroqlar ({len(flags)}):")
    if not flags:
        print("  — Hammasi toza, bayroq yo'q.")
    for fl in flags:
        print("  !", fl)

if __name__ == "__main__":
    main()
