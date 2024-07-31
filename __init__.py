import sys, os
sys.path.append(os.path.dirname(__file__))
from .node import (ResetModelPatcherCalculateWeight,
                   MakeModelMemorySafe,
                   SimpleDummyModel,
                   SimpleDummyRun)

NODE_CLASS_MAPPINGS = {
    "ResetModelPatcher-safewrapper": ResetModelPatcherCalculateWeight,
    "MakeModelMemorySafe-safewrapper": MakeModelMemorySafe,
    "SimpleDummyModel-safewrapper": SimpleDummyModel,
    "SimpleDummyRun-safewrapper": SimpleDummyRun,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "ResetModelPatcher-safewrapper": "Reset model patcher (middlek)",
    "MakeModelMemorySafe-safewrapper": "Memory safe wrap (middlek)",
    "SimpleDummyModel-safewrapper": "Simple dummy model (middlek)",
    "SimpleDummyRun-safewrapper": "Simpler dummy run (middlek)",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
