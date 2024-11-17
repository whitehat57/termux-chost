import requests
import time
from prettytable import PrettyTable
from colorama import Fore, Style

# Fungsi untuk memformat warna status HTTP
def format_status(http_status):
    if http_status == "200":
        return f"{Fore.GREEN}{http_status}{Style.RESET_ALL}"  # Hijau untuk sukses
    elif http_status == "404" or http_status == "500":
        return f"{Fore.RED}{http_status}{Style.RESET_ALL}"  # Merah untuk error
    elif http_status == "N/A":
        return f"{Fore.YELLOW}{http_status}{Style.RESET_ALL}"  # Kuning untuk tidak tersedia
    return f"{Fore.CYAN}{http_status}{Style.RESET_ALL}"  # Default untuk status lainnya

# Fungsi untuk melakukan pengecekan host menggunakan Check Host API
def check_host_http(target_url):
    # Endpoint API untuk memulai pemeriksaan
    base_url = "https://check-host.net/check-http"
    params = {
        "host": target_url,
        "max_nodes": 20  # Maksimum node (bisa diatur hingga 20)
    }

    try:
        # Memulai pemeriksaan
        response = requests.get(base_url, headers={"Accept": "application/json"}, params=params)
        response.raise_for_status()
        data = response.json()

        # Mengambil request ID dan permanent link
        request_id = data.get("request_id")
        permanent_link = data.get("permanent_link")
        if not request_id or not permanent_link:
            print("Error: Gagal mendapatkan request ID atau permanent link.")
            return

        print(f"\nPermanent Link Hasil: {Fore.BLUE}{permanent_link}{Style.RESET_ALL}")

        # Menunggu beberapa detik agar hasil siap
        print(f"{Fore.YELLOW}Mengumpulkan data dari node, harap tunggu...{Style.RESET_ALL}")
        time.sleep(10)

        # Mendapatkan hasil pemeriksaan
        results_url = f"https://check-host.net/check-result/{request_id}"
        results_response = requests.get(results_url, headers={"Accept": "application/json"})
        results_response.raise_for_status()
        results_data = results_response.json()

        # Menampilkan hasil dalam tabel
        table = PrettyTable()
        table.field_names = ["Kode Negara", "Lokasi Node", "Status HTTP", "IP Target"]

        for node, result_list in results_data.items():
            if result_list and isinstance(result_list, list):
                result = result_list[0]  # Menggunakan hasil pertama untuk kesederhanaan
                country_code = node.split(".")[0]
                location = node
                http_status = result[3] if len(result) > 3 else "N/A"
                target_ip = result[4] if len(result) > 4 else "N/A"
                # Menambahkan hasil ke tabel dengan warna pada HTTP Status
                table.add_row([country_code, location, format_status(http_status), target_ip])

        print(table)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error Tidak Terduga: {e}")

# Fungsi utama
if __name__ == "__main__":
    print(f"{Fore.CYAN}Check Host HTTP Checker{Style.RESET_ALL}")
    target_url = input("Masukkan URL untuk diperiksa (contoh: gabut.com): ").strip()
    if target_url:
        check_host_http(target_url)
    else:
        print(f"{Fore.RED}Error: Harap masukkan URL yang valid.{Style.RESET_ALL}")
