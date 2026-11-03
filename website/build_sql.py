#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate the SQL import for the CubeIT project page on giannialagna.me.

Target: WordPress with the GA Portfolio Core + GA i18n plugins, table prefix `pws_`.
  - post type  ga_project            (public at /projects/cubeit/)
  - meta       _ga_category, _ga_status, _ga_year, _ga_start, _ga_role,
               _ga_repo, _ga_stack, _ga_facts, _ga_featured, _ga_log_hide
  - meta       _ga_i18n = PHP-serialized [ lang => [ field => text ] ]
               languages: de, it, fr, es, la (en is the source in the post itself)

The script is idempotent: running the produced SQL twice updates the same post.

Usage:  python3 website/build_sql.py > website/pws_cubeit_project.sql
"""
import sys

PREFIX = "pws_"
SLUG = "cubeit"
REPO = "https://github.com/GianniAlagna/CubeIT"

# --------------------------------------------------------------------------
# English source (stored in pws_posts / pws_postmeta)
# --------------------------------------------------------------------------
EN = {
    "title": "CubeIT – Magnetic Cube Computer for Schools",
    "excerpt": (
        "An open-hardware learning computer for Swiss schools (2015): every component – processor, "
        "power, display, USB, sound – sits in its own magnetic cube. Children snap the cubes together, "
        "the computer boots, and they learn how a computer really works."
    ),
    "content": [
        ("p", "CubeIT turned the black box “computer” into building blocks that children can hold in their "
              "hands. Each function sat in its own 50 mm cube with magnetic faces: a C.H.I.P. board as the "
              "brain, a power cube, an HDMI/DVI display cube, a USB cube and a sound cube. When the right cubes "
              "touch, the computer boots – input, processing and output become something children can see and feel."),
        ("h2", "What we built in 2015"),
        ("ul", [
            "Cube concept and magnetic CubeBus connector (5 V, GND, I2C, mirror-symmetric pinout)",
            "First C.H.I.P. board order and 3D-printed prototype shells",
            "First learning games in Python and pygame, running directly on the board",
            "Tools for cube identification (I2C EEPROM), GPIO tests and classroom provisioning",
        ]),
        ("h2", "Why it stopped"),
        ("p", "The technology worked – market access did not. Compulsory schooling in Switzerland is a cantonal "
              "matter (Art. 62 Federal Constitution), so there is no single federal customer. Product conformity "
              "(toy safety, EMC, radio, batteries), a pilot evaluated by a university of teacher education, cantonal "
              "teaching-material approval and public procurement would have required an estimated CHF 30–80k and "
              "2–4 years before the first sale – out of reach for an early-stage team."),
        ("h2", "Open source today"),
        ("p", "Concept, hardware architecture, Lehrplan 21 mapping, the Swiss regulatory roadmap, the tools and a "
              "free micro learning game (“Build your computer”, three missions in DE/FR/IT/EN) are published on "
              "GitHub under MIT and CC BY-SA – free for every school."),
    ],
    "category": "EdTech · Hardware Engineering",
    "role": "Co-Founder · Concept & Development",
    "facts": "Year|2015\nBrain|C.H.I.P. (USD 9)\nCurriculum|Lehrplan 21 · MI\nLicense|MIT · CC BY-SA",
}

META = {
    "_ga_category": EN["category"],
    "_ga_status": "discontinued",
    "_ga_year": "2015",
    "_ga_start": "2015",
    "_ga_role": EN["role"],
    "_ga_url": "",
    "_ga_repo": REPO,
    "_ga_log_hide": "",
    "_ga_stack": "C.H.I.P., Debian, Python, pygame, I2C, KiCad, 3D printing",
    "_ga_facts": EN["facts"],
    "_ga_featured": "",
}

# --------------------------------------------------------------------------
# Translations (GA i18n: title, excerpt, content, category, facts, role)
# --------------------------------------------------------------------------
TR = {
    "de": {
        "title": "CubeIT – Magnetischer Würfel-Computer für Schulen",
        "excerpt": (
            "Ein Open-Hardware-Lerncomputer für Schweizer Schulen (2015): Jede Komponente – Prozessor, Strom, "
            "Bildschirm, USB, Ton – steckt in einem eigenen Magnetwürfel. Kinder fügen die Würfel zusammen, der "
            "Computer startet, und sie verstehen, wie ein Computer wirklich funktioniert."
        ),
        "content": [
            ("p", "CubeIT machte aus der Blackbox «Computer» Bausteine, die Kinder in die Hand nehmen können. Jede "
                  "Funktion sass in einem eigenen 50-mm-Würfel mit magnetischen Seiten: ein C.H.I.P.-Board als Gehirn, "
                  "ein Strom-Würfel, ein HDMI/DVI-Bildschirm-Würfel, ein USB-Würfel und ein Ton-Würfel. Berühren sich "
                  "die richtigen Würfel, startet der Computer – Eingabe, Verarbeitung und Ausgabe werden sicht- und greifbar."),
            ("h2", "Was wir 2015 gebaut haben"),
            ("ul", [
                "Würfelkonzept und magnetischer CubeBus-Stecker (5 V, GND, I2C, spiegelsymmetrische Belegung)",
                "Erste C.H.I.P.-Board-Bestellung und 3D-gedruckte Prototyp-Gehäuse",
                "Erste Lernspiele in Python und pygame, direkt auf dem Board",
                "Werkzeuge für Würfel-Erkennung (I2C-EEPROM), GPIO-Tests und die Einrichtung von Klassencomputern",
            ]),
            ("h2", "Warum wir gestoppt haben"),
            ("p", "Die Technik funktionierte – der Marktzugang nicht. Die Volksschule ist in der Schweiz Sache der "
                  "Kantone (Art. 62 BV); einen einzelnen Bundeskunden gibt es nicht. Produktkonformität (Spielzeugsicherheit, "
                  "EMV, Funk, Batterien), ein von einer Pädagogischen Hochschule evaluierter Pilot, die kantonale "
                  "Lehrmittelzulassung und das öffentliche Beschaffungswesen hätten vor dem ersten Verkauf geschätzt "
                  "CHF 30–80k und 2–4 Jahre erfordert – für ein Team in der Frühphase nicht machbar."),
            ("h2", "Heute Open Source"),
            ("p", "Konzept, Hardware-Architektur, Lehrplan-21-Zuordnung, die Schweizer Regulierungs-Roadmap, die "
                  "Werkzeuge und ein kostenloses Micro-Learning-Spiel («Bau deinen Computer», drei Missionen in "
                  "DE/FR/IT/EN) sind auf GitHub unter MIT und CC BY-SA veröffentlicht – frei für jede Schule."),
        ],
        "category": "EdTech · Hardware Engineering",
        "role": "Mitgründer · Konzept & Entwicklung",
        "facts": "Jahr|2015\nGehirn|C.H.I.P. (USD 9)\nLehrplan|Lehrplan 21 · MI\nLizenz|MIT · CC BY-SA",
    },
    "it": {
        "title": "CubeIT – Computer a cubi magnetici per le scuole",
        "excerpt": (
            "Un computer didattico open hardware per le scuole svizzere (2015): ogni componente – processore, "
            "alimentazione, schermo, USB, audio – si trova in un proprio cubo magnetico. I bambini uniscono i cubi, "
            "il computer si avvia e imparano come funziona davvero un computer."
        ),
        "content": [
            ("p", "CubeIT ha trasformato la scatola nera «computer» in mattoncini che i bambini possono tenere in mano. "
                  "Ogni funzione era in un cubo di 50 mm con facce magnetiche: una scheda C.H.I.P. come cervello, un cubo "
                  "di alimentazione, un cubo schermo HDMI/DVI, un cubo USB e un cubo audio. Quando i cubi giusti si "
                  "toccano, il computer si avvia – input, elaborazione e output diventano visibili e tangibili."),
            ("h2", "Cosa abbiamo costruito nel 2015"),
            ("ul", [
                "Concetto dei cubi e connettore magnetico CubeBus (5 V, GND, I2C, piedinatura simmetrica a specchio)",
                "Primo ordine di schede C.H.I.P. e involucri prototipo stampati in 3D",
                "Primi giochi didattici in Python e pygame, direttamente sulla scheda",
                "Strumenti per l'identificazione dei cubi (EEPROM I2C), test GPIO e configurazione dei computer di classe",
            ]),
            ("h2", "Perché ci siamo fermati"),
            ("p", "La tecnologia funzionava – l'accesso al mercato no. In Svizzera la scuola dell'obbligo è di competenza "
                  "cantonale (art. 62 Cost.), quindi non esiste un unico cliente federale. Conformità del prodotto "
                  "(sicurezza dei giocattoli, CEM, radio, batterie), un progetto pilota valutato da un'alta scuola "
                  "pedagogica, l'approvazione cantonale dei mezzi didattici e gli appalti pubblici avrebbero richiesto "
                  "circa CHF 30–80k e 2–4 anni prima della prima vendita – fuori portata per un team in fase iniziale."),
            ("h2", "Oggi open source"),
            ("p", "Concetto, architettura hardware, corrispondenza con il Lehrplan 21, la roadmap normativa svizzera, gli "
                  "strumenti e un gioco di micro-apprendimento gratuito («Costruisci il tuo computer», tre missioni in "
                  "DE/FR/IT/EN) sono pubblicati su GitHub con licenza MIT e CC BY-SA – gratuiti per ogni scuola."),
        ],
        "category": "EdTech · Hardware Engineering",
        "role": "Co-fondatore · Concetto e sviluppo",
        "facts": "Anno|2015\nCervello|C.H.I.P. (USD 9)\nPiano di studio|Lehrplan 21 · MI\nLicenza|MIT · CC BY-SA",
    },
    "fr": {
        "title": "CubeIT – Ordinateur à cubes magnétiques pour les écoles",
        "excerpt": (
            "Un ordinateur pédagogique open hardware pour les écoles suisses (2015) : chaque composant – processeur, "
            "alimentation, écran, USB, son – se trouve dans son propre cube magnétique. Les enfants assemblent les "
            "cubes, l'ordinateur démarre, et ils comprennent comment fonctionne vraiment un ordinateur."
        ),
        "content": [
            ("p", "CubeIT a transformé la boîte noire « ordinateur » en blocs que les enfants peuvent tenir en main. "
                  "Chaque fonction se trouvait dans un cube de 50 mm aux faces magnétiques : une carte C.H.I.P. comme "
                  "cerveau, un cube d'alimentation, un cube écran HDMI/DVI, un cube USB et un cube son. Quand les bons "
                  "cubes se touchent, l'ordinateur démarre – entrée, traitement et sortie deviennent visibles et tangibles."),
            ("h2", "Ce que nous avons construit en 2015"),
            ("ul", [
                "Concept des cubes et connecteur magnétique CubeBus (5 V, GND, I2C, brochage symétrique en miroir)",
                "Première commande de cartes C.H.I.P. et boîtiers prototypes imprimés en 3D",
                "Premiers jeux éducatifs en Python et pygame, directement sur la carte",
                "Outils d'identification des cubes (EEPROM I2C), tests GPIO et préparation des ordinateurs de classe",
            ]),
            ("h2", "Pourquoi nous avons arrêté"),
            ("p", "La technique fonctionnait – l'accès au marché, non. En Suisse, l'école obligatoire relève des cantons "
                  "(art. 62 Cst.) : il n'existe pas de client fédéral unique. La conformité du produit (sécurité des jouets, "
                  "CEM, radio, batteries), un projet pilote évalué par une haute école pédagogique, l'agrément cantonal "
                  "des moyens d'enseignement et les marchés publics auraient exigé environ CHF 30–80k et 2–4 ans avant la "
                  "première vente – hors de portée pour une équipe en phase de démarrage."),
            ("h2", "Aujourd'hui en open source"),
            ("p", "Concept, architecture matérielle, correspondance avec le Lehrplan 21, feuille de route réglementaire "
                  "suisse, outils et un jeu de micro-apprentissage gratuit (« Construis ton ordinateur », trois missions en "
                  "DE/FR/IT/EN) sont publiés sur GitHub sous licences MIT et CC BY-SA – gratuits pour chaque école."),
        ],
        "category": "EdTech · Hardware Engineering",
        "role": "Cofondateur · Concept et développement",
        "facts": "Année|2015\nCerveau|C.H.I.P. (USD 9)\nPlan d'études|Lehrplan 21 · MI\nLicence|MIT · CC BY-SA",
    },
    "es": {
        "title": "CubeIT – Ordenador de cubos magnéticos para escuelas",
        "excerpt": (
            "Un ordenador educativo de hardware abierto para las escuelas suizas (2015): cada componente – procesador, "
            "alimentación, pantalla, USB, sonido – está en su propio cubo magnético. Los niños unen los cubos, el "
            "ordenador arranca y aprenden cómo funciona realmente un ordenador."
        ),
        "content": [
            ("p", "CubeIT convirtió la caja negra «ordenador» en bloques que los niños pueden tener en la mano. Cada "
                  "función estaba en un cubo de 50 mm con caras magnéticas: una placa C.H.I.P. como cerebro, un cubo de "
                  "alimentación, un cubo de pantalla HDMI/DVI, un cubo USB y un cubo de sonido. Cuando los cubos correctos "
                  "se tocan, el ordenador arranca: entrada, procesamiento y salida se vuelven visibles y tangibles."),
            ("h2", "Lo que construimos en 2015"),
            ("ul", [
                "Concepto de cubos y conector magnético CubeBus (5 V, GND, I2C, asignación de pines simétrica en espejo)",
                "Primer pedido de placas C.H.I.P. y carcasas prototipo impresas en 3D",
                "Primeros juegos educativos en Python y pygame, directamente en la placa",
                "Herramientas para identificar cubos (EEPROM I2C), pruebas GPIO y preparación de ordenadores de aula",
            ]),
            ("h2", "Por qué lo detuvimos"),
            ("p", "La tecnología funcionaba; el acceso al mercado, no. En Suiza la escuela obligatoria es competencia de "
                  "los cantones (art. 62 de la Constitución Federal), por lo que no existe un único cliente federal. La "
                  "conformidad del producto (seguridad de juguetes, CEM, radio, baterías), un piloto evaluado por una "
                  "universidad de formación docente, la aprobación cantonal de material didáctico y la contratación "
                  "pública habrían requerido unos CHF 30–80k y 2–4 años antes de la primera venta: fuera del alcance de "
                  "un equipo en fase inicial."),
            ("h2", "Hoy en código abierto"),
            ("p", "El concepto, la arquitectura de hardware, la correspondencia con el Lehrplan 21, la hoja de ruta "
                  "regulatoria suiza, las herramientas y un juego de microaprendizaje gratuito («Construye tu ordenador», "
                  "tres misiones en DE/FR/IT/EN) están publicados en GitHub con licencias MIT y CC BY-SA: gratis para "
                  "cualquier escuela."),
        ],
        "category": "EdTech · Ingeniería de hardware",
        "role": "Cofundador · Concepto y desarrollo",
        "facts": "Año|2015\nCerebro|C.H.I.P. (USD 9)\nPlan de estudios|Lehrplan 21 · MI\nLicencia|MIT · CC BY-SA",
    },
    "la": {
        "title": "CubeIT – Computatrum cubis magneticis scholis",
        "excerpt": (
            "Computatrum discendi apertum scholis Helveticis (MMXV): quaeque pars – processor, vis electrica, "
            "monitorium, USB, sonus – in suo cubo magnetico inest. Pueri cubos coniungunt, computatrum incipit, "
            "et discunt quomodo computatrum vere operetur."
        ),
        "content": [
            ("p", "CubeIT arcam obscuram «computatrum» in lapides aedificandi mutavit, quos pueri manibus tenere possunt. "
                  "Quodque munus in suo cubo quinquaginta millimetrorum lateribus magneticis inerat: tabula C.H.I.P. ut "
                  "cerebrum, cubus vis electricae, cubus monitorii HDMI/DVI, cubus USB et cubus soni. Cum cubi recti se "
                  "tangunt, computatrum incipit – ingressus, tractatio et egressus visibiles et tangibiles fiunt."),
            ("h2", "Quid anno MMXV aedificavimus"),
            ("ul", [
                "Consilium cuborum et nexus magneticus CubeBus (5 V, GND, I2C, dispositio speculariter symmetrica)",
                "Prima tabularum C.H.I.P. emptio et involucra exemplaria typis tridimensionalibus facta",
                "Primi ludi discendi Python et pygame scripti, in ipsa tabula currentes",
                "Instrumenta ad cubos agnoscendos (EEPROM I2C), probationes GPIO et computatra classium paranda",
            ]),
            ("h2", "Cur destitimus"),
            ("p", "Ars technica operabatur – aditus ad forum non. In Helvetia schola publica res pagorum est (art. 62 "
                  "Constitutionis Foederalis); emptor foederalis unus non exstat. Conformitas producti (securitas ludibriorum, "
                  "EMC, radiophonia, pilae electricae), experimentum ab universitate paedagogica aestimatum, approbatio "
                  "pagana instrumentorum docendi et emptiones publicae ante primam venditionem circiter CHF 30–80 milia "
                  "et duos ad quattuor annos postulavissent – parvae turmae incipienti impossibile."),
            ("h2", "Hodie fons apertus"),
            ("p", "Consilium, architectura machinalis, concordantia cum Lehrplan 21, via regulatoria Helvetica, instrumenta "
                  "et ludus brevis discendi gratuitus («Aedifica computatrum tuum», tres missiones DE/FR/IT/EN) in GitHub "
                  "sub licentiis MIT et CC BY-SA publicata sunt – omnibus scholis libera."),
        ],
        "category": "EdTech · Ars machinalis",
        "role": "Conditor socius · Consilium et evolutio",
        "facts": "Annus|MMXV\nCerebrum|C.H.I.P. (USD 9)\nOrdo studiorum|Lehrplan 21 · MI\nLicentia|MIT · CC BY-SA",
    },
}

LANG_ORDER = ["de", "it", "fr", "es", "la"]
FIELD_ORDER = ["title", "excerpt", "content", "category", "facts", "role"]


# --------------------------------------------------------------------------
# Renderers
# --------------------------------------------------------------------------
def esc_html(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def blocks(parts):
    """Gutenberg block markup for the English post_content."""
    out = []
    for kind, val in parts:
        if kind == "p":
            out.append("<!-- wp:paragraph -->\n<p>%s</p>\n<!-- /wp:paragraph -->" % esc_html(val))
        elif kind == "h2":
            out.append('<!-- wp:heading -->\n<h2 class="wp-block-heading">%s</h2>\n<!-- /wp:heading -->' % esc_html(val))
        elif kind == "ul":
            items = "".join("<!-- wp:list-item -->\n<li>%s</li>\n<!-- /wp:list-item -->\n" % esc_html(i) for i in val)
            out.append('<!-- wp:list -->\n<ul class="wp-block-list">\n%s</ul>\n<!-- /wp:list -->' % items)
    return "\n\n".join(out)


def plain_html(parts):
    """Translated content: GA i18n runs it through wp_kses_post + wpautop."""
    out = []
    for kind, val in parts:
        if kind == "p":
            out.append("<p>%s</p>" % esc_html(val))
        elif kind == "h2":
            out.append("<h2>%s</h2>" % esc_html(val))
        elif kind == "ul":
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % esc_html(i) for i in val))
    return "\n".join(out)


def php_serialize(value):
    """Minimal PHP serialize() for nested dicts of strings (byte lengths in UTF-8)."""
    if isinstance(value, dict):
        inner = "".join(php_serialize(k) + php_serialize(v) for k, v in value.items())
        return "a:%d:{%s}" % (len(value), inner)
    s = str(value)
    return 's:%d:"%s";' % (len(s.encode("utf-8")), s)


def sql(s):
    """MySQL string literal (NO_BACKSLASH_ESCAPES off, the default)."""
    return "'" + s.replace("\\", "\\\\").replace("'", "''").replace("\n", "\\n").replace("\r", "") + "'"


# --------------------------------------------------------------------------
# Build
# --------------------------------------------------------------------------
def build():
    p = PREFIX
    i18n = {}
    for lang in LANG_ORDER:
        t = TR[lang]
        i18n[lang] = {}
        for f in FIELD_ORDER:
            i18n[lang][f] = plain_html(t[f]) if f == "content" else t[f]
    meta = dict(META)
    meta["_ga_i18n"] = php_serialize(i18n)

    content = blocks(EN["content"])
    L = []
    w = L.append
    w("-- ==========================================================================")
    w("-- CubeIT – project entry for giannialagna.me (GA Portfolio Core + GA i18n)")
    w("-- Table prefix: %s   ·   Post type: ga_project   ·   Slug: %s" % (p, SLUG))
    w("-- Languages: EN (source) + DE, IT, FR, ES, LA (meta _ga_i18n)")
    w("-- Generated by website/build_sql.py – edit the generator, not this file.")
    w("-- Idempotent: re-running updates the same post instead of duplicating it.")
    w("-- BACKUP FIRST:  mysqldump --default-character-set=utf8mb4 DB > backup.sql")
    w("-- ==========================================================================")
    w("")
    w("SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;")
    w("START TRANSACTION;")
    w("")
    w("-- Author: first administrator, fallback user 1")
    w("SET @ga_author := COALESCE((SELECT um.user_id FROM `%susermeta` um WHERE um.meta_key = '%scapabilities' "
      "AND um.meta_value LIKE '%%\"administrator\"%%' ORDER BY um.user_id LIMIT 1), 1);" % (p, p))
    w("SET @ga_order := (SELECT COALESCE(MAX(menu_order) + 1, 0) FROM `%sposts` WHERE post_type = 'ga_project');" % p)
    w("")
    w("-- 1) Create the post only if it does not exist yet")
    w("INSERT INTO `%sposts` (post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt, "
      "post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged, post_modified, "
      "post_modified_gmt, post_content_filtered, post_parent, guid, menu_order, post_type, post_mime_type, comment_count)" % p)
    w("SELECT @ga_author, NOW(), UTC_TIMESTAMP(), '', %s, '', 'publish', 'closed', 'closed', '', %s, '', '', "
      "NOW(), UTC_TIMESTAMP(), '', 0, '', @ga_order, 'ga_project', '', 0" % (sql(EN["title"]), sql(SLUG)))
    w("FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM `%sposts` WHERE post_type = 'ga_project' AND post_name = %s);"
      % (p, sql(SLUG)))
    w("")
    w("SET @ga_pid := (SELECT ID FROM `%sposts` WHERE post_type = 'ga_project' AND post_name = %s ORDER BY ID LIMIT 1);"
      % (p, sql(SLUG)))
    w("")
    w("-- 2) English source text (always refreshed)")
    w("UPDATE `%sposts` SET" % p)
    w("  post_title   = %s," % sql(EN["title"]))
    w("  post_excerpt = %s," % sql(EN["excerpt"]))
    w("  post_content = %s," % sql(content))
    w("  post_status  = 'publish',")
    w("  post_modified = NOW(), post_modified_gmt = UTC_TIMESTAMP(),")
    w("  guid = CONCAT('https://giannialagna.me/?post_type=ga_project&p=', @ga_pid)")
    w("WHERE ID = @ga_pid;")
    w("")
    w("-- 3) Portfolio fields + translations (replace managed keys only)")
    keys = ", ".join(sql(k) for k in meta)
    w("DELETE FROM `%spostmeta` WHERE post_id = @ga_pid AND meta_key IN (%s);" % (p, keys))
    w("INSERT INTO `%spostmeta` (post_id, meta_key, meta_value) VALUES" % p)
    rows = ["  (@ga_pid, %s, %s)" % (sql(k), sql(v)) for k, v in meta.items()]
    w(",\n".join(rows) + ";")
    w("")
    w("COMMIT;")
    w("")
    w("-- Check")
    w("SELECT ID, post_name, post_status, post_title FROM `%sposts` WHERE ID = @ga_pid;" % p)
    w("SELECT meta_key, LEFT(meta_value, 80) AS value FROM `%spostmeta` WHERE post_id = @ga_pid AND meta_key LIKE '\\_ga\\_%%';" % p)
    w("")
    w("-- After import: Settings → Permalinks → Save (flush rewrite rules) and purge any page/object cache.")
    w("-- Optional: set a featured image (e.g. docs/img/de_1_build.png from the CubeIT repo) in the editor.")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    sys.stdout.write(build())
