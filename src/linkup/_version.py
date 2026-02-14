from importlib.metadata import PackageNotFoundError, version

try:
    __version__: str = version("linkup-sdk")
except PackageNotFoundError:  # pragma: no cover
    # Fallback for when package metadata is not available (e.g., PyInstaller builds)
    __version__ = "0.0.0"
