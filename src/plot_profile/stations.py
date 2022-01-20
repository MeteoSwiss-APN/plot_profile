"""Purpose: Define stations and their attributes.

Author: Stephanie Westerhuis

Date: 12/24/2021
"""
# Third-party
import pandas as pd

sdf = pd.DataFrame(
    # variables
    columns=[
        "abo",  # Adelboden
        "aig",  # Aigle
        "alt",  # Altdorf
        "and",  # Andeer
        "ant",  # Andermatt
        "arh",  # Altenrhein
        "aro",  # Arosa
        "att",  # Les Attelas
        "ban",  # Bantiger
        "bas",  # Basel / Binningen
        "beh",  # Passo del Bernina
        "ber",  # Bern / Zollikofen
        "bez",  # Beznau
        "bia",  # Biasca
        "bie",  # Bière
        "bin",  # Binn
        "biv",  # Bivio
        "biz",  # Bischofszell / Sitterdorf
        "bla",  # Blatten, Lötschental
        "bol",  # Boltigen
        "bou",  # Bouveret
        "brl",  # La Brévine
        "buf",  # Buffalora
        "bus",  # Buchs / Aarau
        "cdf",  # La Chaux-de-Fonds
        "cdm",  # Col des Mosses
        "cev",  # Cevio
        "cgi",  # Nyon / Changins
        "cha",  # Chasseral
        "chb",  # Les Charbonnières
        "chd",  # Château-d'Oex
        "chm",  # Chaumont
        "chu",  # Chur
        "chz",  # Cham
        "cim",  # Cimetta
        "cma",  # Crap Masegn
        "com",  # Acquarossa / Comprovasco
        "cov",  # Piz Corvatsch
        "coy",  # Courtelary
        "crm",  # Cressier
        "dav",  # Davos
        "dem",  # Delémont
        "dia",  # Les Diablerets
        "dis",  # Disentis
        "dol",  # La Dôle
        "ebk",  # Ebnat-Kappel
        "egh",  # Eggishorn
        "ego",  # Egolzwil
        "ein",  # Einsiedeln
        "elm",  # Elm
        "eng",  # Engelberg
        "evi",  # Evionnaz
        "evo",  # Evolène / Villa
        "fah",  # Fahy
        "flu",  # Flühli, LU
        "fre",  # Bullet / La Frétaz
        "fru",  # Frutigen
        "gen",  # Monte Generoso
        "ges",  # Gersau
        "gih",  # Giswil
        "gla",  # Glarus
        "goe",  # Gösgen
        "gor",  # Gornergrat
        "gos",  # Göschenen
        "gra",  # Fribourg / Grangeneuve
        "grc",  # Grächen
        "gre",  # Grenchen
        "grh",  # Grimsel Hospiz
        "gro",  # Grono
        "gsb",  # Col du Grand St-Bernard
        "gue",  # Gütsch, Andermatt
        "gut",  # Güttingen
        "gve",  # Genève / Cointrin
        "hai",  # Salen-Reutenen
        "hll",  # Hallau
        "hoe",  # Hörnli
        "ilz",  # Ilanz
        "int",  # Interlaken
        "jun",  # Jungfraujoch
        "klo",  # Zurich Kloten
        "kop",  # Koppigen
        "lac",  # Lachen / Galgenen
        "lae",  # Lägern
        "lag",  # Langnau i.E.
        "lat",  # Bergün / Latsch
        "lei",  # Leibstadt
        "lug",  # Lugano
        "luz",  # Luzern
        "mag",  # Magadino / Cadenazzo
        "mah",  # Mathod
        "mar",  # Les Marécottes
        "mas",  # Marsens
        "mer",  # Meiringen
        "mls",  # Le Moléson
        "moa",  # Mosen
        "mob",  # Montagnier, Bagnes
        "moe",  # Möhlin
        "mrp",  # Monte Rosa-Plattje
        "mte",  # Mottec
        "mtr",  # Matro
        "mub",  # Mühleberg
        "mve",  # Montana
        "nap",  # Napf
        "nas",  # Naluns / Schlivera
        "neu",  # Neuchâtel
        "obr",  # Oberriet / Kriessern
        "oro",  # Oron
        "otl",  # Locarno / Monti
        "pay",  # Payerne
        "pil",  # Pilatus
        "pio",  # Piotta
        "plf",  # Plaffeien
        "pma",  # Piz Martegnas
        "psi",  # Würenlingen / PSI
        "puy",  # Pully
        "rag",  # Bad Ragaz
        "reh",  # Zürich / Affoltern
        "rob",  # Poschiavo / Robbia
        "roe",  # Robièi
        "rue",  # Rünenberg
        "sae",  # Säntis
        "sag",  # Sattel, SZ
        "sam",  # Samedan
        "sbe",  # S. Bernardino
        "sbo",  # Stabio
        "scu",  # Scuol
        "sha",  # Schaffhausen
        "sia",  # Segl-Maria
        "sim",  # Simplon-Dorf
        "sio",  # Sion
        "sma",  # Zürich / Fluntern
        "smm",  # Sta. Maria, Val Müstair
        "spf",  # Schüpfheim
        "srs",  # Schiers
        "stc",  # St. Chrischona
        "stg",  # St. Gallen
        "tae",  # Aadorf / Tänikon
        "thu",  # Thun
        "tit",  # Titlis
        "ulr",  # Ulrichen
        "vab",  # Valbella
        "vad",  # Vaduz
        "vev",  # Vevey / Corseaux
        "vio",  # Vicosoprano
        "vis",  # Visp
        "vit",  # Villars-Tiercelin
        "vls",  # Vals
        "wae",  # Wädenswil
        "wfj",  # Weissfluhjoch
        "wyn",  # Wynau
        "zer",  # Zermatt
    ],
    # attributes
    index=[
        "short_name",
        "long_name",
        "dwh_id",
        "lat",
        "lon",
        "elevation",  # it's not called "height", neither "altitude"
    ],
)

# payerne
sdf["pay"].short_name = "pay"
sdf["pay"].long_name = "Payerne"
sdf["pay"].dwh_id = "06610"
sdf["pay"].dwh_name = "PAY"
sdf["pay"].lat = 46.81291
sdf["pay"].lon = 6.94418
sdf["pay"].elevation = 490.0

# zurich kloten
sdf["klo"].short_name = "klo"
sdf["klo"].long_name = "Kloten"
sdf["klo"].dwh_id = "06670"
sdf["klo"].dwh_name = "KLO"
sdf["klo"].lat = 47.479611
sdf["klo"].lon = 8.535961
sdf["klo"].elevation = 426

# grenchen
sdf["gre"].short_name = "gre"
sdf["gre"].long_name = "Grenchen"
sdf["gre"].dwh_id = "06632"
sdf["gre"].dwh_name = "GRE"
sdf["gre"].lat = 47.179097
sdf["gre"].lon = 7.415144
sdf["gre"].elevation = 428

