# Tech-Lupe Folge 2: Das Jahr-2038-Problem (17.11.2026)

Ablauf: Uhr 19.01.2038 04:14:05 → 07 → Glitch → 13.12.1901 21:45:52 · Unix-Zeit zählt Sekunden seit 1970 · heute
1.794.934.800 · 32-Bit-Register (heute, dann Maximum 2.147.483.647, Vorzeichen-Bit markiert) · +1 → Übertrag läuft durch,
Vorzeichen kippt → −2.147.483.648 · Zeitstrahl springt von 2038 auf 1901 · 64 Bit = 292 Mrd. Jahre · neue Systeme schon
64 Bit, alte Geräte teils noch 32 Bit · Folgen.
Fakten geprüft mit Python (siehe Kopf von `make_script.py`). Video 37,1 s, −14,2 LUFS, F0 110–132 Hz.
