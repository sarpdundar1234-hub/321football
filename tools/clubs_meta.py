# Display names and extra aliases for eligible clubs (Transfermarkt club id -> (display, short, [aliases]))
DISPLAY = {
 # LaLiga
 '621': ('Athletic Club', 'ATH', ['athletic bilbao', 'bilbao']),
 '13': ('Atlético Madrid', 'ATM', ['atletico madrid', 'atleti', 'atletico']),
 '331': ('Osasuna', 'OSA', []), '1244': ('Leganés', 'LEG', []), '940': ('Celta Vigo', 'CEL', ['celta']),
 '2687': ('Cádiz', 'CAD', []), '993': ('Córdoba', 'COR', []), '1108': ('Alavés', 'ALA', ['deportivo alaves']),
 '897': ('Deportivo La Coruña', 'DEP', ['deportivo', 'depor', 'la coruna']), '1531': ('Elche', 'ELC', []),
 '131': ('Barcelona', 'BAR', ['barca', 'barça', 'fcb', 'fc barcelona']), '3709': ('Getafe', 'GET', []),
 '12321': ('Girona', 'GIR', []), '16795': ('Granada', 'GRA', []), '7971': ('Hércules', 'HER', []),
 '3368': ('Levante', 'LEV', []), '1084': ('Málaga', 'MAL', []), '714': ('Espanyol', 'ESP', ['espanyol barcelona']),
 '237': ('Mallorca', 'MLL', []), '630': ('Racing Santander', 'RAC', []), '367': ('Rayo Vallecano', 'RAY', ['rayo']),
 '150': ('Real Betis', 'BET', ['betis']), '418': ('Real Madrid', 'RMA', ['madrid', 'rmcf']), '2497': ('Real Oviedo', 'OVI', ['oviedo']),
 '681': ('Real Sociedad', 'RSO', ['la real', 'sociedad']), '366': ('Real Valladolid', 'VLL', ['valladolid']),
 '142': ('Real Zaragoza', 'ZAR', ['zaragoza']), '1533': ('Eibar', 'EIB', []), '5358': ('Huesca', 'HUE', []),
 '368': ('Sevilla', 'SEV', []), '2448': ('Sporting Gijón', 'SPG', ['gijon']), '3302': ('Almería', 'ALM', []),
 '472': ('Las Palmas', 'LPA', []), '1049': ('Valencia', 'VAL', []), '1050': ('Villarreal', 'VIL', []),
 # Ligue 1
 '1147': ('AC Ajaccio', 'ACA', []), '290': ('Auxerre', 'AUX', []), '162': ('Monaco', 'MON', []),
 '1159': ('Nancy', 'NAN', []), '618': ('Saint-Étienne', 'STE', ['st etienne', 'asse']), '1416': ('Amiens', 'AMI', []),
 '1420': ('Angers', 'ANG', []), '11300': ('Arles-Avignon', 'ARL', ['arles']), '3524': ('Clermont Foot', 'CLE', ['clermont']),
 '2969': ('Dijon', 'DIJ', []), '855': ('Guingamp', 'GUI', []), '1095': ('Troyes', 'TRO', []),
 '40': ('Bordeaux', 'BOR', ['girondins']), '1158': ('Lorient', 'LOR', []), '347': ('Metz', 'MET', []),
 '995': ('Nantes', 'NAT', []), '750': ('Sochaux', 'SOC', []), '415': ('Toulouse', 'TFC', []),
 '3558': ('GFC Ajaccio', 'GFC', ['gazelec ajaccio']), '1082': ('Lille', 'LIL', ['losc']), '738': ('Le Havre', 'HAC', []),
 '969': ('Montpellier', 'MPL', []), '1160': ('Nîmes', 'NIM', []), '417': ('Nice', 'NCE', []),
 '1041': ('Lyon', 'OL', ['olympique lyonnais', 'ol']), '244': ('Marseille', 'OM', ['om', 'olympique de marseille']),
 '10004': ('Paris FC', 'PFC', []), '583': ('Paris Saint-Germain', 'PSG', ['psg', 'paris sg', 'paris s-g', 'paris saint germain']),
 '826': ('Lens', 'RCL', []), '667': ('Strasbourg', 'STR', []), '595': ('Bastia', 'BAS', []), '1162': ('Caen', 'CAE', []),
 '3911': ('Brest', 'BRE', ['brestois']), '1421': ('Reims', 'REI', []), '273': ('Rennes', 'REN', ['stade rennais']),
 '14171': ('Évian TG', 'ETG', ['evian']), '1423': ('Valenciennes', 'VAF', []),
 # Premier League
 '989': ('Bournemouth', 'BOU', []), '11': ('Arsenal', 'ARS', []), '405': ('Aston Villa', 'AVL', ['villa']),
 '337': ('Birmingham City', 'BIR', ['birmingham']), '164': ('Blackburn Rovers', 'BLB', ['blackburn']), '1181': ('Blackpool', 'BPL', []),
 '355': ('Bolton Wanderers', 'BOL', ['bolton']), '1148': ('Brentford', 'BRF', []), '1237': ('Brighton', 'BHA', ['brighton and hove albion', 'brighton hove']),
 '1132': ('Burnley', 'BUR', []), '603': ('Cardiff City', 'CAR', ['cardiff']), '631': ('Chelsea', 'CHE', []),
 '873': ('Crystal Palace', 'CRY', ['palace']), '29': ('Everton', 'EVE', []), '931': ('Fulham', 'FUL', []),
 '1110': ('Huddersfield Town', 'HUD', ['huddersfield']), '3008': ('Hull City', 'HUL', ['hull']), '677': ('Ipswich Town', 'IPS', ['ipswich']),
 '399': ('Leeds United', 'LEE', ['leeds', 'leeds utd']), '1003': ('Leicester City', 'LEI', ['leicester']), '31': ('Liverpool', 'LIV', ['lfc']),
 '1031': ('Luton Town', 'LUT', ['luton']), '281': ('Manchester City', 'MCI', ['man city', 'city', 'mcfc']),
 '985': ('Manchester United', 'MUN', ['man utd', 'man united', 'manchester utd', 'united', 'mufc']),
 '641': ('Middlesbrough', 'MID', ['boro']), '762': ('Newcastle United', 'NEW', ['newcastle', 'newcastle utd']),
 '1123': ('Norwich City', 'NOR', ['norwich']), '703': ('Nottingham Forest', 'NFO', ['forest', 'nottm forest', "nott'ham forest", 'nottham forest']),
 '1039': ('QPR', 'QPR', ['queens park rangers']), '1032': ('Reading', 'REA', []), '350': ('Sheffield United', 'SHU', ['sheffield utd', 'sheff utd']),
 '180': ('Southampton', 'SOU', ['saints']), '512': ('Stoke City', 'STK', ['stoke']), '289': ('Sunderland', 'SUN', []),
 '2288': ('Swansea City', 'SWA', ['swansea']), '148': ('Tottenham Hotspur', 'TOT', ['tottenham', 'spurs']), '1010': ('Watford', 'WAT', []),
 '984': ('West Brom', 'WBA', ['west bromwich albion', 'west bromwich']), '379': ('West Ham United', 'WHU', ['west ham']),
 '1071': ('Wigan Athletic', 'WIG', ['wigan']), '543': ('Wolves', 'WOL', ['wolverhampton', 'wolverhampton wanderers']),
 # Serie A
 '4102': ('Carpi', 'CRP', []), '5': ('AC Milan', 'MIL', ['milan', 'acm']), '2919': ('Monza', 'MNZ', []),
 '430': ('Fiorentina', 'FIO', []), '12': ('Roma', 'ROM', ['as roma']), '800': ('Atalanta', 'ATA', []),
 '4171': ('Benevento', 'BEN', []), '1025': ('Bologna', 'BOL', []), '19': ('Brescia', 'BRS', []), '1390': ('Cagliari', 'CAG', []),
 '1627': ('Catania', 'CTN', []), '1429': ('Cesena', 'CES', []), '862': ('Chievo', 'CHI', ['chievo verona']), '1047': ('Como', 'COM', []),
 '2921': ('Pescara', 'PES', []), '4083': ('Crotone', 'CRO', []), '749': ('Empoli', 'EMP', []), '8970': ('Frosinone', 'FRO', []),
 '252': ('Genoa', 'GEN', []), '276': ('Hellas Verona', 'VER', ['verona']), '46': ('Inter', 'INT', ['inter milan', 'internazionale', 'inter']),
 '506': ('Juventus', 'JUV', ['juve']), '6692': ('Novara', 'NOV', []), '458': ('Palermo', 'PAL', []), '130': ('Parma', 'PAR', []),
 '4172': ('Pisa', 'PIS', []), '2722': ('SPAL', 'SPA', []), '398': ('Lazio', 'LAZ', []), '332': ('Bari', 'BRI', []),
 '6195': ('Napoli', 'NAP', ['ssc napoli']), '1387': ('Siena', 'SIE', []), '3522': ('Spezia', 'SPE', []), '416': ('Torino', 'TOR', []),
 '1038': ('Sampdoria', 'SAM', []), '2239': ('Cremonese', 'CRE', []), '1005': ('Lecce', 'LEC', []), '1210': ('Livorno', 'LIV', []),
 '380': ('Salernitana', 'SAL', []), '6574': ('Sassuolo', 'SAS', []), '410': ('Udinese', 'UDI', []), '607': ('Venezia', 'VEN', []),
 # Bundesliga
 '2036': ('Heidenheim', 'HDH', []), '2': ('Kaiserslautern', 'FCK', []), '3': ('1. FC Köln', 'KOE', ['koln', 'cologne', 'fc koln']),
 '4': ('Nürnberg', 'FCN', ['nuremberg', 'nurnberg', 'nuernberg']), '89': ('Union Berlin', 'FCU', []), '39': ('Mainz 05', 'M05', ['mainz']),
 '10': ('Arminia Bielefeld', 'DSC', ['bielefeld']), '15': ('Bayer Leverkusen', 'B04', ['leverkusen']),
 '27': ('Bayern Munich', 'FCB', ['bayern', 'fc bayern', 'bayern munchen', 'bayern muenchen']), '16': ('Borussia Dortmund', 'BVB', ['dortmund', 'bvb']),
 '18': ('Borussia Mönchengladbach', 'BMG', ['gladbach', "m'gladbach", 'monchengladbach', 'moenchengladbach']),
 '23': ('Eintracht Braunschweig', 'EBS', ['braunschweig']), '24': ('Eintracht Frankfurt', 'SGE', ['frankfurt', 'eintracht']),
 '167': ('Augsburg', 'FCA', []), '4795': ('Ingolstadt', 'FCI', []), '33': ('Schalke 04', 'S04', ['schalke']),
 '35': ('St. Pauli', 'STP', ['st pauli']), '38': ('Fortuna Düsseldorf', 'F95', ['dusseldorf', 'fortuna']), '41': ('Hamburger SV', 'HSV', ['hamburg', 'hsv']),
 '42': ('Hannover 96', 'H96', ['hannover']), '44': ('Hertha BSC', 'BSC', ['hertha', 'hertha berlin']), '269': ('Holstein Kiel', 'KSV', ['kiel']),
 '23826': ('RB Leipzig', 'RBL', ['leipzig']), '60': ('Freiburg', 'SCF', []), '127': ('Paderborn', 'SCP', []),
 '105': ('Darmstadt 98', 'D98', ['darmstadt']), '86': ('Werder Bremen', 'SVW', ['bremen', 'werder']),
 '65': ('Greuther Fürth', 'SGF', ['furth', 'greuther furth']), '533': ('Hoffenheim', 'TSG', []), '79': ('VfB Stuttgart', 'VFB', ['stuttgart']),
 '80': ('VfL Bochum', 'BOC', ['bochum']), '82': ('VfL Wolfsburg', 'WOB', ['wolfsburg']),
 # Liga Portugal
 '2990': ('Académica', 'ACA', ['academica coimbra']), '4814': ('Naval', 'NAV', []), '110302': ('AVS', 'AVS', ['avs futebol']),
 '2457': ('B-SAD', 'BSD', ['belenenses sad']), '2503': ('Boavista', 'BOA', []), '3349': ('Feirense', 'FEI', []),
 '982': ('Nacional', 'NAC', []), '2423': ('Santa Clara', 'SCL', []), '7179': ('Tondela', 'TON', []),
 '2431': ('Estrela da Amadora', 'EST', ['estrela amadora']), '68608': ('Belenenses', 'BEL', ['os belenenses']),
 '976': ('União da Madeira', 'UMA', ['uniao madeira']), '1301': ('Marítimo', 'MAR', []), '3268': ('Casa Pia', 'CPA', []),
 '3336': ('Desportivo das Aves', 'AVE', ['aves', 'desportivo aves']), '2521': ('Alverca', 'ALV', []), '8024': ('Arouca', 'ARO', []),
 '3329': ('Famalicão', 'FAM', []), '2995': ('Paços de Ferreira', 'PFE', ['pacos ferreira']), '3327': ('Penafiel', 'PEN', []),
 '720': ('Porto', 'FCP', ['fc porto']), '6912': ('Vizela', 'VIZ', []), '3325': ('Chaves', 'CHA', []), '1465': ('Estoril', 'EST', ['estoril praia']),
 '2424': ('Gil Vicente', 'GIL', []), '979': ('Moreirense', 'MOR', []), '7378': ('Portimonense', 'POR', []), '2425': ('Rio Ave', 'RAV', []),
 '1436': ('Beira-Mar', 'BMA', []), '1075': ('Braga', 'SCB', ['sporting braga', 'sc braga']), '4294': ('Farense', 'FAR', []),
 '4750': ('Olhanense', 'OLH', []), '294': ('Benfica', 'SLB', ['sl benfica']), '336': ('Sporting CP', 'SCP', ['sporting', 'sporting lisbon', 'sporting lisboa']),
 '2639': ('União de Leiria', 'LEI', ['uniao leiria', 'leiria']), '2420': ('Vitória SC', 'VSC', ['vitoria guimaraes', 'guimaraes']),
 '1085': ('Vitória Setúbal', 'VFC', ['vitoria setubal', 'setubal']),
 # Süper Lig
 '3840': ('Adana Demirspor', 'ADS', []), '6': ('Adanaspor', 'ADA', []), '19771': ('Akhisarspor', 'AKH', ['akhisar']),
 '11282': ('Alanyaspor', 'ALN', []), '2375': ('Altay', 'ALT', []), '589': ('Antalyaspor', 'ANT', []),
 '20698': ('Balıkesirspor', 'BAL', []), '6890': ('Başakşehir', 'IBFK', ['istanbul basaksehir', 'basaksehir']),
 '114': ('Beşiktaş', 'BJK', ['besiktas', 'bjk']), '44006': ('Bodrum FK', 'BOD', ['bodrumspor']), '2750': ('Bucaspor', 'BUC', ['buca']),
 '20': ('Bursaspor', 'BUR', []), '126': ('Çaykur Rizespor', 'RIZ', ['rizespor']), '833': ('Denizlispor', 'DEN', []),
 '2292': ('Elazığspor', 'ELZ', []), '39722': ('Erzurumspor', 'ERZ', ['bb erzurumspor']), '825': ('Eskişehirspor', 'ESK', []),
 '7160': ('Eyüpspor', 'EYP', []), '6646': ('Fatih Karagümrük', 'FKG', ['karagumruk']), '36': ('Fenerbahçe', 'FB', ['fenerbahce', 'fener', 'fb']),
 '141': ('Galatasaray', 'GS', ['gala', 'gs', 'cimbom']), '2832': ('Gaziantep FK', 'GFK', ['gaziantep']), '524': ('Gaziantepspor', 'GZS', []),
 '820': ('Gençlerbirliği', 'GNC', ['genclerbirligi']), '11688': ('Giresunspor', 'GIR', []), '1467': ('Göztepe', 'GOZ', []),
 '7775': ('Hatayspor', 'HAT', []), '924': ('İstanbulspor', 'IST', []), '1506': ('Karabükspor', 'KBK', ['karabukspor']),
 '10484': ('Kasımpaşa', 'KAS', ['kasimpasa']), '6894': ('Kayseri Erciyesspor', 'ERC', ['erciyesspor']), '3205': ('Kayserispor', 'KAY', []),
 '120': ('Kocaelispor', 'KOC', []), '2293': ('Konyaspor', 'KON', []), '868': ('Ankaragücü', 'ANK', ['ankaragucu', 'mke ankaragucu']),
 '1267': ('Manisaspor', 'MAN', []), '3216': ('Mersin İdmanyurdu', 'MER', ['mersin idmanyurdu', 'mersin']), '2323': ('Orduspor', 'ORD', []),
 '3209': ('Pendikspor', 'PEN', []), '152': ('Samsunspor', 'SAM', []), '2944': ('Ankaraspor', 'ANS', ['osmanlispor']),
 '2381': ('Sivasspor', 'SIV', []), '449': ('Trabzonspor', 'TS', ['trabzon', 'ts']), '19789': ('Yeni Malatyaspor', 'YMS', ['malatyaspor']),
 '24245': ('Ümraniyespor', 'UMR', []),
}
LEAGUE = {'GB1': 'Premier League', 'ES1': 'LaLiga', 'IT1': 'Serie A', 'L1': 'Bundesliga', 'FR1': 'Ligue 1', 'TR1': 'Süper Lig', 'PO1': 'Liga Portugal'}
# Clubs a bot/practice opponent likes to pick (household names)
POPULAR = ['131','418','13','368','1049','1050','583','244','1041','162','11','631','31','281','985','148','762','379','29','405',
 '5','46','506','12','398','6195','430','800','27','16','15','82','86','33','294','720','336','1075','141','36','114','449']