# genf
sdf["gve"].short_name = "gve"
sdf["gve"].long_name = "Genève"
sdf["gve"].dwh_id = "06700"
sdf["gve"].dwh_name = "GVE"
sdf["gve"].lat = 46.247519
sdf["gve"].lon = 6.127742
sdf["gve"].elevation = 411

# Basel / Binningen
sdf["bas"].short_name = "bas"
sdf["bas"].long_name = "Basel"
sdf["bas"].dwh_id = "06601"
sdf["bas"].dwh_name = "BAS"
sdf["bas"].lat = 47.541142
sdf["bas"].lon = 7.583525
sdf["bas"].elevation = 316

# La Dôle
sdf["dol"].short_name = "dol"
sdf["dol"].long_name = "La Dôle"
sdf["dol"].dwh_id = "06702"
sdf["dol"].dwh_name = "DOL"
sdf["dol"].lat = 46.424794
sdf["dol"].lon = 6.099453
sdf["dol"].elevation = 1670

# Nyon / Changins
sdf["cgi"].short_name = "cgi"
sdf["cgi"].long_name = "Nyon"
sdf["cgi"].dwh_id = "06705"
sdf["cgi"].dwh_name = "CGI"
sdf["cgi"].lat = 46.401053
sdf["cgi"].lon = 6.227722
sdf["cgi"].elevation = 458

# Bière
sdf["bie"].short_name = "bie"
sdf["bie"].long_name = "Bière"
sdf["bie"].dwh_id = "06704"
sdf["bie"].dwh_name = "BIE"
sdf["bie"].lat = 46.524908
sdf["bie"].lon = 6.342386
sdf["bie"].elevation = 684

# Les Charbonnières
sdf["chb"].short_name = "chb"
sdf["chb"].long_name = "Les Charbonnières"
sdf["chb"].dwh_id = "06703"
sdf["chb"].dwh_name = "CHB"
sdf["chb"].lat = 46.67015
sdf["chb"].lon = 6.312428
sdf["chb"].elevation = 1045

# Mathod
sdf["mah"].short_name = "mah"
sdf["mah"].long_name = "Mathod"
sdf["mah"].dwh_id = "06618"
sdf["mah"].dwh_name = "MAH"
sdf["mah"].lat = 46.736978
sdf["mah"].lon = 6.567983
sdf["mah"].elevation = 435

# Bullet / La Frétaz
sdf["fre"].short_name = "fre"
sdf["fre"].long_name = "Bullet"
sdf["fre"].dwh_id = "06619"
sdf["fre"].dwh_name = "FRE"
sdf["fre"].lat = 46.840622
sdf["fre"].lon = 6.576369
sdf["fre"].elevation = 1205

# La Brévine
sdf["brl"].short_name = "brl"
sdf["brl"].long_name = "La Brévine"
sdf["brl"].dwh_id = "06617"
sdf["brl"].dwh_name = "BRL"
sdf["brl"].lat = 46.983844
sdf["brl"].lon = 6.610297
sdf["brl"].elevation = 1050

# La Chaux-de-Fonds
sdf["cdf"].short_name = "cdf"
sdf["cdf"].long_name = "La Chaux-de-Fonds"
sdf["cdf"].dwh_id = "06612"
sdf["cdf"].dwh_name = "CDF"
sdf["cdf"].lat = 47.082947
sdf["cdf"].lon = 6.792314
sdf["cdf"].elevation = 1017

# Villars-Tiercelin
sdf["vit"].short_name = "vit"
sdf["vit"].long_name = "Villars-Tiercelin"
sdf["vit"].dwh_id = "06707"
sdf["vit"].dwh_name = "VIT"
sdf["vit"].lat = 46.621778
sdf["vit"].lon = 6.710069
sdf["vit"].elevation = 859

# Pully
sdf["puy"].short_name = "puy"
sdf["puy"].long_name = "Pully"
sdf["puy"].dwh_id = "06711"
sdf["puy"].dwh_name = "PUY"
sdf["puy"].lat = 46.512283
sdf["puy"].lon = 6.667517
sdf["puy"].elevation = 456

# Neuchâtel
sdf["neu"].short_name = "neu"
sdf["neu"].long_name = "Neuchâtel"
sdf["neu"].dwh_id = "06604"
sdf["neu"].dwh_name = "NEU"
sdf["neu"].lat = 47.000067
sdf["neu"].lon = 6.953297
sdf["neu"].elevation = 485

# Cressier
sdf["crm"].short_name = "crm"
sdf["crm"].long_name = "Cressier"
sdf["crm"].dwh_id = "06606"
sdf["crm"].dwh_name = "CRM"
sdf["crm"].lat = 47.047581
sdf["crm"].lon = 7.059147
sdf["crm"].elevation = 430

# Chaumont
sdf["chm"].short_name = "chm"
sdf["chm"].long_name = "Chaumont"
sdf["chm"].dwh_id = "06608"
sdf["chm"].dwh_name = "CHM"
sdf["chm"].lat = 47.049169
sdf["chm"].lon = 6.978825
sdf["chm"].elevation = 1136

# Chasseral
sdf["cha"].short_name = "cha"
sdf["cha"].long_name = "Chasseral"
sdf["cha"].dwh_id = "06605"
sdf["cha"].dwh_name = "CHA"
sdf["cha"].lat = 47.131761
sdf["cha"].lon = 7.054367
sdf["cha"].elevation = 1594

# Courtelary
sdf["coy"].short_name = "coy"
sdf["coy"].long_name = "Courtelary"
sdf["coy"].dwh_id = "06710"
sdf["coy"].dwh_name = "COY"
sdf["coy"].lat = 47.180811
sdf["coy"].lon = 7.090656
sdf["coy"].elevation = 695

# Fribourg / Grangeneuve
sdf["gra"].short_name = "gra"
sdf["gra"].long_name = "Fribourg"
sdf["gra"].dwh_id = "06625"
sdf["gra"].dwh_name = "GRA"
sdf["gra"].lat = 46.7714
sdf["gra"].lon = 7.113736
sdf["gra"].elevation = 651

# Marsens
sdf["mas"].short_name = "mas"
sdf["mas"].long_name = "Marsens"
sdf["mas"].dwh_id = "06640"
sdf["mas"].dwh_name = "MAS"
sdf["mas"].lat = 46.656486
sdf["mas"].lon = 7.069669
sdf["mas"].elevation = 715

# Le Moléson
sdf["mls"].short_name = "mls"
sdf["mls"].long_name = "Le Moléson"
sdf["mls"].dwh_id = "06609"
sdf["mls"].dwh_name = "MLS"
sdf["mls"].lat = 46.546197
sdf["mls"].lon = 7.017753
sdf["mls"].elevation = 1974

# Château-d'Oex
sdf["chd"].short_name = "chd"
sdf["chd"].long_name = "Château-d'Oex"
sdf["chd"].dwh_id = "06627"
sdf["chd"].dwh_name = "CHD"
sdf["chd"].lat = 46.479819
sdf["chd"].lon = 7.139656
sdf["chd"].elevation = 1028

