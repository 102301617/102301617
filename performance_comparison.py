"""
性能对比测试脚本
对比原始版本和优化版本的性能差异
"""
import time
from data_processor import DanmakuProcessor
from data_processor_optimized import DanmakuProcessorOptimized

# 尝试导入matplotlib（可选依赖）
try:
    import matplotlib.pyplot as plt
    import matplotlib
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
    # 设置中文字体
    matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
    matplotlib.rcParams['axes.unicode_minus'] = False
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("警告: matplotlib未安装，将无法生成可视化图表。")
    print("可以运行 'pip install matplotlib numpy' 来安装。")
    print("性能对比数据仍将正常输出。\n")


def load_test_data():
    """加载测试数据"""
    import os
    
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cache_file = os.path.join(script_dir, 'danmaku_cache.txt')
    
    # 如果当前目录找不到，尝试在脚本目录查找
    if not os.path.exists(cache_file):
        # 尝试当前工作目录
        cache_file = 'danmaku_cache.txt'
    
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    return []


def benchmark_function(func, *args, iterations=5):
    """基准测试函数"""
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        result = func(*args)
        end = time.perf_counter()
        times.append((end - start) * 1000)  # 转换为毫秒
    return result, np.mean(times), np.std(times)


def compare_performance():
    """对比原始版本和优化版本的性能"""
    print("="*80)
    print("性能对比测试")
    print("="*80)
    
    # 加载测试数据
    danmaku_list = load_test_data()
    if not danmaku_list:
        print("未找到测试数据，请先运行主程序")
        return
    
    print(f"\n测试数据量: {len(danmaku_list)} 条弹幕\n")
    
    # 创建处理器实例
    processor_original = DanmakuProcessor()
    processor_optimized = DanmakuProcessorOptimized()
    
    # 测试结果
    results = {}
    
    # 1. 测试 filter_danmaku
    print("测试 filter_danmaku 函数...")
    _, orig_time, orig_std = benchmark_function(
        processor_original.filter_danmaku, danmaku_list
    )
    _, opt_time, opt_std = benchmark_function(
        processor_optimized.filter_danmaku, danmaku_list
    )
    results['filter_danmaku'] = {
        'original': orig_time,
        'optimized': opt_time,
        'improvement': ((orig_time - opt_time) / orig_time * 100)
    }
    print(f"  原始版本: {orig_time:.2f} ± {orig_std:.2f} ms")
    print(f"  优化版本: {opt_time:.2f} ± {opt_std:.2f} ms")
    print(f"  提升: {results['filter_danmaku']['improvement']:.1f}%\n")
    
    # 2. 测试 is_noise (1000次)
    print("测试 is_noise 函数 (1000次调用)...")
    test_texts = danmaku_list[:1000]
    _, orig_time, orig_std = benchmark_function(
        lambda: [processor_original.is_noise(text) for text in test_texts]
    )
    _, opt_time, opt_std = benchmark_function(
        lambda: [processor_optimized.is_noise(text) for text in test_texts]
    )
    results['is_noise'] = {
        'original': orig_time,
        'optimized': opt_time,
        'improvement': ((orig_time - opt_time) / orig_time * 100)
    }
    print(f"  原始版本: {orig_time:.2f} ± {orig_std:.2f} ms")
    print(f"  优化版本: {opt_time:.2f} ± {opt_std:.2f} ms")
    print(f"  提升: {results['is_noise']['improvement']:.1f}%\n")
    
    # 3. 测试 count_word_frequency
    print("测试 count_word_frequency 函数...")
    filtered_orig = processor_original.filter_danmaku(danmaku_list)
    filtered_opt = processor_optimized.filter_danmaku(danmaku_list)
    _, orig_time, orig_std = benchmark_function(
        processor_original.count_word_frequency, filtered_orig, 8
    )
    _, opt_time, opt_std = benchmark_function(
        processor_optimized.count_word_frequency, filtered_opt, 8
    )
    results['count_word_frequency'] = {
        'original': orig_time,
        'optimized': opt_time,
        'improvement': ((orig_time - opt_time) / orig_time * 100)
    }
    print(f"  原始版本: {orig_time:.2f} ± {orig_std:.2f} ms")
    print(f"  优化版本: {opt_time:.2f} ± {opt_std:.2f} ms")
    print(f"  提升: {results['count_word_frequency']['improvement']:.1f}%\n")
    
    # 4. 测试 get_all_stats (整体)
    print("测试 get_all_stats 函数 (整体)...")
    _, orig_time, orig_std = benchmark_function(
        processor_original.get_all_stats, danmaku_list
    )
    _, opt_time, opt_std = benchmark_function(
        processor_optimized.get_all_stats, danmaku_list
    )
    results['get_all_stats'] = {
        'original': orig_time,
        'optimized': opt_time,
        'improvement': ((orig_time - opt_time) / orig_time * 100)
    }
    print(f"  原始版本: {orig_time:.2f} ± {orig_std:.2f} ms")
    print(f"  优化版本: {opt_time:.2f} ± {opt_std:.2f} ms")
    print(f"  提升: {results['get_all_stats']['improvement']:.1f}%\n")
    
    # 生成对比图表
    visualize_comparison(results)
    
    # 打印总结
    print("="*80)
    print("性能对比总结")
    print("="*80)
    print(f"{'函数名':<30} {'原始版本 (ms)':<15} {'优化版本 (ms)':<15} {'提升 (%)':<10}")
    print("-"*80)
    for func_name, data in results.items():
        print(f"{func_name:<30} {data['original']:<15.2f} {data['optimized']:<15.2f} {data['improvement']:<10.1f}")
    print("="*80)
    
    return results


