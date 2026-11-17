# Testvideo: Tech-Lupe „Warum 0,1 + 0,2 nicht 0,3 ist“ (17.11.2026)

Idee des Kanalinhabers (selbst Informatiker): bestehenden Kanal Tech-Lupe zu einem Informatik-Kanal machen,
Themen kurz und animiert erklärt. Reine Bewegtgrafik (Engine-Ebene `alt`, keine Figuren), Erzählerstimme Qwen3-TTS.

- Ablauf: Terminal `0.1 + 0.2` → `0.30000000000000004` → 15 Nullen und eine 4 → Binärsystem → 1/3 = 0,333… →
  0,1 binär endlos → 64 Bit (echte Bits von 0.1 als double, 0x3FB999999999999A) → abschneiden → echte gespeicherte Werte
  (0,1000000000000000055…, 0,2000000000000000111…) → Banken rechnen oft mit ganzen Cent → Folgen + Themenfrage.
- Stimme: `voice/erzaehler.wav` (Entwurf „Male, about 30, clear and friendly German tech YouTuber …“, Kandidat 2, 142 Hz).
  Besser wäre die echte Stimme des Kanalinhabers.
- Achtung Whisper: liest „null Komma eins“ als „0,1“ → WER wirkt hoch, Ton ist trotzdem richtig (Fassungen anhören).
