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

# باقي السكربت موجود مسبقاً...
print("مثال بسيط - السكربت الكامل محفوظ في مشروعك.")