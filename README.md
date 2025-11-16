# B站大语言模型相关视频弹幕数据分析系统

这是一个完整的B站弹幕数据采集、统计、可视化和分析系统，专门用于分析B站用户对大语言模型技术的主流看法。

## 功能特性

### 2.1 数据获取
- 使用`requests`和`BeautifulSoup`爬取B站视频弹幕数据
- 支持搜索关键词："大语言模型"、"大模型"、"LLM"
- 自动获取综合排序前300个相关视频的弹幕
- 智能过滤噪声数据（如"666"、点赞等）

### 2.2 数据统计
- 统计每类弹幕的总数量
- 输出词频排名前8的弹幕
- 自动生成Excel统计表格（`danmaku_statistics.xlsx`）

### 2.3 数据可视化
- 生成美观的词云图
- 支持中文分词和词频统计
- 提供基础版和高级版两种词云图样式

### 2.4 数据结论
- 情感倾向分析（积极/消极/中性）
- 应用成本关注度分析
- 潜在应用领域统计
- 不利影响和担忧提取
- 自动生成完整的分析报告

## 安装依赖

### 方法1: 使用批处理文件（推荐，Windows用户）

**最简单的方式** - 双击运行：
- `快速安装.bat` - 一键快速安装（使用国内镜像）
- `安装依赖.bat` - 完整安装工具（带交互和错误处理）

### 方法2: 使用py命令（Windows Python Launcher）

```bash
py -m pip install -r requirements.txt
```

或使用国内镜像（速度更快）：
```bash
py -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 方法3: 使用python命令

```bash
python -m pip install -r requirements.txt
```

### 方法4: 使用Python脚本

```bash
py install_deps.py
# 或
python install_deps.py
```

### 如果遇到问题

如果提示"python不是内部或外部命令"：
1. 使用 `py` 命令代替 `python`
2. 使用完整路径，例如：`C:\Users\你的用户名\AppData\Local\Programs\Python\Python312\python.exe -m pip install -r requirements.txt`
3. 运行 `安装依赖.bat`，它会自动查找Python

## 使用方法

### 直接运行主程序

```bash
python main.py
```

程序将按以下步骤执行：
1. 搜索并爬取B站相关视频弹幕（或从缓存加载）
2. 过滤噪声数据并进行统计
3. 导出Excel统计表
4. 生成词云图
5. 生成分析结论报告

### 模块化使用

如果只需要部分功能，可以单独运行各个模块：

```bash
# 只爬取数据
python danmaku_crawler.py

# 只处理数据（原始版本）
python data_processor.py

# 只处理数据（优化版本，性能提升23.6%）
python data_processor_optimized.py

# 只生成词云图
python visualizer.py

# 只生成分析报告
python data_analyzer.py
```

### 性能分析

项目包含完整的性能分析和优化工具：

```bash
# 运行性能分析（需要先有danmaku_cache.txt数据文件）
python performance_profiler.py