# Col des Mosses
sdf["cdm"].short_name = "cdm"
sdf["cdm"].long_name = "Col des Mosses"
sdf["cdm"].dwh_id = "06713"
sdf["cdm"].dwh_name = "CDM"
sdf["cdm"].lat = 46.391525
sdf["cdm"].lon = 7.098239
sdf["cdm"].elevation = 1412

# Bouveret
sdf["bou"].short_name = "bou"
sdf["bou"].long_name = "Bouveret"
sdf["bou"].dwh_id = "06709"
sdf["bou"].dwh_name = "BOU"
sdf["bou"].lat = 46.393447
sdf["bou"].lon = 6.857006
sdf["bou"].elevation = 374

# Aigle
sdf["aig"].short_name = "aig"
sdf["aig"].long_name = "Aigle"
sdf["aig"].dwh_id = "06712"
sdf["aig"].dwh_name = "AIG"
sdf["aig"].lat = 46.326647
sdf["aig"].lon = 6.924472
sdf["aig"].elevation = 381

# Evionnaz
sdf["evi"].short_name = "evi"
sdf["evi"].long_name = "Evionnaz"
sdf["evi"].dwh_id = "06715"
sdf["evi"].dwh_name = "EVI"
sdf["evi"].lat = 46.182953
sdf["evi"].lon = 7.026747
sdf["evi"].elevation = 482

# Les Marécottes
sdf["mar"].short_name = "mar"
sdf["mar"].long_name = "Les Marécottes"
sdf["mar"].dwh_id = "06614"
sdf["mar"].dwh_name = "MAR"
sdf["mar"].lat = 46.118903
sdf["mar"].lon = 7.016597
sdf["mar"].elevation = 990

# Montagnier, Bagnes
sdf["mob"].short_name = "mob"
sdf["mob"].long_name = "Montagnier"
sdf["mob"].dwh_id = "06615"
sdf["mob"].dwh_name = "MOB"
sdf["mob"].lat = 46.071019
sdf["mob"].lon = 7.225272
sdf["mob"].elevation = 839

# Les Attelas
sdf["att"].short_name = "att"
sdf["att"].long_name = "Les Attelas"
sdf["att"].dwh_id = "06723"
sdf["att"].dwh_name = "ATT"
sdf["att"].lat = 46.0991
sdf["att"].lon = 7.26865
sdf["att"].elevation = 2734

# Col du Grand St-Bernard
sdf["gsb"].short_name = "gsb"
sdf["gsb"].long_name = "Col du Grand St-Bernard"
sdf["gsb"].dwh_id = "06717"
sdf["gsb"].dwh_name = "GSB"
sdf["gsb"].lat = 45.869092
sdf["gsb"].lon = 7.170683
sdf["gsb"].elevation = 2472

# Sion
sdf["sio"].short_name = "sio"
sdf["sio"].long_name = "Sion"
sdf["sio"].dwh_id = "06720"
sdf["sio"].dwh_name = "SIO"
sdf["sio"].lat = 46.21865
sdf["sio"].lon = 7.330203
sdf["sio"].elevation = 482

# Boltigen
sdf["bol"].short_name = "bol"
sdf["bol"].long_name = "Boltigen"
sdf["bol"].dwh_id = "06733"
sdf["bol"].dwh_name = "BOL"
sdf["bol"].lat = 46.623519
sdf["bol"].lon = 7.384206
sdf["bol"].elevation = 820

# Plaffeien
sdf["plf"].short_name = "plf"
sdf["plf"].long_name = "Plaffeien"
sdf["plf"].dwh_id = "06628"
sdf["plf"].dwh_name = "PLF"
sdf["plf"].lat = 46.747717
sdf["plf"].lon = 7.266264
sdf["plf"].elevation = 1042

# Mühleberg
sdf["mub"].short_name = "mub"
sdf["mub"].long_name = "Mühleberg"
sdf["mub"].dwh_id = "06636"
sdf["mub"].dwh_name = "MUB"
sdf["mub"].lat = 46.973278
sdf["mub"].lon = 7.278217
sdf["mub"].elevation = 480

# Fahy
sdf["fah"].short_name = "fah"
sdf["fah"].long_name = "Fahy"
sdf["fah"].dwh_id = "06636"
sdf["fah"].dwh_name = "FAH"
sdf["fah"].lat = 47.423814
sdf["fah"].lon = 6.941194
sdf["fah"].elevation = 596

# Delémont
sdf["dem"].short_name = "dem"
sdf["dem"].long_name = "Delémont"
sdf["dem"].dwh_id = "06602"
sdf["dem"].dwh_name = "DEM"
sdf["dem"].lat = 47.351706
sdf["dem"].lon = 7.349567
sdf["dem"].elevation = 439

# Bern / Zollikofen
sdf["ber"].short_name = "ber"
sdf["ber"].long_name = "Bern"
sdf["ber"].dwh_id = "06631"
sdf["ber"].dwh_name = "BER"
sdf["ber"].lat = 46.990744
sdf["ber"].lon = 7.464061
sdf["ber"].elevation = 553

# Bantiger
sdf["ban"].short_name = "ban"
sdf["ban"].long_name = "Bantiger"
sdf["ban"].dwh_id = "06634"
sdf["ban"].dwh_name = "BAN"
sdf["ban"].lat = 46.977806
sdf["ban"].lon = 7.528667
sdf["ban"].elevation = 942

# Thun
sdf["thu"].short_name = "thu"
sdf["thu"].long_name = "Thun"
sdf["thu"].dwh_id = "06731"
sdf["thu"].dwh_name = "THU"
sdf["thu"].lat = 46.749853
sdf["thu"].lon = 7.585222
sdf["thu"].elevation = 570

# Frutigen
sdf["fru"].short_name = "fru"
sdf["fru"].long_name = "Frutigen"
sdf["fru"].dwh_id = "06613"
sdf["fru"].dwh_name = "FRU"
sdf["fru"].lat = 46.599003
sdf["fru"].lon = 7.657542
sdf["fru"].elevation = 756

# Adelboden
sdf["abo"].short_name = "abo"
sdf["abo"].long_name = "Adelboden"
sdf["abo"].dwh_id = "06735"
sdf["abo"].dwh_name = "ABO"
sdf["abo"].lat = 46.491703
sdf["abo"].lon = 7.560703
sdf["abo"].elevation = 1321

# Les Diablerets
sdf["dia"].short_name = "dia"
sdf["dia"].long_name = "Les Diablerets"
sdf["dia"].dwh_id = "06714"
sdf["dia"].dwh_name = "DIA"
sdf["dia"].lat = 46.32675
sdf["dia"].lon = 7.203781
sdf["dia"].elevation = 2964

# Montana
sdf["mve"].short_name = "mve"
sdf["mve"].long_name = "Montana"
sdf["mve"].dwh_id = "06724"
sdf["mve"].dwh_name = "MVE"
sdf["mve"].lat = 46.298806
sdf["mve"].lon = 7.460814
sdf["mve"].elevation = 1423

