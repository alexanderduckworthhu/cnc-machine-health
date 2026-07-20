"""
Multilingual UI copy (EN / FR / DE / IT / PT / ES / ZH / RU).

Same pattern as where-needs-overlap and icu-mortality-vital-shap.
Every user-visible string belongs here, charts, cards, alerts, and chrome.
"""

from __future__ import annotations

from typing import Any

SUPPORTED_LANGS = ("en", "fr", "de", "it", "pt", "es", "zh", "ru")

LANGUAGE_LABELS: dict[str, str] = {
    "en": "English",
    "fr": "Français",
    "de": "Deutsch",
    "it": "Italiano",
    "pt": "Português",
    "es": "Español",
    "zh": "中文",
    "ru": "Русский",
}

DEFAULT_LANG = "en"

# Base English strings, other locales override keys they translate.
_EN: dict[str, str] = {
    "lang": "Language",
    "lang_hint": "Switch language anytime. The whole board follows.",
    "brand_eyebrow": "CELL HEALTH",
    "app_title": "CNC Spindle Monitor",
    "tagline": "Which cells need a look before the next precision run?",
    "floor_hint": "Tap a cell, traces and notes update for that cell only.",
    "floor_all_fine": "All four cells look fine right now.",
    "floor_need_look_1": "1 needs a look",
    "floor_need_look_n": "{n} need a look",
    "floor_watch_1": "1 to watch",
    "floor_watch_n": "{n} to watch",
    "floor_tap": "Tap a cell to inspect.",
    "panel_main": "What’s happening on this cell",
    "panel_side": "What to do next",
    "panel_notes": "Notes for this cell",
    "sensor_details": "Latest sensor readings",
    "card_cta": "View cell →",
    "card_cta_selected": "Viewing",
    "card_tooltip": "Open this cell’s health and sensor traces",
    "viewing_pill": "Viewing {machine_id}",
    "roughly_left_prefix": "Roughly ",
    "roughly_left_suffix": " left",
    "health_denom": "/100",
    "chart_health_title": "Health over recent cycles",
    "chart_sensor_title": "Sensor channels (CNC proxy)",
    "chart_empty_health": "No health history for this cell yet.",
    "chart_empty_sensors": "Sensors haven’t checked in for this cell.",
    "chart_axis_cycle": "Cycle",
    "chart_axis_health": "Health",
    "subplot_vibration": "Vibration",
    "subplot_temperature": "Temperature",
    "subplot_current_load": "Current / load",
    "status_green": "Looking good",
    "status_amber": "Keep an eye on it",
    "status_red": "Needs a look",
    "hint_green": "Nothing unusual in the recent window.",
    "hint_amber": "Wear is climbing, worth a glance before the next precision run.",
    "hint_red": "This cell is drifting hard. Check vibration and current before you cut.",
    "aria_green": "status looking good",
    "aria_amber": "status keep an eye on it",
    "aria_red": "status needs a look",
    "sev_high": "Soon",
    "sev_medium": "Soon-ish",
    "sev_low": "Note",
    "bootstrap_error_title": "Couldn’t load the floor board",
    "bootstrap_error_hint": (
        "Rebuild demo artefacts, then refresh: "
        "python scripts/build_demo_data.py && python scripts/train_isolation_forest.py"
    ),
    "empty_fleet": "No machines in the fleet snapshot. Rebuild the demo data to continue.",
    "empty_alerts_floor": "No maintenance notes right now. Enjoy the quiet.",
    "empty_alerts_machine": "Nothing queued for {machine_id}.",
    "disclaimer": (
        "Portfolio demo, not a certified condition monitor. "
        "Sensor streams are a NASA CMAPSS proxy wearing CNC labels, "
        "useful for triage practice, not for real work orders."
    ),
    "opcua_banner": "Reading mock OPC-UA · {n} tags · replay buffer (not a live PLC)",
    "detail_health": "Health {health:.0f}/100, {status}. Approx. time left: {ttf}.",
    "card_aria": "{machine_id}, {status}, health {health:.0f} of 100",
    "alert_red": (
        "{machine_id} is in rough shape (health {health:.0f}/100). "
        "Roughly {ttf} of cutting left on this proxy, "
        "check spindle vibration and current before the next tight-tolerance job."
    ),
    "alert_amber": (
        "{machine_id} is warming up in the wrong way (health {health:.0f}/100). "
        "About {ttf} left if the trend holds, peek at the vibration trace when you can."
    ),
    "alert_drop": (
        "{machine_id} lost {delta:.0f} health points "
        "({prev:.0f} → {health:.0f}) in one window. "
        "That’s a sharper step than usual, worth a quick look."
    ),
    "ttf_days": "~{n:.1f} days",
    "ttf_hours": "~{n:.1f} h",
    "ttf_minutes": "~{n:.0f} min",
    "sensor_vibration_rms": "Vibration RMS (mm/s)",
    "sensor_vibration_peak": "Vibration peak (mm/s)",
    "sensor_temperature_spindle_c": "Spindle temp (°C)",
    "sensor_temperature_coolant_c": "Coolant temp (°C)",
    "sensor_current_draw_a": "Spindle current (A)",
    "sensor_load_pct": "Axis load (%)",
    "machine_CNC-01": "Spindle cell A, bridge mill",
    "machine_CNC-02": "Spindle cell B, turning center",
    "machine_CNC-03": "Micro-milling, watch plate fixture",
    "machine_CNC-04": "Deburr / finish, shared cell",
    "cards_aria": "Machine health cards",
    "health_graph_aria": "Health score over cycles",
    "sensor_graph_aria": "Vibration, temperature, and current traces",
}

