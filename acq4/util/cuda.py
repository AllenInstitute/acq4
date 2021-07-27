import traceback
from functools import lru_cache

from acq4 import getManager
import pyqtgraph as pg

try:
    import cupy
    cupyLibraryAvailable = True
except ImportError:
    cupy = None
    cupyLibraryAvailable = False

try:
    a = cupy.array([1,2,3])
    a = cupy.array([1.0, 2.0, 3.0])
    cupyLibraryWorks = True
except Exception as exc:
    cupyLibraryWorks = False
    cupyLibraryException = traceback.format_exc()


@lru_cache()
def shouldUseCuda():
    if getManager().config.get("cudaImageProcessing", False) is not True:
        print("CUDA acceleration disabled by config key (cudaImageProcessing)")
        return False

    if not cupyLibraryAvailable:
        print("CUDA enabled in config (cudaImageProcessing), but cupy could not be imported.")
        return False

    if not cupyLibraryWorks:
        print("CUDA enabled in config (cudaImageProcessing), but cupy is not working:\n", cupyLibraryException)
        return False

    pg.setConfigOption("useCupy", True)
    True
