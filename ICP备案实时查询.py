import requests
import tkinter as tk
import threading

def get_icp():
    url = 'http://api.aiweikou.com/api/icp'
    params = {
            "key":"", //在这里输入你在API网站注册的key，这里推荐上面提供的网站，也可以使用其它网站
            "url":url_entry.get()
        }
    # 将网络请求放到子线程中执行
    t = threading.Thread(target=requests_get, args=(url,params))
    t.start()

def requests_get(url,params):
    try:
        response = requests.get(url,params=params,timeout=60)
        result = response.json()
        # 在主线程中更新界面
        window.after(0, update_ui, response.status_code, result)
    except Exception as ex:
        window.after(0, update_ui, None, ex)

def update_ui(status_code, result):
    if status_code:
        status_label.config(text="HTTP请求状态码: %s" %(status_code))
        result_text.delete('1.0', tk.END)  # 清空文本框
        for key, value in result.items():
            result_text.insert(tk.END, str(key) + ': ' + str(value) + '\n')  # 在文本框中逐行显示查询结果
    else:
        status_label.config(text="系统异常：{}".format(result))

# 创建窗口
window = tk.Tk()
window.title("ICP备案查询工具")
window.geometry('600x400')

# 创建控件
url_label = tk.Label(window, text="URL:")
url_entry = tk.Entry(window)
status_label = tk.Label(window)
result_label = tk.Label(window, text="查询结果:")
result_text = tk.Text(window, height=10, width=50)
query_button = tk.Button(window, text="查询", command=get_icp)

# 布局控件
url_label.grid(row=0, column=0)
url_entry.grid(row=0, column=1)
query_button.grid(row=1, column=0, columnspan=2)
status_label.grid(row=2, column=0, columnspan=2)
result_label.grid(row=3, column=0)
result_text.grid(row=3, column=1)

# 运行窗口
window.mainloop()