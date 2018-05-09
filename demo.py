import urllib.request,time
import requests

def getHtml(url,data=None):
    """返回一个html原生数据，未使用read()方法，当访问url报错时，返回为None"""
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agnet', "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/48.0.2564.116 Safari/537.36")
        req.add_header('Referer', "http://www.fcw46.com/videos/21869/1080p51/")
        req.add_header('Cookie', "PHPSESSID=0datsd3jk94q27rhqe6vgev3t2; kt_is_visited=1; kt_tcookie=1; kt_tcookie=1")
        html = urllib.request.urlopen(req,data,timeout=5)
        print("get html origin successfully")
        time.sleep(0.1)
        return html
    except Exception as e:
        print("visit picture url Error:"+str(e))
        time.sleep(0.1)
        return None

if __name__ == "__main__":
    data = {"username":"ck1518","pass":"ck1518","pass2":"ck1518","email":"ck1518%40hs.com","code":"58763",\
            "action":"signup","email_link":"http%3A%2F%2Fwww.fcw46.com%2Femail%2F&format=json&mode=async"}
    headers = {'User-Agnet':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/48.0.2564.116 Safari/537.36",
               'Referer':"http://www.fcw46.com/videos/21869/1080p51/",
               'Cookie':"PHPSESSID=0datsd3jk94q27rhqe6vgev3t2; kt_is_visited=1; kt_tcookie=1; kt_tcookie=1"}
    login_url = "http://www.fcw46.com/signup/"
    captcha_url = "http://www.fcw46.com/captcha/signup/?rand=1523759838"
    # print(getHtml(captcha_url))
    # print(getHtml(login_url,data).read().decode())
    # print(requests.post(login_url,data))

