from threading import Thread
from flask import Flask
import os

# Створюємо Flask додаток для keep-alive
app = Flask('')

@app.route('/')
def home():
    """
    Головна сторінка для перевірки статусу бота
    """
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ukrainian Telegram Bot Status</title>
        <meta charset="UTF-8">
        <style>
            body { 
                font-family: Arial, sans-serif; 
                text-align: center; 
                padding: 50px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container { 
                background: rgba(255,255,255,0.1); 
                padding: 30px; 
                border-radius: 10px; 
                max-width: 500px; 
                margin: 0 auto;
            }
            .status { 
                color: #4CAF50; 
                font-size: 24px; 
                font-weight: bold; 
            }
            .flag { font-size: 50px; margin: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="flag">🇺🇦</div>
            <h1>Ukrainian Telegram Bot</h1>
            <p class="status">✅ Bot is running</p>
            <p>Бот працює та готовий обробляти скріншоти!</p>
            <hr style="border-color: rgba(255,255,255,0.3); margin: 20px 0;">
            <p><small>Keep-alive server active</small></p>
        </div>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    """
    Endpoint для перевірки здоров'я бота
    """
    return {
        "status": "healthy",
        "message": "Ukrainian Telegram Bot is running",
        "bot_active": True
    }

def run():
    """
    Запуск Flask сервера для keep-alive
    """
    # Використовуємо порт 5000 для frontend відповідно до вимог
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

def keep_alive():
    """
    Запуск keep-alive сервера в окремому потоці
    """
    t = Thread(target=run)
    t.daemon = True
    t.start()
    print(f"Keep-alive server started on port 5000")