# Mottec
sdf["mte"].short_name = "mte"
sdf["mte"].long_name = "Mottec"
sdf["mte"].dwh_id = "06716"
sdf["mte"].dwh_name = "MTE"
sdf["mte"].lat = 46.147897
sdf["mte"].lon = 7.624033
sdf["mte"].elevation = 1580

# Evolène / Villa
sdf["evo"].short_name = "evo"
sdf["evo"].long_name = "Evolène"
sdf["evo"].dwh_id = "06722"
sdf["evo"].dwh_name = "EVO"
sdf["evo"].lat = 46.112211
sdf["evo"].lon = 7.508631
sdf["evo"].elevation = 1825

# Monte Rosa-Plattje
sdf["mrp"].short_name = "mrp"
sdf["mrp"].long_name = "Monte Rosa-Plattje"
sdf["mrp"].dwh_id = "06747"
sdf["mrp"].dwh_name = "MRP"
sdf["mrp"].lat = 45.956628
sdf["mrp"].lon = 7.814575
sdf["mrp"].elevation = 2885

# Gornergrat
sdf["gor"].short_name = "gor"
sdf["gor"].long_name = "Gornergrat"
sdf["gor"].dwh_id = "06749"
sdf["gor"].dwh_name = "GOR"
sdf["gor"].lat = 45.983633
sdf["gor"].lon = 7.785742
sdf["gor"].elevation = 3129

# Zermatt
sdf["zer"].short_name = "zer"
sdf["zer"].long_name = "Zermatt"
sdf["zer"].dwh_id = "06748"
sdf["zer"].dwh_name = "ZER"
sdf["zer"].lat = 46.029272
sdf["zer"].lon = 7.752433
sdf["zer"].elevation = 1638

# Grächen
sdf["grc"].short_name = "grc"
sdf["grc"].long_name = "Grächen"
sdf["grc"].dwh_id = "06728"
sdf["grc"].dwh_name = "GRC"
sdf["grc"].lat = 46.195314
sdf["grc"].lon = 7.836822
sdf["grc"].elevation = 1605

# Visp
sdf["vis"].short_name = "vis"
sdf["vis"].long_name = "Visp"
sdf["vis"].dwh_id = "06727"
sdf["vis"].dwh_name = "VIS"
sdf["vis"].lat = 46.3029
sdf["vis"].lon = 7.842958
sdf["vis"].elevation = 639

# Blatten, Lötschental
sdf["bla"].short_name = "bla"
sdf["bla"].long_name = "Blatten"
sdf["bla"].dwh_id = "06725"
sdf["bla"].dwh_name = "BLA"
sdf["bla"].lat = 46.420453
sdf["bla"].lon = 7.823194
sdf["bla"].elevation = 1538

# Jungfraujoch
sdf["jun"].short_name = "jun"
sdf["jun"].long_name = "Jungfraujoch"
sdf["jun"].dwh_id = "06730"
sdf["jun"].dwh_name = "JUN"
sdf["jun"].lat = 46.547556
sdf["jun"].lon = 7.985444
sdf["jun"].elevation = 3571

# Interlaken
sdf["int"].short_name = "int"
sdf["int"].long_name = "Interlaken"
sdf["int"].dwh_id = "06734"
sdf["int"].dwh_name = "INT"
sdf["int"].lat = 46.672233
sdf["int"].lon = 7.870194
sdf["int"].elevation = 577

# Langnau i.E.
sdf["lag"].short_name = "lag"
sdf["lag"].long_name = "Langnau i.E."
sdf["lag"].dwh_id = "06638"
sdf["lag"].dwh_name = "LAG"
sdf["lag"].lat = 46.939633
sdf["lag"].lon = 7.806425
sdf["lag"].elevation = 744

# Koppigen
sdf["kop"].short_name = "kop"
sdf["kop"].long_name = "Koppigen"
sdf["kop"].dwh_id = "06635"
sdf["kop"].dwh_name = "KOP"
sdf["kop"].lat = 47.11885
sdf["kop"].lon = 7.605503
sdf["kop"].elevation = 485

# Wynau
sdf["wyn"].short_name = "wyn"
sdf["wyn"].long_name = "Wynau"
sdf["wyn"].dwh_id = "06643"
sdf["wyn"].dwh_name = "WYN"
sdf["wyn"].lat = 47.255025
sdf["wyn"].lon = 7.787475
sdf["wyn"].elevation = 422

# St. Chrischona
sdf["stc"].short_name = "stc"
sdf["stc"].long_name = "St. Chrischona"
sdf["stc"].dwh_id = "06600"
sdf["stc"].dwh_name = "STC"
sdf["stc"].lat = 47.571767
sdf["stc"].lon = 7.687094
sdf["stc"].elevation = 493

# Möhlin
sdf["moe"].short_name = "moe"
sdf["moe"].long_name = "Möhlin"
sdf["moe"].dwh_id = "06641"
sdf["moe"].dwh_name = "MOE"
sdf["moe"].lat = 47.572197
sdf["moe"].lon = 7.877911
sdf["moe"].elevation = 343

# Rünenberg
sdf["rue"].short_name = "rue"
sdf["rue"].long_name = "Rünenberg"
sdf["rue"].dwh_id = "06645"
sdf["rue"].dwh_name = "RUE"
sdf["rue"].lat = 47.434572
sdf["rue"].lon = 7.879414
sdf["rue"].elevation = 611

# Gösgen
sdf["goe"].short_name = "goe"
sdf["goe"].long_name = "Gösgen"
sdf["goe"].dwh_id = "06626"
sdf["goe"].dwh_name = "GOE"
sdf["goe"].lat = 47.363147
sdf["goe"].lon = 7.973733
sdf["goe"].elevation = 380

# Buchs / Aarau
sdf["bus"].short_name = "bus"
sdf["bus"].long_name = "Aarau"
sdf["bus"].dwh_id = "06633"
sdf["bus"].dwh_name = "BUS"
sdf["bus"].lat = 47.384381
sdf["bus"].lon = 8.07955
sdf["bus"].elevation = 387

# Egolzwil
sdf["ego"].short_name = "ego"
sdf["ego"].long_name = "Egolzwil"
sdf["ego"].dwh_id = "06648"
sdf["ego"].dwh_name = "EGO"
sdf["ego"].lat = 47.179428
sdf["ego"].lon = 8.004758
sdf["ego"].elevation = 522

# Andeer
sdf["and"].short_name = "and"
sdf["and"].long_name = "Andeer"
sdf["and"].dwh_id = "06787"
sdf["and"].dwh_name = "AND"
sdf["and"].lat = 46.61
sdf["and"].lon = 9.432
sdf["and"].elevation = 989

# Säntis
sdf["sae"].short_name = "sae"
sdf["sae"].long_name = "Säntis"
sdf["sae"].dwh_id = "06680"
sdf["sae"].dwh_name = "SAE"
sdf["sae"].lat = 47.249
sdf["sae"].lon = 9.343
sdf["sae"].elevation = 2504

