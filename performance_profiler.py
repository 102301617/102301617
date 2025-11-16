"""
性能分析工具
用于分析数据统计接口的性能
"""
import cProfile
import pstats
import time
import io
from functools import wraps
from typing import List, Dict

# 尝试导入matplotlib（可选依赖）
try:
    import matplotlib.pyplot as plt  # type: ignore
    import matplotlib  # type: ignore
    import numpy as np  # type: ignore
    MATPLOTLIB_AVAILABLE = True
    # 设置中文字体
    matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
    matplotlib.rcParams['axes.unicode_minus'] = False
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    # 定义占位符以避免运行时错误
    plt = None  # type: ignore
    matplotlib = None  # type: ignore
    np = None  # type: ignore
    print("警告: matplotlib未安装，将无法生成可视化图表。")
    print("可以运行 'pip install matplotlib numpy' 来安装。")
    print("文本报告仍将正常生成。\n")

from data_processor import DanmakuProcessor


def timing_decorator(func):
    """计时装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = (end_time - start_time) * 1000  # 转换为毫秒
        print(f"{func.__name__} 执行时间: {elapsed_time:.2f} ms")
        return result, elapsed_time
    return wrapper


class PerformanceProfiler:
    """性能分析器"""
    
    def __init__(self):
        self.timings = {}
        self.profiler = cProfile.Profile()
        
    def profile_function(self, func, *args, **kwargs):
        """分析函数性能"""
        # 使用cProfile进行详细分析
        self.profiler.enable()
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        self.profiler.disable()
        
        elapsed_time = (end_time - start_time) * 1000  # 毫秒
        return result, elapsed_time
    
    def get_profile_stats(self, sort_by='cumulative', top_n=20):
        """获取性能统计信息"""
        s = io.StringIO()
        ps = pstats.Stats(self.profiler, stream=s)
        ps.sort_stats(sort_by)
        ps.print_stats(top_n)
        return s.getvalue()
    
    def save_profile_report(self, filename='performance_report.txt'):
        """保存性能报告"""
        stats = self.get_profile_stats()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("数据统计接口性能分析报告\n")
            f.write("="*80 + "\n\n")
            f.write(stats)
        print(f"性能报告已保存到: {filename}")
    
    def visualize_performance(self, timings: Dict[str, float], output_path='performance_chart.png'):
        """可视化性能数据"""
        if not MATPLOTLIB_AVAILABLE:
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # 子图1: 函数执行时间柱状图
        functions = list(timings.keys())
        times = list(timings.values())
        colors = plt.cm.viridis(np.linspace(0, 1, len(functions)))
        
        bars = ax1.barh(functions, times, color=colors)
        ax1.set_xlabel('执行时间 (ms)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('函数名称', fontsize=12, fontweight='bold')
        ax1.set_title('数据统计接口各函数执行时间', fontsize=14, fontweight='bold', pad=20)
        ax1.grid(axis='x', alpha=0.3)
        
        # 添加数值标签
        for i, (bar, time_val) in enumerate(zip(bars, times)):
            ax1.text(time_val + max(times)*0.01, bar.get_y() + bar.get_height()/2, 
                    f'{time_val:.2f} ms', va='center', fontsize=9)
        
        # 子图2: 时间占比饼图
        total_time = sum(times)
        percentages = [t / total_time * 100 for t in times]
        
        # 只显示占比>5%的项，其他合并为"其他"
        threshold = 5
        significant = [(f, p) for f, p in zip(functions, percentages) if p >= threshold]
        other_pct = sum(p for f, p in zip(functions, percentages) if p < threshold)
        
        if other_pct > 0:
            significant.append(('其他', other_pct))
        
        pie_functions = [f[0] for f in significant]
        pie_percentages = [f[1] for f in significant]
        
        wedges, texts, autotexts = ax2.pie(pie_percentages, labels=pie_functions, 
                                           autopct='%1.1f%%', startangle=90,
                                           colors=plt.cm.Set3(np.linspace(0, 1, len(pie_functions))))
        ax2.set_title('函数执行时间占比', fontsize=14, fontweight='bold', pad=20)
        
        # 美化文本
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"性能分析图已保存到: {output_path}")
        plt.close()


def analyze_data_processor_performance(danmaku_list: List[str]):
    """分析数据处理器性能"""
    print("\n" + "="*80)
    print("开始性能分析...")
    print("="*80 + "\n")
    
    profiler = PerformanceProfiler()
    processor = DanmakuProcessor()
    
    # 分析各个函数的性能
    timings = {}
    
    # 1. 分析 is_noise 函数
    print("分析 is_noise 函数性能...")
    test_texts = danmaku_list[:1000]  # 测试前1000条
    _, time_is_noise = profiler.profile_function(
        lambda: [processor.is_noise(text) for text in test_texts]
    )
    timings['is_noise (1000次)'] = time_is_noise
    
    # 2. 分析 filter_danmaku 函数
    print("分析 filter_danmaku 函数性能...")
    _, time_filter = profiler.profile_function(
        processor.filter_danmaku, danmaku_list
    )
    timings['filter_danmaku'] = time_filter
    
    # 3. 分析 count_word_frequency 函数
    print("分析 count_word_frequency 函数性能...")
    filtered = processor.filter_danmaku(danmaku_list)
    _, time_count = profiler.profile_function(
        processor.count_word_frequency, filtered, 8
    )
    timings['count_word_frequency'] = time_count
    
    # 4. 分析 get_all_stats 函数（整体）
    print("分析 get_all_stats 函数性能...")
    _, time_all = profiler.profile_function(
        processor.get_all_stats, danmaku_list
    )
    timings['get_all_stats (整体)'] = time_all
    
    # 保存详细性能报告
    profiler.save_profile_report('performance_report.txt')
    
    # 生成可视化图表
    profiler.visualize_performance(timings, 'performance_chart.png')
    
    # 打印总结
    print("\n" + "="*80)
    print("性能分析总结")
    print("="*80)
    print(f"数据量: {len(danmaku_list)} 条弹幕")
    print(f"过滤后: {len(filtered)} 条弹幕")
    print("\n各函数执行时间:")
    for func_name, exec_time in sorted(timings.items(), key=lambda x: x[1], reverse=True):
        print(f"  {func_name:30s}: {exec_time:8.2f} ms")
    
    max_func = max(timings.items(), key=lambda x: x[1])
    print(f"\n消耗最大的函数: {max_func[0]} ({max_func[1]:.2f} ms)")
    print("="*80 + "\n")
    
    return timings, profiler


if __name__ == '__main__':
    # 从缓存文件加载数据
    import os
    
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cache_file = os.path.join(script_dir, 'danmaku_cache.txt')
    
    # 如果当前目录找不到，尝试在脚本目录查找
    if not os.path.exists(cache_file):
        # 尝试当前工作目录
        cache_file = 'danmaku_cache.txt'
    
    if os.path.exists(cache_file):
        print(f"正在加载数据文件: {cache_file}")
        with open(cache_file, 'r', encoding='utf-8') as f:
            danmaku_list = [line.strip() for line in f if line.strip()]
        
        if danmaku_list:
            print(f"成功加载 {len(danmaku_list)} 条弹幕数据\n")
            analyze_data_processor_performance(danmaku_list)
        else:
            print("缓存文件为空，无法进行性能分析")
    else:
        print(f"未找到缓存文件: {cache_file}")
        print("请先运行主程序 (python main.py) 获取数据")
        print(f"或者将 danmaku_cache.txt 放在以下位置之一:")
        print(f"  1. 当前工作目录: {os.getcwd()}")
        print(f"  2. 脚本所在目录: {script_dir}")

