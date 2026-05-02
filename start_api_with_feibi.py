import os
import json
import sys

import genie_tts as genie
import genie_tts.Server as server_module

MODELS_BASE = os.path.join(os.path.dirname(__file__), "CharacterModels", "v2ProPlus")
DEFAULT_LANGUAGE = "Chinese"

if __name__ == "__main__":
    available = [d for d in os.listdir(MODELS_BASE)
                 if os.path.isdir(os.path.join(MODELS_BASE, d))]

    if not available:
        print(f"在 {MODELS_BASE} 下没有找到任何角色文件夹")
        sys.exit(1)

    print("可用角色：")
    for i, name in enumerate(available, 1):
        print(f"  {i}. {name}")

    choice = input("请输入角色名称或序号 (默认: {}): ".format(available[0])).strip()
    if not choice:
        character_name = available[0]
    elif choice.isdigit() and 1 <= int(choice) <= len(available):
        character_name = available[int(choice) - 1]
    elif choice in available:
        character_name = choice
    else:
        print(f"无效选择: {choice}")
        sys.exit(1)

    save_path = os.path.join(MODELS_BASE, character_name)
    model_dir = os.path.join(save_path, "tts_models")
    language = DEFAULT_LANGUAGE

    print(f"正在把模型 [{character_name}] 载入内存...")
    genie.load_character(character_name, model_dir, language)

    with open(os.path.join(save_path, "prompt_wav.json"), "r", encoding="utf-8") as f:
        prompt_wav_dict = json.load(f)

    audio_text = prompt_wav_dict["Normal"]["text"]
    audio_path = os.path.join(save_path, "prompt_wav", prompt_wav_dict["Normal"]["wav"])

    server_module._reference_audios[character_name] = {
        'audio_path': audio_path,
        'audio_text': audio_text,
        'language': language
    }

    print(f"角色 [{character_name}] 加载完成！")
    print("启动 API 服务 (按 Ctrl+C 退出)...")
    server_module.start_server(host="127.0.0.1", port=8000, workers=1)