_FR: dict[str, str] = {
    "lang": "Langue",
    "lang_hint": "Changez de langue à tout moment. Tout le tableau suit.",
    "brand_eyebrow": "SANTÉ DES CELLULES",
    "app_title": "Moniteur de broche CNC",
    "tagline": "Quelles cellules vérifier avant le prochain usinage de précision ?",
    "floor_hint": "Touchez une cellule, traces et notes se mettent à jour.",
    "floor_all_fine": "Les quatre cellules vont bien pour l’instant.",
    "floor_need_look_1": "1 à vérifier",
    "floor_need_look_n": "{n} à vérifier",
    "floor_watch_1": "1 à surveiller",
    "floor_watch_n": "{n} à surveiller",
    "floor_tap": "Touchez une cellule pour inspecter.",
    "panel_main": "Ce qui se passe sur cette cellule",
    "panel_side": "Prochaine action",
    "panel_notes": "Notes pour cette cellule",
    "sensor_details": "Dernières lectures capteurs",
    "card_cta": "Voir la cellule →",
    "card_cta_selected": "En cours",
    "card_tooltip": "Ouvrir la santé et les traces de cette cellule",
    "viewing_pill": "Cellule {machine_id}",
    "roughly_left_prefix": "Environ ",
    "roughly_left_suffix": " restant",
    "chart_health_title": "Santé sur les cycles récents",
    "chart_sensor_title": "Canaux capteurs (proxy CNC)",
    "chart_empty_health": "Pas encore d’historique de santé pour cette cellule.",
    "chart_empty_sensors": "Les capteurs n’ont pas encore répondu pour cette cellule.",
    "chart_axis_cycle": "Cycle",
    "chart_axis_health": "Santé",
    "subplot_vibration": "Vibration",
    "subplot_temperature": "Température",
    "subplot_current_load": "Courant / charge",
    "status_green": "Tout va bien",
    "status_amber": "À surveiller",
    "status_red": "À vérifier",
    "hint_green": "Rien d’inhabituel sur la fenêtre récente.",
    "hint_amber": "L’usure monte, un coup d’œil avant le prochain usinage précis.",
    "hint_red": "Cette cellule dérive fort. Vérifiez vibration et courant avant de couper.",
    "aria_green": "état tout va bien",
    "aria_amber": "état à surveiller",
    "aria_red": "état à vérifier",
    "sev_high": "Urgent",
    "sev_medium": "Bientôt",
    "sev_low": "Note",
    "bootstrap_error_title": "Impossible de charger le tableau",
    "bootstrap_error_hint": (
        "Régénérez les artefacts, puis rechargez : "
        "python scripts/build_demo_data.py && python scripts/train_isolation_forest.py"
    ),
    "empty_fleet": "Aucune machine dans l’instantané. Régénérez les données de démo.",
    "empty_alerts_floor": "Aucune note de maintenance pour l’instant.",
    "empty_alerts_machine": "Rien en file pour {machine_id}.",
    "disclaimer": (
        "Démo portfolio, pas un système de surveillance certifié. "
        "Les flux capteurs sont un proxy NASA CMAPSS en vocabulaire CNC, "
        "utile pour le triage, pas pour de vrais bons de travail."
    ),
    "opcua_banner": "OPC-UA simulé · {n} tags · tampon de relecture (pas de PLC réel)",
    "detail_health": "Santé {health:.0f}/100, {status}. Temps restant approx. : {ttf}.",
    "card_aria": "{machine_id}, {status}, santé {health:.0f} sur 100",
    "alert_red": (
        "{machine_id} est en mauvais état (santé {health:.0f}/100). "
        "Environ {ttf} d’usinage restant sur ce proxy, "
        "vérifiez vibration et courant avant le prochain usinage serré."
    ),
    "alert_amber": (
        "{machine_id} chauffe dans le mauvais sens (santé {health:.0f}/100). "
        "Environ {ttf} restant si la tendance tient, regardez la trace de vibration."
    ),
    "alert_drop": (
        "{machine_id} a perdu {delta:.0f} points de santé "
        "({prev:.0f} → {health:.0f}) en une fenêtre. "
        "Plus net que d’habitude, un coup d’œil s’impose."
    ),
    "ttf_days": "~{n:.1f} j",
    "ttf_hours": "~{n:.1f} h",
    "ttf_minutes": "~{n:.0f} min",
    "sensor_vibration_rms": "Vibration RMS (mm/s)",
    "sensor_vibration_peak": "Pic de vibration (mm/s)",
    "sensor_temperature_spindle_c": "Temp. broche (°C)",
    "sensor_temperature_coolant_c": "Temp. liquide (°C)",
    "sensor_current_draw_a": "Courant broche (A)",
    "sensor_load_pct": "Charge axes (%)",
    "machine_CNC-01": "Cellule broche A, fraiseuse pont",
    "machine_CNC-02": "Cellule broche B, tour",
    "machine_CNC-03": "Micro-fraisage, plaque montre",
    "machine_CNC-04": "Ébavurage / finition, cellule partagée",
    "cards_aria": "Cartes de santé machines",
    "health_graph_aria": "Score de santé sur les cycles",
    "sensor_graph_aria": "Traces vibration, température et courant",
}

