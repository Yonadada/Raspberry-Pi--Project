from flask import Flask, render_template, request, url_for, session, redirect, jsonify
from login import app # login.py에 있는 app객체를 가져옴
from sensor import read_temp_humid
from sensor import blink_led
from gpio_config import LED_PINS

import time
import threading
import RPi.GPIO as GPIO
import board    # 라즈베리파이 GPIO 핀 제어


# 관리자 허용 여부(관리자 스위치)
LED_ENABLED = True
# LED 깜빡임 상태를 나타내는 플래그 변수 (기본값: OFF)
is_led_blinking = False


# 대시보드 진입 시 기본 LED 깜빡임 시작 (로그인한 사용자에 한함)
@app.route('/dashboard')
def dashboard():
    # 로그인 안 한 경우 → 팝업 띄우고 로그인 페이지로 이동
    if not session.get('logged_in'):
        return '''
            <script>
                alert("로그인이 필요합니다!")
                window.location.href = "/login";
            </script>
        '''
    global is_led_blinking
    if not session.get('logged_in'):
        return redirect('/login')
    
    # 대시보드 들어올 때 기본적으로 led 켜기
    if not is_led_blinking:
        is_led_blinking = True
        threading.Thread(target=blink_led, daemon=True).start()
    
    # 부저도 켜져 있어야함 
    # ----로직 작성----
                    
    # ✅ 로그인한 사용자만 여기에 도달함!
    return render_template("dashboard.html")
 
# =====================
# 대시보드에서 주기적으로 호출되는 센서 데이터 API
# 로그인된 사용자에게만 응답하며, 온도 및 습도 값을 JSON으로 반환함       
@app.route('/dashboard/data')
def dashboard_data():
    if not session.get('logged_in'):
        return {"Error" : "허용되지 않은 접근"}, 401
    
    result = read_temp_humid()
    return jsonify(result)
# =====================



# LED 수동 제어 요청 처리 (ON: 깜빡임 시작, OFF: 즉시 중지)
@app.route("/dashboard/led")
def led_switch_handler():
    global is_led_blinking
    
    #요청 파라미터 가져오기
    state = request.args.get("state") # on 또는 off
    
    if state == "on":
        if not is_led_blinking:
            is_led_blinking = True
            threading.Thread(target=blink_led, daemon=True).start()
        return jsonify({"result" : "LED 깜빡임 시작"})
    
    elif state == "off":
        is_led_blinking = False
        GPIO.output(LED_PINS["red"], GPIO.LOW)
        GPIO.output(LED_PINS["blue"], GPIO.LOW)
        GPIO.output(LED_PINS["green"], GPIO.LOW)
        return jsonify({"result" : "LED 깜빡임 중지"})
    
    else:
        return jsonify({"error" : "잘못된 요청입니다"}), 400
    
    
# 부저 제어 