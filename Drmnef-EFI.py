import subprocess
import sys

# تثبيت المتطلبات تلقائياً إذا لم تكن مثبتة
def install_requirements_and_restart():
    try:
        import colorama
    except ImportError:
        print("لم يتم تثبيت المكتبات المطلوبة، سيتم تثبيتها الآن...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("تم التثبيت! يعاد تشغيل السكربت...")
        subprocess.Popen([sys.executable] + sys.argv)
        sys.exit()

install_requirements_and_restart()

import os
import platform
import subprocess
import json
import zipfile
import shutil
import requests
import time
from colorama import init, Fore

init(autoreset=True)

# ==== Animated Banner ====
def print_banner_animated():
    lines = [
        f"{Fore.CYAN}                      ______                            ___",
        f"{Fore.CYAN}                     (______)                          / __)",
        f"{Fore.CYAN}                      _     _ ____ ____  ____  _____ _| |__",
        f"{Fore.CYAN}                     | |   | / ___)    \\|  _ \\| ___ (_   __)",
        f"{Fore.CYAN}                     | |__/ / |   | | | | | | ____| | |",
        f"{Fore.CYAN}                     |_____/|_|   |_|_| |_|_____) |_|",
        ""
    ]
    for line in lines:
        print(line)
        time.sleep(0.1)

    tagline = f"{Fore.GREEN}            | by {Fore.YELLOW}Drmnef v1 الاصدار الاول"
    for i in range(len(tagline) + 1):
        print(f"\r{tagline[:i]}", end="", flush=True)
        time.sleep(0.04)
    print("\n")

# ==== Animated Tasks List ====
def print_tasks_animated():
    tasks = [
        "استخراج مواصفات جهازك وحفظها.",
        "تحميل أحدث نسخة OpenCore من GitHub.",
        "استخراج ملفات EFI.",
        "تحميل الكيستات الأساسية بأحدث إصدار.",
        "تحميل وتحويل ملفات SSDT."
    ]
    for task in tasks:
        for i in range(len(task) + 1):
            print(f"\r{Fore.GREEN}>>> {task[:i]}{'_' if i < len(task) else ' '}", end="", flush=True)
            time.sleep(0.05)
        print()
    print()

# ==== System Info ====
def get_system_info():
    info = {}
    try:
        info["System"] = platform.system()
        info["Machine"] = platform.machine()
        info["Processor"] = platform.processor()

        if info["System"] == "Windows":
            info["CPU"] = subprocess.check_output("wmic cpu get name", shell=True).decode().split('\n')[1].strip()
            info["GPU"] = subprocess.check_output("wmic path win32_VideoController get name", shell=True).decode().split('\n')[1].strip()
        elif info["System"] == "Linux":
            info["CPU"] = subprocess.check_output("lscpu | grep 'Model name'", shell=True).decode().split(':')[1].strip()
            info["GPU"] = subprocess.check_output("lspci | grep VGA", shell=True).decode().strip()
    except Exception as e:
        info["Error"] = str(e)
    return info

def detect_cpu_architecture(info):
    if "amd" in info["Processor"].lower() or "amd" in info.get("CPU", "").lower():
        return "AMD"
    elif "intel" in info["Processor"].lower() or "intel" in info.get("CPU", "").lower():
        return "Intel"
    else:
        return "Unknown"

# ==== Download helper with User-Agent header ====
def download_file(url, dest_path):
    headers = {"User-Agent": "Mozilla/5.0"}
    with requests.get(url, stream=True, allow_redirects=True, headers=headers) as r:
        r.raise_for_status()
        with open(dest_path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

# ==== GitHub API: Latest OpenCore ====
def get_latest_opencore_release_url():
    api_url = "https://api.github.com/repos/acidanthera/OpenCorePkg/releases/latest"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        assets = response.json().get("assets", [])
        for asset in assets:
            if "release" in asset["name"].lower() and asset["name"].endswith(".zip"):
                return asset["browser_download_url"]
    return None

def download_opencore():
    zip_path = "OpenCore.zip"
    if os.path.exists(zip_path):
        print(f"{Fore.GREEN}[✓] ملف OpenCore.zip موجود.")
        return zip_path

    print(f"{Fore.YELLOW}[+] تحميل أحدث نسخة OpenCore ...")
    url = get_latest_opencore_release_url()
    if not url:
        print(f"{Fore.RED}[!] لم يتم العثور على رابط OpenCore.")
        return None

    try:
        download_file(url, zip_path)
        print(f"{Fore.GREEN}[✓] تم تحميل OpenCore.")
        return zip_path
    except Exception as e:
        print(f"{Fore.RED}[!] خطأ في التحميل: {e}")
        return None

def extract_efi_structure(zip_path, output_dir="EFI"):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("OpenCoreTemp")
    source = "OpenCoreTemp/X64/EFI"
    if not os.path.exists(source):
        print(f"{Fore.RED}[!] مجلد EFI غير موجود في الأرشيف.")
        return False
    shutil.copytree(source, output_dir, dirs_exist_ok=True)
    shutil.rmtree("OpenCoreTemp")
    os.remove(zip_path)
    print(f"{Fore.GREEN}[✓] تم إنشاء مجلد EFI.")
    return True

def get_latest_release_download_url(repo_name, keyword):
    api_url = f"https://api.github.com/repos/acidanthera/{repo_name}/releases/latest"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        for asset in response.json().get("assets", []):
            if keyword.lower() in asset["name"].lower() and asset["name"].endswith(".zip"):
                return asset["browser_download_url"]
    return None

def download_kexts_dynamic(kext_list, kexts_dir="EFI/OC/Kexts"):
    os.makedirs(kexts_dir, exist_ok=True)
    for kext in kext_list:
        print(f"{Fore.YELLOW}[+] تحميل {kext}.kext ...")
        url = get_latest_release_download_url(kext, kext)
        if not url:
            print(f"{Fore.RED}[!] لم يتم العثور على رابط {kext}.")
            continue
        zip_path = f"{kext}.zip"
        try:
            download_file(url, zip_path)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(f"{kext}_temp")
            for root, dirs, _ in os.walk(f"{kext}_temp"):
                for d in dirs:
                    if d.endswith(".kext"):
                        shutil.copytree(os.path.join(root, d), os.path.join(kexts_dir, d), dirs_exist_ok=True)
            shutil.rmtree(f"{kext}_temp")
            os.remove(zip_path)
            print(f"{Fore.GREEN}[✓] تم تثبيت {kext}.")
        except Exception as e:
            print(f"{Fore.RED}[!] خطأ: {e}")

def download_ssdt_files(acpi_dir="EFI/OC/ACPI"):
    print(f"{Fore.YELLOW}[+] تحميل ملفات SSDT ...")
    os.makedirs(acpi_dir, exist_ok=True)
    os.makedirs("tools", exist_ok=True)

    ssdt_urls = {
        "SSDT-EC": "https://github.com/dortania/Getting-Started-With-ACPI/raw/master/extra-files/decompiled/SSDT-EC.dsl",
        "SSDT-AWAC": "https://github.com/dortania/Getting-Started-With-ACPI/raw/master/extra-files/decompiled/SSDT-AWAC.dsl",
        "SSDT-PLUG": "https://github.com/dortania/Getting-Started-With-ACPI/raw/master/extra-files/decompiled/SSDT-PLUG.dsl",
        "SSDT-USBX": "https://github.com/dortania/Getting-Started-With-ACPI/raw/master/extra-files/decompiled/SSDT-USBX.dsl"
    }

    is_windows = platform.system().lower().startswith("win")
    iasl_path = "iasl"
    if is_windows:
        iasl_url = "https://github.com/acidanthera/MaciASL/releases/download/1.5/iasl-win.zip"
        zip_path = "tools/iasl-win.zip"
        exe_path = "tools/iasl.exe"
        if not os.path.exists(exe_path):
            print(f"{Fore.YELLOW}[+] تحميل iasl.exe للويندوز ...")
            try:
                download_file(iasl_url, zip_path)
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall("tools")
                os.remove(zip_path)
                print(f"{Fore.GREEN}[✓] تم تحميل iasl.exe.")
            except Exception as e:
                print(f"{Fore.RED}[!] فشل تحميل iasl.exe: {e}")
                return
        iasl_path = exe_path

    for name, url in ssdt_urls.items():
        dsl_path = os.path.join(acpi_dir, f"{name}.dsl")
        with open(dsl_path, "wb") as f:
            f.write(requests.get(url).content)

        try:
            subprocess.run([iasl_path, dsl_path], check=True)
            os.remove(dsl_path)
            print(f"{Fore.GREEN}[✓] {name}.aml تم توليده.")
        except Exception as e:
            print(f"{Fore.RED}[!] فشل تحويل {name}: {e}")

# ==== Signature ====
def print_signature():
    print(f"\n{Fore.GREEN}{'='*50}")
    time.sleep(0.3)
    message1 = f"{Fore.CYAN}وبحمد الله تم تطوير وبرمجة هذا السكربت Drmnef."
    message2 = f"{Fore.MAGENTA}للاستفسار أو وجود ملاحظات يرجى مراسلتي: Dr.mnef@Gmail.Com"
    for i in range(len(message1) + 1):
        print(f"\r{message1[:i]}", end="", flush=True)
        time.sleep(0.05)
    print()
    for i in range(len(message2) + 1):
        print(f"\r{message2[:i]}", end="", flush=True)
        time.sleep(0.05)
    print(f"\n{Fore.GREEN}{'='*50}\n")

# ==== MAIN ====
def main():
    print_banner_animated()
    print_tasks_animated()
    specs = get_system_info()
    with open("system_specs.json", "w") as f:
        json.dump(specs, f, indent=4)
    cpu_type = detect_cpu_architecture(specs)
    print(f"{Fore.CYAN}[i] نوع المعالج: {cpu_type}")

    zip_path = download_opencore()
    if not zip_path:
        print(f"{Fore.RED}[!] فشل تحميل OpenCore.")
        return

    if extract_efi_structure(zip_path):
        download_kexts_dynamic(["Lilu", "WhateverGreen", "VirtualSMC", "AppleALC"])
        download_ssdt_files()
        print(f"{Fore.GREEN}[✓] تم تجهيز مجلد EFI بالكامل.")
        print_signature()
    else:
        print(f"{Fore.RED}[!] فشل في إنشاء مجلد EFI.")

if __name__ == "__main__":
    main()

