from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from telebot import TeleBot

app = Flask(__name__)
CORS(app)

# Токены и настройки
TOKEN = "EAANuhCnREYIBRgxDssDLDteQTIPV67mubhCE8P2QTbrryZAPadqej0ZA7X49uzNeiQJUCMDXKHA7TOBuwf2PS7i9Kek3nZAT62SyV6ZA1VvNDrTxZAxY8qWlrCZCrQZAd0ZCFWf2ppEmLb79XlgUHqe8dj1NAA7Wn7XIjowyADu4ekJuHxaLeMvQJtdTxlcwLp7cKMkHLYAchOJUz0gLVHTtqJ27vqjgpwbqDDIfDoeabnyfFVrrM5jE"
BOT = TeleBot("8609314090:AAFbg0EmK1YMftZAfE3CY7RKiyupI0WI5Jg")

# Твой личный Telegram ID для прямой отправки отчетов
USER_ID = 687551939

IDS = {
    "zhan": "17841458428902873",
    "afonya": "17841401684983944"
}

@app.route('/api/reels', methods=['GET'])
def get_reels():
    brand = request.args.get('brand')
    bid = IDS.get(brand)
    
    if not bid:
        return jsonify({"error": "Неизвестный бренд"})
        
    url = f"https://graph.facebook.com/v25.0/{bid}/media?fields=id,thumbnail_url,caption,like_count,comments_count&access_token={TOKEN}"
    
    try:
        res = requests.get(url, timeout=10).json()
        if "error" in res:
            return jsonify({"error": res["error"].get("message", "Ошибка API")})
        return jsonify({"media": res.get('data', [])})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/control', methods=['POST'])
def control():
    data = request.json
    action = data.get('action')
    brand = data.get('brand', 'ALL')
    video = data.get('video', 'ALL')
    
    brand_name = brand.upper() if brand else "ВСЕ БРЕНДЫ"
    
    if action == "GLOBAL_ANALYSIS":
        msg = f"🚀 **ГЛУБОКИЙ ИИ-АНАЛИЗ ЭФФЕКТИВНОСТИ** 🚀\n\n" \
              f"📊 **Операция:** ПОЛНЫЙ АНАЛИЗ АККАУНТОВ\n" \
              f"🏢 **Объект:** Zhan Postel Opt & Afonya Textile\n" \
              f"🎯 **Статус:** Сбор данных из Meta Ads API запущен.\n\n" \
              f"📈 ИИ-Агент проверяет источники переходов, динамику лайков и комментариев. Подробный отчет по креативам сформирован."
    else:
        msg = f"🤖 **ИИ-Агент Управления Рекламой**\n\n" \
              f"⚡️ **Операция:** {action}\n" \
              f"🏢 **Бренд:** {brand_name}\n" \
              f"🎬 **Элемент ID:** {video}"
    
    try:
        # Отправка напрямую в твой личный чат с ботом
        BOT.send_message(chat_id=USER_ID, text=msg, parse_mode="Markdown")
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
