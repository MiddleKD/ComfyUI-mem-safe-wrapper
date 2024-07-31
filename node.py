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
                             }}
    RETURN_TYPES = ("MODEL",)
    FUNCTION = "wrap"
    CATEGORY = "safewrapper"

    def wrap(self, model:nn.Module):
        wrapped_model = MemSafeWrapper(model)
        return (wrapped_model, )