# Vaduz
sdf["vad"].short_name = "vad"
sdf["vad"].long_name = "Vaduz"
sdf["vad"].dwh_id = "06990"
sdf["vad"].dwh_name = "VAD"
sdf["vad"].lat = 47.127
sdf["vad"].lon = 9.518
sdf["vad"].elevation = 459

# Pilatus
sdf["pil"].short_name = "pil"
sdf["pil"].long_name = "Pilatus"
sdf["pil"].dwh_id = "06659"
sdf["pil"].dwh_name = "PIL"
sdf["pil"].lat = 46.979
sdf["pil"].lon = 8.252
sdf["pil"].elevation = 2107

# Altdorf
sdf["alt"].short_name = "alt"
sdf["alt"].long_name = "Altdorf"
sdf["alt"].dwh_id = "06672"
sdf["alt"].dwh_name = "ALT"
sdf["alt"].lat = 46.887
sdf["alt"].lon = 8.622
sdf["alt"].elevation = 440

# Ulrichen
sdf["ulr"].short_name = "ulr"
sdf["ulr"].long_name = "Ulrichen"
sdf["ulr"].dwh_id = "06745"
sdf["ulr"].dwh_name = "ULR"
sdf["ulr"].lat = 46.505
sdf["ulr"].lon = 8.308
sdf["ulr"].elevation = 1348

# Piotta
sdf["pio"].short_name = "pio"
sdf["pio"].long_name = "Piotta"
sdf["pio"].dwh_id = "06753"
sdf["pio"].dwh_name = "PIO"
sdf["pio"].lat = 46.515
sdf["pio"].lon = 8.688
sdf["pio"].elevation = 991

# Lugano
sdf["lug"].short_name = "lug"
sdf["lug"].long_name = "Lugano"
sdf["lug"].dwh_id = "06770"
sdf["lug"].dwh_name = "LUG"
sdf["lug"].lat = 46.004
sdf["lug"].lon = 8.96
sdf["lug"].elevation = 275

# Grono
sdf["gro"].short_name = "gro"
sdf["gro"].long_name = "Grono"
sdf["gro"].dwh_id = "06758"
sdf["gro"].dwh_name = "GRO"
sdf["gro"].lat = 46.255
sdf["gro"].lon = 9.164
sdf["gro"].elevation = 326

# Samedan
sdf["sam"].short_name = "sam"
sdf["sam"].long_name = "Samedan"
sdf["sam"].dwh_id = "06792"
sdf["sam"].dwh_name = "SAM"
sdf["sam"].lat = 46.526
sdf["sam"].lon = 9.879
sdf["sam"].elevation = 1711

# Chur
sdf["chu"].short_name = "chu"
sdf["chu"].long_name = "Chur"
sdf["chu"].dwh_id = "06786"
sdf["chu"].dwh_name = "CHU"
sdf["chu"].lat = 46.87
sdf["chu"].lon = 9.531
sdf["chu"].elevation = 558

# Napf
sdf["nap"].short_name = "nap"
sdf["nap"].long_name = "Napf"
sdf["nap"].dwh_id = "06639"
sdf["nap"].dwh_name = "NAP"
sdf["nap"].lat = 47.005
sdf["nap"].lon = 7.94
sdf["nap"].elevation = 1406

# Magadino / Cadenazzo
sdf["mag"].short_name = "mag"
sdf["mag"].long_name = "Magadino"
sdf["mag"].dwh_id = "06762"
sdf["mag"].dwh_name = "MAG"
sdf["mag"].lat = 46.16
sdf["mag"].lon = 8.934
sdf["mag"].elevation = 205

# Stabio
sdf["sbo"].short_name = "sbo"
sdf["sbo"].long_name = "Stabio"
sdf["sbo"].dwh_id = "06771"
sdf["sbo"].dwh_name = "SBO"
sdf["sbo"].lat = 45.843
sdf["sbo"].lon = 8.932
sdf["sbo"].elevation = 353

# Disentis
sdf["dis"].short_name = "dis"
sdf["dis"].long_name = "Disentis"
sdf["dis"].dwh_id = "06782"
sdf["dis"].dwh_name = "DIS"
sdf["dis"].lat = 46.707
sdf["dis"].lon = 8.853
sdf["dis"].elevation = 1199

# Giswil
sdf["gih"].short_name = "gih"
sdf["gih"].long_name = "Giswil"
sdf["gih"].dwh_id = "06657"
sdf["gih"].dwh_name = "GIH"
sdf["gih"].lat = 46.849
sdf["gih"].lon = 8.19
sdf["gih"].elevation = 473

# Altenrhein
sdf["arh"].short_name = "arh"
sdf["arh"].long_name = "Altenrhein"
sdf["arh"].dwh_id = "06690"
sdf["arh"].dwh_name = "ARH"
sdf["arh"].lat = 47.484
sdf["arh"].lon = 9.567
sdf["arh"].elevation = 400

# Davos
sdf["dav"].short_name = "dav"
sdf["dav"].long_name = "Davos"
sdf["dav"].dwh_id = "06784"
sdf["dav"].dwh_name = "DAV"
sdf["dav"].lat = 46.813
sdf["dav"].lon = 9.844
sdf["dav"].elevation = 1596

# St. Gallen
sdf["stg"].short_name = "stg"
sdf["stg"].long_name = "St. Gallen"
sdf["stg"].dwh_id = "06681"
sdf["stg"].dwh_name = "STG"
sdf["stg"].lat = 47.425
sdf["stg"].lon = 9.399
sdf["stg"].elevation = 778

# Glarus
sdf["gla"].short_name = "gla"
sdf["gla"].long_name = "Glarus"
sdf["gla"].dwh_id = "06685"
sdf["gla"].dwh_name = "GLA"
sdf["gla"].lat = 47.035
sdf["gla"].lon = 9.067
sdf["gla"].elevation = 519

# Gütsch, Andermatt
sdf["gue"].short_name = "gue"
sdf["gue"].long_name = "Gütsch"
sdf["gue"].dwh_id = "06750"
sdf["gue"].dwh_name = "GUE"
sdf["gue"].lat = 46.652
sdf["gue"].lon = 8.616
sdf["gue"].elevation = 2288

# Luzern
sdf["luz"].short_name = "luz"
sdf["luz"].long_name = "Luzern"
sdf["luz"].dwh_id = "06650"
sdf["luz"].dwh_name = "LUZ"
sdf["luz"].lat = 47.036
sdf["luz"].lon = 8.301
sdf["luz"].elevation = 456

# Engelberg
sdf["eng"].short_name = "eng"
sdf["eng"].long_name = "Engelberg"
sdf["eng"].dwh_id = "06655"
sdf["eng"].dwh_name = "ENG"
sdf["eng"].lat = 46.822
sdf["eng"].lon = 8.411
sdf["eng"].elevation = 1037

# Schaffhausen
sdf["sha"].short_name = "sha"
sdf["sha"].long_name = "Schaffhausen"
sdf["sha"].dwh_id = "06620"
sdf["sha"].dwh_name = "SHA"
sdf["sha"].lat = 47.69
sdf["sha"].lon = 8.62
sdf["sha"].elevation = 441

