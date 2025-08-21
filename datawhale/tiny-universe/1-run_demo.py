from transformers4393.src.transformers.models.qwen2 import Qwen2Config, Qwen2Model
import torch

"""
环境配置：
python 3.11
方式一：
1. 下载 transformers 4.39.3
2. 源码模式安装：`pip install -e .`

方式二：
直接在文件头导入包

注意依赖库：tokenizers==0.15.2
"""

def run_qwen2():
    qwen2config = Qwen2Config(
        vocab_size=151936,  # 词表
        hidden_size=4096//2,
        intermediate_size=22016//2,
        num_hidden_layers=32//2,
        num_attention_heads=32,
        max_position_embeddings=2048//2
    )

    # 根据配置创建一个model
    qwen2model = Qwen2Model(config=qwen2config)

    # 从指定词表里面，随机采样一个(4, 30)的张量作为输入，可以理解成随机生成4个句子，每个句子有30个词
    input_ids = torch.randint(0, qwen2config.vocab_size, (4, 30))

    res = qwen2model(input_ids)
    print(type(res))

if __name__ == '__main__':
    run_qwen2()