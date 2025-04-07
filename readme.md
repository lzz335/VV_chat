# 技术说明

## 数据来源  

本项目使用的张维为相关表情包数据集源自[知乎](https://www.zhihu.com/question/656505859/answer/55843704436)公开内容。**此为第三方资源，与本项目无隶属或认可关系。本项目仅使用该数据集作为算法效果演示**。若您是权利人认为需要移除任何内容，请立即通过neuliuzz@163.com联系我们。  

**本项目的出发点源于对张老师学术观点的欣赏**  

**重要提示**：用户须自行从知乎下载数据集，并确保对任何可能超出适用著作权法合理使用保护范围的使用行为已获得适当授权。  

## 技术规格  

- 采用**ChromaDB**作为数据库系统，需配置可用的**C++编译环境**。配置参考：[C++环境指南](https://blog.csdn.net/...)  
- 文本嵌入处理使用北京智源研究院开发的**bgaaai/bge-large-zh-v1.5**模型  
- 界面实现基于**Gradio**框架  

## 使用说明  

1. 首次使用需通过Anaconda安装`requirements.txt`列出的依赖项  
2. 在项目根目录通过命令行执行`init.sh`  

**注意**：用户须根据系统配置自定义`init.sh`中的环境变量和文件路径  

3. 初始化成功后，后续执行使用`run.sh`  

## 更新日志（4月7日）  
- 优化GUI界面提升用户体验  
- 新增通过界面直接定制模型功能  
- 修改源码路径后系统将自动保存：  
  - 您的API密钥（如需要）  
  - 您的LLM服务平台URL  
- 优化用户操作流程使运行更流畅  

**提示**：基础执行流程不变，设置路径后可直接运行：python demo.py（无需使用run.sh）  

## 示例输出  

[![pE6KVG4.png](https://s21.ax1x.com/2025/04/03/pE6KVG4.png)](https://imgse.com/i/pE6KVG4)  

## 许可与免责声明  

**关于AI生成内容的重要声明**：  
所有生成的表情包内容均为算法实验性输出，未经人工编辑控制。这些输出：  
- 不表达或反映开发者观点  
- 可能包含非预期的偏见或错误  
- 严格按"原样"提供，不作任何担保  

**仅供学术使用**：  
本项目仅作为深度学习课程演示，严禁商业用途。用户须自行承担以下合规责任：  
1. 当地AI治理法规  
2. 知识产权法律  
3. 内容审核要求  

**第三方资源**：  
本实现包含受各自许可证约束的外部系统和数据集引用，建议用户独立核实所有引用元素的授权要求。


# Notice  

## Data Source  



The meme dataset associated with Zhang Weiwei used in this project originates from publicly available content on [Zhihu](https://www.zhihu.com/question/656505859/answer/55843704436). **This is a third-party resource not affiliated with or endorsed by this project. This project only uses this dataset as a demonstration of the algorithm's effectiveness** If you are a rights holder and believe any content requires removal, please promptly contact us via neuliuzz@163.com.  


**The starting point of this project comes from the admiration for Teacher Zhang**

**Important Notice:** Users must independently download the dataset from Zhihu and ensure they have obtained proper authorization for any usage that may exceed fair use protections under applicable copyright laws.  



## Technical Specifications  



- This project utilizes **ChromaDB** as its database system. A functional **C++ compilation environment** is required for operation. Configuration reference: [C++ Environment Guide](https://blog.csdn.net/...)  

- Text embedding processing employs the **bgaaai/bge-large-zh-v1.5** model developed by Beijing Academy of Artificial Intelligence.  

- Interface implementation uses **Gradio** framework.  



## Usage Instructions  
﻿
1. First-time users must install dependencies via the provided `requirements.txt` using Anaconda.  
2. Execute `init.sh` from the project root directory via command prompt.  
﻿
**Note:** Users must customize environment variables and file paths within `init.sh` according to their system configuration.  
﻿
3. Subsequent executions utilize `run.sh` after successful initialization.  
﻿
## Update Notes (4/7)  
- Implemented GUI improvements for better user experience  
- Added direct model customization through the user interface  
- After modifying source code paths, the system will automatically save:  
- Your API key (if required)  
- The URL of your LLM service provider platform  
- Optimized user workflow for smoother operation  
﻿
**Note:** The basic execution flow remains unchanged, you can directly run: python demo.py after set the path instead of using run.sh.



## Example Output  



[![pE6KVG4.png](https://s21.ax1x.com/2025/04/03/pE6KVG4.png)](https://imgse.com/i/pE6KVG4)



## Licensing & Disclaimers  



**Critical Notice Regarding AI Outputs:**  

All generated meme content represents experimental algorithmic outputs without human editorial control. These outputs:  

- Do not express or reflect developer opinions  

- May contain unintended biases or inaccuracies  

- Are provided strictly "as-is" without warranty  



**Academic Use Only:**  

This project serves exclusively as a deep learning course demonstration. Commercial use is strictly prohibited. Users assume full responsibility for compliance with:  

1. Local AI governance regulations  
2. Intellectual property laws  
3. Content moderation requirements  



**Third-Party Resources:**  

This implementation contains references to external systems and datasets subject to their respective licenses. It is recommended that users independently verify authorization requirements for all incorporated elements.
