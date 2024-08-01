import logging
import torch
from comfy import model_management
from comfy.model_patcher import ModelPatcher

class MemSafeWrapper(ModelPatcher):
    def __init__(self, model:torch.nn.Module, device:torch.device=None, offload_device:torch.device=None, dtype:torch.dtype=None):    
        if dtype is None:
            device = model_management.get_torch_device()
        if offload_device is None:
            offload_device = model_management.intermediate_device()
        if dtype is None:
            dtype = model_management.unet_dtype()
    
        self.model = model.to(device=offload_device, dtype=dtype)
        self.model.eval()
        super().__init__(self.model, device, offload_device)

        overlap_attr = set(dir(super())) & set(dir(self.model)) - set(dir(object))
        if len(overlap_attr) != 0:
            attr_list = ", ".join(sorted(overlap_attr))
            logging.warning(
                f"WARNING[MemSafeWrapper]: The following attributes are present in both "
                f"'{self.__class__.__name__}' and '{self.model.__class__.__name__}':\n"
                f"{attr_list}\n"
                f"Attributes from '{self.model.__class__.__name__}' will be ignored for these."
            )

    def to_gpu(self, func):
        def wrapper(*args, **kwargs):
            if self.current_device == self.offload_device:
               model_management.load_model_gpu(self)
            return func(*args, **kwargs)
        return wrapper

    def __getattr__(self, name:str):
        if hasattr(self.model, name):
            attr = getattr(self.model, name)
            if callable(attr):
                return self.to_gpu(attr)
            else:
                return attr            
        else:
            raise AttributeError(f"{self.__class__.__name__} does not has {name} attribute.")

    def __call__(self, *args, **kwargs):
        return self.model(*args, **kwargs)
