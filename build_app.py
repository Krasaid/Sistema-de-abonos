import os
import shutil
import subprocess
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules

NOMBRE_SCRIPT = "main.py"
NOMBRE_APP = "main"

def limpiar_builds():
    for carpeta in ["build", "dist"]:
        if os.path.exists(carpeta):
            shutil.rmtree(carpeta)
            print(f"🧹 Carpeta eliminada: {carpeta}")

def obtener_ruta_plugin():
    try:
        import mysql.connector.plugins
        plugin = Path(mysql.connector.plugins.__file__).parent / "mysql_native_password.py"
        return plugin.as_posix()
    except Exception as e:
        print(f"❌ No se encontró el plugin mysql_native_password: {e}")
        exit(1)

def crear_spec(ruta_plugin):
    ruta_actual = os.getcwd().replace("\\", "/")
    contenido = f"""# -- mode: python ; coding: utf-8 --
import os
from PyInstaller.utils.hooks import collect_submodules

a = Analysis(
    ['{NOMBRE_SCRIPT}'],
    pathex=['{ruta_actual}'],
    binaries=[],
    datas=[('{ruta_plugin}', 'mysql/connector/plugins')],
    hiddenimports={collect_submodules('mysql')},
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='{NOMBRE_APP}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='{NOMBRE_APP}',
)
"""
    with open("main.spec", "w", encoding="utf-8") as f:
        f.write(contenido)
    print("✅ Archivo main.spec creado correctamente.")

def compilar():
    print("🚀 Ejecutando PyInstaller...")
    subprocess.run(["pyinstaller", "main.spec"])
    print("\n✅ Compilación finalizada. El ejecutable está en la carpeta /dist")

if __name__ == "__main__":
    limpiar_builds()
    ruta_plugin = obtener_ruta_plugin()
    crear_spec(ruta_plugin)
    compilar()