# Source-name variants seen in the raw dumps that don't auto-match (not shown to users)
EXTRA = {
 '24': ['eint frankfurt', 'e frankfurt'], '630': ['racing sant'], '141': ['galatasaray a s'], '15': ['bay leverkusen'],
 '40': ['g bordeaux'], '667': ['r strasbourg'], '897': ['dep la coruna'], '16': ['bor dortmund'], '23': ['e braunschweig'],
 '6894': ['k erciyesspor'], '38': ['f dusseldorf'], '10': ['arm bielefeld'], '3216': ['mersin ty', 'mersin iy'],
 '3558': ['gfco ajaccio', 'gazelec football club olympique ajaccio'], '3524': ['clermont fa', 'clermont foot auvergne 63', 'clermont foot auvergne'],
 '3911': ['stade brest 29'], '1095': ['es troyes ac', 'association troyes aube champagne'], '2503': ['boavista porto fc'],
 '39722': ['buyuksehir belediye erzurumspor'], '2944': ['bb ankaraspor'], '2919': ['ac monza brianza', 'ssd monza 1912'],
 '1387': ['robur siena', 'acr siena 1904'], '1627': ['catania ssd'], '458': ['ssd palermo'], '3522': ['asd spezia calcio 2008'],
 '14171': ['fc evian thonon gaillard', 'thonon evian savoie fc'], '607': ['unione venezia', 'fbc unione venezia'],
 '2431': ['clube futebol estrela da amadora'], '2832': ['gaziantep bb'], '4814': ['naval 1 de maio'], '1429': ['rc cesena'],
}

