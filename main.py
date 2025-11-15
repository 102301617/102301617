"""
主程序
整合所有功能模块
"""
import os
import sys
from danmaku_crawler import BilibiliDanmakuCrawler
from data_processor import DanmakuProcessor
from excel_writer import ExcelWriter
from visualizer import Visualizer
from data_analyzer import DataAnalyzer


def main():
    print("="*80)
    print("B站大语言模型相关视频弹幕数据采集与分析系统")
    print("="*80)
    
    # 步骤1: 数据获取
    print("\n【步骤1】开始数据获取...")
    crawler = BilibiliDanmakuCrawler()
    keywords = ['大语言模型', '大模型', 'LLM']
    
    # 检查是否已有缓存数据
    cache_file = 'danmaku_cache.txt'
    if os.path.exists(cache_file):
        # 先检查缓存文件是否为空
        with open(cache_file, 'r', encoding='utf-8') as f:
            cached_lines = [line.strip() for line in f if line.strip()]
        
        if cached_lines:
            print(f"发现缓存文件 {cache_file}，包含 {len(cached_lines)} 条弹幕")
            while True:
                user_input = input("是否使用缓存？(y/n，默认y): ").strip().lower()
                if user_input == '' or user_input == 'y':
                    use_cache = True
                    break
                elif user_input == 'n':
                    use_cache = False
                    break
                else:
                    print("请输入 y 或 n")
            
            if use_cache:
                all_danmaku = cached_lines
                print(f"从缓存加载 {len(all_danmaku)} 条弹幕")
            else:
                print("开始爬取数据（这可能需要较长时间）...")
                all_danmaku = crawler.crawl_danmaku(keywords, max_videos=300)
                # 保存缓存
                if all_danmaku:
                    with open(cache_file, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(all_danmaku))
                    print(f"数据已缓存到 {cache_file}")
        else:
            print(f"发现缓存文件 {cache_file}，但文件为空")
            print("将重新爬取数据...")
            all_danmaku = crawler.crawl_danmaku(keywords, max_videos=300)
            # 保存缓存
            if all_danmaku:
                with open(cache_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(all_danmaku))
                print(f"数据已缓存到 {cache_file}")
    else:
        print("开始爬取数据（这可能需要较长时间）...")
        all_danmaku = crawler.crawl_danmaku(keywords, max_videos=300)
        # 保存缓存
        if all_danmaku:
            with open(cache_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(all_danmaku))
            print(f"数据已缓存到 {cache_file}")
    
    if not all_danmaku:
        print("错误: 未获取到任何弹幕数据！")
        return
    
    print(f"\n总共获取 {len(all_danmaku)} 条原始弹幕")
    
    # 步骤2: 数据统计
    print("\n【步骤2】开始数据统计...")
    processor = DanmakuProcessor()
    stats = processor.get_all_stats(all_danmaku)
    
    print(f"\n词频排名前8的弹幕:")
    for item in stats['top_8_danmaku']:
        print(f"  {item['rank']}. {item['danmaku']}: {item['count']} 次")
    
    # 导出Excel
    print("\n【步骤2.1】导出Excel统计表...")
    excel_writer = ExcelWriter('danmaku_statistics.xlsx')
    excel_writer.write_statistics(stats)
    
    # 步骤3: 数据可视化
    print("\n【步骤3】生成词云图...")
    visualizer = Visualizer()
    visualizer.create_wordcloud(stats['all_danmaku'], 'wordcloud.png')
    visualizer.create_advanced_wordcloud(stats['all_danmaku'], 'wordcloud_advanced.png')
    
    # 步骤4: 数据结论
    print("\n【步骤4】生成分析结论...")
    analyzer = DataAnalyzer()
    conclusion = analyzer.generate_conclusion(stats['all_danmaku'], stats)
    
    # 保存结论到文件
    conclusion_file = 'analysis_conclusion.txt'
    with open(conclusion_file, 'w', encoding='utf-8') as f:
        f.write(conclusion)
    
    print(conclusion)
    print(f"\n结论已保存到: {conclusion_file}")
    
    print("\n" + "="*80)
    print("所有任务完成！")
    print("="*80)
    print("\n生成的文件:")
    print(f"  1. {cache_file} - 原始弹幕数据")
    print(f"  2. danmaku_statistics.xlsx - 统计数据表")
    print(f"  3. wordcloud.png - 词云图（基础版）")
    print(f"  4. wordcloud_advanced.png - 词云图（高级版）")
    print(f"  5. {conclusion_file} - 分析结论报告")
    print("="*80)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n程序运行出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

