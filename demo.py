import re
import gradio as gr
import chromadb
from FlagEmbedding import FlagModel
from openai import OpenAI
import os

# Hardcoded ChromaDB paths
CHROMA_PATH = "C:/NeurIPS2025/open source/database"  # Replace with your actual path
COLLECTION_NAME = "vv_chat"
MODEL_LIST = ["gpt-4o-mini", "deepseek-r1:1.5b", "gemma3:latest", "gpt-4o", "gpt4", "deepseek-v3"]
# Initialize components
embeddings_model = FlagModel('BAAI/bge-large-zh-v1.5',
                             query_instruction_for_retrieval="为这个句子生成表示以用于检索相关文章：",
                             use_fp16=True)

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_collection(COLLECTION_NAME)

# Data file path
DATA_FILE = "data.txt"


def load_api_data():
    """Load API URL and key from data file if exists"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            lines = f.readlines()
            if len(lines) >= 2:
                return lines[0].strip(), lines[1].strip()
    return "", ""


def save_api_data(url, api_key):
    """Save API URL and key to data file"""
    with open(DATA_FILE, 'w') as f:
        f.write(f"{url}\n{api_key}")


# Initialize OpenAI client with loaded data or empty
openai_url, openai_key = load_api_data()
client = OpenAI(base_url=openai_url, api_key=openai_key) if openai_url and openai_key else None


def generate_response(query, model_name):
    if not client:
        raise gr.Error("请先设置OpenAI API URL和密钥")

    completion_instance = client.chat.completions.create(
        model=model_name,
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
    return figure_files, recall["documents"][0]


def extract_answer(input_text):
    # 使用正则表达式查找<answer>标签内容
    match = re.search(r'<answer>(.*?)</answer>', input_text)
    if match:
        return match.group(1)  # 返回标签内的内容
    return None


def get_figure_path(answer, figure_list, abc_dict):
    figures = []
    for index, alphabeta in enumerate(abc_dict):
        if alphabeta in answer:
            figures.append(figure_list[index])
    return figures


def judge(query, figure_list, documents_list, model_name):
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
    res = generate_response(query_for_gpt, model_name)
    answer = extract_answer(res)
    return res, get_figure_path(answer, figure_list, abc_dict)


def process_input(query, recall_length, model_name):
    rag_images, documents_list = rag(query, recall_length)
    reasoning, judgement_image = judge(query, rag_images, documents_list, model_name)
    return reasoning, rag_images, judgement_image


def update_api_settings(api_url, api_key):
    save_api_data(api_url, api_key)
    global client
    client = OpenAI(base_url=api_url, api_key=api_key)
    return "设置已保存！"


with gr.Blocks(theme=gr.themes.Soft(), title="表情包推荐系统") as demo:
    # API Settings Section
    with gr.Accordion("API 设置", open=False):
        with gr.Row():
            with gr.Column():
                api_url = gr.Textbox(label="API URL",
                                     value=load_api_data()[0],
                                     placeholder="https://api.openai.com/v1")
                api_key = gr.Textbox(label="API Key",
                                     type="password",
                                     value=load_api_data()[1],
                                     placeholder="输入你的API密钥")
                model_selector = gr.Dropdown(MODEL_LIST,
                                             label="模型选择",
                                             value="gpt-4o-mini",
                                             info="选择要使用的语言模型")
                with gr.Row():
                    save_btn = gr.Button("保存设置", variant="primary")
                    save_status = gr.Textbox(label="状态",
                                             interactive=False,
                                             show_label=False)

    # Main Interface
    with gr.Row():
        # Left Main Column (now contains reasoning + related images)
        with gr.Column(scale=4):
            # Input Area
            with gr.Group():
                input_box = gr.Textbox(label="输入查询内容",
                                       placeholder="输入你想表达的情绪或场景...",
                                       lines=3,
                                       max_lines=6)
                with gr.Row():
                    submit_btn = gr.Button("生成推荐", variant="primary")
                    clear_btn = gr.Button("清空")

            # Split left column into two sub-columns
            with gr.Row():
                # Left sub-column: Reasoning Process
                with gr.Column(scale=1):
                    reasoning_box = gr.Textbox(label="推理过程",
                                               lines=12,
                                               max_lines=20,
                                               interactive=False)

                # Right sub-column: Related Images (previously gallery)

                with gr.Column(scale=1):
                    judgement_output = gr.Gallery(label="推荐表情包",
                                                  columns=3,
                                                  height=600,
                                                  object_fit="contain")

        # Right Column: Meme Recommendations (now moved here)
        with gr.Column(scale=3):
            gallery = gr.Gallery(label="直接检索的文件结果",
                                 columns=2,
                                 height=500,
                                 object_fit="cover")

            with gr.Accordion("检索设置", open=False):
                recall_slider = gr.Slider(minimum=2,
                                          maximum=20,
                                          step=1,
                                          value=5,
                                          label="召回数量")

    # Event handlers (unchanged)
    save_btn.click(
        fn=update_api_settings,
        inputs=[api_url, api_key],
        outputs=[save_status]
    ).then(
        fn=lambda: gr.Info("API设置已保存"),
        outputs=[]
    )

    submit_btn.click(
        fn=process_input,
        inputs=[input_box, recall_slider, model_selector],
        outputs=[reasoning_box, gallery, judgement_output]
    )

    clear_btn.click(
        fn=lambda: [None, None, None],
        outputs=[input_box, reasoning_box, judgement_output]
    )

if __name__ == "__main__":
    demo.launch()
