import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

# 配置参数
EXCEL_PATH = ""  # Excel文件路径
COLUMN_NAME = ""  # 目标列名
INDEX_DIR = "./faiss"  # 索引存储目录

# 1. 初始化嵌入模型
embedding_model = HuggingFaceEmbeddings(
    model_name="bge-large-zh-v1.5",  # 轻量级嵌入模型
    model_kwargs={"device": "cuda:0"},  # 使用GPU可改为"cuda",
    encode_kwargs = {'normalize_embeddings': True}
)

# 2. 读取Excel文件
all_texts = []
xls = pd.ExcelFile(EXCEL_PATH)
all_metadata = []
for sheet_name in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet_name)
    
    # 检查目标列是否存在
    if COLUMN_NAME in df.columns:
        # 提取非空内容
        sheet_texts = df[COLUMN_NAME].dropna().astype(str).tolist()
        for text in sheet_texts:
            for i in range(0, 1000, len(text)):
                all_texts.append(text[i:i+1000])
                
            # all_texts.append(text)
                all_metadata.append(sheet_name)
        print(f"Sheet '{sheet_name}' 提取到 {len(sheet_texts)} 条记录")
    else:
        print(f"警告: Sheet '{sheet_name}' 中未找到列 '{COLUMN_NAME}'")

# 3. 创建向量数据库
if all_texts:
    print(f"总共提取到 {len(all_texts)} 条文本")
    
    # 创建FAISS索引
    vector_db = FAISS.from_texts(
        texts=all_texts,
        embedding=embedding_model,
        metadatas=[{"source": metadata} for metadata in all_metadata],
    )
    
    # 保存索引
    vector_db.save_local(INDEX_DIR)
    print(f"FAISS索引已保存至 {INDEX_DIR}")
    
    # 验证索引
    loaded_db = FAISS.load_local(INDEX_DIR, embedding_model, allow_dangerous_deserialization=True)
    print(f"索引验证: 数据库包含 {loaded_db.index.ntotal} 个向量")
else:
    print("未找到有效文本内容")