_DE: dict[str, str] = {
    "lang": "Sprache",
    "lang_hint": "Sprache jederzeit wechseln. Das ganze Board folgt.",
    "brand_eyebrow": "ZELLGESUNDHEIT",
    "app_title": "CNC-Spindelmonitor",
    "tagline": "Welche Zellen vor dem nächsten Präzisionslauf prüfen?",
    "floor_hint": "Zelle antippen. Spuren und Notizen aktualisieren sich.",
    "floor_all_fine": "Alle vier Zellen sehen gerade gut aus.",
    "floor_need_look_1": "1 braucht Kontrolle",
    "floor_need_look_n": "{n} brauchen Kontrolle",
    "floor_watch_1": "1 beobachten",
    "floor_watch_n": "{n} beobachten",
    "floor_tap": "Zelle antippen zum Prüfen.",
    "panel_main": "Was auf dieser Zelle passiert",
    "panel_side": "Nächster Schritt",
    "panel_notes": "Notizen zu dieser Zelle",
    "sensor_details": "Aktuelle Sensorwerte",
    "card_cta": "Zelle ansehen →",
    "card_cta_selected": "Aktiv",
    "card_tooltip": "Gesundheit und Spuren dieser Zelle öffnen",
    "viewing_pill": "Zelle {machine_id}",
    "roughly_left_prefix": "Etwa ",
    "roughly_left_suffix": " übrig",
    "chart_health_title": "Gesundheit über aktuelle Zyklen",
    "chart_sensor_title": "Sensorkanäle (CNC-Proxy)",
    "chart_empty_health": "Noch keine Gesundheitsdaten für diese Zelle.",
    "chart_empty_sensors": "Sensoren haben für diese Zelle noch nicht gemeldet.",
    "chart_axis_cycle": "Zyklus",
    "chart_axis_health": "Gesundheit",
    "subplot_vibration": "Vibration",
    "subplot_temperature": "Temperatur",
    "subplot_current_load": "Strom / Last",
    "status_green": "Sieht gut aus",
    "status_amber": "Im Auge behalten",
    "status_red": "Kontrolle nötig",
    "hint_green": "Nichts Ungewöhnliches im letzten Fenster.",
    "hint_amber": "Verschleiß steigt, vor dem nächsten Präzisionslauf kurz prüfen.",
    "hint_red": "Diese Zelle driftet stark. Vibration und Strom vor dem Schnitt prüfen.",
    "aria_green": "Status sieht gut aus",
    "aria_amber": "Status im Auge behalten",
    "aria_red": "Status Kontrolle nötig",
    "sev_high": "Bald",
    "sev_medium": "Demnächst",
    "sev_low": "Hinweis",
    "bootstrap_error_title": "Board konnte nicht geladen werden",
    "bootstrap_error_hint": (
        "Demo-Artefakte neu bauen, dann neu laden: "
        "python scripts/build_demo_data.py && python scripts/train_isolation_forest.py"
    ),
    "empty_fleet": "Keine Maschinen im Snapshot. Demo-Daten neu erzeugen.",
    "empty_alerts_floor": "Keine Wartungshinweise gerade.",
    "empty_alerts_machine": "Nichts in der Warteschlange für {machine_id}.",
    "disclaimer": (
        "Portfolio-Demo, kein zertifiziertes Condition-Monitoring. "
        "Sensorsignale sind ein NASA-CMAPSS-Proxy mit CNC-Begriffen, "
        "für Triage, nicht für echte Arbeitsaufträge."
    ),
    "opcua_banner": "OPC-UA-Mock · {n} Tags · Replay-Puffer (kein echtes PLC)",
    "detail_health": "Gesundheit {health:.0f}/100, {status}. Restzeit ca.: {ttf}.",
    "card_aria": "{machine_id}, {status}, Gesundheit {health:.0f} von 100",
    "alert_red": (
        "{machine_id} ist in schlechtem Zustand (Gesundheit {health:.0f}/100). "
        "Etwa {ttf} Schnittzeit auf diesem Proxy, "
        "Vibration und Strom vor dem nächsten Engtoleranz-Job prüfen."
    ),
    "alert_amber": (
        "{machine_id} läuft in die falsche Richtung warm (Gesundheit {health:.0f}/100). "
        "Etwa {ttf} übrig, wenn der Trend hält. Vibrationsspur prüfen."
    ),
    "alert_drop": (
        "{machine_id} verlor {delta:.0f} Gesundheitspunkte "
        "({prev:.0f} → {health:.0f}) in einem Fenster. "
        "Schärfer als üblich, kurz nachschauen."
    ),
    "ttf_days": "~{n:.1f} T",
    "ttf_hours": "~{n:.1f} h",
    "ttf_minutes": "~{n:.0f} min",
    "sensor_vibration_rms": "Vibration RMS (mm/s)",
    "sensor_vibration_peak": "Vibrationsspitze (mm/s)",
    "sensor_temperature_spindle_c": "Spindeltemp. (°C)",
    "sensor_temperature_coolant_c": "Kühlmitteltemp. (°C)",
    "sensor_current_draw_a": "Spindelstrom (A)",
    "sensor_load_pct": "Achslast (%)",
    "machine_CNC-01": "Spindelzelle A. Portalfräse",
    "machine_CNC-02": "Spindelzelle B. Drehzentrum",
    "machine_CNC-03": "Mikrofräsen. Uhrwerkplatte",
    "machine_CNC-04": "Entgraten / Finish, gemeinsame Zelle",
    "cards_aria": "Maschinen-Gesundheitskarten",
    "health_graph_aria": "Gesundheitsscore über Zyklen",
    "sensor_graph_aria": "Vibrations-, Temperatur- und Stromspuren",
}

