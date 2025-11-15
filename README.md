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

```bash
pip install -r requirements.txt
```

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

# 只处理数据
python data_processor.py

# 只生成词云图
python visualizer.py

# 只生成分析报告
python data_analyzer.py
```

## 输出文件

运行完成后，将生成以下文件：

1. **danmaku_cache.txt** - 原始弹幕数据缓存
2. **danmaku_statistics.xlsx** - 统计数据Excel表格
3. **wordcloud.png** - 词云图（基础版）
4. **wordcloud_advanced.png** - 词云图（高级版）
5. **analysis_conclusion.txt** - 分析结论报告

## 项目结构

```
.
├── main.py                 # 主程序入口
├── danmaku_crawler.py      # 弹幕爬虫模块
├── data_processor.py       # 数据处理模块
├── excel_writer.py         # Excel导出模块
├── visualizer.py           # 可视化模块
├── data_analyzer.py        # 数据分析模块
├── requirements.txt        # 依赖包列表
└── README.md              # 项目说明
```

## 注意事项

1. **爬取速度**: 为避免被B站限制，程序内置了请求延迟。首次运行可能需要较长时间。
2. **缓存机制**: 程序会自动缓存爬取的弹幕数据，下次运行时会询问是否使用缓存。
3. **中文字体**: 词云图生成需要中文字体支持。程序会自动查找Windows系统中的中文字体。
4. **数据量**: 默认爬取前300个视频的弹幕，数据量较大时处理时间较长。

## 技术栈

- **爬虫**: requests, BeautifulSoup4
- **数据处理**: pandas, jieba
- **可视化**: wordcloud, matplotlib
- **Excel操作**: openpyxl
- **数据分析**: collections.Counter

## 许可证

MIT License

## 作者

102301617

