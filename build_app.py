import json
import os

with open(r"c:\Curso Cejas\BELLA_QUIZ_WEB\questions_data_20.json", encoding="utf-8") as f:
    questions = json.load(f)

questions_json_str = json.dumps(questions, ensure_ascii=False)

import base64, io
from PIL import Image

ASSETS = r"c:\Curso Cejas\BELLA_QUIZ_WEB\assets"

def _data_uri(img, fmt, mime, **kw):
    buf = io.BytesIO()
    img.save(buf, fmt, **kw)
    return "data:%s;base64,%s" % (mime, base64.b64encode(buf.getvalue()).decode("ascii"))

# Background: crop to A4 ratio (1.414) and upscale for crisp 2x PDF capture
_bg = Image.open(os.path.join(ASSETS, "bg_spiral_gold.jpg")).convert("RGB")
_w, _h = _bg.size
_cw = int(_h * 1123 / 794)
_x0 = (_w - _cw) // 2
_bg = _bg.crop((_x0, 0, _x0 + _cw, _h)).resize((1700, 1202), Image.LANCZOS)
CERT_BG_B64 = _data_uri(_bg, "JPEG", "image/jpeg", quality=88, optimize=True)

_logo = Image.open(os.path.join(ASSETS, "logo_bella_gold_transparent.png")).convert("RGBA")
_px = _logo.load()
for _yy in range(_logo.size[1]):
    for _xx in range(_logo.size[0]):
        _r, _g, _b, _a = _px[_xx, _yy]
        if _a < 255 and (_r - _b) < 14 and max(_r, _g, _b) < 140:
            _px[_xx, _yy] = (_r, _g, _b, 0)
_logo = _logo.resize((720, int(720 * _logo.size[1] / _logo.size[0])), Image.LANCZOS)
CERT_LOGO_B64 = _data_uri(_logo, "PNG", "image/png", optimize=True)

_sig = Image.open(os.path.join(ASSETS, "signature_gold_clean.png")).convert("RGBA")
_sig = _sig.resize((_sig.size[0] * 2, _sig.size[1] * 2), Image.LANCZOS)
CERT_SIG_B64 = _data_uri(_sig, "PNG", "image/png", optimize=True)