_IT: dict[str, str] = {
    "lang": "Lingua",
    "lang_hint": "Cambia lingua quando vuoi. Tutto il pannello segue.",
    "brand_eyebrow": "SALUTE CELLE",
    "app_title": "Monitor mandrino CNC",
    "tagline": "Quali celle controllare prima della prossima lavorazione di precisione?",
    "floor_hint": "Tocca una cella, tracce e note si aggiornano.",
    "floor_all_fine": "Le quattro celle sembrano a posto adesso.",
    "floor_need_look_1": "1 da controllare",
    "floor_need_look_n": "{n} da controllare",
    "floor_watch_1": "1 da osservare",
    "floor_watch_n": "{n} da osservare",
    "floor_tap": "Tocca una cella per ispezionare.",
    "panel_main": "Cosa succede su questa cella",
    "panel_side": "Prossimo passo",
    "panel_notes": "Note per questa cella",
    "sensor_details": "Ultime letture sensori",
    "card_cta": "Vedi cella →",
    "card_cta_selected": "In vista",
    "card_tooltip": "Apri salute e tracce di questa cella",
    "viewing_pill": "Cella {machine_id}",
    "roughly_left_prefix": "Circa ",
    "roughly_left_suffix": " rimasti",
    "chart_health_title": "Salute sugli ultimi cicli",
    "chart_sensor_title": "Canali sensori (proxy CNC)",
    "chart_empty_health": "Nessuna cronologia di salute per questa cella.",
    "chart_empty_sensors": "I sensori non hanno ancora risposto per questa cella.",
    "chart_axis_cycle": "Ciclo",
    "chart_axis_health": "Salute",
    "subplot_vibration": "Vibrazione",
    "subplot_temperature": "Temperatura",
    "subplot_current_load": "Corrente / carico",
    "status_green": "Tutto ok",
    "status_amber": "Da tenere d’occhio",
    "status_red": "Da controllare",
    "hint_green": "Niente di insolito nella finestra recente.",
    "hint_amber": "L’usura sale, uno sguardo prima della prossima corsa di precisione.",
    "hint_red": "Questa cella deriva forte. Controlla vibrazione e corrente prima di tagliare.",
    "aria_green": "stato tutto ok",
    "aria_amber": "stato da tenere d’occhio",
    "aria_red": "stato da controllare",
    "sev_high": "Presto",
    "sev_medium": "A breve",
    "sev_low": "Nota",
    "bootstrap_error_title": "Impossibile caricare il pannello",
    "bootstrap_error_hint": (
        "Rigenera gli artefatti, poi aggiorna: "
        "python scripts/build_demo_data.py && python scripts/train_isolation_forest.py"
    ),
    "empty_fleet": "Nessuna macchina nello snapshot. Rigenera i dati demo.",
    "empty_alerts_floor": "Nessuna nota di manutenzione al momento.",
    "empty_alerts_machine": "Niente in coda per {machine_id}.",
    "disclaimer": (
        "Demo portfolio, non un sistema di condition monitoring certificato. "
        "I flussi sensore sono un proxy NASA CMAPSS con etichette CNC, "
        "utile per il triage, non per ordini di lavoro reali."
    ),
    "opcua_banner": "OPC-UA mock · {n} tag · buffer di replay (nessun PLC reale)",
    "detail_health": "Salute {health:.0f}/100, {status}. Tempo rimasto approx.: {ttf}.",
    "card_aria": "{machine_id}, {status}, salute {health:.0f} su 100",
    "alert_red": (
        "{machine_id} è in cattive condizioni (salute {health:.0f}/100). "
        "Circa {ttf} di taglio rimasti su questo proxy, "
        "controlla vibrazione e corrente prima del prossimo lavoro stretto."
    ),
    "alert_amber": (
        "{machine_id} si sta scaldando nel verso sbagliato (salute {health:.0f}/100). "
        "Circa {ttf} rimasti se il trend tiene, guarda la traccia di vibrazione."
    ),
    "alert_drop": (
        "{machine_id} ha perso {delta:.0f} punti di salute "
        "({prev:.0f} → {health:.0f}) in una finestra. "
        "Più netto del solito, vale uno sguardo."
    ),
    "ttf_days": "~{n:.1f} g",
    "ttf_hours": "~{n:.1f} h",
    "ttf_minutes": "~{n:.0f} min",
    "sensor_vibration_rms": "Vibrazione RMS (mm/s)",
    "sensor_vibration_peak": "Picco vibrazione (mm/s)",
    "sensor_temperature_spindle_c": "Temp. mandrino (°C)",
    "sensor_temperature_coolant_c": "Temp. refrigerante (°C)",
    "sensor_current_draw_a": "Corrente mandrino (A)",
    "sensor_load_pct": "Carico assi (%)",
    "machine_CNC-01": "Cella mandrino A, fresatrice a ponte",
    "machine_CNC-02": "Cella mandrino B, tornio",
    "machine_CNC-03": "Microfresatura, piastra orologio",
    "machine_CNC-04": "Sbavatura / finitura, cella condivisa",
    "cards_aria": "Schede salute macchine",
    "health_graph_aria": "Punteggio salute sui cicli",
    "sensor_graph_aria": "Tracce vibrazione, temperatura e corrente",
}

