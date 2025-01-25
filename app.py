from flask import Flask,request,render_template,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/request",methods=["POST","GET"])
def datas():
    if request.method == "POST":
        try:
            input = request.form["input"].replace(" ","")
            url = "https://www.amazon.in/s?k="+input
            amazon_page = requests.get(url)
            if amazon_page.status_code == 200:
                amazon_page_bs = bs(amazon_page.text,"html.parser")
                phones = amazon_page_bs.findAll("div",{"class":"s-main-slot"})
                if phones and len(phones) > 0:
                    ind_phone = phones[0].findAll("div",{"class":"sg-col-20-of-24"})
                    datas = []
                    for i in ind_phone:
                        try:
                            names = i.findAll("h2",{"class":"a-size-medium"})[0].text
                        except:
                            names = "no name"
                        try:
                            price = i.findAll("span",{"class":"a-price-whole"})[0].text
                        except:
                            price = "no price"
                        try:
                            reviews = i.findAll("span",{"class":"a-size-base"})[0].text
                        except:
                            reviews = "no reviews"
                        try:
                            buyers = i.findAll("div",{"class":"a-row a-size-base"})[0].span.text
                        except:
                            buyers = "No data"
                        dic = {"Name" : names, "Price":price, "Review" : reviews,"Buyers":buyers}
                        datas.append(dic)
                    return render_template("result.html", datas = datas)
                else:
                    return "No products found."
            else:
                return render_template("index.html")
        except Exception as e:
            print("exception is ",e)
    else:
        return "problem in post method"

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=5000)