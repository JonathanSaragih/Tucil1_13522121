from typing import List, Tuple, Set
import time 

# Fungsi untuk membaca matriks, sekuens, dan points dari file
def baca_file(filename):
    with open(filename, 'r') as file:
        ukuranbuffer = int(file.readline()) #membaca ukuran buffer
        ukuranmatriks = tuple(map(int, file.readline().split())) #membaca ukuran matriks
        matrix = [list(file.readline().split()) for _ in range(ukuranmatriks[1])]
        jumlahseqs = int(file.readline())
        sekuens = [] #Membuat array kosong untuk diisi sekuensnya
        points = [] #Membuat array kosong untuk reward dari path yang dilewati
        for i in range(jumlahseqs):
            sekuens.append(file.readline().strip().split())
            points.append(int(file.readline()))
    return ukuranbuffer, matrix, sekuens, points #Mereturn jawaban dan data yang dicari

# Fungsi untuk mencari semua kemungkinan path yang memenuhi aturan
def cari_semua_pola(matrix: List[List[str]], step: int) -> List[List[Tuple[str, Tuple[int, int]]]]:
    rows = len(matrix)
    cols = len(matrix[0])
    all_paths = []
    #Menghasilkan semua pola yang ada dengan menggunakan rekursif
    def semua_path(x: int, y: int, path: List[Tuple[str, Tuple[int, int]]], lewat: Set[Tuple[int, int]], langkah: int) -> None: 
        if langkah == 0:
            all_paths.append(path.copy())
            return
        lewat.add((x, y))
        path.append((matrix[y][x], (x, y)))

        # Mencari rute selanjutnya yang ada disebelah sebelahnya
        for dx, dy in [(0, 1), (1, 0)]:
            next_x, next_y = x + dx, y + dy
            if 0 <= next_x < cols and 0 <= next_y < rows and (next_x, next_y) not in lewat:
                semua_path(next_x, next_y, path, lewat, langkah - 1)

        # Kembali mencari
        lewat.remove((x, y))
        path.pop()

    for x in range(cols):
        for y in range(rows):
            semua_path(x, y, [], set(), step)

    return all_paths

# Menghitung reward atau point dari pola yang sudah ditentukan
def hitung_point(matrix, path, sekuens, points):
    total_reward = 0
    buffer_tokens = []
    for token, i in path: #Looping menghitung pointnya
        buffer_tokens.append(token)
        for seq, reward in zip(sekuens, points):
            if all(t in buffer_tokens for t in seq):
                total_reward += reward #Menjumlahkan point sesuai dengan path yang sudah dijalani
                buffer_tokens = [t for t in buffer_tokens if t not in seq]
    return total_reward

# Mencari path paling optimal
def pola_optimal(matrix, ukuranbuffer, sekuens, points): 
    point_maks = float('-inf')
    optimal_path = []

    all_paths = cari_semua_pola(matrix, ukuranbuffer)
    for path in all_paths: #Looping untuk membandingkan
        path_reward = hitung_point(matrix, path, sekuens, points) 
        if path_reward > point_maks: #Membandingkan point dengan point sebelumnya untuk mencari yang maksimal
            point_maks = path_reward
            optimal_path = path

    return point_maks, optimal_path #Mengembalikan point dan pola yang optimal

def tampilan_awal():
    print("* * * * * * * * * * * * * * * * * ")
    print("! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ")
    print("Selamat Datang di Cyberpunk 2077")
    print("! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ")
    print("* * * * * * * * * * * * * * * * * ")
    print("")
    input("CLICK ENTER TO START THE GAME !!!!")

def simpan_jawaban(filename, point_maks, optimal_path):
    with open(filename, 'w') as file:
        file.write(f"Point yang didapat: {point_maks}\n")
        file.write("Jalur yang dipilih: " + ' '.join(token for token, _ in optimal_path) + "\n")
        file.write("Koordinat Jalur yang dipilih:\n")
        for _, (x, y) in optimal_path:
            file.write(f"{x + 1}, {y + 1}\n")

def main():
    tampilan_awal()
    ukuranbuffer, matrix, sekuens, points = baca_file('input.txt')
    
    # Menampilkan teks loading
    print("Sedang menghitung jalur optimal...")
    start_time = time.time()
    for _ in range(5):
        time.sleep(0.00001)
        print(".", end='', flush=True)
    print("\n")
    print("Optimal path telah ditemukan!\n")
    point_maks, optimal_path = pola_optimal(matrix, ukuranbuffer, sekuens, points)
    end_time = time.time()
    waktufinal = end_time - start_time
    print("Point yang didapat :", point_maks)
    print("Jalur yang dipilih:", ' '.join(token for token, _ in optimal_path))
    print("Koordinat Jalur yang dipilih:")
    for _, (x, y) in optimal_path:
        print(f"{x + 1}, {y + 1}")
    print(waktufinal * 1000 ,"ms")

    # Menyimpan jawaban ke dalam file
    simpan_jawaban('jawaban.txt', point_maks, optimal_path)

if __name__ == "__main__":
    main()
