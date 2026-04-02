[![en](https://img.shields.io/badge/language-english-red.svg)](https://github.com/Vaseksch/linefollower-telemetry-tool/blob/master/docs/readme.md)
[![cz](https://img.shields.io/badge/jazyk-česky-blue.svg)](https://github.com/Vaseksch/linefollower-telemetry-tool/blob/master/docs/README.CZ.md)


# LapLog

Podpůrný nástroj pro můj projekt [Linefollower](https://github.com/Vaseksch/linefollower_esp32s3_Rev_C). Umožňuje načítat telemetrická data z robota přes sériové připojení nebo ze souborů, zobrazovat je ve formě grafů a exportovat pro další analýzu. Součástí je také výpočet PID parametrů metodou Ziegler-Nichols přímo z naměřených dat.

## Funkce
- Načítání dat z robota přes sériové připojení
- Načítání a ukládání dat ze souborů CSV
- Vykreslování libovolné kombinace sloupců do grafů
- Čtení, zápis a otevírání souborů `.xlsx` přímo v aplikaci, nebo jejich okamžité otevření v Excelu
- Výpočet hodnot PID zesílení (Kp, Kd) z naměřených dat pomocí metody Ziegler-Nichols

![img](image.png)