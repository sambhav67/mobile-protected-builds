import os
import sys
import tempfile
import urllib.request
import runpy

# ============================================================
# CONFIG
# ============================================================

BASE_URL = (
    "https://raw.githubusercontent.com/"
    "sambhav67/mobile-protected-builds/main/"
)

# ============================================================
# ENVIRONMENT DETECTION
# ============================================================

def detect_environment():
    version = f"{sys.version_info.major}.{sys.version_info.minor}"

    executable = os.path.abspath(sys.executable).lower()
    prefix = os.path.abspath(sys.prefix).lower()

    # Termux
    if (
        "/com.termux/" in executable
        or "/com.termux/" in prefix
        or "com.termux" in executable
        or "com.termux" in prefix
    ):
        platform_name = "termux"

    # Pydroid
    elif (
        "ru.iiec.pydroid3" in executable
        or "ru.iiec.pydroid3" in prefix
    ):
        platform_name = "pydroid"

    else:
        platform_name = "unknown"

    return platform_name, version


# ============================================================
# SELECT BUILD
# ============================================================

def select_build():
    platform_name, version = detect_environment()

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("          MOBILE PROTECTED LOADER")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"Platform : {platform_name}")
    print(f"Python   : {version}")
    print()

    if platform_name == "pydroid" and version == "3.11":
        return "pydroid_311.py"

    if platform_name == "pydroid" and version == "3.13":
        return "pydroid_313.py"

    if platform_name == "termux" and version == "3.13":
        return "termux_313.py"

    print("❌ Unsupported environment.")
    print()
    print("Supported:")
    print("  Pydroid 3.11")
    print("  Pydroid 3.13")
    print("  Termux 3.13")
    sys.exit(1)


# ============================================================
# DOWNLOAD
# ============================================================

def download_build(filename):
    url = BASE_URL + filename

    cache_dir = os.path.join(
        tempfile.gettempdir(),
        "mobile_protected_build"
    )

    os.makedirs(cache_dir, exist_ok=True)

    destination = os.path.join(cache_dir, filename)

    print(f"[+] Selected : {filename}")
    print("[+] Downloading protected build...")

    try:
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "MobileProtectedLoader/1.0"
            }
        )

        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read()

        if not data:
            raise RuntimeError("Downloaded file is empty.")

        with open(destination, "wb") as f:
            f.write(data)

    except Exception as e:
        print(f"\n❌ Download failed:")
        print(e)
        sys.exit(1)

    print("[+] Download complete.")

    return destination


# ============================================================
# RUN
# ============================================================

def main():
    filename = select_build()
    protected_file = download_build(filename)

    print("[+] Starting protected application...")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    try:
        runpy.run_path(
            protected_file,
            run_name="__main__"
        )

    except KeyboardInterrupt:
        print("\n\nApplication stopped.")

    except SystemExit:
        raise

    except Exception as e:
        print("\n❌ Protected application failed.")
        print(f"Reason: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
