"""
数据过滤和处理模块
过滤噪声数据，进行词频统计
"""
import re
from collections import Counter
from typing import List, Dict


class DanmakuProcessor:
    def __init__(self):
        # 定义噪声关键词（点赞、666等）
        self.noise_patterns = [
            r'^6+$',  # 纯6
            r'^[\d\s]+$',  # 纯数字
            r'^[a-zA-Z\s]+$',  # 纯英文（短词）
            r'^[^\u4e00-\u9fa5]+$',  # 不包含中文
            r'点赞', r'三连', r'关注', r'投币',
            r'^\s*$',  # 空字符串
        ]
        
        # 关键词相关词汇
        self.keywords = ['大语言模型', '大模型', 'LLM', 'GPT', 'ChatGPT', 
                        '语言模型', 'AI模型', '人工智能模型']
    
    def is_noise(self, text: str) -> bool:
        """
        判断是否为噪声数据
        """
        if len(text) < 2:  # 太短的弹幕
            return True
            
        text = text.strip()
        if not text:
            return True
            
        # 检查是否匹配噪声模式
        for pattern in self.noise_patterns:
            if re.match(pattern, text, re.IGNORECASE):
                return True
                
        # 如果弹幕太短且不包含关键词，可能是噪声
        if len(text) < 3 and not any(kw in text for kw in self.keywords):
            return True
            
        return False
    
    def filter_danmaku(self, danmaku_list: List[str]) -> List[str]:
        """
        过滤噪声弹幕
        """
        filtered = []
        noise_count = 0
        
        for danmaku in danmaku_list:
            if not self.is_noise(danmaku):
                filtered.append(danmaku)
            else:
                noise_count += 1
                
        print(f"过滤前: {len(danmaku_list)} 条弹幕")
        print(f"过滤后: {len(filtered)} 条弹幕")
        print(f"过滤噪声: {noise_count} 条")
        
        return filtered
    
    def count_word_frequency(self, danmaku_list: List[str], top_n: int = 8) -> List[Dict]:
        """
        统计词频，返回排名前N的弹幕
        """
        counter = Counter(danmaku_list)
        top_items = counter.most_common(top_n)
        
        result = []
        for i, (text, count) in enumerate(top_items, 1):
            result.append({
                'rank': i,
                'danmaku': text,
                'count': count
            })
            
        return result
    
    def get_all_stats(self, danmaku_list: List[str]) -> Dict:
        """
        获取所有统计数据
        """
        filtered = self.filter_danmaku(danmaku_list)
        top_8 = self.count_word_frequency(filtered, top_n=8)
        
        return {
            'total_count': len(filtered),
            'original_count': len(danmaku_list),
            'top_8_danmaku': top_8,
            'all_danmaku': filtered
        }


if __name__ == '__main__':
    processor = DanmakuProcessor()
    test_data = ['666', '大模型真厉害', '6', '点赞', '这个模型不错', '666666']
    stats = processor.get_all_stats(test_data)
    print(stats)

