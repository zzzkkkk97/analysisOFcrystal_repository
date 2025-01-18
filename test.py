import requests
import re
import csv
import time

# 设置目标 URL
base_url = "https://github.com/crystal-lang/crystal/issues?page={}"

headers = {
    'Cookie': '_device_id=4fa68362950d4d06252c186eaad61d85; _octo=GH1.1.549837167.1736940028; saved_user_sessions=187375867%3AIUsH8ag-p_jicReXL3fgh2NEynKEClXAta4lRW9NOIYjp8_J; user_session=IUsH8ag-p_jicReXL3fgh2NEynKEClXAta4lRW9NOIYjp8_J; __Host-user_session_same_site=IUsH8ag-p_jicReXL3fgh2NEynKEClXAta4lRW9NOIYjp8_J; logged_in=yes; dotcom_user=xiaoyucodequeen; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; cpu_bucket=xlg; preferred_color_mode=dark; tz=Asia%2FShanghai; _gh_sess=R4oZPumE2ozdFyeDlinh%2FkUeMKGqsxKWvJmyZRQr4L9cJaxN9XHOehx7JUqF5e52sbnIkvwdxxquSH7MMySuZEc%2FWZtogBR85kaq8WVjgR4Aygs93pAI9xdKVs8LtJAKi0JDntxdztGfcuR611oaBjoYl33dh4FvKXza9NxmGw8llOyyQGSisL1vDM4Cz8njsN%2F6QXoE7VXwh%2BXDy7aV7zrFEmyOwd1Qvr8BeiTwcqHCbh549KpwIMywhWNSRO0i%2BxNutZI1zuBsusvv388Fa8iS%2BaEZ3J0QsH4YmWDOgsA9nuteu04ik6rDcQVEK4VxAWYzB6bjVl%2BFg8BcqMEoSLVPDA6UJpGB2speudf7w4sVy5zflzvk3%2BG70zo2%2BnWH%2FR6qJqn%2Bs5TEiv48ypW%2FKbKSUKg%3D--QyIaHK4UzwjzpghW--%2BFUuMXV7jiZiVHQbkUV%2F0w%3D%3D',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
}

# 存储数据
data = []

# 循环爬取每一页
for page in range(1, 21):  # 页码范围从1到20
    print(f"正在爬取第 {page} 页...")
    url = base_url.format(page)

    # 发送 GET 请求
    response = requests.get(url=url, headers=headers, verify=False)

    if response.status_code != 200:
        print(f"请求失败，状态码: {response.status_code}")
        continue

    content = response.content.decode('utf8')

    update_content_temp = re.findall('<span class="Text__StyledText-sc-17v1xeu-0 hWqAbU">(.*?)</span>', content, re.DOTALL)
    update_type = re.findall(
        '<div class="Box-sc-g0xbh4-0 TrailingBadge-module__container--gg6pc" data-listview-component="trailing-badge">.*?<span class="Text__StyledText-sc-17v1xeu-0 hWqAbU">(.*?)</span>',
        content, re.DOTALL)
    update_content = list(set(update_content_temp)-set(update_type))
    view_count = re.findall('<span class="issue-item-module__defaultNumberDescription--GXzri">.*?<!.*?>(.*?)</span>',
                            content, re.DOTALL)
    update_time = re.findall('<relative-time class="sc-aXZVg".*?<!.*?>(.*?)</relative-time>', content, re.DOTALL)

    for i in range(len(update_content)):
        data.append({
            'Update Content': update_content[i],
            'Update Type': update_type[i] if i < len(update_type) else None,
            'View Count': view_count[i] if i < len(view_count) else None,
            'Update Time': update_time[i] if i < len(update_time) else None,
        })

    time.sleep(1)  # 延迟1秒以避免过于频繁的请求

# 将数据写入 CSV 文件
with open('issues_data.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Update Content', 'Update Type', 'View Count', 'Update Time']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for row in data:
        writer.writerow(row)

print("数据爬取完毕，已保存至 issues_data.csv。")
