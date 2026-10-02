# 数据采集与分析工具

## 功能
- 输入网址，自动爬取网页数据
- 支持多页爬取
- 表格展示数据
- 导出 Excel
- 生成价格分布图

## 使用方法
1. 运行 `main.py`
2. 输入要爬取的网址
3. 勾选“多页”可爬取多页
4. 点击“开始爬取”
5. 在弹出窗口中选择“导出 Excel”或“画价格分布图”

## 文件说明
- `main.py`：主程序，GUI 界面
- `spider.py`：爬虫逻辑
- `processor.py`：数据处理和导出

## 依赖
- requests
- beautifulsoup4
- pandas
- matplotlib
- openpyxl