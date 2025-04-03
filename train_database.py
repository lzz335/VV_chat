import sys
from FlagEmbedding import FlagModel
import chromadb
from tqdm import tqdm
import glob
import os

# 固定的参数
MODEL_NAME = "BAAI/bge-large-zh-v1.5"
QUERY_INSTRUCTION = "为这个句子生成表示以用于检索相关文章："
USE_FP16 = True
COLLECTION_NAME = "vv_chat"

# 获取从Shell脚本传递的参数
folder_path = sys.argv[1]
database_path = sys.argv[2]
batch_size = int(sys.argv[3])

# 创建模型实例
embeddings_model = FlagModel(
    MODEL_NAME,
    query_instruction_for_retrieval=QUERY_INSTRUCTION,
    use_fp16=USE_FP16
)


def get_png_files(folder_path):
    """
    获取指定文件夹下所有的PNG文件路径。

    参数:
    folder_path (str): 指定的文件夹路径，用于搜索PNG文件。

    返回:
    list: 包含所有PNG文件路径的列表。
    """
    png_files = glob.glob(os.path.join(folder_path, "*.png"))
    return png_files


# 获取文件夹中所有PNG文件的文件名（不包括扩展名）
documents = [item.split("/")[-1].split("\\")[-1].split(".")[0] for item in get_png_files(folder_path)]

# 创建ChromaDB客户端并连接到指定路径的数据库
chroma_client = chromadb.PersistentClient(path=database_path)
chroma_client.delete_collection(COLLECTION_NAME)  # 测试使用
collection = chroma_client.create_collection(name=COLLECTION_NAME)

# 初始化索引计数器
index = 0
# 遍历文档列表，按批次处理
for i in tqdm(range(0, len(documents), batch_size)):
    batch_data = documents[i:min(len(documents), i + batch_size)]
    # 为当前批次的文档生成嵌入向量
    embeddings = embeddings_model.encode(batch_data)
    # 将嵌入向量和文档信息添加到集合中
    for embedding, document in zip(embeddings, batch_data):
        index += 1
        collection.add(
            ids=["figure id: {}".format(index)],
            documents=[document],
            embeddings=[embedding],
            metadatas=[{"path": folder_path + "/" + document + ".png"}]  # 可选，我这里仅仅用于标记对应表情所在的文件夹
        )
