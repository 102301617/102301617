"""
数据过滤和处理模块（性能优化版）
过滤噪声数据，进行词频统计
优化点：
1. 预编译正则表达式
2. 使用集合进行关键词查找
3. 优化循环逻辑
"""
import re
from collections import Counter
from typing import List, Dict


class DanmakuProcessorOptimized:
    def __init__(self):
        # 预编译正则表达式（性能优化1）
        self.noise_patterns = [
            re.compile(r'^6+$'),  # 纯6
            re.compile(r'^[\d\s]+$'),  # 纯数字
            re.compile(r'^[a-zA-Z\s]+$'),  # 纯英文（短词）
            re.compile(r'^[^\u4e00-\u9fa5]+$'),  # 不包含中文
            re.compile(r'点赞'), 
            re.compile(r'三连'), 
            re.compile(r'关注'), 
            re.compile(r'投币'),
            re.compile(r'^\s*$'),  # 空字符串
        ]
        
        # 使用集合进行关键词查找（性能优化2）
        self.keywords = {'大语言模型', '大模型', 'LLM', 'GPT', 'ChatGPT', 
                        '语言模型', 'AI模型', '人工智能模型'}
    
    def is_noise(self, text: str) -> bool:
        """
        判断是否为噪声数据（优化版）
        """
        # 快速长度检查
        if len(text) < 2:
            return True
            
        text = text.strip()
        if not text:
            return True
        
        # 使用预编译的正则表达式（性能优化）
        for pattern in self.noise_patterns:
            if pattern.match(text):
                return True
                
        # 使用集合查找（性能优化）
        if len(text) < 3 and not any(kw in text for kw in self.keywords):
            return True
            
        return False
    
    def filter_danmaku(self, danmaku_list: List[str]) -> List[str]:
        """
        过滤噪声弹幕（优化版：使用列表推导式）
        """
        # 使用列表推导式替代循环（性能优化3）
        filtered = [danmaku for danmaku in danmaku_list if not self.is_noise(danmaku)]
        noise_count = len(danmaku_list) - len(filtered)
                
        print(f"过滤前: {len(danmaku_list)} 条弹幕")
        print(f"过滤后: {len(filtered)} 条弹幕")
        print(f"过滤噪声: {noise_count} 条")
        
        return filtered
    
    def count_word_frequency(self, danmaku_list: List[str], top_n: int = 8) -> List[Dict]:
        """
        统计词频，返回排名前N的弹幕（优化版：使用列表推导式）
        """
        counter = Counter(danmaku_list)
        top_items = counter.most_common(top_n)
        
        # 使用列表推导式（性能优化4）
        result = [
            {
                'rank': i,
                'danmaku': text,
                'count': count
            }
            for i, (text, count) in enumerate(top_items, 1)
        ]
            
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
    processor = DanmakuProcessorOptimized()
    test_data = ['666', '大模型真厉害', '6', '点赞', '这个模型不错', '666666']
    stats = processor.get_all_stats(test_data)
    print(stats)

