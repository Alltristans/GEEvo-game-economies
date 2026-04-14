import os
import PyPDF2  # Library untuk membaca stream biner file PDF
import glob

# Mengambil semua file yang memiliki ekstensi .pdf di direktori saat ini 
# menggunakan teknik wildcard matching (*.pdf)
pdf_files = glob.glob('*.pdf')

# Membuka/membuat blok penulisan stream file teks untuk hasil
with open('pdf_results.txt', 'w', encoding='utf-8') as out:
    # Melakukan iterasi ke setiap file di list pdf_files
    for file in pdf_files:
        out.write(f"=== {file} ===\n")
        try:
            # Membuka stream bacaan byte (rb = read binary) dari dokumen PDF
            with open(file, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                num_pages = len(reader.pages) # Menghitung skalar panjang daftar halaman (N)
                out.write(f"Total pages: {num_pages}\n")
                
                text = ""
                # Looping ekstraksi untuk maksimal 5 halaman pertama teks pengantar pdf
                # Menggunakan limit min(5, N) untuk mencegah index out of bound error
                for i in range(min(5, num_pages)):
                    page = reader.pages[i]
                    text += page.extract_text() or ""
                    
                # Mengambil teks sampel hingga 1000 karakter, menggunakan syntax array slicing (irisan)
                out.write(text[:1000] + "...\n")
                
                # Daftar kata-kata spesifik terkait aliran sistem ekonomi (Terminologi Game Economy)
                economy_keywords = ['economy', 'resource', 'gold', 'currency', 'crafting', 'shop', 'shop', 'market', 'trade', 'item', 'inventory', 'balance', 'cost', 'drop', 'reward']
                
                # Inisialisasi dictionary {String: Integer} (Map fungsi) bernilai awalan 0 untuk setiap keyword 
                # (bentuk vektor frekuensi spasial awal: v_0 = [0, 0, ..., 0])
                found_keywords = {kw: 0 for kw in economy_keywords}
                
                # Memindai konten string di N halaman per file PDF (limit iterasi hingga maksimal 50 hal)
                for i in range(min(50, num_pages)):
                    page = reader.pages[i]
                    # Menormalisasi format teks menjadi bentuk lowercase agar kebal dari aspek sensitivitas kapital (Case-Insensitive)
                    page_text = (page.extract_text() or "").lower()
                    
                    # Transformasi linier komulatif untuk frekuensi string pada sebuah himpunan variabel diskrit
                    for kw in economy_keywords:
                        found_keywords[kw] += page_text.count(kw)
                        
                # Menulis pemetaan hasil pencarian distribusi frekuensi ke dalam output
                out.write(f"Economy related keywords found: {found_keywords}\n")
                out.write("-" * 50 + "\n")
                
        except Exception as e:
            # Error handling jika pembacaan byte gagal (Misal karena file corrupt)
            out.write(f"Error reading {file}: {e}\n")