# Zürich / Fluntern
sdf["sma"].short_name = "sma"
sdf["sma"].long_name = "Fluntern"
sdf["sma"].dwh_id = "06660"
sdf["sma"].dwh_name = "SMA"
sdf["sma"].lat = 47.378
sdf["sma"].lon = 8.566
sdf["sma"].elevation = 558

# S. Bernardino
sdf["sbe"].short_name = "sbe"
sdf["sbe"].long_name = "S. Bernardino"
sdf["sbe"].dwh_id = "06783"
sdf["sbe"].dwh_name = "SBE"
sdf["sbe"].lat = 46.464
sdf["sbe"].lon = 9.185
sdf["sbe"].elevation = 1641

# Weissfluhjoch
sdf["wfj"].short_name = "wfj"
sdf["wfj"].long_name = "Weissfluhjoch"
sdf["wfj"].dwh_id = "06780"
sdf["wfj"].dwh_name = "WFJ"
sdf["wfj"].lat = 46.833
sdf["wfj"].lon = 9.806
sdf["wfj"].elevation = 2694

# Piz Corvatsch
sdf["cov"].short_name = "cov"
sdf["cov"].long_name = "Piz Corvatsch"
sdf["cov"].dwh_id = "06791"
sdf["cov"].dwh_name = "COV"
sdf["cov"].lat = 46.418
sdf["cov"].lon = 9.821
sdf["cov"].elevation = 3297

# Poschiavo / Robbia
sdf["rob"].short_name = "rob"
sdf["rob"].long_name = "Poschiavo"
sdf["rob"].dwh_id = "06794"
sdf["rob"].dwh_name = "ROB"
sdf["rob"].lat = 46.347
sdf["rob"].lon = 10.063
sdf["rob"].elevation = 1080

# Scuol
sdf["scu"].short_name = "scu"
sdf["scu"].long_name = "Scuol"
sdf["scu"].dwh_id = "06798"
sdf["scu"].dwh_name = "SCU"
sdf["scu"].lat = 46.793
sdf["scu"].lon = 10.283
sdf["scu"].elevation = 1306

# Güttingen
sdf["gut"].short_name = "gut"
sdf["gut"].long_name = "Güttingen"
sdf["gut"].dwh_id = "06621"
sdf["gut"].dwh_name = "GUT"
sdf["gut"].lat = 47.602
sdf["gut"].lon = 9.279
sdf["gut"].elevation = 442

# Wädenswil
sdf["wae"].short_name = "wae"
sdf["wae"].long_name = "Wädenswil"
sdf["wae"].dwh_id = "06673"
sdf["wae"].dwh_name = "WAE"
sdf["wae"].lat = 47.221
sdf["wae"].lon = 8.678
sdf["wae"].elevation = 488

# # Aadorf / Tänikon
sdf["tae"].short_name = "tae"
sdf["tae"].long_name = "Tänikon"
sdf["tae"].dwh_id = "06679"
sdf["tae"].dwh_name = "TAE"
sdf["tae"].lat = 47.48
sdf["tae"].lon = 8.905
sdf["tae"].elevation = 540

# Zürich / Affoltern
sdf["reh"].short_name = "reh"
sdf["reh"].long_name = "Zürich"
sdf["reh"].dwh_id = "06664"
sdf["reh"].dwh_name = "REH"
sdf["reh"].lat = 47.428
sdf["reh"].lon = 8.518
sdf["reh"].elevation = 445

# Locarno / Monti
sdf["otl"].short_name = "otl"
sdf["otl"].long_name = "Locarno"
sdf["otl"].dwh_id = "06760"
sdf["otl"].dwh_name = "OTL"
sdf["otl"].lat = 46.172
sdf["otl"].lon = 8.787
sdf["otl"].elevation = 369

# Beznau
sdf["bez"].short_name = "bez"
sdf["bez"].long_name = "Beznau"
sdf["bez"].dwh_id = "06646"
sdf["bez"].dwh_name = "BEZ"
sdf["bez"].lat = 47.557
sdf["bez"].lon = 8.233
sdf["bez"].elevation = 328

# Cimetta
sdf["cim"].short_name = "cim"
sdf["cim"].long_name = "Cimetta"
sdf["cim"].dwh_id = "06759"
sdf["cim"].dwh_name = "CIM"
sdf["cim"].lat = 46.2
sdf["cim"].lon = 8.792
sdf["cim"].elevation = 1663

# Leibstadt
sdf["lei"].short_name = "lei"
sdf["lei"].long_name = "Leibstadt"
sdf["lei"].dwh_id = "06666"
sdf["lei"].dwh_name = "LEI"
sdf["lei"].lat = 47.597
sdf["lei"].lon = 8.188
sdf["lei"].elevation = 343

# Grimsel Hospiz
sdf["grh"].short_name = "grh"
sdf["grh"].long_name = "Grimsel"
sdf["grh"].dwh_id = "06744"
sdf["grh"].dwh_name = "GRH"
sdf["grh"].lat = 46.572
sdf["grh"].lon = 8.333
sdf["grh"].elevation = 1988

# Acquarossa / Comprovasco
sdf["com"].short_name = "com"
sdf["com"].long_name = "Acquarossa"
sdf["com"].dwh_id = "06756"
sdf["com"].dwh_name = "COM"
sdf["com"].lat = 46.46
sdf["com"].lon = 8.935
sdf["com"].elevation = 577

# Lägern
sdf["lae"].short_name = "lae"
sdf["lae"].long_name = "Lägern"
sdf["lae"].dwh_id = "06669"
sdf["lae"].dwh_name = "LAE"
sdf["lae"].lat = 47.482
sdf["lae"].lon = 8.397
sdf["lae"].elevation = 873

# Hörnli
sdf["hoe"].short_name = "hoe"
sdf["hoe"].long_name = "Hörnli"
sdf["hoe"].dwh_id = "06689"
sdf["hoe"].dwh_name = "HOE"
sdf["hoe"].lat = 47.371
sdf["hoe"].lon = 8.942
sdf["hoe"].elevation = 1134

# Robièi
sdf["roe"].short_name = "roe"
sdf["roe"].long_name = "Robièi"
sdf["roe"].dwh_id = "06751"
sdf["roe"].dwh_name = "ROE"
sdf["roe"].lat = 46.443
sdf["roe"].lon = 8.513
sdf["roe"].elevation = 1904

# Würenlingen / PSI
sdf["psi"].short_name = "psi"
sdf["psi"].long_name = "Würenlingen"
sdf["psi"].dwh_id = "06647"
sdf["psi"].dwh_name = "PSI"
sdf["psi"].lat = 47.536
sdf["psi"].lon = 8.227
sdf["psi"].elevation = 336

# Flühli, LU
sdf["flu"].short_name = "flu"
sdf["flu"].long_name = "Flühli"
sdf["flu"].dwh_id = "06652"
sdf["flu"].dwh_name = "FLU"
sdf["flu"].lat = 46.889
sdf["flu"].lon = 8.02
sdf["flu"].elevation = 942

