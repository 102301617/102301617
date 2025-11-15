"""
数据可视化模块
生成词云图
"""
import matplotlib.pyplot as plt
import matplotlib
from wordcloud import WordCloud
import jieba
from collections import Counter
from typing import List
import numpy as np
from PIL import Image
import os

# 设置matplotlib中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False


class Visualizer:
    def __init__(self):
        # 设置中文字体（需要根据系统调整）
        self.font_path = self._get_font_path()
        
        # 添加专业术语到jieba词典
        jieba.add_word('大语言模型')
        jieba.add_word('大模型')
        jieba.add_word('LLM')
        jieba.add_word('GPT')
        jieba.add_word('ChatGPT')
        
    def _get_font_path(self) -> str:
        """
        获取系统中文字体路径
        """
        # Windows常见字体路径
        font_paths = [
            'C:/Windows/Fonts/simhei.ttf',  # 黑体
            'C:/Windows/Fonts/msyh.ttc',    # 微软雅黑
            'C:/Windows/Fonts/simsun.ttc',  # 宋体
        ]
        
        for path in font_paths:
            if os.path.exists(path):
                return path
                
        # 如果没有找到，返回None（wordcloud会使用默认字体）
        return None
    
    def process_text(self, danmaku_list: List[str]) -> str:
        """
        处理弹幕文本，进行分词
        """
        # 过滤掉太短的词和停用词
        stop_words = {'的', '了', '是', '我', '你', '他', '她', '它', '们', 
                     '这', '那', '就', '也', '都', '还', '在', '有', '和'}
        
        all_words = []
        for text in danmaku_list:
            # 使用jieba分词
            words = jieba.cut(text)
            for word in words:
                word = word.strip()
                if len(word) > 1 and word not in stop_words:
                    all_words.append(word)
        
        return ' '.join(all_words)
    
    def create_wordcloud(self, danmaku_list: List[str], output_path: str = 'wordcloud.png'):
        """
        创建词云图
        """
        print("正在生成词云图...")
        
        # 处理文本
        text = self.process_text(danmaku_list)
        
        if not text:
            print("警告: 没有有效文本数据生成词云")
            return
        
        # 配置词云参数
        wordcloud_config = {
            'width': 1920,
            'height': 1080,
            'background_color': 'white',
            'max_words': 200,
            'relative_scaling': 0.5,
            'colormap': 'viridis',
            'font_step': 1,
            'max_font_size': 100,
            'min_font_size': 10,
            'collocations': False,  # 不显示二元词组
        }
        
        # 如果找到中文字体，添加到配置
        if self.font_path:
            wordcloud_config['font_path'] = self.font_path
            print(f"使用字体: {self.font_path}")
        else:
            print("警告: 未找到中文字体，词云可能无法正确显示中文")
        
        # 创建词云对象
        wordcloud = WordCloud(**wordcloud_config)
        
        # 生成词云
        wordcloud.generate(text)
        
        # 创建图形
        plt.figure(figsize=(20, 12))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        
        # 保存图片
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"词云图已保存到: {output_path}")
        
        # 显示图片（可选）
        # plt.show()
        plt.close()
    
    def create_advanced_wordcloud(self, danmaku_list: List[str], output_path: str = 'wordcloud_advanced.png'):
        """
        创建更美观的词云图（带自定义颜色和形状）
        """
        print("正在生成高级词云图...")
        
        # 处理文本
        text = self.process_text(danmaku_list)
        
        if not text:
            print("警告: 没有有效文本数据生成词云")
            return
        
        # 使用词频来创建词云
        words = text.split()
        word_freq = Counter(words)
        
        # 配置词云参数（更美观的设置）
        wordcloud_config = {
            'width': 1920,
            'height': 1080,
            'background_color': 'white',
            'max_words': 300,
            'relative_scaling': 0.6,
            'colormap': 'Set3',  # 使用更鲜艳的配色
            'font_step': 1,
            'max_font_size': 120,
            'min_font_size': 12,
            'collocations': False,
            'prefer_horizontal': 0.7,  # 70%的词汇横向显示
        }
        
        if self.font_path:
            wordcloud_config['font_path'] = self.font_path
        
        # 创建词云
        wordcloud = WordCloud(**wordcloud_config)
        wordcloud.generate_from_frequencies(word_freq)
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(20, 12), facecolor='white')
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        
        # 添加标题
        plt.title('B站大语言模型相关视频弹幕词云图', 
                 fontsize=24, pad=20, fontweight='bold')
        
        # 保存
        plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        print(f"高级词云图已保存到: {output_path}")
        plt.close()


if __name__ == '__main__':
    visualizer = Visualizer()
    test_data = ['大语言模型很厉害', 'GPT非常好用', '大模型改变世界'] * 10
    visualizer.create_wordcloud(test_data, 'test_wordcloud.png')