# 对比原始版本和优化版本的性能
python performance_comparison.py
```

性能分析结果：
- **总体性能提升**: 23.6%（从312.45ms降至238.67ms）
- **最大改进**: `is_noise`函数提升28.2%
- **关键改进**: `filter_danmaku`函数提升24.0%

详细性能分析报告请参考：
- `performance_analysis.md` - 详细性能分析报告
- `性能改进总结.md` - 性能改进思路和成果总结
- `PERFORMANCE_README.md` - 性能分析工具使用说明

## 输出文件

运行完成后，将生成以下文件：

1. **danmaku_cache.txt** - 原始弹幕数据缓存
2. **danmaku_statistics.xlsx** - 统计数据Excel表格
3. **wordcloud.png** - 词云图（基础版）
4. **wordcloud_advanced.png** - 词云图（高级版）
5. **analysis_conclusion.txt** - 分析结论报告

### 性能分析输出文件（可选）

运行性能分析工具后，将生成：

1. **performance_report.txt** - 详细的cProfile性能报告
2. **performance_chart.png** - 性能分析可视化图表
3. **performance_comparison.png** - 原始版本vs优化版本性能对比图

## 项目结构

```
.
├── main.py                      # 主程序入口
├── danmaku_crawler.py           # 弹幕爬虫模块
├── data_processor.py            # 数据处理模块（原始版本）
├── data_processor_optimized.py  # 数据处理模块（性能优化版本）
├── excel_writer.py              # Excel导出模块
├── visualizer.py                # 可视化模块
├── data_analyzer.py             # 数据分析模块
├── performance_profiler.py      # 性能分析工具
├── performance_comparison.py    # 性能对比测试工具
├── requirements.txt             # 依赖包列表
├── README.md                    # 项目说明
├── performance_analysis.md   # 性能分析报告
├── PERFORMANCE_README.md        # 性能分析使用说明
└── 性能改进总结.md              # 性能改进总结文档
```

## 注意事项

1. **爬取速度**: 为避免被B站限制，程序内置了请求延迟。首次运行可能需要较长时间。
2. **缓存机制**: 程序会自动缓存爬取的弹幕数据，下次运行时会询问是否使用缓存。
3. **中文字体**: 词云图生成需要中文字体支持。程序会自动查找Windows系统中的中文字体。
4. **数据量**: 默认爬取前300个视频的弹幕，数据量较大时处理时间较长。
5. **性能优化**: 项目提供了优化版本的数据处理器（`data_processor_optimized.py`），性能提升23.6%，建议使用优化版本。

## 性能优化

项目包含完整的性能分析和优化方案：

### 性能改进成果

- ✅ **总体性能提升**: 23.6%（从312.45ms降至238.67ms）
- ✅ **最大瓶颈优化**: `filter_danmaku`函数提升24.0%
- ✅ **核心函数优化**: `is_noise`函数提升28.2%

### 主要优化点

1. **预编译正则表达式**: 避免重复编译，减少15-20%开销
2. **使用集合查找**: 关键词查找从O(n)优化到更高效
3. **列表推导式**: 减少函数调用开销，提升5-10%性能

### 消耗最大的函数

- **原始版本**: `filter_danmaku` (245.32 ms, 78.5%)
- **优化版本**: `filter_danmaku` (186.45 ms, 78.1%)
- **改进**: 减少58.87 ms (24.0%提升)

详细性能分析请参考：
- `performance_analysis.md` - 详细性能分析报告
- `性能改进总结.md` - 性能改进思路和成果
- `PERFORMANCE_README.md` - 性能分析工具使用说明

## 技术栈

- **爬虫**: requests, BeautifulSoup4
- **数据处理**: pandas, jieba, collections.Counter
- **可视化**: wordcloud, matplotlib
- **Excel操作**: openpyxl
- **数据分析**: collections.Counter, jieba, re
- **性能分析**: cProfile, pstats, matplotlib, time

## PSP表格

| PSP2.1 | 阶段 | 预估时间（分钟） | 实际时间（分钟） |
|--------|------|-----------------|-----------------|
| Planning | 计划 | 60 | 45 |
| - Estimate | 估计任务时间 | 60 | 45 |
| Development | 开发 | 480 | 520 |
| - Analysis | 需求分析 | 60 | 50 |
| - Design Spec | 生成设计文档 | 30 | 25 |
| - Design Review | 设计复审 | 20 | 15 |
| - Coding Standard | 代码规范 | 10 | 10 |
| - Design | 具体设计 | 60 | 70 |
| - Coding | 具体编码 | 200 | 250 |
| - Code Review | 代码复审 | 30 | 40 |
| - Test | 测试（自测、修改代码、提交修改） | 70 | 60 |
| Reporting | 报告 | 90 | 85 |
| - Test Report | 测试报告 | 30 | 25 |
| - Size Measurement | 计算工作量 | 20 | 15 |
| - Postmortem & Process Improvement Plan | 事后总结，并提出过程改进计划 | 40 | 45 |
| **合计** | | **630** | **650** |

### 各阶段说明

- **Planning（计划）**: 分析需求，制定开发计划，预估开发时间
- **Development（开发）**: 
  - **Analysis（需求分析）**: 理解项目需求，确定功能模块
  - **Design Spec（设计文档）**: 编写模块设计文档
  - **Design Review（设计复审）**: 检查设计文档的合理性
  - **Coding Standard（代码规范）**: 确定代码编写规范
  - **Design（具体设计）**: 设计各模块的接口和实现方案
  - **Coding（具体编码）**: 实现各功能模块（爬虫、数据处理、可视化、分析等）
  - **Code Review（代码复审）**: 检查代码质量和规范性
  - **Test（测试）**: 单元测试、集成测试、修复bug
- **Reporting（报告）**: 
  - **Test Report（测试报告）**: 编写测试报告
  - **Size Measurement（计算工作量）**: 统计代码行数、功能点等
  - **Postmortem（事后总结）**: 总结项目经验，提出改进建议

## 许可证

MIT License

## 作者

102301617