_PT: dict[str, str] = {
    "lang": "Idioma",
    "lang_hint": "Mude o idioma a qualquer momento. Todo o painel acompanha.",
    "brand_eyebrow": "SAÚDE DAS CÉLULAS",
    "app_title": "Monitor de fuso CNC",
    "tagline": "Quais células verificar antes da próxima corrida de precisão?",
    "floor_hint": "Toque numa célula, traços e notas atualizam.",
    "floor_all_fine": "As quatro células estão bem agora.",
    "floor_need_look_1": "1 precisa de atenção",
    "floor_need_look_n": "{n} precisam de atenção",
    "floor_watch_1": "1 para vigiar",
    "floor_watch_n": "{n} para vigiar",
    "floor_tap": "Toque numa célula para inspecionar.",
    "panel_main": "O que acontece nesta célula",
    "panel_side": "Próximo passo",
    "panel_notes": "Notas para esta célula",
    "sensor_details": "Últimas leituras dos sensores",
    "card_cta": "Ver célula →",
    "card_cta_selected": "A ver",
    "card_tooltip": "Abrir saúde e traços desta célula",
    "viewing_pill": "Célula {machine_id}",
    "roughly_left_prefix": "Cerca de ",
    "roughly_left_suffix": " restantes",
    "chart_health_title": "Saúde nos ciclos recentes",
    "chart_sensor_title": "Canais de sensores (proxy CNC)",
    "chart_empty_health": "Ainda sem histórico de saúde para esta célula.",
    "chart_empty_sensors": "Os sensores ainda não responderam nesta célula.",
    "chart_axis_cycle": "Ciclo",
    "chart_axis_health": "Saúde",
    "subplot_vibration": "Vibração",
    "subplot_temperature": "Temperatura",
    "subplot_current_load": "Corrente / carga",
    "status_green": "Tudo bem",
    "status_amber": "Manter de olho",
    "status_red": "Precisa de atenção",
    "hint_green": "Nada invulgar na janela recente.",
    "hint_amber": "O desgaste sobe, vale um olhar antes da próxima corrida de precisão.",
    "hint_red": "Esta célula está a derivar. Verifique vibração e corrente antes de cortar.",
    "aria_green": "estado tudo bem",
    "aria_amber": "estado manter de olho",
    "aria_red": "estado precisa de atenção",
    "sev_high": "Em breve",
    "sev_medium": "Em breve",
    "sev_low": "Nota",
    "bootstrap_error_title": "Não foi possível carregar o painel",
    "bootstrap_error_hint": (
        "Regenere os artefactos e atualize: "
        "python scripts/build_demo_data.py && python scripts/train_isolation_forest.py"
    ),
    "empty_fleet": "Sem máquinas no snapshot. Regenere os dados de demo.",
    "empty_alerts_floor": "Sem notas de manutenção agora.",
    "empty_alerts_machine": "Nada na fila para {machine_id}.",
    "disclaimer": (
        "Demo de portfólio, não um sistema de monitorização certificado. "
        "Os sensores são um proxy NASA CMAPSS com rótulos CNC, "
        "útil para triagem, não para ordens de trabalho reais."
    ),
    "opcua_banner": "OPC-UA mock · {n} tags · buffer de replay (sem PLC real)",
    "detail_health": "Saúde {health:.0f}/100, {status}. Tempo restante approx.: {ttf}.",
    "card_aria": "{machine_id}, {status}, saúde {health:.0f} de 100",
    "alert_red": (
        "{machine_id} está em mau estado (saúde {health:.0f}/100). "
        "Cerca de {ttf} de corte restantes neste proxy, "
        "verifique vibração e corrente antes do próximo trabalho apertado."
    ),
    "alert_amber": (
        "{machine_id} aquece no sentido errado (saúde {health:.0f}/100). "
        "Cerca de {ttf} restantes se a tendência se mantiver, veja o traço de vibração."
    ),
    "alert_drop": (
        "{machine_id} perdeu {delta:.0f} pontos de saúde "
        "({prev:.0f} → {health:.0f}) numa janela. "
        "Mais acentuado do que o habitual, vale um olhar."
    ),
    "ttf_days": "~{n:.1f} d",
    "ttf_hours": "~{n:.1f} h",
    "ttf_minutes": "~{n:.0f} min",
    "sensor_vibration_rms": "Vibração RMS (mm/s)",
    "sensor_vibration_peak": "Pico de vibração (mm/s)",
    "sensor_temperature_spindle_c": "Temp. do fuso (°C)",
    "sensor_temperature_coolant_c": "Temp. do refrigerante (°C)",
    "sensor_current_draw_a": "Corrente do fuso (A)",
    "sensor_load_pct": "Carga dos eixos (%)",
    "machine_CNC-01": "Célula de fuso A, fresadora ponte",
    "machine_CNC-02": "Célula de fuso B, torno",
    "machine_CNC-03": "Microfresagem, placa de relógio",
    "machine_CNC-04": "Rebarbação / acabamento, célula partilhada",
    "cards_aria": "Cartões de saúde das máquinas",
    "health_graph_aria": "Pontuação de saúde ao longo dos ciclos",
    "sensor_graph_aria": "Traços de vibração, temperatura e corrente",
}