html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>BELLA BEAUTY ACADEMY · Evaluación Curso Brow Artist</title>
  
  <!-- Fallback Google Fonts for cross-device compatibility -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700;900&family=Montserrat:wght@300;400;500;600;700&family=Pinyon+Script&family=Alex+Brush&display=swap" rel="stylesheet">

  <!-- html2pdf.js (CDN, with local fallback) -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js" onerror="this.onerror=null;var s=document.createElement('script');s.src='assets/html2pdf.bundle.min.js';document.head.appendChild(s);"></script>

  <style>
    /* ==========================================================
       FONT DEFINITIONS (Local custom fonts + luxury fallbacks)
       ========================================================== */
    @font-face {{
      font-family: 'Hatton';
      src: local('Hatton'), local('PP Hatton Medium'), url('fonts/Hatton-Medium.otf') format('opentype');
      font-weight: 500;
      font-style: normal;
    }}
    @font-face {{
      font-family: 'La Luxes Script';
      src: local('La Luxes Script'), url('fonts/LaLuxesScript-Regular.otf') format('opentype');
      font-weight: normal;
      font-style: normal;
    }}
    @font-face {{
      font-family: 'La Luxes Serif';
      src: local('La Luxes Serif'), url('fonts/LaLuxesSerif-Regular.otf') format('opentype');
      font-weight: normal;
      font-style: normal;
    }}
    @font-face {{
      font-family: 'Now';
      src: local('Now'), url('fonts/Now-Regular.otf') format('opentype');
      font-weight: 400;
      font-style: normal;
    }}
    @font-face {{
      font-family: 'Now';
      src: local('Now Medium'), url('fonts/Now-Medium.otf') format('opentype');
      font-weight: 500;
      font-style: normal;
    }}
    @font-face {{
      font-family: 'Now';
      src: local('Now Bold'), url('fonts/Now-Bold.otf') format('opentype');
      font-weight: 700;
      font-style: normal;
    }}

    /* ==========================================================
       CSS LUXURY VARIABLES (Deep Black & Metallic Gold)
       ========================================================== */
    :root {{
      --font-title: 'Hatton', 'Cinzel', 'Playfair Display', Georgia, serif;
      --font-script: 'La Luxes Script', 'Alex Brush', 'Pinyon Script', cursive;
      --font-sub: 'Now', 'Montserrat', 'Segoe UI', sans-serif;
      --font-body: 'Now', 'Montserrat', -apple-system, BlinkMacSystemFont, sans-serif;

      --gold-primary: #D4AF37;
      --gold-light: #F7E1A1;
      --gold-dark: #9A741E;
      --gold-shimmer: linear-gradient(135deg, #ECC880 0%, #D4AF37 40%, #B8860B 75%, #F7E1A1 100%);
      --gold-glow: 0 0 20px rgba(212, 175, 55, 0.45);
      
      --bg-deep: #080808;
      --card-bg: rgba(14, 13, 11, 0.90);
      --card-border: 1px solid rgba(212, 175, 55, 0.35);
      
      --text-main: #F3EBDD;
      --text-muted: #B8AC98;
      
      --color-correct: #2ECC71;
      --color-wrong: #E74C3C;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }}

    body {{
      background-color: var(--bg-deep);
      color: var(--text-main);
      font-family: var(--font-body);
      min-height: 100vh;
      overflow-x: hidden;
      position: relative;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    /* BACKGROUND WITH GOLD SACRED GEOMETRY SPIRAL & BOKEH */
    .bg-canvas-wrapper {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      z-index: 0;
      pointer-events: none;
      background-image: 
        radial-gradient(circle at 50% 25%, rgba(20, 18, 14, 0.45) 0%, rgba(8, 8, 8, 0.96) 100%),
        url('assets/bg_spiral_gold.jpg');
      background-size: cover;
      background-position: center center;
      background-repeat: no-repeat;
      opacity: 0.82;
    }}

    #particle-canvas {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      z-index: 1;
      pointer-events: none;
    }}

    #confetti-canvas {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      z-index: 9999;
      pointer-events: none;
    }}

    /* MAIN CONTAINER */
    .app-viewport {{
      position: relative;
      z-index: 10;
      width: 100%;
      max-width: 900px;
      margin: 0 auto;
      padding: 12px 18px 60px;
      flex: 1;
      display: flex;
      flex-direction: column;
    }}

    /* TOP BAR / NAVIGATION */
    .top-bar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 18px;
      background: rgba(14, 13, 11, 0.75);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid rgba(212, 175, 55, 0.25);
      border-radius: 40px;
      margin-bottom: 14px;
      transition: all 0.3s ease;
    }}

    .brand-compact {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .brand-compact img {{
      height: 28px;
      width: auto;
      object-fit: contain;
      filter: drop-shadow(0 0 6px rgba(212, 175, 55, 0.5));
    }}

    .brand-text-mini {{
      font-family: var(--font-title);
      font-size: 13px;
      letter-spacing: 0.15em;
      color: var(--gold-primary);
      text-transform: uppercase;
    }}

    .top-actions {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .icon-btn {{
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(212, 175, 55, 0.3);
      color: var(--gold-light);
      width: 36px;
      height: 36px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.25s ease;
      font-size: 15px;
    }}

    .icon-btn:hover {{
      background: rgba(212, 175, 55, 0.2);
      border-color: var(--gold-primary);
      transform: scale(1.05);
      box-shadow: 0 0 10px rgba(212, 175, 55, 0.3);
    }}

    /* LUXURY CARDS */
    .luxury-card {{
      background: var(--card-bg);
      backdrop-filter: blur(18px);
      -webkit-backdrop-filter: blur(18px);
      border: var(--card-border);
      border-radius: 22px;
      padding: 26px 26px;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.8), 0 0 30px rgba(212, 175, 55, 0.1);
      position: relative;
      overflow: hidden;
      transition: transform 0.3s ease, opacity 0.3s ease;
    }}

    .luxury-card::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 2px;
      background: var(--gold-shimmer);
      box-shadow: 0 0 12px rgba(212, 175, 55, 0.7);
    }}

    /* SCREEN 1: WELCOME SCREEN */
    .welcome-screen {{
      text-align: center;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 14px;
    }}

    .logo-hero-container {{
      margin-top: 4px;
      margin-bottom: 0px;
      position: relative;
    }}

    .logo-hero {{
      max-width: 290px;
      width: 80%;
      height: auto;
      filter: drop-shadow(0 0 20px rgba(212, 175, 55, 0.5));
      animation: floatLogo 6s ease-in-out infinite;
    }}

    @keyframes floatLogo {{
      0%, 100% {{ transform: translateY(0); }}
      50% {{ transform: translateY(-4px); }}
    }}

    .script-sub {{
      font-family: var(--font-script);
      font-size: 32px;
      color: var(--gold-light);
      margin-top: -6px;
      margin-bottom: 0px;
      text-shadow: 0 0 15px rgba(212, 175, 55, 0.5);
      letter-spacing: 0.04em;
    }}

    .hero-title {{
      font-family: var(--font-title);
      font-size: 26px;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      background: var(--gold-shimmer);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      line-height: 1.25;
      margin-bottom: 6px;
    }}

    .hero-trainer-badge {{
      display: inline-flex;
      align-items: center;
      gap: 10px;
      padding: 6px 16px;
      background: rgba(212, 175, 55, 0.08);
      border: 1px solid rgba(212, 175, 55, 0.3);
      border-radius: 30px;
      font-size: 12px;
      letter-spacing: 0.08em;
      color: var(--gold-light);
      text-transform: uppercase;
    }}

    .trainer-avatar-mini {{
      width: 28px;
      height: 28px;
      border-radius: 50%;
      border: 1px solid var(--gold-primary);
      object-fit: cover;
    }}

    .welcome-intro-text {{
      font-size: 14.5px;
      line-height: 1.6;
      color: var(--text-muted);
      max-width: 660px;
      margin: 4px 0 6px;
    }}

    .scale-info-box {{
      background: rgba(212, 175, 55, 0.06);
      border: 1px solid rgba(212, 175, 55, 0.25);
      border-radius: 14px;
      padding: 12px 18px;
      max-width: 660px;
      width: 100%;
      font-size: 12.5px;
      color: var(--text-main);
      line-height: 1.5;
      text-align: left;
    }}

    .scale-info-box strong {{
      color: var(--gold-light);
    }}

    .features-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      width: 100%;
      margin: 8px 0 12px;
    }}

    .feature-item {{
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid rgba(212, 175, 55, 0.18);
      border-radius: 14px;
      padding: 12px 8px;
      text-align: center;
    }}

    .feature-icon {{
      font-size: 20px;
      color: var(--gold-primary);
      margin-bottom: 4px;
    }}

    .feature-text {{
      font-size: 11.5px;
      font-weight: 500;
      color: var(--text-main);
      letter-spacing: 0.03em;
    }}

    .name-input-group {{
      width: 100%;
      max-width: 440px;
      margin: 4px 0 12px;
      text-align: left;
    }}

    .name-input-label {{
      display: block;
      font-size: 11px;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: var(--gold-primary);
      margin-bottom: 6px;
      margin-left: 4px;
    }}

    .luxury-input {{
      width: 100%;
      padding: 14px 20px;
      background: rgba(10, 10, 10, 0.85);
      border: 1.5px solid rgba(212, 175, 55, 0.4);
      border-radius: 14px;
      color: #fff;
      font-family: var(--font-sub);
      font-size: 15px;
      letter-spacing: 0.04em;
      outline: none;
      transition: all 0.3s ease;
    }}

    .luxury-input:focus {{
      border-color: var(--gold-light);
      box-shadow: 0 0 20px rgba(212, 175, 55, 0.35);
      background: rgba(18, 17, 14, 0.95);
    }}

    /* BUTTONS */
    .btn-gold-cta {{
      position: relative;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      padding: 15px 38px;
      background: var(--gold-shimmer);
      border: none;
      border-radius: 40px;
      color: #0E0D0B;
      font-family: var(--font-title);
      font-size: 15px;
      font-weight: 700;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      cursor: pointer;
      box-shadow: 0 8px 30px rgba(212, 175, 55, 0.45);
      transition: all 0.3s ease;
      overflow: hidden;
    }}

    .btn-gold-cta::after {{
      content: '';
      position: absolute;
      top: -50%;
      left: -60%;
      width: 40%;
      height: 200%;
      background: rgba(255, 255, 255, 0.4);
      transform: rotate(30deg);
      transition: all 0.8s ease;
    }}

    .btn-gold-cta:hover {{
      transform: translateY(-2px) scale(1.02);
      box-shadow: 0 12px 35px rgba(212, 175, 55, 0.65);
    }}

    .btn-gold-cta:hover::after {{
      left: 120%;
    }}

    .btn-gold-cta:active {{
      transform: translateY(0);
    }}

    /* SCREEN 2: ACTIVE QUIZ */
    .quiz-hud {{
      margin-bottom: 14px;
    }}

    .hud-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }}

    .hud-case-counter {{
      font-family: var(--font-title);
      font-size: 13px;
      letter-spacing: 0.15em;
      color: var(--gold-light);
      text-transform: uppercase;
    }}

    .hud-score-pill {{
      padding: 5px 14px;
      background: rgba(212, 175, 55, 0.1);
      border: 1px solid rgba(212, 175, 55, 0.3);
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      color: var(--gold-primary);
    }}

    .progress-bar-wrap {{
      width: 100%;
      height: 7px;
      background: rgba(255, 255, 255, 0.08);
      border-radius: 10px;
      overflow: hidden;
      position: relative;
    }}

    .progress-bar-fill {{
      height: 100%;
      background: var(--gold-shimmer);
      box-shadow: 0 0 12px rgba(212, 175, 55, 0.8);
      border-radius: 10px;
      width: 0%;
      transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    /* QUESTION CARD */
    .case-category-pill {{
      display: inline-block;
      padding: 5px 12px;
      background: rgba(212, 175, 55, 0.12);
      border: 1px solid rgba(212, 175, 55, 0.4);
      border-radius: 20px;
      font-family: var(--font-sub);
      font-size: 10.5px;
      font-weight: 600;
      letter-spacing: 0.14em;
      color: var(--gold-light);
      text-transform: uppercase;
      margin-bottom: 10px;
    }}

    .case-title-num {{
      font-family: var(--font-script);
      font-size: 28px;
      color: var(--gold-primary);
      margin-bottom: 4px;
    }}

    .case-question-text {{
      font-size: 16.5px;
      line-height: 1.6;
      color: #FFFFFF;
      font-weight: 500;
      margin-bottom: 18px;
    }}

    /* OPTIONS LIST */
    .options-grid {{
      display: flex;
      flex-direction: column;
      gap: 11px;
    }}

    .option-card {{
      display: flex;
      align-items: flex-start;
      gap: 14px;
      padding: 14px 18px;
      background: rgba(255, 255, 255, 0.03);
      border: 1.5px solid rgba(212, 175, 55, 0.22);
      border-radius: 14px;
      cursor: pointer;
      transition: all 0.25s ease;
      text-align: left;
      color: var(--text-main);
      font-family: var(--font-body);
      font-size: 14.5px;
      line-height: 1.5;
      position: relative;
    }}

    .option-card:hover:not(.locked) {{
      background: rgba(212, 175, 55, 0.08);
      border-color: var(--gold-primary);
      transform: translateX(4px);
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }}

    .option-card.locked {{
      cursor: default;
    }}

    .option-letter {{
      width: 30px;
      height: 30px;
      min-width: 30px;
      border-radius: 50%;
      background: rgba(212, 175, 55, 0.12);
      border: 1px solid var(--gold-primary);
      color: var(--gold-light);
      font-family: var(--font-title);
      font-size: 13px;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.3s ease;
    }}

    /* OPTION STATES AFTER ANSWER */
    .option-card.correct {{
      background: rgba(46, 204, 113, 0.14) !important;
      border-color: var(--color-correct) !important;
      box-shadow: 0 0 25px rgba(46, 204, 113, 0.35);
    }}

    .option-card.correct .option-letter {{
      background: var(--color-correct);
      border-color: var(--color-correct);
      color: #0E0D0B;
    }}

    .option-card.incorrect-selected {{
      background: rgba(231, 76, 60, 0.14) !important;
      border-color: var(--color-wrong) !important;
      box-shadow: 0 0 25px rgba(231, 76, 60, 0.35);
      animation: shake 0.4s ease;
    }}

    .option-card.incorrect-selected .option-letter {{
      background: var(--color-wrong);
      border-color: var(--color-wrong);
      color: #fff;
    }}

    .option-card.faded {{
      opacity: 0.45;
    }}

    @keyframes shake {{
      0%, 100% {{ transform: translateX(0); }}
      20%, 60% {{ transform: translateX(-6px); }}
      40%, 80% {{ transform: translateX(6px); }}
    }}

    /* FEEDBACK CARD / CLINICAL EXPLANATION */
    .feedback-drawer {{
      margin-top: 18px;
      padding: 18px 20px;
      background: rgba(18, 16, 12, 0.95);
      border-left: 4px solid var(--gold-primary);
      border-radius: 0 14px 14px 0;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
      display: none;
      animation: fadeInUp 0.4s ease;
    }}

    .feedback-status-badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-bottom: 8px;
    }}

    .feedback-status-badge.ok {{
      color: var(--color-correct);
    }}

    .feedback-status-badge.bad {{
      color: var(--color-wrong);
    }}

    .feedback-user-rationale {{
      font-size: 14.5px;
      line-height: 1.6;
      color: var(--text-main);
      margin-bottom: 10px;
    }}

    .feedback-correct-recap {{
      padding: 10px 14px;
      background: rgba(212, 175, 55, 0.08);
      border: 1px solid rgba(212, 175, 55, 0.25);
      border-radius: 10px;
      font-size: 13.5px;
      line-height: 1.5;
      color: var(--gold-light);
      margin-bottom: 10px;
    }}

    .feedback-source-ref {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 11.5px;
      letter-spacing: 0.06em;
      color: var(--text-muted);
      text-transform: uppercase;
    }}

    .feedback-source-ref span {{
      color: var(--gold-primary);
      font-weight: 600;
    }}

    .quiz-next-actions {{
      margin-top: 20px;
      display: flex;
      justify-content: flex-end;
    }}

    /* ==========================================================
       SCREEN 3: CERTIFICADO DE RENDIMIENTO (PREMIUM LANDSCAPE)
       ========================================================== */
    /* Fixed A4-landscape stage (1123 x 794 px) scaled to fit the viewport */
    .cert-stage {{
      width: 100%;
      position: relative;
      margin: 0 auto 30px;
    }}

    .cert-scaler {{
      position: absolute;
      top: 0;
      left: 0;
      width: 1123px;
      height: 794px;
      transform-origin: top left;
      box-shadow: 0 0 60px rgba(212, 175, 55, 0.30), 0 25px 70px rgba(0, 0, 0, 0.9);
    }}

    .certificate-card {{
      position: relative;
      width: 1123px;
      height: 794px;
      overflow: hidden;
      box-sizing: border-box;
      background-color: #0a0908;
      background-size: cover;
      background-position: center center;
      background-repeat: no-repeat;
      color: #F3EBD3;
      text-align: center;
    }}

    .certificate-card * {{
      box-sizing: border-box;
    }}

    .cert-shade {{
      position: absolute;
      left: 0; top: 0; width: 1123px; height: 794px;
      background: radial-gradient(ellipse at 50% 42%, rgba(10, 9, 8, 0.62) 0%, rgba(8, 7, 6, 0.80) 70%, rgba(5, 5, 4, 0.90) 100%);
    }}

    .cert-frame-outer {{
      position: absolute;
      left: 20px; top: 20px; width: 1083px; height: 754px;
      border: 3px solid #D4AF37;
    }}

    .cert-frame-inner {{
      position: absolute;
      left: 32px; top: 32px; width: 1059px; height: 730px;
      border: 1px solid rgba(212, 175, 55, 0.65);
    }}

    .cert-corner {{
      position: absolute;
      width: 26px; height: 26px;
      border: 0 solid #E8C766;
    }}
    .cert-corner.tl {{ left: 42px; top: 42px; border-top-width: 2px; border-left-width: 2px; }}
    .cert-corner.tr {{ right: 42px; top: 42px; border-top-width: 2px; border-right-width: 2px; }}
    .cert-corner.bl {{ left: 42px; bottom: 42px; border-bottom-width: 2px; border-left-width: 2px; }}
    .cert-corner.br {{ right: 42px; bottom: 42px; border-bottom-width: 2px; border-right-width: 2px; }}

    .cert-abs {{
      position: absolute;
      left: 0;
      width: 1123px;
      text-align: center;
      margin: 0;
      padding: 0;
    }}

    .cert-logo-img {{
      position: absolute;
      left: 413px;
      top: 50px;
      width: 297px;
      height: auto;
    }}

    .cert-main-title {{
      top: 166px;
      font-family: var(--font-title);
      font-size: 38px;
      line-height: 46px;
      letter-spacing: 0.15em;
      color: #E3C26B;
      text-transform: uppercase;
      text-shadow: 0 2px 14px rgba(0, 0, 0, 0.7);
    }}

    .cert-preamble {{
      top: 224px;
      font-family: var(--font-body);
      font-weight: 500;
      font-size: 12px;
      line-height: 16px;
      letter-spacing: 0.32em;
      color: #EFE6CC;
      text-transform: uppercase;
    }}

    .cert-course-name {{
      top: 242px;
      font-family: var(--font-script);
      font-size: 64px;
      line-height: 76px;
      color: #FFFFFF;
      text-shadow: 0 0 18px rgba(212, 175, 55, 0.55);
    }}

    .cert-mencion {{
      top: 328px;
      height: 22px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 22px;
    }}

    .cert-mencion-line {{
      display: block;
      width: 120px;
      height: 1px;
      background: #D4AF37;
    }}

    .cert-mencion-text {{
      font-family: var(--font-body);
      font-weight: 700;
      font-size: 15px;
      line-height: 22px;
      letter-spacing: 0.42em;
      color: #E3C26B;
      text-transform: uppercase;
      white-space: nowrap;
      margin-right: -0.42em;
    }}

    .cert-award-to {{
      top: 380px;
      font-family: var(--font-body);
      font-weight: 500;
      font-size: 11.5px;
      line-height: 16px;
      letter-spacing: 0.32em;
      color: #D9CFB2;
      text-transform: uppercase;
    }}

    .cert-student-name {{
      top: 402px;
      height: 112px;
      font-family: var(--font-script);
      font-size: 92px;
      line-height: 112px;
      color: #EBCB77;
      white-space: nowrap;
      text-shadow: 0 2px 16px rgba(0, 0, 0, 0.75), 0 0 22px rgba(212, 175, 55, 0.35);
    }}

    .cert-name-rule {{
      position: absolute;
      left: 391px;
      top: 522px;
      width: 340px;
      height: 1px;
      background: linear-gradient(90deg, rgba(212,175,55,0) 0%, rgba(212,175,55,0.95) 50%, rgba(212,175,55,0) 100%);
    }}

    .cert-body-text {{
      left: 171px;
      top: 540px;
      width: 781px;
      font-family: var(--font-body);
      font-weight: 400;
      font-size: 14.5px;
      line-height: 25px;
      color: #E9E0C6;
    }}

    .cert-body-text strong {{
      color: #FFFFFF;
      font-weight: 700;
    }}

    .cert-sig-left, .cert-sig-right {{
      position: absolute;
      width: 300px;
      text-align: center;
    }}
    .cert-sig-left {{ left: 120px; top: 628px; height: 90px; }}
    .cert-sig-right {{ left: 703px; top: 628px; height: 90px; }}

    .cert-signature-img {{
      position: absolute;
      left: 40px;
      top: 0;
      width: 220px;
      height: auto;
    }}

    .cert-sig-line {{
      position: absolute;
      left: 40px;
      top: 42px;
      width: 220px;
      height: 1px;
      background: #D4AF37;
    }}

    .cert-sig-name {{
      position: absolute;
      left: 0; top: 52px; width: 300px;
      font-family: var(--font-title);
      font-size: 13px;
      line-height: 18px;
      letter-spacing: 0.12em;
      color: #E3C26B;
      text-transform: uppercase;
      white-space: nowrap;
    }}

    .cert-sig-role {{
      position: absolute;
      left: 0; top: 73px; width: 300px;
      font-family: var(--font-body);
      font-size: 10px;
      line-height: 14px;
      letter-spacing: 0.2em;
      color: #CFC4A5;
      text-transform: uppercase;
      white-space: nowrap;
    }}

    .cert-date-label {{
      position: absolute;
      left: 0; top: 20px; width: 300px;
      font-family: var(--font-body);
      font-weight: 600;
      font-size: 10.5px;
      line-height: 14px;
      letter-spacing: 0.26em;
      color: #D4AF37;
      text-transform: uppercase;
      white-space: nowrap;
    }}

    .cert-date-val {{
      position: absolute;
      left: 0; top: 40px; width: 300px;
      font-family: var(--font-title);
      font-size: 18px;
      line-height: 24px;
      letter-spacing: 0.1em;
      color: #FFFFFF;
      text-transform: uppercase;
      white-space: nowrap;
    }}

    .cert-date-sub {{
      position: absolute;
      left: 0; top: 73px; width: 300px;
      font-family: var(--font-body);
      font-size: 10px;
      line-height: 14px;
      letter-spacing: 0.2em;
      color: #CFC4A5;
      text-transform: uppercase;
      white-space: nowrap;
    }}

    /* ==========================================================
       INDEPENDENT CONSOLIDATED REPORT (BELOW CERTIFICATE)
       ========================================================== */
    .summary-report-card {{
      width: 100%;
      background: rgba(14, 13, 11, 0.92);
      border: 1px solid rgba(212, 175, 55, 0.35);
      border-radius: 20px;
      padding: 28px 24px;
      margin-top: 10px;
      box-shadow: 0 15px 40px rgba(0, 0, 0, 0.8);
    }}

    .summary-title {{
      font-family: var(--font-title);
      font-size: 20px;
      letter-spacing: 0.12em;
      color: var(--gold-primary);
      text-transform: uppercase;
      text-align: center;
      margin-bottom: 20px;
    }}

    .summary-kpi-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 14px;
      margin-bottom: 24px;
    }}

    .kpi-card {{
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid rgba(212, 175, 55, 0.2);
      border-radius: 14px;
      padding: 16px 12px;
      text-align: center;
    }}

    .kpi-label {{
      font-size: 11px;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--text-muted);
      margin-bottom: 6px;
    }}

    .kpi-val {{
      font-family: var(--font-title);
      font-size: 28px;
      color: var(--gold-light);
    }}

    .kpi-status {{
      font-size: 11.5px;
      font-weight: 600;
      margin-top: 4px;
      text-transform: uppercase;
    }}

    .kpi-status.ok {{
      color: var(--color-correct);
    }}

    .kpi-status.bad {{
      color: var(--color-wrong);
    }}

    /* "DÓNDE REFORZAR" SECTION */
    .reinforce-box {{
      background: rgba(231, 76, 60, 0.07);
      border: 1px solid rgba(231, 76, 60, 0.35);
      border-radius: 14px;
      padding: 20px 22px;
      margin-bottom: 24px;
      text-align: left;
    }}

    .reinforce-box.all-correct {{
      background: rgba(46, 204, 113, 0.07);
      border-color: rgba(46, 204, 113, 0.35);
    }}

    .reinforce-heading {{
      font-family: var(--font-title);
      font-size: 16px;
      letter-spacing: 0.1em;
      color: var(--gold-light);
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .reinforce-items-list {{
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}

    .reinforce-item {{
      font-size: 13.5px;
      line-height: 1.5;
      color: var(--text-main);
      padding-left: 12px;
      border-left: 2px solid var(--gold-primary);
    }}

    .reinforce-item span {{
      color: var(--gold-light);
      font-weight: 600;
      display: block;
      font-size: 12px;
      margin-top: 2px;
    }}

    .motivational-msg {{
      margin-top: 16px;
      padding-top: 14px;
      border-top: 1px solid rgba(212, 175, 55, 0.2);
      font-size: 13.5px;
      line-height: 1.6;
      color: #E2D7BC;
      font-style: italic;
    }}

    /* ACCORDION REVIEW OF ALL CASES */
    .review-section {{
      width: 100%;
      text-align: left;
      margin-top: 8px;
    }}

    .review-header-title {{
      font-family: var(--font-title);
      font-size: 18px;
      letter-spacing: 0.1em;
      color: var(--gold-primary);
      text-transform: uppercase;
      margin-bottom: 14px;
      text-align: center;
    }}

    .review-list {{
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}

    .review-card {{
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid rgba(212, 175, 55, 0.2);
      border-radius: 12px;
      padding: 14px 18px;
      cursor: pointer;
      transition: all 0.25s ease;
    }}

    .review-card:hover {{
      border-color: var(--gold-primary);
      background: rgba(212, 175, 55, 0.05);
    }}

    .review-card-head {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
    }}

    .review-card-title {{
      font-size: 13.5px;
      font-weight: 600;
      color: #fff;
    }}

    .review-tag {{
      padding: 3px 10px;
      border-radius: 20px;
      font-size: 10.5px;
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      white-space: nowrap;
    }}

    .review-tag.ok {{
      background: rgba(46, 204, 113, 0.15);
      border: 1px solid var(--color-correct);
      color: var(--color-correct);
    }}

    .review-tag.bad {{
      background: rgba(231, 76, 60, 0.15);
      border: 1px solid var(--color-wrong);
      color: var(--color-wrong);
    }}

    .review-card-details {{
      margin-top: 12px;
      padding-top: 10px;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      font-size: 13px;
      line-height: 1.6;
      color: var(--text-muted);
      display: none;
    }}

    .review-card.open .review-card-details {{
      display: block;
    }}

    .results-actions {{
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 12px;
      margin-top: 24px;
      width: 100%;
    }}

    .btn-secondary {{
      padding: 14px 28px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(212, 175, 55, 0.4);
      border-radius: 30px;
      color: var(--gold-light);
      font-family: var(--font-sub);
      font-size: 13.5px;
      font-weight: 600;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      cursor: pointer;
      transition: all 0.25s ease;
    }}

    .btn-secondary:hover {{
      background: rgba(212, 175, 55, 0.15);
      border-color: var(--gold-primary);
    }}

    /* FOOTER */
    footer {{
      position: relative;
      z-index: 10;
      text-align: center;
      padding: 14px;
      background: rgba(8, 8, 8, 0.95);
      border-top: 1px solid rgba(212, 175, 55, 0.25);
      color: var(--gold-primary);
      font-size: 11px;
      letter-spacing: 0.22em;
      text-transform: uppercase;
    }}

    footer em {{
      font-style: normal;
      color: #FFFFFF;
      font-weight: 700;
    }}

    /* ANIMATIONS */
    @keyframes fadeInUp {{
      from {{
        opacity: 0;
        transform: translateY(12px);
      }}
      to {{
        opacity: 1;
        transform: translateY(0);
      }}
    }}

    /* TOAST ALERT */
    .toast-box {{
      position: fixed;
      bottom: 50px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(20, 18, 14, 0.95);
      border: 1px solid var(--gold-primary);
      color: var(--gold-light);
      padding: 10px 22px;
      border-radius: 30px;
      font-size: 13px;
      box-shadow: 0 8px 25px rgba(0, 0, 0, 0.8);
      z-index: 1000;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.3s ease;
    }}

    .toast-box.show {{
      opacity: 1;
      pointer-events: auto;
    }}

    /* RESPONSIVE DESIGN */
    @media (max-width: 768px) {{
      .app-viewport {{
        padding: 10px 12px 50px;
      }}
      .luxury-card {{
        padding: 20px 16px;
        border-radius: 16px;
      }}
      .summary-kpi-grid {{
        grid-template-columns: 1fr;
      }}
      .features-grid {{
        grid-template-columns: repeat(2, 1fr);
      }}
    }}

  </style>
</head>
<body>

  <!-- BACKGROUND TEXTURE + SACRED GEOMETRY SPIRAL -->
  <div class="bg-canvas-wrapper"></div>
  <canvas id="particle-canvas"></canvas>
  <canvas id="confetti-canvas"></canvas>

  <div class="app-viewport">
    
    <!-- TOP NAVIGATION BAR -->
    <header class="top-bar">
      <div class="brand-compact">
        <img src="assets/logo_bella_gold_transparent.png" alt="BELLA Beauty Academy">
        <span class="brand-text-mini">BELLA BEAUTY ACADEMY</span>
      </div>
      <div class="top-actions">
        <button class="icon-btn" id="soundToggle" title="Activar/Silenciar Efectos de Audio">🔊</button>
      </div>
    </header>

    <!-- DYNAMIC CONTAINER -->
    <main id="app-content"></main>

  </div>

  <!-- TOAST NOTIFICATION -->
  <div id="toast" class="toast-box">Enlace copiado con éxito</div>

  <!-- LUXURY FOOTER -->
  <footer>
    ♥ REALZA TU BELLEZA, SIÉNTETE <em>BELLA</em> ♥
  </footer>

  <script>
    const CERT_IMG = {{
      bg: "{CERT_BG_B64}",
      logo: "{CERT_LOGO_B64}",
      sig: "{CERT_SIG_B64}"
    }};

    /* ==========================================================
       DATA SOURCE: 20 CLINICAL CASES FROM GUÍA MAESTRA
       ========================================================== */
    const QUESTIONS_DATA = {questions_json_str};

    /* ==========================================================
       WEB AUDIO SYNTHESIZER (Tactile sound effects)
       ========================================================== */
    class SoundManager {{
      constructor() {{
        this.enabled = true;
        this.ctx = null;
      }}

      init() {{
        if (!this.ctx) {{
          const AudioContext = window.AudioContext || window.webkitAudioContext;
          if (AudioContext) {{
            this.ctx = new AudioContext();
          }}
        }}
        if (this.ctx && this.ctx.state === 'suspended') {{
          this.ctx.resume();
        }}
      }}

      toggle() {{
        this.enabled = !this.enabled;
        return this.enabled;
      }}

      playCorrect() {{
        if (!this.enabled) return;
        this.init();
        if (!this.ctx) return;

        const now = this.ctx.currentTime;
        [523.25, 659.25, 783.99, 1046.50].forEach((freq, i) => {{
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(freq, now + i * 0.08);

          gain.gain.setValueAtTime(0, now + i * 0.08);
          gain.gain.linearRampToValueAtTime(0.12, now + i * 0.08 + 0.02);
          gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.08 + 0.5);

          osc.connect(gain);
          gain.connect(this.ctx.destination);

          osc.start(now + i * 0.08);
          osc.stop(now + i * 0.08 + 0.5);
        }});
      }}

      playIncorrect() {{
        if (!this.enabled) return;
        this.init();
        if (!this.ctx) return;

        const now = this.ctx.currentTime;
        [220, 196].forEach((freq, i) => {{
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(freq, now + i * 0.12);

          gain.gain.setValueAtTime(0.15, now + i * 0.12);
          gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.12 + 0.35);

          osc.connect(gain);
          gain.connect(this.ctx.destination);

          osc.start(now + i * 0.12);
          osc.stop(now + i * 0.12 + 0.35);
        }});
      }}

      playFanfare() {{
        if (!this.enabled) return;
        this.init();
        if (!this.ctx) return;

        const now = this.ctx.currentTime;
        const notes = [523.25, 659.25, 783.99, 1046.50, 1318.51, 1567.98];
        notes.forEach((freq, i) => {{
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(freq, now + i * 0.09);

          gain.gain.setValueAtTime(0, now + i * 0.09);
          gain.gain.linearRampToValueAtTime(0.16, now + i * 0.09 + 0.03);
          gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.09 + 0.85);

          osc.connect(gain);
          gain.connect(this.ctx.destination);

          osc.start(now + i * 0.09);
          osc.stop(now + i * 0.09 + 0.85);
        }});
      }}
    }}

    const sound = new SoundManager();

    /* ==========================================================
       PARTICLE CANVAS (Golden sparkles & bokeh background)
       ========================================================== */
    const particleCanvas = document.getElementById('particle-canvas');
    const pCtx = particleCanvas.getContext('2d');
    let particles = [];

    function resizeParticleCanvas() {{
      particleCanvas.width = window.innerWidth;
      particleCanvas.height = window.innerHeight;
    }}
    window.addEventListener('resize', resizeParticleCanvas);
    resizeParticleCanvas();

    class GoldParticle {{
      constructor() {{
        this.reset();
      }}
      reset() {{
        this.x = Math.random() * particleCanvas.width;
        this.y = Math.random() * particleCanvas.height;
        this.size = Math.random() * 2.2 + 0.6;
        this.speedY = -(Math.random() * 0.4 + 0.15);
        this.speedX = (Math.random() - 0.5) * 0.2;
        this.alpha = Math.random() * 0.6 + 0.2;
        this.pulse = Math.random() * 0.02 + 0.005;
      }}
      update() {{
        this.y += this.speedY;
        this.x += this.speedX;
        this.alpha += Math.sin(Date.now() * 0.002) * this.pulse;
        if (this.y < -10 || this.x < -10 || this.x > particleCanvas.width + 10) {{
          this.reset();
          this.y = particleCanvas.height + 10;
        }}
      }}
      draw() {{
        pCtx.save();
        pCtx.beginPath();
        pCtx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        pCtx.fillStyle = `rgba(236, 200, 128, ${{Math.max(0.1, Math.min(0.8, this.alpha))}})`;
        pCtx.shadowBlur = 8;
        pCtx.shadowColor = 'rgba(212, 175, 55, 0.8)';
        pCtx.fill();
        pCtx.restore();
      }}
    }}

    for (let i = 0; i < 45; i++) {{
      particles.push(new GoldParticle());
    }}

    function animateParticles() {{
      pCtx.clearRect(0, 0, particleCanvas.width, particleCanvas.height);
      particles.forEach(p => {{
        p.update();
        p.draw();
      }});
      requestAnimationFrame(animateParticles);
    }}
    animateParticles();

    /* ==========================================================
       CONFETTI CANVAS (Golden Celebration)
       ========================================================== */
    const confettiCanvas = document.getElementById('confetti-canvas');
    const cCtx = confettiCanvas.getContext('2d');
    let confettiList = [];
    let confettiRunning = false;

    function resizeConfetti() {{
      confettiCanvas.width = window.innerWidth;
      confettiCanvas.height = window.innerHeight;
    }}
    window.addEventListener('resize', resizeConfetti);
    resizeConfetti();

    class ConfettiPiece {{
      constructor() {{
        this.x = Math.random() * confettiCanvas.width;
        this.y = -20;
        this.size = Math.random() * 9 + 5;
        this.speedY = Math.random() * 3 + 2;
        this.speedX = (Math.random() - 0.5) * 2;
        this.rotation = Math.random() * 360;
        this.rotationSpeed = (Math.random() - 0.5) * 6;
        const goldShades = ['#D4AF37', '#F7E1A1', '#ECC880', '#B8860B', '#FFF'];
        this.color = goldShades[Math.floor(Math.random() * goldShades.length)];
      }}
      update() {{
        this.y += this.speedY;
        this.x += this.speedX;
        this.rotation += this.rotationSpeed;
      }}
      draw() {{
        cCtx.save();
        cCtx.translate(this.x, this.y);
        cCtx.rotate((this.rotation * Math.PI) / 180);
        cCtx.fillStyle = this.color;
        cCtx.fillRect(-this.size / 2, -this.size / 2, this.size, this.size * 0.6);
        cCtx.restore();
      }}
    }}

    function triggerGoldenConfetti() {{
      confettiList = [];
      for (let i = 0; i < 110; i++) {{
        confettiList.push(new ConfettiPiece());
      }}
      confettiRunning = true;
    }}

    function animateConfetti() {{
      if (confettiRunning) {{
        cCtx.clearRect(0, 0, confettiCanvas.width, confettiCanvas.height);
        confettiList.forEach((c, idx) => {{
          c.update();
          c.draw();
          if (c.y > confettiCanvas.height + 20) {{
            confettiList.splice(idx, 1);
          }}
        }});
        if (confettiList.length === 0) {{
          confettiRunning = false;
        }}
      }}
      requestAnimationFrame(animateConfetti);
    }}
    animateConfetti();

    /* ==========================================================
       QUIZ APPLICATION CONTROLLER
       ========================================================== */
    const appContent = document.getElementById('app-content');
    const soundToggle = document.getElementById('soundToggle');
    const toast = document.getElementById('toast');

    soundToggle.addEventListener('click', () => {{
      const isOn = sound.toggle();
      soundToggle.textContent = isOn ? '🔊' : '🔇';
      showToast(isOn ? 'Efectos de audio activados' : 'Audio silenciado');
    }});

    function showToast(msg) {{
      toast.textContent = msg;
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 2400);
    }}

    let state = {{
      studentName: '',
      currentIndex: 0,
      score: 0,
      answersLog: []
    }};

    /* GRADING SYSTEM: Scale 0 to 7.0 (Minimum Passing Grade: 4.0 at 60%) */
    function calculateGrade(score, total = 20) {{
      const passingScore = Math.round(total * 0.6); // 12
      let grade;
      if (score <= passingScore) {{
        grade = (score / passingScore) * 4.0;
      }} else {{
        grade = 4.0 + ((score - passingScore) / (total - passingScore)) * 3.0;
      }}
      return Math.round(grade * 10) / 10;
    }}

    /* PERFORMANCE CLASSIFICATION SYSTEM */
    function getClassification(grade) {{
      if (grade >= 6.0) {{
        return {{
          name: 'Excelencia Académica',
          range: '6.0 – 7.0',
          desc: 'Representa rendimiento sobresaliente, demostrando dominio avanzado y desempeño cercano al máximo estándar institucional.',
          badgeClass: 'excelencia',
          isApproved: true
        }};
      }} else if (grade >= 5.0) {{
        return {{
          name: 'Mérito Académico',
          range: '5.0 – 5.9',
          desc: 'Indica un desempeño sólido, por encima del promedio, con comprensión amplia y aplicación adecuada de los contenidos.',
          badgeClass: 'merito',
          isApproved: true
        }};
      }} else if (grade >= 4.0) {{
        return {{
          name: 'Participación Académica',
          range: '4.0 – 4.9',
          desc: 'Corresponde al cumplimiento mínimo de los objetivos académicos establecidos. Refleja dominio fundamental de los contenidos evaluados.',
          badgeClass: 'participacion',
          isApproved: true
        }};
      }} else {{
        return {{
          name: 'Refuerzo Requerido',
          range: '0.0 – 3.9',
          desc: 'No se ha alcanzado la nota mínima aprobatoria (4.0). Se requiere profundizar en la Guía Maestra para obtener la certificación.',
          badgeClass: 'reprobado',
          isApproved: false
        }};
      }}
    }}

    function renderWelcomeScreen() {{
      appContent.innerHTML = `
        <div class="luxury-card welcome-screen">
          <div class="logo-hero-container">
            <img src="assets/logo_bella_gold_transparent.png" alt="BELLA Beauty Academy Logo" class="logo-hero">
          </div>
          
          <div class="script-sub">Evaluación de Desempeño Académico</div>
          <h1 class="hero-title">CASOS CLÍNICOS DE CABINA</h1>
          
          <div class="hero-trainer-badge">
            <img src="assets/master_trainer_esmeralda.jpg" alt="Esmeralda Rodríguez" class="trainer-avatar-mini">
            <span>Master Trainer Esmeralda Ysbely Rodríguez</span>
          </div>

          <p class="welcome-intro-text">
            Bienvenida a la evaluación oficial del <strong>Curso Brow Artist</strong> de <strong>BELLA BEAUTY ACADEMY</strong>. 
            Esta instancia mide tu capacidad de resolución técnica en 20 casos de cabina fundamentados estrictamente en la 
            <strong>Guía Maestra Profesional</strong>.
          </p>

          <div class="scale-info-box">
            <strong>Criterios de Evaluación y Clasificación Institucional:</strong><br>
            • <strong>Escala de Calificación:</strong> 0.0 a 7.0 · <strong>Nota mínima de aprobación:</strong> 4.0<br>
            • <strong>Participación Académica (4.0 – 4.9):</strong> Cumplimiento y dominio fundamental.<br>
            • <strong>Mérito Académico (5.0 – 5.9):</strong> Desempeño sólido y aplicación adecuada.<br>
            • <strong>Excelencia Académica (6.0 – 7.0):</strong> Rendimiento sobresaliente y dominio avanzado.<br>
            <span style="font-size: 11.5px; color: var(--gold-primary); display: block; margin-top: 4px;">
              * El Certificado Oficial de Rendimiento se emitirá exclusivamente al alcanzar una calificación igual o superior a 4.0.
            </span>
          </div>

          <div class="features-grid">
            <div class="feature-item">
              <div class="feature-icon">✨</div>
              <div class="feature-text">20 Casos Reales</div>
            </div>
            <div class="feature-item">
              <div class="feature-icon">🔬</div>
              <div class="feature-text">8 Horas Académicas</div>
            </div>
            <div class="feature-item">
              <div class="feature-icon">⚡</div>
              <div class="feature-text">Feedback Inmediato</div>
            </div>
            <div class="feature-item">
              <div class="feature-icon">🏆</div>
              <div class="feature-text">Certificación Oficial</div>
            </div>
          </div>

          <div class="name-input-group">
            <label class="name-input-label" for="studentNameInput">Ingresa tu Nombre y Apellido Completo:</label>
            <input type="text" id="studentNameInput" class="luxury-input" placeholder="Ej. Valentina Morales Gómez" autocomplete="off">
          </div>

          <button class="btn-gold-cta" onclick="startQuiz()">
            <span>Comenzar Evaluación</span>
            <span>›</span>
          </button>
        </div>
      `;

      const input = document.getElementById('studentNameInput');
      input.addEventListener('keypress', (e) => {{
        if (e.key === 'Enter') startQuiz();
      }});
      input.focus();
    }}

    function startQuiz() {{
      const name = document.getElementById('studentNameInput').value.trim();
      if (!name) {{
        showToast('Por favor, ingresa tu nombre completo para continuar');
        document.getElementById('studentNameInput').focus();
        return;
      }}
      sound.init();
      state.studentName = name;
      state.currentIndex = 0;
      state.score = 0;
      state.answersLog = [];
      renderQuestionScreen();
    }}

    function renderQuestionScreen() {{
      const q = QUESTIONS_DATA[state.currentIndex];
      const total = QUESTIONS_DATA.length;
      const progressPct = ((state.currentIndex) / total) * 100;

      appContent.innerHTML = `
        <div class="quiz-hud">
          <div class="hud-header">
            <span class="hud-case-counter">Caso Clínico ${{state.currentIndex + 1}} de ${{total}}</span>
            <span class="hud-score-pill">Aciertos: ${{state.score}} / ${{state.currentIndex}}</span>
          </div>
          <div class="progress-bar-wrap">
            <div class="progress-bar-fill" style="width: ${{progressPct}}%"></div>
          </div>
        </div>

        <div class="luxury-card">
          <div class="case-category-pill">${{q.category}}</div>
          <div class="case-title-num">Caso Nº ${{state.currentIndex + 1}}</div>
          <div class="case-question-text">${{q.question}}</div>

          <div class="options-grid" id="optionsContainer">
            ${{q.options.map(opt => `
              <div class="option-card" data-letter="${{opt.letter}}" onclick="selectOption('${{opt.letter}}')">
                <div class="option-letter">${{opt.letter}}</div>
                <div class="option-body">${{opt.text}}</div>
              </div>
            `).join('')}}
          </div>

          <div class="feedback-drawer" id="feedbackDrawer"></div>

          <div class="quiz-next-actions" id="nextActions" style="display: none;">
            <button class="btn-gold-cta" onclick="nextQuestion()">
              <span>${{state.currentIndex + 1 < total ? 'Siguiente Caso' : 'Ver Resultados y Certificado'}}</span>
              <span>›</span>
            </button>
          </div>
        </div>
      `;
    }}

    function selectOption(selectedLetter) {{
      const q = QUESTIONS_DATA[state.currentIndex];
      const container = document.getElementById('optionsContainer');
      const optionCards = container.querySelectorAll('.option-card');
      
      // Lock options
      optionCards.forEach(c => c.classList.add('locked'));
      
      const chosenOpt = q.options.find(o => o.letter === selectedLetter);
      const correctOpt = q.options.find(o => o.isCorrect);
      const isUserCorrect = chosenOpt.isCorrect;

      if (isUserCorrect) {{
        state.score++;
        sound.playCorrect();
      }} else {{
        sound.playIncorrect();
      }}

      // Record in history log
      state.answersLog.push({{
        caseId: q.id,
        question: q.question,
        category: q.category,
        reference: q.reference,
        selectedLetter: selectedLetter,
        isCorrect: isUserCorrect,
        chosenFeedback: chosenOpt.feedback,
        correctOption: correctOpt
      }});

      // Stylize cards
      optionCards.forEach(card => {{
        const letter = card.getAttribute('data-letter');
        if (letter === correctOpt.letter) {{
          card.classList.add('correct');
        }} else if (letter === selectedLetter && !isUserCorrect) {{
          card.classList.add('incorrect-selected');
        }} else {{
          card.classList.add('faded');
        }}
      }});

      // Display Detailed Feedback Drawer
      const feedbackDrawer = document.getElementById('feedbackDrawer');
      feedbackDrawer.style.display = 'block';

      feedbackDrawer.innerHTML = `
        <div class="feedback-status-badge ${{isUserCorrect ? 'ok' : 'bad'}}">
          <span>${{isUserCorrect ? '✔ ¡Respuesta Correcta!' : '✖ Análisis del Error'}}</span>
        </div>
        
        <div class="feedback-user-rationale">
          <strong>Dictamen Técnico:</strong> ${{chosenOpt.feedback}}
        </div>

        ${{!isUserCorrect ? `
          <div class="feedback-correct-recap">
            <strong>Conducta Correcta (${{correctOpt.letter}}):</strong> ${{correctOpt.text}}<br>
            <span style="font-size: 13px; color: var(--text-main); margin-top: 4px; display: block;">${{correctOpt.feedback}}</span>
          </div>
        ` : ''}}

        <div class="feedback-source-ref">
          <span>Fundamentación:</span> ${{q.reference}}
        </div>
      `;

      document.getElementById('nextActions').style.display = 'flex';
      feedbackDrawer.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
    }}

    function nextQuestion() {{
      state.currentIndex++;
      if (state.currentIndex < QUESTIONS_DATA.length) {{
        renderQuestionScreen();
      }} else {{
        renderResultsScreen();
      }}
    }}

    function renderResultsScreen() {{
      const total = QUESTIONS_DATA.length;
      const score = state.score;
      const percentage = Math.round((score / total) * 100);
      const grade = calculateGrade(score, total);
      const classif = getClassification(grade);

      if (classif.isApproved) {{
        sound.playFanfare();
        triggerGoldenConfetti();
      }}

      const currentDate = new Date().toLocaleDateString('es-ES', {{
        day: '2-digit',
        month: 'long',
        year: 'numeric'
      }});

      // Errors list for "¿Dónde reforzar?"
      const errors = state.answersLog.filter(x => !x.isCorrect);

      appContent.innerHTML = `
        <!-- CERTIFICATE SECTION (ONLY VISIBLE AND DOWNLOADABLE IF GRADE >= 4.0) -->
        ${{classif.isApproved ? `
          <div class="cert-stage" id="certStage">
            <div class="cert-scaler" id="certScaler">
              <div class="certificate-card" id="certificateToPrint" style="background-image: url('${{CERT_IMG.bg}}');">
                <div class="cert-shade"></div>
                <div class="cert-frame-outer"></div>
                <div class="cert-frame-inner"></div>
                <div class="cert-corner tl"></div><div class="cert-corner tr"></div>
                <div class="cert-corner bl"></div><div class="cert-corner br"></div>

                <img class="cert-logo-img" src="${{CERT_IMG.logo}}" alt="BELLA Beauty Academy">

                <div class="cert-abs cert-main-title">Certificado de Rendimiento</div>
                <div class="cert-abs cert-preamble">Por haber acreditado satisfactoriamente el</div>
                <div class="cert-abs cert-course-name">Curso Brow Artist</div>

                <div class="cert-abs cert-mencion">
                  <span class="cert-mencion-line"></span>
                  <span class="cert-mencion-text">Mención ${{classif.name}}</span>
                  <span class="cert-mencion-line"></span>
                </div>

                <div class="cert-abs cert-award-to">Se otorga la siguiente distinción a:</div>
                <div class="cert-abs cert-student-name" id="certStudentName">${{formatStudentName(state.studentName)}}</div>
                <div class="cert-name-rule"></div>

                <p class="cert-abs cert-body-text">
                  Con una carga académica de <strong>8 horas pedagógicas</strong>, demostrando conocimientos formativos y prácticos de alto estándar en:
                  <strong>Diseño, Mapping, Epilación, Tinturado Semipermanente con Henna y Laminado de Cejas</strong>.
                </p>

                <div class="cert-sig-left">
                  <img class="cert-signature-img" src="${{CERT_IMG.sig}}" alt="Firma Esmeralda Rodríguez">
                  <div class="cert-sig-line"></div>
                  <div class="cert-sig-name">Esmeralda Y. Rodríguez Araviche</div>
                  <div class="cert-sig-role">Master Trainer de BELLA ACADEMY</div>
                </div>

                <div class="cert-sig-right">
                  <div class="cert-date-label">Fecha de Evaluación Oficial</div>
                  <div class="cert-date-val">${{currentDate}}</div>
                  <div class="cert-date-sub">Bella Beauty Academy · Chile</div>
                </div>
              </div>
            </div>
          </div>
        ` : ''}}

        <!-- INDEPENDENT SUMMARY SECTION BELOW (CONSOLIDADO DE NOTAS Y DIAGNÓSTICO) -->
        <div class="summary-report-card">
          
          <h2 class="summary-title">Consolidado de Desempeño y Diagnóstico Clínico</h2>

          <div class="summary-kpi-grid">
            <div class="kpi-card">
              <div class="kpi-label">Nota Final Oficial</div>
              <div class="kpi-val">${{grade.toFixed(1)}}</div>
              <div class="kpi-status ${{classif.isApproved ? 'ok' : 'bad'}}">
                ${{classif.isApproved ? 'Aprobada (Mínimo 4.0)' : 'No Aprobada (Mínimo 4.0)'}}
              </div>
            </div>

            <div class="kpi-card">
              <div class="kpi-label">Aciertos Totales</div>
              <div class="kpi-val">${{score}} / ${{total}}</div>
              <div class="kpi-status ${{classif.isApproved ? 'ok' : 'bad'}}">${{percentage}}% de Efectividad</div>
            </div>

            <div class="kpi-card">
              <div class="kpi-label">Clasificación Institucional</div>
              <div class="kpi-val" style="font-size: 18px; line-height: 1.3; margin-top: 4px;">${{classif.name}}</div>
              <div class="kpi-status ok" style="color: var(--gold-primary); font-size: 11px;">Rango ${{classif.range}}</div>
            </div>
          </div>

          <!-- SECCIÓN: ¿DÓNDE REFORZAR? -->
          <div class="reinforce-box ${{errors.length === 0 ? 'all-correct' : ''}}">
            <div class="reinforce-heading">
              <span>${{errors.length === 0 ? '🌟 ¡Dominio Clínico Impecable!' : '📌 Diagnóstico de Casos: ¿Dónde Reforzar?'}}</span>
            </div>
            
            ${{errors.length > 0 ? `
              <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 12px;">
                Para alcanzar la máxima maestría en cabina y proteger la integridad de tus clientas, te recomendamos revisar los siguientes temas específicos:
              </p>
              <div class="reinforce-items-list">
                ${{errors.map(err => `
                  <div class="reinforce-item">
                    <strong>Caso ${{err.caseId}}: ${{err.category}}</strong><br>
                    <span style="color: var(--text-main); font-weight: normal;">Situación evaluada: "${{err.question}}"</span>
                    <span>Consúltalo en: ${{err.reference}}</span>
                  </div>
                `).join('')}}
              </div>
            ` : `
              <p style="font-size: 14px; color: var(--text-main); line-height: 1.6;">
                ¡Felicidades, ${{state.studentName}}! Has resuelto de forma 100% correcta los 20 casos clínicos evaluados. Tu criterio técnico y de bioseguridad se encuentra en el estándar superior de la industria.
              </p>
            `}}

            <div class="motivational-msg">
              "Tu pasión, compromiso y rigor técnico son los que marcan la diferencia en el mundo de la belleza profesional. 
              En <strong>BELLA BEAUTY ACADEMY</strong> te felicitamos por tu entrega y te motivamos a continuar capacitándote 
              en nuestras próximas certificaciones internacionales con la Master Trainer Esmeralda Rodríguez."
            </div>
          </div>

          <!-- CASOS CLÍNICOS DESGLOSADOS (ACORDEÓN DE REVISIÓN) -->
          <div class="review-section">
            <h3 class="review-header-title">Revisión Detallada de los 20 Casos</h3>
            <div class="review-list">
              ${{state.answersLog.map((log, idx) => `
                <div class="review-card" onclick="toggleReviewCard(this)">
                  <div class="review-card-head">
                    <span class="review-card-title">Caso ${{idx + 1}}: ${{log.category}}</span>
                    <span class="review-tag ${{log.isCorrect ? 'ok' : 'bad'}}">
                      ${{log.isCorrect ? '✔ Acierto' : '✖ Reforzar'}}
                    </span>
                  </div>
                  <div class="review-card-details">
                    <p style="margin-bottom: 6px; color: #fff;"><strong>Situación:</strong> ${{log.question}}</p>
                    <p style="margin-bottom: 6px;"><strong>Opción elegida (${{log.selectedLetter}}):</strong> ${{log.chosenFeedback}}</p>
                    ${{!log.isCorrect ? `
                      <p style="margin-bottom: 6px; color: var(--gold-light);">
                        <strong>Conducta correcta (${{log.correctOption.letter}}):</strong> ${{log.correctOption.text}}<br>
                        <em>${{log.correctOption.feedback}}</em>
                      </p>
                    ` : ''}}
                    <p style="font-size: 11.5px; color: var(--gold-primary);">
                      <strong>Capítulo Guía:</strong> ${{log.reference}}
                    </p>
                  </div>
                </div>
              `).join('')}}
            </div>
          </div>

          <div class="results-actions">
            ${{classif.isApproved ? `
              <button class="btn-gold-cta" id="btnDownloadCert" onclick="downloadCertificatePDF()">
                <span>Descargar Certificado en PDF</span>
              </button>
            ` : `
              <button class="btn-gold-cta" onclick="renderWelcomeScreen()">
                <span>Repasar Guía y Reintentar Evaluación</span>
              </button>
            `}}
            <button class="btn-secondary" onclick="shareResults()">
              <span>Compartir Rendimiento</span>
            </button>
            ${{classif.isApproved ? `
              <button class="btn-secondary" onclick="renderWelcomeScreen()">
                <span>Reevaluar</span>
              </button>
            ` : ''}}
          </div>

        </div>
      `;
      requestAnimationFrame(() => {{ fitCertificate(); }});
    }}

    function toggleReviewCard(card) {{
      card.classList.toggle('open');
    }}

    function formatStudentName(raw) {{
      const small = ['de', 'del', 'la', 'las', 'los', 'y', 'e', 'da', 'di', 'van', 'von'];
      return String(raw || '').trim().replace(/\\s+/g, ' ').toLowerCase().split(' ').map((w, i) =>
        (i > 0 && small.includes(w)) ? w : w.charAt(0).toUpperCase() + w.slice(1)
      ).join(' ').replace(/[<>&]/g, '');
    }}

    // Shrink the student's name if it would not fit inside the frame
    function fitStudentName(root) {{
      const el = (root || document).querySelector('#certStudentName, .cert-student-name');
      if (!el) return;
      let size = 92;
      el.style.fontSize = size + 'px';
      const probe = document.createElement('span');
      probe.style.cssText = 'position:absolute;visibility:hidden;white-space:nowrap;font:inherit;';
      probe.textContent = el.textContent;
      el.appendChild(probe);
      while (probe.offsetWidth > 880 && size > 40) {{
        size -= 2;
        el.style.fontSize = size + 'px';
      }}
      el.removeChild(probe);
    }}

    // Scale the fixed 1123x794 certificate to the available width (on screen only)
    function fitCertificate() {{
      const stage = document.getElementById('certStage');
      const scaler = document.getElementById('certScaler');
      if (!stage || !scaler) return;
      fitStudentName(scaler);
      const w = stage.clientWidth;
      const s = Math.min(1, w / 1123);
      scaler.style.transform = 'scale(' + s + ')';
      scaler.style.left = Math.max(0, (w - 1123 * s) / 2) + 'px';
      stage.style.height = (794 * s) + 'px';
    }}
    window.addEventListener('resize', fitCertificate);
    if (document.fonts && document.fonts.ready) {{
      document.fonts.ready.then(() => {{ fitCertificate(); }});
    }}

    async function buildCertificatePDF(mode) {{
      const src = document.getElementById('certificateToPrint');
      if (!src) throw new Error('Certificado no disponible');
      if (typeof html2pdf === 'undefined') throw new Error('html2pdf no cargado');

      // html2pdf clones the node by itself (no parent scale transform), so the capture is always 1123 x 794 px
      try {{
        if (document.fonts && document.fonts.ready) await document.fonts.ready;
        fitStudentName(src);
        const safeName = formatStudentName(state.studentName).replace(/[^A-Za-z0-9ÁÉÍÓÚáéíóúÑñÜü ]/g, '').trim().replace(/\\s+/g, '_') || 'Alumna';
        const opt = {{
          margin: 0,
          filename: 'Certificado_Brow_Artist_' + safeName + '.pdf',
          image: {{ type: 'jpeg', quality: 0.98 }},
          html2canvas: {{
            scale: 2,
            useCORS: true,
            backgroundColor: '#0a0908',
            scrollX: 0,
            scrollY: 0,
            logging: false
          }},
          jsPDF: {{ unit: 'px', format: [1123, 794], orientation: 'landscape', hotfixes: ['px_scaling'] }}
        }};
        // Force a single-page PDF (remove any trailing blank page caused by rounding)
        const worker = html2pdf().set(opt).from(src).toPdf().get('pdf').then(pdf => {{
          while (pdf.internal.getNumberOfPages() > 1) {{
            pdf.deletePage(pdf.internal.getNumberOfPages());
          }}
        }});
        if (mode === 'datauri') {{
          return await worker.outputPdf('datauristring');
        }}
        await worker.save();
        return null;
      }} finally {{
        fitCertificate();
      }}
    }}

    async function downloadCertificatePDF() {{
      const btn = document.getElementById('btnDownloadCert');
      const label = btn ? btn.querySelector('span') : null;
      const original = label ? label.textContent : '';
      if (btn) {{ btn.disabled = true; btn.style.opacity = '0.7'; }}
      if (label) label.textContent = 'Generando PDF...';
      try {{
        await buildCertificatePDF('save');
        showToast('¡Certificado descargado en PDF!');
      }} catch (err) {{
        console.error(err);
        showToast('No se pudo generar el PDF. Verifica tu conexión e inténtalo nuevamente.');
      }} finally {{
        if (btn) {{ btn.disabled = false; btn.style.opacity = ''; }}
        if (label) label.textContent = original;
      }}
    }}

    function shareResults() {{
      const total = QUESTIONS_DATA.length;
      const score = state.score;
      const pct = Math.round((score / total) * 100);
      const grade = calculateGrade(score, total);
      const classif = getClassification(grade);

      const text = `🏆 ¡Evaluación Curso Brow Artist en BELLA BEAUTY ACADEMY!\\nAlumna: ${{state.studentName}}\\nNota: ${{grade.toFixed(1)}}/7.0 · ${{classif.name}}\\nAciertos: ${{score}}/${{total}} (${{pct}}%)\\nInstructora: Master Trainer Esmeralda Rodríguez Araviche`;
      
      if (navigator.clipboard) {{
        navigator.clipboard.writeText(text).then(() => {{
          showToast('¡Resumen de rendimiento copiado al portapapeles!');
        }});
      }} else {{
        showToast('Nota: ' + grade.toFixed(1) + ' · ' + classif.name);
      }}
    }}

    // Direct Test URL parameters for design verification
    const urlParams = new URLSearchParams(window.location.search);
    const testMode = urlParams.get('test');
    if (testMode === 'quiz') {{
      state.studentName = 'Alumna Prueba';
      state.currentIndex = 0;
      renderQuestionScreen();
    }} else if (testMode === 'approved' || testMode === 'excelencia' || testMode === 'pdfdump') {{
      state.studentName = 'Cinthya Gómez Germán';
      state.score = 18; // Grade 6.3 - Excelencia
      state.answersLog = QUESTIONS_DATA.map((q, i) => ({{
        caseId: q.id,
        question: q.question,
        category: q.category,
        reference: q.reference,
        selectedLetter: q.options.find(o => o.isCorrect).letter,
        isCorrect: i < 18,
        chosenFeedback: q.options.find(o => o.isCorrect).feedback,
        correctOption: q.options.find(o => o.isCorrect)
      }}));
      renderResultsScreen();
    }} else if (testMode === 'participacion') {{
      state.studentName = 'Jose Lino Carcamo';
      state.score = 13; // Grade 4.4 - Participación Académica
      state.answersLog = QUESTIONS_DATA.map((q, i) => ({{
        caseId: q.id,
        question: q.question,
        category: q.category,
        reference: q.reference,
        selectedLetter: q.options.find(o => o.isCorrect).letter,
        isCorrect: i < 13,
        chosenFeedback: q.options.find(o => o.isCorrect).feedback,
        correctOption: q.options.find(o => o.isCorrect)
      }}));
      renderResultsScreen();
    }} else if (testMode === 'merito') {{
      state.studentName = 'Valentina Paz Silva';
      state.score = 16; // Grade 5.5 - Mérito Académico
      state.answersLog = QUESTIONS_DATA.map((q, i) => ({{
        caseId: q.id,
        question: q.question,
        category: q.category,
        reference: q.reference,
        selectedLetter: q.options.find(o => o.isCorrect).letter,
        isCorrect: i < 16,
        chosenFeedback: q.options.find(o => o.isCorrect).feedback,
        correctOption: q.options.find(o => o.isCorrect)
      }}));
      renderResultsScreen();
    }} else if (testMode === 'failed') {{
      state.studentName = 'Alumna Prueba';
      state.score = 7; // Grade 2.3 - Reprobado (< 4.0)
      state.answersLog = QUESTIONS_DATA.map((q, i) => ({{
        caseId: q.id,
        question: q.question,
        category: q.category,
        reference: q.reference,
        selectedLetter: 'A',
        isCorrect: i < 7,
        chosenFeedback: q.options[0].feedback,
        correctOption: q.options.find(o => o.isCorrect)
      }}));
      renderResultsScreen();
    }} else {{
      renderWelcomeScreen();
    }}

    if (testMode === 'pdfdump') {{
      window.addEventListener('load', async () => {{
        const out = document.createElement('pre');
        out.id = 'pdfdump';
        document.body.appendChild(out);
        try {{
          await new Promise(r => setTimeout(r, 800));
          out.textContent = 'PDFDATA:' + await buildCertificatePDF('datauri');
        }} catch (e) {{
          out.textContent = 'PDFERROR:' + e;
        }}
      }});
    }}
  </script>
</body>
</html>
"""

# Save to BELLA_QUIZ_WEB
with open(r"c:\Curso Cejas\BELLA_QUIZ_WEB\index.html", "w", encoding="utf-8") as f:
    f.write(html)

# Save copy to GUIAS FINALES
with open(r"c:\Curso Cejas\GUIAS FINALES\Cuestionario_Casos_BELLA.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated app with 20 questions, grading scale 0-7.0, and luxury certificate successfully.")
