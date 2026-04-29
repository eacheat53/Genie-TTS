import os
import json
import sys

import genie_tts as genie
from genie_tts.PredefinedCharacter import download_chara, CHARA_LANG
import genie_tts.Server as server_module

if __name__ == "__main__":
    print("🚀 准备加载角色 feibi...")
    character_name = "feibi"
    
    # 1. 下载并获取路径
    save_path = download_chara(character_name)
    model_dir = os.path.join(save_path, 'tts_models')
    language = CHARA_LANG[character_name]

    # 2. 直接调用底层的加载方法
    print("⏳ 正在把模型载入内存...")
    genie.load_character(character_name, model_dir, language)

    # 3. 读取参考音频的配置
    with open(os.path.join(save_path, "prompt_wav.json"), "r", encoding="utf-8") as f:
        prompt_wav_dict = json.load(f)
    
    audio_text = prompt_wav_dict["Normal"]["text"]
    audio_path = os.path.join(save_path, "prompt_wav", prompt_wav_dict["Normal"]["wav"])
    
    # 4. 🔥关键点：直接把配置注入到 Server 模块的全局字典里
    server_module._reference_audios[character_name] = {
        'audio_path': audio_path,
        'audio_text': audio_text,
        'language': language
    }
    
    print("✅ 角色及参考音频配置完成！")
    print("🎉 现在去 Chrome 里面用插件划词朗读吧！")
    print("🚀 启动 API 服务 (按 Ctrl+C 退出)...")

    # 5. 启动 FastAPI 服务，这会阻塞当前进程
    server_module.start_server(host="127.0.0.1", port=8000, workers=1)