_ES: dict[str, str] = {
    "lang": "Idioma",
    "lang_hint": "Cambia el idioma cuando quieras. Todo el panel sigue.",
    "brand_eyebrow": "SALUD DE CELDAS",
    "app_title": "Monitor de husillo CNC",
    "tagline": "¿Qué celdas revisar antes de la próxima carrera de precisión?",
    "floor_hint": "Toca una celda, las trazas y notas se actualizan.",
    "floor_all_fine": "Las cuatro celdas se ven bien ahora.",
    "floor_need_look_1": "1 necesita revisión",
    "floor_need_look_n": "{n} necesitan revisión",
    "floor_watch_1": "1 a vigilar",
    "floor_watch_n": "{n} a vigilar",
    "floor_tap": "Toca una celda para inspeccionar.",
    "panel_main": "Qué ocurre en esta celda",
    "panel_side": "Siguiente paso",
    "panel_notes": "Notas de esta celda",
    "sensor_details": "Últimas lecturas de sensores",
    "card_cta": "Ver celda →",
    "card_cta_selected": "Viendo",
    "card_tooltip": "Abrir salud y trazas de esta celda",
    "viewing_pill": "Celda {machine_id}",
    "roughly_left_prefix": "Aprox. ",
    "roughly_left_suffix": " restantes",
    "chart_health_title": "Salud en ciclos recientes",
    "chart_sensor_title": "Canales de sensores (proxy CNC)",
    "chart_empty_health": "Aún no hay historial de salud para esta celda.",
    "chart_empty_sensors": "Los sensores aún no han respondido en esta celda.",
    "chart_axis_cycle": "Ciclo",
    "chart_axis_health": "Salud",
    "subplot_vibration": "Vibración",
    "subplot_temperature": "Temperatura",
    "subplot_current_load": "Corriente / carga",
    "status_green": "Todo bien",
    "status_amber": "Vigilar",
    "status_red": "Revisar",
    "hint_green": "Nada raro en la ventana reciente.",
    "hint_amber": "El desgaste sube, echa un vistazo antes de la próxima carrera precisa.",
    "hint_red": "Esta celda deriva fuerte. Revisa vibración y corriente antes de cortar.",
    "aria_green": "estado todo bien",
    "aria_amber": "estado vigilar",
    "aria_red": "estado revisar",
    "sev_high": "Pronto",
    "sev_medium": "En breve",
    "sev_low": "Nota",
    "bootstrap_error_title": "No se pudo cargar el panel",
    "bootstrap_error_hint": (
        "Regenera los artefactos y recarga: "
        "python scripts/build_demo_data.py && python scripts/train_isolation_forest.py"
    ),
    "empty_fleet": "No hay máquinas en el snapshot. Regenera los datos demo.",
    "empty_alerts_floor": "Sin notas de mantenimiento ahora.",
    "empty_alerts_machine": "Nada en cola para {machine_id}.",
    "disclaimer": (
        "Demo de portafolio, no un sistema de condition monitoring certificado. "
        "Los sensores son un proxy NASA CMAPSS con etiquetas CNC, "
        "útil para el triage, no para órdenes de trabajo reales."
    ),
    "opcua_banner": "OPC-UA mock · {n} tags · búfer de replay (sin PLC real)",
    "detail_health": "Salud {health:.0f}/100, {status}. Tiempo restante approx.: {ttf}.",
    "card_aria": "{machine_id}, {status}, salud {health:.0f} de 100",
    "alert_red": (
        "{machine_id} está en mal estado (salud {health:.0f}/100). "
        "Aprox. {ttf} de corte restantes en este proxy, "
        "revisa vibración y corriente antes del próximo trabajo de tolerancia estrecha."
    ),
    "alert_amber": (
        "{machine_id} se calienta en la dirección equivocada (salud {health:.0f}/100). "
        "Aprox. {ttf} restantes si la tendencia se mantiene, mira la traza de vibración."
    ),
    "alert_drop": (
        "{machine_id} perdió {delta:.0f} puntos de salud "
        "({prev:.0f} → {health:.0f}) en una ventana. "
        "Más brusco de lo habitual, merece un vistazo."
    ),
    "ttf_days": "~{n:.1f} d",
    "ttf_hours": "~{n:.1f} h",
    "ttf_minutes": "~{n:.0f} min",
    "sensor_vibration_rms": "Vibración RMS (mm/s)",
    "sensor_vibration_peak": "Pico de vibración (mm/s)",
    "sensor_temperature_spindle_c": "Temp. del husillo (°C)",
    "sensor_temperature_coolant_c": "Temp. del refrigerante (°C)",
    "sensor_current_draw_a": "Corriente del husillo (A)",
    "sensor_load_pct": "Carga de ejes (%)",
    "machine_CNC-01": "Celda de husillo A, fresadora puente",
    "machine_CNC-02": "Celda de husillo B, torno",
    "machine_CNC-03": "Microfresado, placa de reloj",
    "machine_CNC-04": "Desbarbado / acabado, celda compartida",
    "cards_aria": "Tarjetas de salud de máquinas",
    "health_graph_aria": "Puntuación de salud a lo largo de los ciclos",
    "sensor_graph_aria": "Trazas de vibración, temperatura y corriente",
}