# Original "basic crest" styling: club colours + a generic kit pattern. Not the clubs' real crests.
# id: primary, secondary, pattern  (patterns: solid halves stripes hoops band sash checks)
_KIT = """
621 CB3524 FFFFFF stripes|13 CB3524 FFFFFF stripes|331 D91A21 0A346F solid|1244 1D5BA4 FFFFFF stripes|940 8AC3EE FFFFFF solid
2687 FCE100 0045A7 solid|993 00804A FFFFFF stripes|1108 0761AF FFFFFF stripes|897 1A4FA0 FFFFFF stripes|1531 FFFFFF 05642C band
131 A50044 004D98 stripes|3709 005999 FFFFFF solid|12321 DA291C FFFFFF stripes|16795 C8102E FFFFFF hoops|7971 0055A4 FFFFFF stripes
3368 B4053F 004A9F stripes|1084 4DA3E0 FFFFFF stripes|714 007FC8 FFFFFF stripes|237 E20613 000000 solid|630 FFFFFF 008D3F band
367 FFFFFF E53027 sash|150 00954C FFFFFF stripes|418 FFFFFF FEBE10 solid|2497 0B4EA2 FFFFFF solid|681 0067B1 FFFFFF stripes
366 921B88 FFFFFF stripes|142 FFFFFF 0A3A87 band|1533 003DA5 A6192E stripes|5358 A6192E 003DA5 stripes|368 FFFFFF D71A28 band
2448 E2001A FFFFFF stripes|3302 EE1119 FFFFFF stripes|472 FFE400 0055A5 solid|1049 FFFFFF 1A1A1A band|1050 FFE114 005187 solid
1147 FFFFFF D2001F band|290 FFFFFF 0A3D8F band|162 E7192B FFFFFF sash|1159 E30613 FFFFFF solid|618 00843D FFFFFF solid
1416 FFFFFF 1A1A1A band|1420 1A1A1A FFFFFF stripes|11300 00A1DE 1B3C8C solid|3524 C8102E 002F6C halves|2969 C8102E FFFFFF solid
855 C8102E 1A1A1A halves|1095 0062AD FFFFFF solid|40 00205B FFFFFF band|1158 F58025 1A1A1A solid|347 7A0F2D FFFFFF solid
995 FFE500 009540 solid|750 FFD200 003C82 solid|415 5E2B7E FFFFFF solid|3558 E30613 0066B3 halves|1082 E01E13 001F4D solid
738 79B8E5 1A2A57 halves|969 002C5F F27E22 solid|1160 E2001A FFFFFF solid|417 E30613 1A1A1A stripes|1041 FFFFFF 1B3E91 band
244 FFFFFF 2FAEE0 band|10004 0E2B5C 79BDE8 solid|583 004170 DA291C band|826 FFDD00 E30613 halves|667 009FE3 FFFFFF solid
595 0055A4 FFFFFF solid|1162 1E3B8B E2001A stripes|3911 E30613 FFFFFF solid|1421 E2001A FFFFFF solid|273 E13327 1A1A1A halves
14171 E4007C FFFFFF solid|1423 E3001B FFFFFF solid
989 DA291C 1A1A1A stripes|11 EF0107 FFFFFF solid|405 670E36 95BFE5 solid|337 1C3C8F FFFFFF solid|164 009EE0 FFFFFF halves
1181 F68712 FFFFFF solid|355 FFFFFF 263C7E band|1148 E30613 FFFFFF stripes|1237 0057B8 FFFFFF stripes|1132 6C1D45 99D6EA solid
603 0070B5 FFFFFF solid|631 034694 FFFFFF solid|873 1B458F C4122E stripes|29 003399 FFFFFF solid|931 FFFFFF 1A1A1A band
1110 0E63AD FFFFFF stripes|3008 F5A12D 1A1A1A stripes|677 3A64A3 FFFFFF solid|399 FFFFFF 1D428A band|1003 003090 FDBE11 solid
31 C8102E F6EB61 solid|1031 F78F1E 002D62 solid|281 6CABDD FFFFFF solid|985 DA291C 1A1A1A solid|641 E11B22 FFFFFF band
762 241F20 FFFFFF stripes|1123 FFF200 00A650 solid|703 DD0000 FFFFFF solid|1039 1D5BA4 FFFFFF hoops|1032 004494 FFFFFF hoops
350 EE2737 FFFFFF stripes|180 D71920 FFFFFF stripes|512 E03A3E FFFFFF stripes|289 EB172B FFFFFF stripes|2288 FFFFFF 121212 solid
148 FFFFFF 132257 band|1010 FBEE23 ED2127 solid|984 122F67 FFFFFF stripes|379 7A263A 1BB1E7 solid|1071 1D59AF FFFFFF stripes
543 FDB913 231F20 solid
4102 D2001F FFFFFF solid|5 FB090B 1A1A1A stripes|2919 E2001A FFFFFF solid|430 592C82 FFFFFF solid|12 8E1F2F F0BC42 solid
800 1E71B8 1A1A1A stripes|4171 FFDD00 E2001A stripes|1025 A21C26 1A2F48 halves|19 0055A4 FFFFFF band|1390 A6192E 002350 halves
1627 E30613 00539F stripes|1429 FFFFFF 1A1A1A solid|862 FFE100 0A2C6E solid|1047 1F5AA6 FFFFFF solid|2921 FFFFFF 4FA3DB stripes
4083 E30613 003399 stripes|749 0057B8 FFFFFF solid|8970 FFDD00 0047AB solid|252 A91E2C 002B5C halves|276 FFDD00 002F6C solid
46 0068A8 1A1A1A stripes|506 1A1A1A FFFFFF stripes|6692 0098DA FFFFFF solid|458 F5A3C7 1A1A1A solid|130 FFDD00 1B3D8F solid
4172 1A1A1A 0066B3 stripes|2722 7DC0E8 FFFFFF stripes|398 87D8F7 FFFFFF solid|332 E30613 FFFFFF solid|6195 12A0D7 FFFFFF solid
1387 1A1A1A FFFFFF stripes|3522 FFFFFF 1A1A1A band|416 8A1E03 FFFFFF solid|1038 1B5497 FFFFFF band|2239 E30613 9A9A9A stripes
1005 FFDD00 E30613 stripes|1210 7B1E3A FFFFFF solid|380 7B1E2C FFFFFF solid|6574 00A752 1A1A1A stripes|410 1A1A1A FFFFFF stripes
607 1A1A1A F37021 band
2036 E2001A 003B79 solid|2 E2001A FFFFFF solid|3 FFFFFF ED1C24 band|4 AA1124 1A1A1A solid|89 EB1923 FFFFFF solid
39 C3141E FFFFFF solid|10 004E95 1A1A1A solid|15 E32221 1A1A1A solid|27 DC052D FFFFFF solid|16 FDE100 1A1A1A solid
18 FFFFFF 00A650 band|23 FFD100 004A99 solid|24 1A1A1A E1000F solid|167 BA3733 46714D solid|4795 1A1A1A C8102E solid
33 004D9D FFFFFF solid|35 5C3317 FFFFFF solid|38 E30613 FFFFFF solid|41 FFFFFF 0A3F86 band|42 C3001A 1A1A1A solid
44 005CA9 FFFFFF stripes|269 0055A4 E30613 solid|23826 FFFFFF DD0741 band|60 E30613 1A1A1A solid|127 005CA9 1A1A1A solid
105 004E9E FFFFFF solid|86 1D9053 FFFFFF solid|65 009639 FFFFFF solid|533 1C63B7 FFFFFF solid|79 FFFFFF E32219 band
80 005CA9 FFFFFF solid|82 65B32E FFFFFF solid
2990 1A1A1A FFFFFF solid|4814 007A33 FFFFFF stripes|110302 D2001F 1A1A1A solid|2457 1E5AA8 FFFFFF solid|2503 1A1A1A FFFFFF checks
3349 0055A4 FFFFFF solid|982 1A1A1A FFFFFF stripes|2423 D2001F FFFFFF solid|7179 00843D FFD200 stripes|2431 D2001F 00843D stripes
68608 1E5AA8 FFFFFF solid|976 FFDD00 004A99 solid|1301 E30613 00843D stripes|3268 1A1A1A FFFFFF solid|3336 E30613 FFFFFF solid
2521 C8102E 1E3B8B solid|8024 FFD200 003A80 solid|3329 0055A4 FFFFFF solid|2995 F5A800 003A70 solid|3327 D2001F 1A1A1A solid
720 00428C FFFFFF stripes|6912 5EB6E4 FFFFFF solid|3325 00519E D2001F stripes|1465 FFDD00 0055A4 solid|2424 E2001A 0E3A84 solid
979 00843D FFFFFF solid|7378 1A1A1A FFFFFF stripes|2425 00843D FFFFFF stripes|1436 1A1A1A FFD200 stripes|1075 E2001A FFFFFF solid
4294 1A1A1A FFFFFF solid|4750 D2001F 1A1A1A stripes|294 E83030 FFFFFF solid|336 008057 FFFFFF hoops|2639 1A1A1A FFFFFF solid
2420 FFFFFF 1A1A1A band|1085 00843D FFFFFF stripes
3840 1E3B8B 6EC1E4 stripes|6 F47920 FFFFFF solid|19771 00843D 1A1A1A solid|11282 F7941D 00843D solid|2375 1A1A1A FFFFFF stripes
589 E30613 FFFFFF solid|20698 E30613 1A1A1A solid|6890 F26522 1D2F5E solid|114 1A1A1A FFFFFF stripes|44006 00843D FFFFFF solid
2750 1D2F5E FFD200 solid|20 009639 FFFFFF stripes|126 00A650 0055A4 halves|833 00843D 1A1A1A stripes|2292 7A1E3A FFFFFF solid
39722 1D2F5E FFFFFF solid|825 E30613 1A1A1A stripes|7160 5E2B7E FFD200 solid|6646 E30613 1A1A1A stripes|36 FFED00 002B5C stripes
141 FDB912 A90432 halves|2832 E30613 1A1A1A solid|524 C8102E 1A1A1A stripes|820 E30613 1A1A1A halves|11688 009639 FFFFFF solid
1467 FFD200 E30613 stripes|7775 7A1E3A FFFFFF solid|924 FFD200 1A1A1A stripes|1506 E30613 003A80 solid|10484 1D2F5E FFFFFF solid
6894 E30613 FFD200 solid|3205 FFD200 E30613 stripes|120 00843D 1A1A1A stripes|2293 00843D FFFFFF band|868 FFD200 1D2F5E solid
1267 1A1A1A FFFFFF solid|3216 E30613 0055A4 solid|2323 5E2B7E FFFFFF solid|3209 E30613 FFFFFF solid|152 E30613 FFFFFF band
2944 5E2B7E FFFFFF solid|2381 E30613 FFFFFF stripes|449 7A1E3A 4FA3DB stripes|19789 FFD200 1A1A1A solid|24245 E30613 1D2F5E solid
"""
KIT = {}
for _item in _KIT.replace('\n', '|').split('|'):
    if _item.strip():
        _cid, _p, _s, _pat = _item.split()
        KIT[_cid] = (_p, _s, _pat)

# League order in the picker, with country flags.
LEAGUE_META = [
    ('Premier League', 'England', '🏴\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007F'),
    ('LaLiga', 'Spain', '🇪🇸'),
    ('Serie A', 'Italy', '🇮🇹'),
    ('Bundesliga', 'Germany', '🇩🇪'),
    ('Ligue 1', 'France', '🇫🇷'),
    ('Süper Lig', 'Türkiye', '🇹🇷'),
    ('Liga Portugal', 'Portugal', '🇵🇹'),
]

# Eligible clubs: every top-5-league club since 2010/11, plus only these from Türkiye and Portugal.
BIG5 = ['GB1', 'ES1', 'IT1', 'L1', 'FR1']
EXTRA_CLUBS = ['141', '114', '36', '449', '294', '720', '336']  # GS, BJK, FB, TS, Benfica, Porto, Sporting CP
