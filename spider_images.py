from icrawler.builtin import BaiduImageCrawler
import os

# 1. 针对百度图库优化的中文关键词字典
search_queries = {
    "Halal": ["清真 牛肉干 包装袋", "清真 方便面 实拍", "Halal chicken nuggets box"],
    "Organic": ["有机 纯牛奶 包装盒", "有机 燕麦片 包装", "USDA organic cereal"],
    "Recyclable": ["可口可乐 环保标志 瓶身", "矿泉水瓶 可回收标志 实拍", "纸盒 循环利用标志"]
}

# 2. 设置新的下载目录，和之前的区分开
base_dir = "raw_images_baidu"
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

# 3. 开始循环抓取
for category, keywords in search_queries.items():
    save_dir = os.path.join(base_dir, category)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for keyword in keywords:
        print(f"========== 正在使用百度抓取关键词: {keyword} ==========")
        # 换成百度引擎，对国内网络极其友好
        crawler = BaiduImageCrawler(
            storage={'root_dir': save_dir},
            downloader_threads=4
        )

        # 开始下载
        crawler.crawl(
            keyword=keyword,
            max_num=60,  # 每个关键词最多抓取 60 张
            file_idx_offset='auto'
        )

print("🎉 百度图库抓取完成！请前往 raw_images_baidu 文件夹查看。")