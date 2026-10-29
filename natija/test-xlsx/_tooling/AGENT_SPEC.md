# Sub-agent topshirig'i: test savollari (content JSON) tuzish

Sen tibbiyot oliygohi test tuzuvchi mutaxassissan. Senga bir nechta mavzu
beriladi (masalan 011..020). Har bir mavzu matni `/projects/sandbox/work/docx/NNN.docx`
da. Matnni o'qib olish uchun ushbu buyruqni ishlat:

    cd /projects/sandbox/work && python3 extract_docx.py docx/NNN.docx

Har mavzu matnining oxirida "Foydalanilgan adabiyotlar" bo'limi bor — Comment
ustunidagi manbalar uchun AYNAN shulardan foydalan (WHO, CDC, ASM/CMPH,
Bailey & Scott, Murray, Koneman, SanQvaN va h.k.).

## Natija: bitta JSON fayl yoz
Fayl yo'li: `/projects/sandbox/work/content_NNN-MMM.json` (senga aytilgan nom).
Tuzilishi — mavzu raqami -> 10 ta savol ro'yxati:

```json
{
  "011": [
    {
      "q": "Savol matni?",
      "correct": "To'g'ri javob matni",
      "wrongs": ["noto'g'ri 1", "noto'g'ri 2", "noto'g'ri 3", "noto'g'ri 4"],
      "comment": "To'g'ri javob: <correct matni AYNAN>. <qisqa ilmiy izoh>. Manba: <manba1>; <manba2>.",
      "numeric": true
    },
    ... (jami 10 ta)
  ],
  "012": [ ... 10 ta ... ],
  ...
}
```

- `correct` — faqat to'g'ri javob matni (harf EMAS; joylashtirish keyin qilinadi).
- `wrongs` — AYNAN 4 ta noto'g'ri javob.
- `numeric` — agar savol raqamli/formulali bo'lsa yoki barcha variantlar bir xil
  tuzilishda bo'lsa (masalan harorat, kattalashtirish, foiz) `true` qo'y; aks holda
  umuman yozma.
- Comment HAR DOIM `"To'g'ri javob: "` + `correct` matni bilan AYNAN boshlanishi shart.

## QAT'IY QOIDALAR (avtomatik tekshiriladi — buzilsa qaytariladi)

1. Har mavzuda AYNAN 10 ta savol.
2. Savollar FAQAT shu mavzu matniga va ishonchli manbalarga asoslansin. To'qima
   fakt YO'Q. Mavzuda "tasdiqlanmagan" deb belgilangan narsani savolga olma.
3. Savollar turli qismlarni qamrasin: ta'rif, qo'zg'atuvchi, yuqish, klinika,
   laboratoriya usullari, me'yor/raqamlar, hisob-kitob, profilaktika.
4. UZUNLIK: `correct` matni eng uzun `wrongs` dan 10% dan ortiq uzun BO'LMASIN.
   Amaliy qoida: to'g'ri javobni qisqa tut, 4 ta noto'g'ri javobni unga YAQIN
   uzunlikda yoz (belgi soni taxminan teng). Tafsilotni Comment ga ko'chir, javobga emas.
5. Noto'g'ri javoblar ishonarli, lekin ANIQ noto'g'ri bo'lsin (boshqa mikrob,
   boshqa usul, boshqa raqam, yaqin tushuncha). Ikki ma'noli bo'lmasin.
6. "Faqat/Hech/Umuman/Barcha" bilan boshlanadigan noto'g'ri javob bitta savolda
   KO'PI BILAN 1 ta. (numeric savollarda bu qoida yumshoq.)
7. Bir savolda 3+ noto'g'ri javob BIR XIL so'z bilan boshlanmasin (agar to'g'ri
   javob ham shu so'z bilan boshlanmasa). numeric savollar bundan mustasno.
8. Barcha 5 variant savolga grammatik mos bo'lsin (to'g'ri javob grammatikasi
   bilan ajralib qolmasin).

## Comment manbalari — namunalar
- "WHO. Laboratory biosafety manual, 4th ed. (2020)"
- "CDC/NIH. BMBL, 6th ed. (2020)"
- "Leber AL (ed). CMPH, 4th ed. (ASM, 2016)"
- "Tille PM. Bailey & Scott's Diagnostic Microbiology, 15th ed. (2022)"
- "Murray PR va boshq. Medical Microbiology, 9th ed. (2021)"
- "Procop GW va boshq. Koneman's Atlas, 7th ed. (2017)"
- "SanQvaN № ..." (mavzu matnidagi aniq raqam bilan)
- Faqat mavzuga xos fakt uchun: "Mavzu materiali (NNN.docx)"

## Muhim
- JSON to'g'ri (valid) bo'lsin: qo'shtirnoqlar, vergullar joyida. O'zbekcha apostrof
  uchun oddiy `'` ishlat (masalan: bo'yash, qo'zg'atuvchi).
- Faqat JSON faylni yoz; boshqa fayllarga tegma.
- Ishni tugatgach, qaysi mavzularni va nechta savol yozganingni qisqa xabar qil.
