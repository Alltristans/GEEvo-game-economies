import fitz  # PyMuPDF: Digunakan untuk membaca file PDF dan mengekstraksi teks
import re    # Regular Expression: Digunakan untuk pencarian pola teks

def analyze_pdf(filepath, keywords, out_file):
    """
    Fungsi ini membaca sebuah dokumen PDF dan mengekstrak halaman yang relevan
    dengan sistem ekonomi ("economy") berdasarkan Tabel of Content (Daftar Isi)
    atau frekuensi kemunculan term (keyword density). Pada konteks analitik, 
    ini mirip dengan pendekatan Information Retrieval dasar.
    """
    doc = fitz.open(filepath)
    out_file.write(f"\n--- Analyzing {filepath} ---\n")
    
    # Mencari entri "Economy" di tingkat Daftar Isi / Table of Contents (TOC)
    toc = doc.get_toc()
    economy_page = -1
    for level, title, page in toc:
        if "econom" in title.lower():
            economy_page = page
            out_file.write(f"Found Economy section in TOC at page {page}\n")
            break
            
    if economy_page != -1:
        # Jika ditemukan, ambil halamannya dengan batas jendela (windowing) selisih -2 s/d +3 halaman 
        # untuk memastikan seluruh konteks materi (sekuensial naratif) tercakup.
        start = max(0, economy_page - 2)
        end = min(len(doc), economy_page + 3)
        out_file.write(f"Extracting pages {start} to {end} around Economy section\n")
        for i in range(start, end):
            text = doc[i].get_text()
            out_file.write(f"--- PAGE {i+1} ---\n")
            out_file.write(text + "\n")
    else:
        # Jika tidak ditemukan pada daftar isi, gunakan metode pencarian heuristik berdasar frekuensi kata.
        # Algoritma iteratif ini menghitung total kemunculan himpunan kata kunci untuk mendapatkan vektor frekuensi,
        # dan menghasilkan skor densitas kemunculan term dokumen.
        page_scores = []
        for i in range(len(doc)):
            text = doc[i].get_text().lower()
            # Kalkulasi skor penjumlahan sebaran/frekuensi unigram: S_i = \sum_{k \in K} frekuensi(k, teks_halaman)
            score = sum(text.count(kw) for kw in keywords)
            if score > 0:
                page_scores.append((score, i))
                
        # Mengurutkan pasangan (skor, nomor halaman) secara menurun (descending sort)
        page_scores.sort(reverse=True, key=lambda x: x[0])
        out_file.write(f"Top 3 keyword dense pages: {page_scores[:3]}\n")
        
        # Mengekstrak 3 elemen dengan skor tertinggi (Top-k selection dengan k=3)
        for score, i in page_scores[:3]:
            out_file.write(f"\n--- PAGE {i+1} (Score: {score}) ---\n")
            out_file.write(doc[i].get_text()[:2000] + "\n")

if __name__ == "__main__":
    # Himpunan (set) variabel diskrit dari terminologi sistem pertukaran & ekonomi (Himpunan K)
    keywords = ["economy", "crafting", "trade", "shop", "currency", "gold", "resource", "market", "auction"]
    
    # Operasi I/O untuk penulisan file keluaran
    with open("economy_output.txt", "w", encoding="utf-8") as out:
        analyze_pdf("MMORPG_GameDesign_v27.pdf", keywords, out)
        analyze_pdf("VHS-Horror-Game-Design-Document.pdf", keywords, out)
