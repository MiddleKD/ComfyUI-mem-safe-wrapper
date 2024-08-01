import torch
from torch import nn
from comfy.model_patcher import ModelPatcher
from .wrapper import MemSafeWrapper

# ModelPatcher의 calculate_weight 메서드를 초기화하는 클래스
class ResetModelPatcherCalculateWeight:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"model":("MODEL", ),
                             }}
    RETURN_TYPES = ("MODEL",)
    FUNCTION = "reset_moodelpatcher_weight"
    CATEGORY = "safewrapper"

    def reset_moodelpatcher_weight(self, model:ModelPatcher):
        # 원래의 calculate_weight 메서드로 복원
        if hasattr(model, "original_calculate_weight"):
            model.calculate_weight = ModelPatcher.original_calculate_weight
            ModelPatcher.calculate_weight = ModelPatcher.original_calculate_weight
        return (model, )

# comfyui에서 지원하는, 메모리 추적이 가능하게 함, MemSafeWrapper로 감싸기
class MakeModelMemorySafe:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"model":("MODEL", ),
                             "dtype":(["auto", "fp32", "fp16", "bf16"], "auto")}}
    RETURN_TYPES = ("MODEL",)
    FUNCTION = "wrap"
    CATEGORY = "safewrapper"

    def wrap(self, model:nn.Module, dtype):
        if dtype == "fp32":
            dtype = torch.float32
        elif dtype == "fp16":
            dtype = torch.float16
        elif dtype == "bf16":
            dtype = torch.bfloat16
        else:
            dtype = None
        wrapped_model = MemSafeWrapper(model, dtype=dtype)
        return (wrapped_model, )

# Dummy model for test
class SimpleDummyModel:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {}}
    RETURN_TYPES = ("MODEL",)
    FUNCTION = "load"
    CATEGORY = "safewrapper"

    def load(self):
        class DummyModel(nn.Module):
            def __init__(self):
                super().__init__()
                self.layer = nn.Sequential(nn.Conv2d(3,3,3,1,1))
            def forward(self, x):
                return self.layer(x)
        model = DummyModel()
        return (model, )

# Dummy run for test
class SimpleDummyRun:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"model":("MODEL",)}}
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "run"
    CATEGORY = "safewrapper"

    def run(self, model):
        model_param = next(model.parameters())
        x = torch.randn((1,3,256,256), device=model_param.device, dtype=model_param.dtype)
        output = model(x).permute(0,2,3,1)
        return (output, )