# Oberriet / Kriessern
sdf["obr"].short_name = "obr"
sdf["obr"].long_name = "Oberriet"
sdf["obr"].dwh_id = "06649"
sdf["obr"].dwh_name = "OBR"
sdf["obr"].lat = 47.377
sdf["obr"].lon = 9.613
sdf["obr"].elevation = 411

# Bergün / Latsch
sdf["lat"].short_name = "lat"
sdf["lat"].long_name = "Bergün"
sdf["lat"].dwh_id = "06642"
sdf["lat"].dwh_name = "LAT"
sdf["lat"].lat = 46.627
sdf["lat"].lon = 9.754
sdf["lat"].elevation = 1410

# Vals
sdf["vls"].short_name = "vls"
sdf["vls"].long_name = "Vals"
sdf["vls"].dwh_id = "06663"
sdf["vls"].dwh_name = "VLS"
sdf["vls"].lat = 46.628
sdf["vls"].lon = 9.189
sdf["vls"].elevation = 1244

# Gersau
sdf["ges"].short_name = "ges"
sdf["ges"].long_name = "Gersau"
sdf["ges"].dwh_id = "06653"
sdf["ges"].dwh_name = "GES"
sdf["ges"].lat = 46.996
sdf["ges"].lon = 8.523
sdf["ges"].elevation = 522

# Lachen / Galgenen
sdf["lac"].short_name = "lac"
sdf["lac"].long_name = "Lachen"
sdf["lac"].dwh_id = "06665"
sdf["lac"].dwh_name = "LAC"
sdf["lac"].lat = 47.179
sdf["lac"].lon = 8.859
sdf["lac"].elevation = 470

# Bivio
sdf["biv"].short_name = "biv"
sdf["biv"].long_name = "Bivio"
sdf["biv"].dwh_id = "06774"
sdf["biv"].dwh_name = "BIV"
sdf["biv"].lat = 46.462
sdf["biv"].lon = 9.669
sdf["biv"].elevation = 1858

# Meiringen
sdf["mer"].short_name = "mer"
sdf["mer"].long_name = "Meiringen"
sdf["mer"].dwh_id = "06637"
sdf["mer"].dwh_name = "MER"
sdf["mer"].lat = 46.732
sdf["mer"].lon = 8.169
sdf["mer"].elevation = 591

# Matro
sdf["mtr"].short_name = "mtr"
sdf["mtr"].long_name = "Matro"
sdf["mtr"].dwh_id = "06754"
sdf["mtr"].dwh_name = "MTR"
sdf["mtr"].lat = 46.41
sdf["mtr"].lon = 8.925
sdf["mtr"].elevation = 2193

# Biasca
sdf["bia"].short_name = "bia"
sdf["bia"].long_name = "Biasca"
sdf["bia"].dwh_id = "9110"
sdf["bia"].dwh_name = "BIA"
sdf["bia"].lat = 46.336
sdf["bia"].lon = 8.978
sdf["bia"].elevation = 280

# Titlis
sdf["tit"].short_name = "tit"
sdf["tit"].long_name = "Titlis"
sdf["tit"].dwh_id = "06740"
sdf["tit"].dwh_name = "TIT"
sdf["tit"].lat = 46.771
sdf["tit"].lon = 8.426
sdf["tit"].elevation = 3096

# Vicosoprano
sdf["vio"].short_name = "vio"
sdf["vio"].long_name = "Vicosoprano"
sdf["vio"].dwh_id = "06788"
sdf["vio"].dwh_name = "VIO"
sdf["vio"].lat = 46.353
sdf["vio"].lon = 9.628
sdf["vio"].elevation = 1091

# Elm
sdf["elm"].short_name = "elm"
sdf["elm"].long_name = "Elm"
sdf["elm"].dwh_id = "06682"
sdf["elm"].dwh_name = "ELM"
sdf["elm"].lat = 46.924
sdf["elm"].lon = 9.175
sdf["elm"].elevation = 960

# Andermatt
sdf["ant"].short_name = "ant"
sdf["ant"].long_name = "Andermatt"
sdf["ant"].dwh_id = "06695"
sdf["ant"].dwh_name = "ANT"
sdf["ant"].lat = 46.631
sdf["ant"].lon = 8.581
sdf["ant"].elevation = 1437

# Sattel, SZ
sdf["sag"].short_name = "sag"
sdf["sag"].long_name = "Sattel"
sdf["sag"].dwh_id = "06662"
sdf["sag"].dwh_name = "SAG"
sdf["sag"].lat = 47.081
sdf["sag"].lon = 8.637
sdf["sag"].elevation = 792

# Ilanz
sdf["ilz"].short_name = "ilz"
sdf["ilz"].long_name = "Ilanz"
sdf["ilz"].dwh_id = "06789"
sdf["ilz"].dwh_name = "ILZ"
sdf["ilz"].lat = 46.775
sdf["ilz"].lon = 9.215
sdf["ilz"].elevation = 700

# Schiers
sdf["srs"].short_name = "srs"
sdf["srs"].long_name = "Schiers"
sdf["srs"].dwh_id = "06790"
sdf["srs"].dwh_name = "SRS"
sdf["srs"].lat = 46.976
sdf["srs"].lon = 9.668
sdf["srs"].elevation = 628

# Vevey / Corseaux
sdf["vev"].short_name = "vev"
sdf["vev"].long_name = "Vevey"
sdf["vev"].dwh_id = "06603"
sdf["vev"].dwh_name = "VEV"
sdf["vev"].lat = 46.471
sdf["vev"].lon = 6.815
sdf["vev"].elevation = 407

# Cham
sdf["chz"].short_name = "chz"
sdf["chz"].long_name = "Cham"
sdf["chz"].dwh_id = "06674"
sdf["chz"].dwh_name = "CHZ"
sdf["chz"].lat = 47.188
sdf["chz"].lon = 8.465
sdf["chz"].elevation = 445

# Binn
sdf["bin"].short_name = "bin"
sdf["bin"].long_name = "Binn"
sdf["bin"].dwh_id = "06721"
sdf["bin"].dwh_name = "BIN"
sdf["bin"].lat = 46.368
sdf["bin"].lon = 8.192
sdf["bin"].elevation = 1481

# Hallau
sdf["hll"].short_name = "hll"
sdf["hll"].long_name = "Hallau"
sdf["hll"].dwh_id = "06624"
sdf["hll"].dwh_name = "HLL"
sdf["hll"].lat = 47.697
sdf["hll"].lon = 8.47
sdf["hll"].elevation = 421

# Mosen
sdf["moa"].short_name = "moa"
sdf["moa"].long_name = "Mosen"
sdf["moa"].dwh_id = "06644"
sdf["moa"].dwh_name = "MOA"
sdf["moa"].lat = 47.244
sdf["moa"].lon = 8.233
sdf["moa"].elevation = 454

