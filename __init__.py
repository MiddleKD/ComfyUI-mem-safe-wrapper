import sys, os
sys.path.append(os.path.dirname(__file__))
from .node import (ResetModelPatcherCalculateWeight,
                   MakeModelMemorySafe)

NODE_CLASS_MAPPINGS = {
    "ResetModelPatcher-safewrapper": ResetModelPatcherCalculateWeight,
    "MakeModelMemorySafe-safewrapper": MakeModelMemorySafe,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "ResetModelPatcher-safewrapper": "Reset model patcher (middlek)",
    "MakeModelMemorySafe-safewrapper": "Memory safe wrap (middlek)",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
