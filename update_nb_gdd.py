"""
Script untuk memperbarui sel gdd_conf_extractor di demo_agent.ipynb
agar memanggil extract_conf_from_gdd dari modul geevo.gdd_extractor
(bukan mendefinisikan fungsi inline di dalam notebook).
"""
import json

nb_path = 'demo_agent.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Konten baru untuk sel GDD extractor:
# Hanya import + konfigurasi + pemanggilan fungsi dari modul.
new_source = [
    'import os\n',
    'from geevo.gdd_extractor import extract_conf_from_gdd\n',
    '\n',
    '# =====================================================================\n',
    '# Konfigurasi: pilih mode dan file GDD\n',
    '# =====================================================================\n',
    '\n',
    '# Set True untuk menggunakan konfigurasi dari GDD,\n',
    '# Set False untuk menggunakan konfigurasi manual/random di atas.\n',
    'USE_GDD_CONF = True\n',
    '\n',
    '# Path ke file GDD (relatif dari direktori notebook ini)\n',
    '# Ganti ke salah satu file berikut sesuai kebutuhan:\n',
    "#   'Gdd/MMORPG_GameDesign_v27.pdf'\n",
    "#   'Gdd/VHS-Horror-Game-Design-Document.pdf'\n",
    "#   'Gdd/Battle For Treasure.pdf'\n",
    "#   'Gdd/Pierre_GDD.pdf'\n",
    "gdd_path = 'Gdd/MMORPG_GameDesign_v27.pdf'\n",
    '\n',
    '# --- Tampilkan daftar file PDF yang tersedia di folder Gdd/ ---\n',
    "gdd_dir = 'Gdd'\n",
    'if os.path.isdir(gdd_dir):\n',
    '    pdf_files = sorted([f for f in os.listdir(gdd_dir) if f.lower().endswith(".pdf")])\n',
    "    print('File GDD PDF yang tersedia di folder Gdd/:')\n",
    '    for pf in pdf_files:\n',
    "        is_selected = (gdd_dir + '/' + pf == gdd_path) or (gdd_dir + os.sep + pf == gdd_path)\n",
    "        marker = ' <-- (dipilih)' if is_selected else ''\n",
    "        print(f'  - {gdd_dir}/{pf}{marker}')\n",
    '    print()\n',
    'else:\n',
    "    print(f'PERINGATAN: Folder {gdd_dir!r} tidak ditemukan!')\n",
    '\n',
    '# --- Ekstraksi atau gunakan konfigurasi manual ---\n',
    'if USE_GDD_CONF:\n',
    "    print(f'[GDD MODE] Mengekstrak rasio node ekonomi dari: {gdd_path}')\n",
    '    if os.path.exists(gdd_path):\n',
    '        gdd_conf = extract_conf_from_gdd(gdd_path)\n',
    "        print(f'\\nDistribusi struktur nodes dari GDD ({gdd_path}):')\n",
    '        for node_type, node_count in gdd_conf.items():\n',
    "            print(f'  {node_type.__name__:>12s} : {node_count}')\n",
    '        conf = gdd_conf\n',
    "        print('\\n[*] SUKSES: Variabel `conf` disetel menggunakan metadata GDD.')\n",
    '    else:\n',
    "        print(f'[!] File tidak ditemukan: {gdd_path}')\n",
    "        print('[!] Menggunakan konfigurasi manual dari sel sebelumnya.')\n",
    'else:\n',
    "    print('[MANUAL MODE] USE_GDD_CONF = False.')\n",
    "    print('Menggunakan konfigurasi manual/random dari sel sebelumnya.')\n",
    '\n',
    "print(f'\\nKonfigurasi `conf` yang akan digunakan Generator:')\n",
    'for node_type, node_count in conf.items():\n',
    "    print(f'  {node_type.__name__:>12s} : {node_count}')\n",
]

# Temukan sel dengan id 'gdd_conf_extractor' dan ganti source-nya
found = False
for cell in nb['cells']:
    if cell.get('id') == 'gdd_conf_extractor':
        cell['source'] = new_source
        cell['execution_count'] = None
        cell['outputs'] = []
        found = True
        print('Sel gdd_conf_extractor ditemukan dan diperbarui.')
        break

if not found:
    print('ERROR: Sel gdd_conf_extractor tidak ditemukan di notebook!')

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print('Notebook berhasil disimpan!')
