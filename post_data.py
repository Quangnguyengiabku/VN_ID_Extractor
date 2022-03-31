import requests
from requests.structures import CaseInsensitiveDict
# defining the api-endpoint 
#API_ENDPOINT = "http://pastebin.com/api/api_post.php"
def post_data(data):
    password={
        "USERNAME": "91999.VNCARE",
        "PASSWORD": "His@2016",
        "HOSPITALID": "91999"
    }
    # your API key here
    #API_KEY = "XXXXXXXXXXXXXXXXX"
    response = requests.post("https://bvdkkiengiang.vnpthis.vn/web_his/api/gettoken",json=password)
    #print(response.text)
    key=[]
    for x in range(len(response.text)):
        if response.text[x:x+12]=='access_token':
            for y in range(x+15,len(response.text)):
                if response.text[y]=='"':
                    key=response.text[x+15:y]
                    break
            break
    Authorization='Bearer '+key
    #print('Bearer '+key)
    headers = CaseInsensitiveDict()
    #data='{'+str(data)+'}'
    #print(data)
    headers["Accept"] = "application/json"
    headers["Authorization"] = Authorization
    post_data=requests.post("https://bvdkkiengiang.vnpthis.vn/web_his/api/tiepnhancmnd",headers=headers,json=data)
    # your source code here
    print('Response',post_data)
    print(post_data.text)
if __name__=="__main__":
    data={"SOCMND":"371370987","HO_TEN":"Trần Hoàng Gia Quang","NGAY_SINH":"30/04/1992","GIOI_TINH":"Nam","DIA_CHI":"487 Nguyễn Trung Trực, phường Vĩnh Lạc, tp Rạch Giá, tỉnh Kiên Giang","DAN_TOC":"Kinh","QUOC_TICH":"Việt Nam","NGAY_CAP":"01/01/2010","NOI_CAP":"CA Kiên Giang"}
    post_data(data)


  