_ZH: dict[str, str] = {
    "lang": "语言",
    "lang_hint": "随时切换语言，整块看板会一起更新。",
    "brand_eyebrow": "单元健康",
    "app_title": "CNC 主轴监测",
    "tagline": "下一次精密加工前，哪些单元需要先看一眼？",
    "floor_hint": "点选单元, 曲线与备注会随之更新。",
    "floor_all_fine": "四个单元目前都正常。",
    "floor_need_look_1": "1 台需要检查",
    "floor_need_look_n": "{n} 台需要检查",
    "floor_watch_1": "1 台需关注",
    "floor_watch_n": "{n} 台需关注",
    "floor_tap": "点选单元以查看详情。",
    "panel_main": "该单元当前状况",
    "panel_side": "下一步",
    "panel_notes": "该单元备注",
    "sensor_details": "最新传感器读数",
    "card_cta": "查看单元 →",
    "card_cta_selected": "查看中",
    "card_tooltip": "打开该单元的健康度与传感器曲线",
    "viewing_pill": "正在查看 {machine_id}",
    "roughly_left_prefix": "大约还剩 ",
    "roughly_left_suffix": "",
    "chart_health_title": "近期周期健康度",
    "chart_sensor_title": "传感器通道（CNC 代理）",
    "chart_empty_health": "该单元尚无健康历史。",
    "chart_empty_sensors": "该单元传感器尚未上报。",
    "chart_axis_cycle": "周期",
    "chart_axis_health": "健康度",
    "subplot_vibration": "振动",
    "subplot_temperature": "温度",
    "subplot_current_load": "电流 / 负载",
    "status_green": "状态良好",
    "status_amber": "需关注",
    "status_red": "需检查",
    "hint_green": "近期窗口无明显异常。",
    "hint_amber": "磨损在上升, 下次精密加工前值得看一眼。",
    "hint_red": "该单元漂移明显。切削前请检查振动与电流。",
    "aria_green": "状态良好",
    "aria_amber": "状态需关注",
    "aria_red": "状态需检查",
    "sev_high": "尽快",
    "sev_medium": "留意",
    "sev_low": "备注",
    "bootstrap_error_title": "无法加载看板",
    "bootstrap_error_hint": (
        "重新生成演示数据后刷新："
        "python scripts/build_demo_data.py && python scripts/train_isolation_forest.py"
    ),
    "empty_fleet": "快照中无机器。请重新生成演示数据。",
    "empty_alerts_floor": "当前无维护备注。",
    "empty_alerts_machine": "{machine_id} 暂无排队事项。",
    "disclaimer": (
        "作品集演示，非认证状态监测系统。"
        "传感器流为 NASA CMAPSS 代理并映射为 CNC 术语, "
        "用于分诊练习，不可用于真实工单。"
    ),
    "opcua_banner": "模拟 OPC-UA · {n} 个标签 · 回放缓冲（非真实 PLC）",
    "detail_health": "健康度 {health:.0f}/100, {status}。预计剩余时间：{ttf}。",
    "card_aria": "{machine_id}，{status}，健康度 {health:.0f}/100",
    "alert_red": (
        "{machine_id} 状况较差（健康度 {health:.0f}/100）。"
        "此代理大约还剩 {ttf} 切削时间, "
        "下次紧公差加工前请检查主轴振动与电流。"
    ),
    "alert_amber": (
        "{machine_id} 正在向不利方向升温（健康度 {health:.0f}/100）。"
        "若趋势持续大约还剩 {ttf}, 请查看振动曲线。"
    ),
    "alert_drop": (
        "{machine_id} 在一个窗口内下降了 {delta:.0f} 健康分 "
        "（{prev:.0f} → {health:.0f}）。"
        "比平时更陡, 值得快速查看。"
    ),
    "ttf_days": "~{n:.1f} 天",
    "ttf_hours": "~{n:.1f} 小时",
    "ttf_minutes": "~{n:.0f} 分钟",
    "sensor_vibration_rms": "振动 RMS (mm/s)",
    "sensor_vibration_peak": "振动峰值 (mm/s)",
    "sensor_temperature_spindle_c": "主轴温度 (°C)",
    "sensor_temperature_coolant_c": "冷却液温度 (°C)",
    "sensor_current_draw_a": "主轴电流 (A)",
    "sensor_load_pct": "轴负载 (%)",
    "machine_CNC-01": "主轴单元 A, 龙门铣",
    "machine_CNC-02": "主轴单元 B, 车削中心",
    "machine_CNC-03": "微铣, 表盘夹具",
    "machine_CNC-04": "去毛刺 / 精整, 共用单元",
    "cards_aria": "机器健康卡片",
    "health_graph_aria": "各周期健康分数",
    "sensor_graph_aria": "振动、温度与电流曲线",
}

_RU: dict[str, str] = {
    "lang": "Язык",
    "lang_hint": "Меняйте язык в любой момент. Вся панель обновится.",
    "brand_eyebrow": "ЗДОРОВЬЕ ЯЧЕЕК",
    "app_title": "Монитор шпинделя CNC",
    "tagline": "Какие ячейки проверить перед следующим точным прогоном?",
    "floor_hint": "Нажмите ячейку, графики и заметки обновятся.",
    "floor_all_fine": "Все четыре ячейки сейчас в порядке.",
    "floor_need_look_1": "1 требует проверки",
    "floor_need_look_n": "{n} требуют проверки",
    "floor_watch_1": "1 под наблюдением",
    "floor_watch_n": "{n} под наблюдением",
    "floor_tap": "Нажмите ячейку для осмотра.",
    "panel_main": "Что происходит на этой ячейке",
    "panel_side": "Что делать дальше",
    "panel_notes": "Заметки по этой ячейке",
    "sensor_details": "Последние показания датчиков",
    "card_cta": "Открыть ячейку →",
    "card_cta_selected": "Просмотр",
    "card_tooltip": "Открыть здоровье и графики этой ячейки",
    "viewing_pill": "Ячейка {machine_id}",
    "roughly_left_prefix": "Около ",
    "roughly_left_suffix": " осталось",
    "chart_health_title": "Здоровье по недавним циклам",
    "chart_sensor_title": "Каналы датчиков (прокси CNC)",
    "chart_empty_health": "Пока нет истории здоровья для этой ячейки.",
    "chart_empty_sensors": "Датчики ещё не ответили для этой ячейки.",
    "chart_axis_cycle": "Цикл",
    "chart_axis_health": "Здоровье",
    "subplot_vibration": "Вибрация",
    "subplot_temperature": "Температура",
    "subplot_current_load": "Ток / нагрузка",
    "status_green": "Всё хорошо",
    "status_amber": "Наблюдать",
    "status_red": "Проверить",
    "hint_green": "В недавнем окне ничего необычного.",
    "hint_amber": "Износ растёт, стоит взглянуть перед следующим точным прогоном.",
    "hint_red": "Ячейка сильно дрейфует. Проверьте вибрацию и ток перед резанием.",
    "aria_green": "статус всё хорошо",
    "aria_amber": "статус наблюдать",
    "aria_red": "статус проверить",
    "sev_high": "Скоро",
    "sev_medium": "Вскоре",
    "sev_low": "Заметка",
    "bootstrap_error_title": "Не удалось загрузить панель",
    "bootstrap_error_hint": (
        "Пересоберите артефакты и обновите страницу: "
        "python scripts/build_demo_data.py && python scripts/train_isolation_forest.py"
    ),
    "empty_fleet": "В снимке нет станков. Пересоздайте демо-данные.",
    "empty_alerts_floor": "Сейчас нет заметок по обслуживанию.",
    "empty_alerts_machine": "Нет очереди для {machine_id}.",
    "disclaimer": (
        "Портфолио-демо, не сертифицированная система мониторинга. "
        "Потоки датчиков, прокси NASA CMAPSS в терминах CNC, "
        "для практики triage, не для реальных нарядов."
    ),
    "opcua_banner": "Макет OPC-UA · {n} тегов · буфер воспроизведения (не живой ПЛК)",
    "detail_health": "Здоровье {health:.0f}/100, {status}. Осталось примерно: {ttf}.",
    "card_aria": "{machine_id}, {status}, здоровье {health:.0f} из 100",
    "alert_red": (
        "{machine_id} в плохом состоянии (здоровье {health:.0f}/100). "
        "Около {ttf} резания на этом прокси, "
        "проверьте вибрацию и ток перед следующей жёсткой точностью."
    ),
    "alert_amber": (
        "{machine_id} греется не в ту сторону (здоровье {health:.0f}/100). "
        "Около {ttf}, если тренд сохранится, посмотрите трасс вибрации."
    ),
    "alert_drop": (
        "{machine_id} потерял {delta:.0f} пунктов здоровья "
        "({prev:.0f} → {health:.0f}) за одно окно. "
        "Резче обычного, стоит быстро глянуть."
    ),
    "ttf_days": "~{n:.1f} д",
    "ttf_hours": "~{n:.1f} ч",
    "ttf_minutes": "~{n:.0f} мин",
    "sensor_vibration_rms": "Вибрация RMS (мм/с)",
    "sensor_vibration_peak": "Пик вибрации (мм/с)",
    "sensor_temperature_spindle_c": "Темп. шпинделя (°C)",
    "sensor_temperature_coolant_c": "Темп. СОЖ (°C)",
    "sensor_current_draw_a": "Ток шпинделя (А)",
    "sensor_load_pct": "Нагрузка осей (%)",
    "machine_CNC-01": "Шпиндельная ячейка A, мостовой фрезер",
    "machine_CNC-02": "Шпиндельная ячейка B, токарный центр",
    "machine_CNC-03": "Микрофрезерование, пластина часов",
    "machine_CNC-04": "Зачистка / финиш, общая ячейка",
    "cards_aria": "Карточки здоровья станков",
    "health_graph_aria": "Оценка здоровья по циклам",
    "sensor_graph_aria": "Трассы вибрации, температуры и тока",
}