def visualize_comparison(results):
    """可视化性能对比"""
    if not MATPLOTLIB_AVAILABLE:
        return
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    functions = list(results.keys())
    orig_times = [results[f]['original'] for f in functions]
    opt_times = [results[f]['optimized'] for f in functions]
    improvements = [results[f]['improvement'] for f in functions]
    
    x = np.arange(len(functions))
    width = 0.35
    
    # 子图1: 执行时间对比柱状图
    bars1 = ax1.bar(x - width/2, orig_times, width, label='原始版本', color='#4472C4', alpha=0.8)
    bars2 = ax1.bar(x + width/2, opt_times, width, label='优化版本', color='#70AD47', alpha=0.8)
    
    ax1.set_xlabel('函数名称', fontsize=12, fontweight='bold')
    ax1.set_ylabel('执行时间 (ms)', fontsize=12, fontweight='bold')
    ax1.set_title('原始版本 vs 优化版本执行时间对比', fontsize=14, fontweight='bold', pad=20)
    ax1.set_xticks(x)
    ax1.set_xticklabels(functions, rotation=15, ha='right')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # 添加数值标签
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}',
                    ha='center', va='bottom', fontsize=9)
    
    # 子图2: 性能提升百分比
    colors = ['#FF6B6B' if imp < 10 else '#4ECDC4' if imp < 20 else '#95E1D3' 
              for imp in improvements]
    bars = ax2.barh(functions, improvements, color=colors, alpha=0.8)
    ax2.set_xlabel('性能提升 (%)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('函数名称', fontsize=12, fontweight='bold')
    ax2.set_title('性能提升百分比', fontsize=14, fontweight='bold', pad=20)
    ax2.grid(axis='x', alpha=0.3)
    
    # 添加数值标签
    for i, (bar, imp) in enumerate(zip(bars, improvements)):
        ax2.text(imp + max(improvements)*0.02, bar.get_y() + bar.get_height()/2,
                f'{imp:.1f}%', va='center', fontsize=10, fontweight='bold')
    
    # 添加零线
    ax2.axvline(x=0, color='black', linestyle='--', linewidth=1)
    
    plt.tight_layout()
    plt.savefig('performance_comparison.png', dpi=300, bbox_inches='tight')
    print(f"\n性能对比图已保存到: performance_comparison.png")
    plt.close()


if __name__ == '__main__':
    compare_performance()

