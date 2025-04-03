import re
import gradio as gr
import chromadb
from FlagEmbedding import FlagModel
from openai import OpenAI
import argparse

# 创建ArgumentParser对象
parser = argparse.ArgumentParser(description='RAG Application with Gradio')
parser.add_argument('--chroma_path', type=str, required=True, help='Path to ChromaDB database')
parser.add_argument('--collection_name', type=str, default='vv_chat', help='Name of the collection in ChromaDB')
parser.add_argument('--openai_base_url', type=str, required=True, help='Base URL for OpenAI API')
parser.add_argument('--openai_api_key', type=str, required=True, help='API key for OpenAI')
parser.add_argument('--model', type=str, required=True, help='model name')
# 解析命令行参数
args = parser.parse_args()

# 使用解析出的参数初始化ChromaDB和OpenAI客户端
embeddings_model = FlagModel('BAAI/bge-large-zh-v1.5',
                             query_instruction_for_retrieval="为这个句子生成表示以用于检索相关文章：",
                             use_fp16=True)

chroma_client = chromadb.PersistentClient(path=args.chroma_path)
collection = chroma_client.get_collection(args.collection_name)

client = OpenAI(
    base_url=args.openai_base_url,
    api_key=args.openai_api_key
)


def generate_response(query):
    completion_instance = client.chat.completions.create(
        model=args.model,
        messages=[{"role": "user", "content": query}],
        temperature=0.5,
        top_p=1,
        max_tokens=1024
    )
    return completion_instance.choices[0].message.content


def rag(query, recall_length):
    embeddings = embeddings_model.encode(query)
    recall = collection.query(
        embeddings,
        n_results=recall_length
    )
    figure_files = [metadata["path"] for metadata in recall["metadatas"][0]]
    # print(figure_files, recall["documents"][0])
    return figure_files, recall["documents"][0]


def extract_answer(input_text):
    match = re.search(r'<answer>(.*?)</answer>', input_text)
    if match:
        return match.group(1)
    return None


def get_figure_path(answer, figure_list, abc_dict):
    figures = []
    for index, alphabeta in enumerate(abc_dict):
        if alphabeta in answer:
            figures.append(figure_list[index])
    return figures


def judge(query, figure_list, documents_list):
    abc_dict = list(map(chr, range(65, 65 + len(documents_list))))
    query_for_gpt = '''
**任务说明**
你需根据用户的问题内容和候选图片描述，选择最匹配的图片选项。请严格按照以下步骤执行：

**输入信息**
1. 用户问题："{query}"
2. 候选图片（格式：选项标号 + 描述）：
{image_options}

**选择要求**
1. 核心匹配：所选图片必须直接反映问题核心主题
2. 多选条件：当存在多个完全符合主题的选项时可多选，但需谨慎判断
3. 禁止行为：不得自行创作描述，必须从给定选项中选择

**输出规范**（必须严格遵循）
<thinking>
用100字以内中文说明：
1. 用户问题的核心需求分析
2. 各选项匹配度评估
3. 最终选择理由
</thinking>
<answer>
使用选项标号的字母，多个时用英文逗号分隔。示例："A" 或 "B,C"
</answer>

**示例参考**
输入问题："分析全球变暖对北极生态的影响"
候选图片：
A. 北极熊站在浮冰上
B. 温室气体排放柱状图
C. 冰川融化对比卫星图

正确输出：
<thinking>
问题聚焦北极生态变化，A直观展示生物栖息地危机，C体现环境变化证据。B虽相关但侧重成因而非影响
</thinking>
<answer>"A,C"</answer>
'''.format(
        query=query,
        image_options="\n".join([f"{chr(65 + i)}. {desc}" for i, desc in enumerate(documents_list)])
    )
    res = generate_response(query_for_gpt)
    answer = extract_answer(res)
    # print(res)

    return get_figure_path(answer, figure_list, abc_dict)


def process_input(query, recall_length):
    rag_images, documents_list = rag(query, recall_length)
    judgement_image = judge(query, rag_images, documents_list)

    return {
        gallery: rag_images,
        judgement_output: judgement_image
    }


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=3):
            input_box = gr.Textbox(label="输入查询内容")
            submit_btn = gr.Button("提交")

            with gr.Column():
                judgement_output = gr.Gallery(columns=1, height="auto", label="推荐插入表情包")
        with gr.Column(scale=2):
            gr.Markdown("## 检索到的图片")
            gallery = gr.Gallery(columns=3, height="auto")
            recall_slider = gr.Slider(minimum=2, maximum=20, step=1, value=5, label="召回长度")

    submit_btn.click(
        fn=process_input,
        inputs=[input_box, recall_slider],
        outputs=[gallery, judgement_output]
    )

if __name__ == "__main__":
    demo.launch()
