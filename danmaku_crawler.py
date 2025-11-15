"""
B站弹幕爬虫模块
使用requests和BeautifulSoup爬取B站视频弹幕数据
"""
import requests
import json
import time
import re
import random
from urllib.parse import quote
from typing import List, Dict
from bs4 import BeautifulSoup


class BilibiliDanmakuCrawler:
    def __init__(self):
        self.session = requests.Session()
        # 更完整的浏览器请求头
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Referer': 'https://www.bilibili.com/',
            'Origin': 'https://www.bilibili.com',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        })
        self.base_url = 'https://www.bilibili.com'
        self.search_url = 'https://api.bilibili.com/x/web-interface/search/type'
        
        # 初始化时访问主页获取cookies
        self._init_session()
    
    def _init_session(self):
        """
        初始化session，访问主页获取必要的cookies
        """
        try:
            print("正在初始化连接...")
            response = self.session.get(self.base_url, timeout=10)
            if response.status_code == 200:
                print("连接初始化成功")
            time.sleep(1)  # 等待一下
        except Exception as e:
            print(f"初始化连接时出错: {e}")
        
    def search_videos(self, keyword: str, max_videos: int = 300) -> List[Dict]:
        """
        搜索相关视频，返回视频信息列表
        """
        videos = []
        page = 1
        page_size = 20
        
        print(f"开始搜索关键词: {keyword}")
        
        while len(videos) < max_videos:
            params = {
                'search_type': 'video',
                'keyword': keyword,
                'page': page,
                'pagesize': page_size,
                'order': 'totalrank'  # 综合排序
            }
            
            try:
                # 随机延迟，模拟人类行为
                time.sleep(random.uniform(1.5, 3.0))
                
                # 更新Referer为搜索页面（URL编码关键词）
                encoded_keyword = quote(keyword)
                self.session.headers.update({
                    'Referer': f'https://www.bilibili.com/search?keyword={encoded_keyword}'
                })
                
                response = self.session.get(self.search_url, params=params, timeout=15)
                
                # 检查响应状态
                if response.status_code == 412:
                    print(f"请求被B站封禁（状态码412）")
                    print("提示: B站检测到自动化请求。建议：")
                    print("  1. 等待几分钟后重试")
                    print("  2. 检查网络连接")
                    print("  3. 考虑使用浏览器手动访问获取cookies")
                    # 尝试等待后重试一次
                    if page == 1:
                        print("等待5秒后重试...")
                        time.sleep(5)
                        continue
                    break
                elif response.status_code != 200:
                    print(f"搜索请求失败，状态码: {response.status_code}")
                    try:
                        error_data = response.json()
                        print(f"错误信息: {error_data.get('message', '未知错误')}")
                    except:
                        print(f"响应内容: {response.text[:200]}")
                    break
                
                # 检查响应内容类型
                if not response.text or not response.text.strip():
                    print(f"搜索响应为空")
                    break
                
                # 检查是否为JSON格式
                try:
                    data = response.json()
                except json.JSONDecodeError as json_err:
                    print(f"JSON解析失败: {json_err}")
                    print(f"响应内容前500字符: {response.text[:500]}")
                    break
                
                if data.get('code') != 0:
                    print(f"搜索出错: {data.get('message', '未知错误')}, code: {data.get('code')}")
                    break
                    
                result = data.get('data', {}).get('result', [])
                if not result:
                    print(f"第 {page} 页没有更多结果")
                    break
                    
                for item in result:
                    if len(videos) >= max_videos:
                        break
                    videos.append({
                        'bvid': item.get('bvid', ''),
                        'title': item.get('title', ''),
                        'aid': item.get('aid', 0),
                        'view': item.get('play', 0),
                        'danmaku': item.get('video_review', 0)
                    })
                
                print(f"已获取 {len(videos)} 个视频信息...")
                page += 1
                # 页面之间的延迟已经在请求前添加
                
            except requests.RequestException as e:
                print(f"搜索请求异常: {e}")
                break
            except Exception as e:
                print(f"搜索过程出错: {e}")
                break
                
        return videos[:max_videos]
    
    def get_cid(self, bvid: str) -> int:
        """
        根据BV号获取cid（弹幕文件ID）
        """
        url = f"https://api.bilibili.com/x/player/pagelist?bvid={bvid}"
        try:
            response = self.session.get(url, timeout=10)
            data = response.json()
            if data.get('code') == 0:
                pages = data.get('data', [])
                if pages:
                    return pages[0].get('cid', 0)
        except Exception as e:
            print(f"获取cid失败 {bvid}: {e}")
        return 0
    
    def get_danmaku(self, cid: int) -> List[str]:
        """
        获取指定cid的弹幕数据
        """
        url = f"https://api.bilibili.com/x/v1/dm/list.so?oid={cid}"
        danmaku_list = []
        
        try:
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            
            # 解析XML格式的弹幕
            soup = BeautifulSoup(response.text, 'xml')
            d_elements = soup.find_all('d')
            
            for d in d_elements:
                text = d.get_text().strip()
                if text:
                    danmaku_list.append(text)
                    
        except Exception as e:
            print(f"获取弹幕失败 cid={cid}: {e}")
            
        return danmaku_list
    
    def crawl_danmaku(self, keywords: List[str], max_videos: int = 300) -> List[str]:
        """
        爬取多个关键词相关的视频弹幕
        """
        all_danmaku = []
        processed_bvids = set()
        
        for keyword in keywords:
            print(f"\n处理关键词: {keyword}")
            videos = self.search_videos(keyword, max_videos)
            
            for i, video in enumerate(videos, 1):
                bvid = video['bvid']
                if bvid in processed_bvids:
                    continue
                processed_bvids.add(bvid)
                
                print(f"[{i}/{len(videos)}] 处理视频: {video['title'][:50]}")
                
                cid = self.get_cid(bvid)
                if cid:
                    danmaku = self.get_danmaku(cid)
                    all_danmaku.extend(danmaku)
                    print(f"  获取到 {len(danmaku)} 条弹幕")
                    time.sleep(0.5)  # 避免请求过快
                else:
                    print(f"  无法获取cid")
                    
        return all_danmaku


if __name__ == '__main__':
    crawler = BilibiliDanmakuCrawler()
    keywords = ['大语言模型', '大模型', 'LLM']
    danmaku = crawler.crawl_danmaku(keywords, max_videos=300)
    print(f"\n总共获取 {len(danmaku)} 条弹幕")