# Göschenen
sdf["gos"].short_name = "gos"
sdf["gos"].long_name = "Göschenen"
sdf["gos"].dwh_id = "06668"
sdf["gos"].dwh_name = "GOS"
sdf["gos"].lat = 46.693
sdf["gos"].lon = 8.595
sdf["gos"].elevation = 952

# Cevio
sdf["cev"].short_name = "cev"
sdf["cev"].long_name = "Cevio"
sdf["cev"].dwh_id = "06752"
sdf["cev"].dwh_name = "CEV"
sdf["cev"].lat = 46.32
sdf["cev"].lon = 8.603
sdf["cev"].elevation = 421

# Arosa
sdf["aro"].short_name = "aro"
sdf["aro"].long_name = "Arosa"
sdf["aro"].dwh_id = "06785"
sdf["aro"].dwh_name = "ARO"
sdf["aro"].lat = 46.793
sdf["aro"].lon = 9.679
sdf["aro"].elevation = 1880

# Bischofszell / Sitterdorf
sdf["biz"].short_name = "biz"
sdf["biz"].long_name = "Bischofszell"
sdf["biz"].dwh_id = "06678"
sdf["biz"].dwh_name = "BIZ"
sdf["biz"].lat = 47.509
sdf["biz"].lon = 9.267
sdf["biz"].elevation = 509

# Segl-Maria
sdf["sia"].short_name = "sia"
sdf["sia"].long_name = "Segl-Maria"
sdf["sia"].dwh_id = "06779"
sdf["sia"].dwh_name = "SIA"
sdf["sia"].lat = 46.432
sdf["sia"].lon = 9.762
sdf["sia"].elevation = 1806

# Passo del Bernina
sdf["beh"].short_name = "beh"
sdf["beh"].long_name = "Berninapass"
sdf["beh"].dwh_id = "06797"
sdf["beh"].dwh_name = "BEH"
sdf["beh"].lat = 46.409
sdf["beh"].lon = 10.02
sdf["beh"].elevation = 2267

# Buffalora
sdf["buf"].short_name = "buf"
sdf["buf"].long_name = "Buffalora"
sdf["buf"].dwh_id = "06778"
sdf["buf"].dwh_name = "BUF"
sdf["buf"].lat = 46.648
sdf["buf"].lon = 10.267
sdf["buf"].elevation = 1973

# Crap Masegn
sdf["cma"].short_name = "cma"
sdf["cma"].long_name = "Crap Masegn"
sdf["cma"].dwh_id = "06688"
sdf["cma"].dwh_name = "CMA"
sdf["cma"].lat = 46.842
sdf["cma"].lon = 9.18
sdf["cma"].elevation = 2471

# Monte Generoso
sdf["gen"].short_name = "gen"
sdf["gen"].long_name = "Monte Generoso"
sdf["gen"].dwh_id = "06777"
sdf["gen"].dwh_name = "GEN"
sdf["gen"].lat = 45.928
sdf["gen"].lon = 9.018
sdf["gen"].elevation = 1602

# Oron
sdf["oro"].short_name = "oro"
sdf["oro"].long_name = "Oron"
sdf["oro"].dwh_id = "06708"
sdf["oro"].dwh_name = "ORO"
sdf["oro"].lat = 46.572
sdf["oro"].lon = 6.858
sdf["oro"].elevation = 829


# Schüpfheim
sdf["spf"].short_name = "spf"
sdf["spf"].long_name = "Schüpfheim"
sdf["spf"].dwh_id = "06651"
sdf["spf"].dwh_name = "SPF"
sdf["spf"].lat = 46.947
sdf["spf"].lon = 8.012
sdf["spf"].elevation = 746

# Valbella
sdf["vab"].short_name = "vab"
sdf["vab"].long_name = "Valbella"
sdf["vab"].dwh_id = "06793"
sdf["vab"].dwh_name = "VAB"
sdf["vab"].lat = 46.755
sdf["vab"].lon = 9.554
sdf["vab"].elevation = 1571

# Piz Martegnas
sdf["pma"].short_name = "pma"
sdf["pma"].long_name = "Piz Martegnas"
sdf["pma"].dwh_id = "06795"
sdf["pma"].dwh_name = "PMA"
sdf["pma"].lat = 46.577
sdf["pma"].lon = 9.53
sdf["pma"].elevation = 2670

# Naluns / Schlivera
sdf["nas"].short_name = "nas"
sdf["nas"].long_name = "Naluns"
sdf["nas"].dwh_id = "06799"
sdf["nas"].dwh_name = "NAS"
sdf["nas"].lat = 46.817
sdf["nas"].lon = 10.261
sdf["nas"].elevation = 2382

# Simplon-Dorf
sdf["sim"].short_name = "sim"
sdf["sim"].long_name = "Simplon Dorf"
sdf["sim"].dwh_id = "06654"
sdf["sim"].dwh_name = "SIM"
sdf["sim"].lat = 46.197
sdf["sim"].lon = 8.056
sdf["sim"].elevation = 1467

# Eggishorn
sdf["egh"].short_name = "egh"
sdf["egh"].long_name = "Eggishorn"
sdf["egh"].dwh_id = "06739"
sdf["egh"].dwh_name = "EGH"
sdf["egh"].lat = 46.427
sdf["egh"].lon = 8.093
sdf["egh"].elevation = 2895

# Ebnat-Kappel
sdf["ebk"].short_name = "ebk"
sdf["ebk"].long_name = "Ebnat-Kappel"
sdf["ebk"].dwh_id = "06693"
sdf["ebk"].dwh_name = "EBK"
sdf["ebk"].lat = 47.273
sdf["ebk"].lon = 9.108
sdf["ebk"].elevation = 625

# Sta. Maria, Val Müstair
sdf["smm"].short_name = "smm"
sdf["smm"].long_name = "Sta. Maria"
sdf["smm"].dwh_id = "06796"
sdf["smm"].dwh_name = "SMM"
sdf["smm"].lat = 46.602
sdf["smm"].lon = 10.426
sdf["smm"].elevation = 1388

# Bad Ragaz
sdf["rag"].short_name = "rag"
sdf["rag"].long_name = "Bad Ragaz"
sdf["rag"].dwh_id = "06686"
sdf["rag"].dwh_name = "RAG"
sdf["rag"].lat = 47.017
sdf["rag"].lon = 9.503
sdf["rag"].elevation = 498

# Einsiedeln
sdf["ein"].short_name = "ein"
sdf["ein"].long_name = "Einsiedeln"
sdf["ein"].dwh_id = "06675"
sdf["ein"].dwh_name = "EIN"
sdf["ein"].lat = 47.133
sdf["ein"].lon = 8.757
sdf["ein"].elevation = 912

# Salen-Reutenen
sdf["hai"].short_name = "hai"
sdf["hai"].long_name = "Salen-Reutenen"
sdf["hai"].dwh_id = "06623"
sdf["hai"].dwh_name = "HAI"
sdf["hai"].lat = 47.651
sdf["hai"].lon = 9.024
sdf["hai"].elevation = 720
