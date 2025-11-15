"""
数据分析模块
分析弹幕数据，生成结论
"""
import re
from collections import Counter
from typing import Dict, List
import jieba


class DataAnalyzer:
    def __init__(self):
        # 定义分析维度
        self.cost_keywords = ['成本', '价格', '费用', '昂贵', '便宜', '免费', '收费', '付费']
        self.application_keywords = ['应用', '用途', '场景', '领域', '行业', '工作', '学习', 
                                    '教育', '医疗', '金融', '客服', '创作', '编程', '翻译']
        self.negative_keywords = ['问题', '缺点', '不足', '风险', '危险', '担忧', '失业', 
                                 '替代', '错误', '不准确', '幻觉', '偏见']
        self.positive_keywords = ['好', '棒', '厉害', '强大', '优秀', '先进', '创新', 
                                 '进步', '革命', '改变', '未来', '希望']
        
    def analyze_sentiment(self, danmaku_list: List[str]) -> Dict:
        """
        分析情感倾向
        """
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        for text in danmaku_list:
            pos_score = sum(1 for kw in self.positive_keywords if kw in text)
            neg_score = sum(1 for kw in self.negative_keywords if kw in text)
            
            if pos_score > neg_score:
                positive_count += 1
            elif neg_score > pos_score:
                negative_count += 1
            else:
                neutral_count += 1
        
        total = len(danmaku_list)
        return {
            'positive': positive_count,
            'negative': negative_count,
            'neutral': neutral_count,
            'positive_rate': positive_count / total if total > 0 else 0,
            'negative_rate': negative_count / total if total > 0 else 0
        }
    
    def analyze_cost_mentions(self, danmaku_list: List[str]) -> List[str]:
        """
        提取与成本相关的弹幕
        """
        cost_related = []
        for text in danmaku_list:
            if any(kw in text for kw in self.cost_keywords):
                cost_related.append(text)
        return cost_related[:20]  # 返回前20条
    
    def analyze_application_mentions(self, danmaku_list: List[str]) -> Dict:
        """
        分析应用领域提及情况
        """
        application_count = {}
        for text in danmaku_list:
            for kw in self.application_keywords:
                if kw in text:
                    application_count[kw] = application_count.get(kw, 0) + 1
        return dict(sorted(application_count.items(), key=lambda x: x[1], reverse=True)[:10])
    
    def analyze_concerns(self, danmaku_list: List[str]) -> List[str]:
        """
        提取担忧和不利影响相关的弹幕
        """
        concerns = []
        for text in danmaku_list:
            if any(kw in text for kw in self.negative_keywords):
                concerns.append(text)
        return concerns[:20]  # 返回前20条
    
    def extract_key_topics(self, danmaku_list: List[str]) -> List[str]:
        """
        提取关键话题
        """
        # 使用jieba分词和词频统计
        all_words = []
        important_words = ['模型', 'AI', '人工智能', '技术', '发展', '未来', 
                          '应用', '能力', '效果', '使用', '体验']
        
        for text in danmaku_list:
            words = jieba.cut(text)
            for word in words:
                word = word.strip()
                if len(word) > 1 and word in important_words:
                    all_words.append(word)
        
        counter = Counter(all_words)
        return [word for word, count in counter.most_common(10)]
    
    def generate_conclusion(self, danmaku_list: List[str], stats: Dict) -> str:
        """
        生成分析结论
        """
        print("\n正在进行数据分析...")
        
        # 情感分析
        sentiment = self.analyze_sentiment(danmaku_list)
        
        # 应用领域分析
        applications = self.analyze_application_mentions(danmaku_list)
        
        # 成本相关分析
        cost_mentions = self.analyze_cost_mentions(danmaku_list)
        
        # 担忧分析
        concerns = self.analyze_concerns(danmaku_list)
        
        # 关键话题
        topics = self.extract_key_topics(danmaku_list)
        
        # 生成结论文本
        conclusion = f"""
{'='*80}
B站用户对大语言模型技术的主流看法分析报告
{'='*80}

一、总体概况
-----------
- 有效弹幕总数: {stats['total_count']:,} 条
- 原始弹幕数: {stats['original_count']:,} 条
- 数据来源: B站综合排序前300个相关视频

二、情感倾向分析
---------------
- 积极态度: {sentiment['positive']} 条 ({sentiment['positive_rate']*100:.1f}%)
- 消极态度: {sentiment['negative']} 条 ({sentiment['negative_rate']*100:.1f}%)
- 中性态度: {sentiment['neutral']} 条 ({(1-sentiment['positive_rate']-sentiment['negative_rate'])*100:.1f}%)

总体来看，用户对大语言模型技术的态度{'较为积极' if sentiment['positive_rate'] > sentiment['negative_rate'] else '存在一定担忧'}。

三、应用成本关注
---------------
与成本相关的弹幕共发现 {len(cost_mentions)} 条，主要关注点包括：
"""
        
        if cost_mentions:
            conclusion += "\n典型评论示例：\n"
            for i, mention in enumerate(cost_mentions[:5], 1):
                conclusion += f"  {i}. {mention}\n"
        else:
            conclusion += "用户对成本的直接讨论相对较少。\n"
        
        conclusion += f"""
四、潜在应用领域
---------------
用户提及的主要应用领域（按提及次数排序）：
"""
        for i, (app, count) in enumerate(list(applications.items())[:8], 1):
            conclusion += f"  {i}. {app}: {count} 次提及\n"
        
        conclusion += f"""
五、不利影响和担忧
---------------
与不利影响相关的弹幕共发现 {len(concerns)} 条，主要担忧包括：
"""
        
        if concerns:
            conclusion += "\n典型担忧示例：\n"
            for i, concern in enumerate(concerns[:5], 1):
                conclusion += f"  {i}. {concern}\n"
        else:
            conclusion += "用户对不利影响的讨论相对较少。\n"
        
        conclusion += f"""
六、关键话题
-----------
弹幕中最常提及的关键话题：
"""
        for i, topic in enumerate(topics[:8], 1):
            conclusion += f"  {i}. {topic}\n"
        
        conclusion += f"""
七、主要结论
-----------
1. 用户关注度: 大语言模型技术在B站用户中引起了广泛关注
2. 态度倾向: {'用户整体态度积极，看好技术发展前景' if sentiment['positive_rate'] > 0.5 else '用户态度较为复杂，既有期待也有担忧'}
3. 应用场景: 用户关注的应用领域主要集中在{', '.join(list(applications.keys())[:3]) if applications else '多个'}等方面
4. 成本因素: {'用户对成本问题有一定关注' if len(cost_mentions) > 10 else '用户对成本问题的讨论相对较少'}
5. 风险意识: {'用户对技术带来的潜在风险有一定认识' if len(concerns) > 10 else '用户的风险讨论相对较少'}

{'='*80}
报告生成时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*80}
"""
        
        return conclusion


if __name__ == '__main__':
    analyzer = DataAnalyzer()
    test_data = ['大模型成本很高', 'GPT在教育领域应用很好', '担心AI会替代工作'] * 10
    stats = {'total_count': 30, 'original_count': 35}
    conclusion = analyzer.generate_conclusion(test_data, stats)
    print(conclusion)