def _merge(overrides: dict[str, str]) -> dict[str, str]:
    """Return English base with locale overrides applied."""
    merged = dict(_EN)
    merged.update(overrides)
    return merged


COPY: dict[str, dict[str, str]] = {
    "en": dict(_EN),
    "fr": _merge(_FR),
    "de": _merge(_DE),
    "it": _merge(_IT),
    "pt": _merge(_PT),
    "es": _merge(_ES),
    "zh": _merge(_ZH),
    "ru": _merge(_RU),
}

SENSOR_I18N_KEYS = {
    "vibration_rms": "sensor_vibration_rms",
    "vibration_peak": "sensor_vibration_peak",
    "temperature_spindle_c": "sensor_temperature_spindle_c",
    "temperature_coolant_c": "sensor_temperature_coolant_c",
    "current_draw_a": "sensor_current_draw_a",
    "load_pct": "sensor_load_pct",
}


def normalize_lang(lang: str | None) -> str:
    """Return a supported language code from a control value."""
    if not lang:
        return DEFAULT_LANG
    raw = str(lang).strip().lower()
    aliases = {
        "zh": "zh",
        "zh-cn": "zh",
        "zh-tw": "zh",
        "cn": "zh",
        "中文": "zh",
        "mandarin": "zh",
        "pt": "pt",
        "pt-br": "pt",
        "pt-pt": "pt",
        "portuguese": "pt",
        "português": "pt",
        "es": "es",
        "es-es": "es",
        "es-mx": "es",
        "spanish": "es",
        "español": "es",
        "ru": "ru",
        "ru-ru": "ru",
        "russian": "ru",
        "русский": "ru",
    }
    if raw in aliases:
        return aliases[raw]
    code = raw[:2]
    if code in SUPPORTED_LANGS:
        return code
    return DEFAULT_LANG


def t(key: str, lang: str = DEFAULT_LANG, **kwargs: Any) -> str:
    """Look up a UI string; fall back to English, then the key itself."""
    code = normalize_lang(lang)
    template = COPY[code].get(key, COPY[DEFAULT_LANG].get(key, key))
    if kwargs:
        try:
            return template.format(**kwargs)
        except (KeyError, ValueError):
            return template
    return template


def status_label(status: str, lang: str = DEFAULT_LANG) -> str:
    """Return translated shop-floor status label."""
    return t(f"status_{status}", lang)


def status_hint(status: str, lang: str = DEFAULT_LANG) -> str:
    """Return translated status hint for the side panel."""
    return t(f"hint_{status}", lang)


def severity_label(severity: str, lang: str = DEFAULT_LANG) -> str:
    """Return translated alert severity chip."""
    return t(f"sev_{severity}", lang)


def sensor_label(column: str, lang: str = DEFAULT_LANG) -> str:
    """Return translated sensor channel name for legends and lists."""
    key = SENSOR_I18N_KEYS.get(column)
    if key is None:
        return column
    return t(key, lang)


def machine_label(machine_id: str, lang: str = DEFAULT_LANG) -> str:
    """Return translated machine role label."""
    return t(f"machine_{machine_id}", lang)


def language_dropdown_options() -> list[dict[str, str]]:
    """Return Dash dropdown options for the language switcher."""
    return [{"label": LANGUAGE_LABELS[code], "value": code} for code in SUPPORTED_LANGS]
