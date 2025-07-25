# import RPi.GPIO as GPIO
from flask import Flask, render_template, request, redirect, url_for, session
import secrets
#print(secrets.token_hex(32)) # app.secret_key에 문자열 넣으면 secrets.token_kex(32) 필요없음

app = Flask(__name__) # 한곳에서만 설정하고 다른 파일에서는 불러오기

app.secret_key = '652a5a1a538576b37d504d971d17bde7b9fc4ea9161d0f08b058c44f1595a25d'  

# 회사 홍보 이미지랑 우측 상단에 로그인 하러 가기 누르면 /login 페이지로 이동 -> 구현
@app.route('/home')
def home():
    return render_template('home.html')            
    
@app.route('/login', methods=['GET','POST']) # Flask는 get,post 둘다 대문자
def login():
    if request.method == 'POST':
    # id/pw 처리
        id = request.form['id'] 
        pw = request.form['pw']
        if id == 'admin' and pw == '1234':
            session['logged_in'] = True
            
            # return redirect('/home.html') # Flask는 html 파일경로 직접 리디렉션 안함
            return redirect(url_for('dashboard'))
        else: 
            return "<script>alert('로그인 실패!'); location.href='/login';</script>"
       
    # 로그인 화면(get)
    else:
        return render_template('login.html')
            
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == "__main__":
    from dashboard import *
    app.run(host='0.0.0.0', port=5000)
