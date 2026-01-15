from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("linkup-sdk")
except PackageNotFoundError:
    # Fallback for when package metadata is not available (e.g., PyInstaller builds)
    __version__ = "0.0.0"
