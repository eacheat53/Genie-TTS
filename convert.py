import sys
import os

sys.path.insert(0, os.path.abspath("src"))  # If needed
try:
    import genie_tts as genie
except ImportError:
    print("Could not import genie_tts. Please ensure it is installed or in PYTHONPATH.")
    sys.exit(1)
genie.convert_to_onnx(
    torch_pth_path=r"ywl-max_e16_s336.pth",
    torch_ckpt_path=r"ywl-max-e30.ckpt",
    output_dir=r"CharacterModels/v2ProPlus/ywl-max/tts_models",
)
