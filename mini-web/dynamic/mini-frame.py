import time
import re
from pymysql import *


STASUS_ROOT = "./templates"

url = dict()


def route(temp):
    def set_func(func):
        # 添加文件对应的函数名到字典
        url[temp] = func
        def call_func(file_name):
            return func(file_name)
        return call_func
    return set_func


@route(r"/index\.html$")
def index(file_name, url):
    # file_name = file_name.replace(".py", ".html")
    try:
        f = open(STASUS_ROOT+file_name)
    except Exception as result:
        print(result)
    else:
        # 读取body数据，返回给服务器的调用
        content = f.read()
        # 获取connection对象
        conn = connect(host='localhost', port=3306, user='root', password='mysql',database='stock_db', charset='utf8')
        # 获取cursor对象
        cursor = conn.cursor()
        sql = """select * from info;"""
        cursor.execute(sql)
        data = cursor.fetchall()  # 获取的数据信息是元祖信息
        cursor.close()
        conn.close()

        html_str = """  
                    <tr>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>
                            <input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="000039">
                        </td>
                    </tr>""" 
        html = ""
        for temp in data:
            html += html_str % (temp[0],temp[1],temp[2],temp[3],temp[4],temp[5],temp[6],temp[7])

        content = re.sub(r"\{%content%\}", html, content)
        return content


@route(r"/center\.html$")
def center(file_name):
    # file_name = file_name.replace(".py", ".html")
    try:
        f = open(STASUS_ROOT + file_name)
    except Exception as result:
        print(result)
    else:
        # 读取body数据，返回给服务器的调用
        content = f.read()
        # 获取connection对象
        conn = connect(host='localhost', port=3306, user='root', password='mysql',database='stock_db', charset='utf8')
        # 获取cursor对象
        cursor = conn.cursor()
        sql = """select i.code,i.short,i.chg,i.turnover,i.price,i.highs,f.note_info from info as i inner join focus as f on i.id=f.info_id;"""
        cursor.execute(sql)
        data = cursor.fetchall()  # 获取的数据信息是元祖信息
        cursor.close()
        conn.close()
        html_str = """  
                    <tr>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>
                            <a type="button" class="btn btn-default btn-xs" href="/update/300280.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
                        </td>
                        <td>
                            <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="300280">
                        </td>
                    </tr>""" 
        html = ""
        for temp in data:
            html += html_str % (temp[0],temp[1],temp[2],temp[3],temp[4],temp[5],temp[6])

        content = re.sub(r"\{%content%\}", html, content)
        return content


def app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    file_name = environ["PATH_INFO"]
    try:
        # url = {r"/index\.html$": index,
        #     r"/center\.html$": center,
        #     r"/add/\d+\.html$": add} 字典里保存着文件与对应函数名
        for url, func in url.items():
            ret = re.match(url, file_name)
            if ret:
                return func(file_name, url)
        else:
            return "请求有误"
    except Exception as ret:
        return "产生了异常。。。异常信息是：%s, 时间是：%s" % (str(ret), str(time.ctime()))
