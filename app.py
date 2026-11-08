from flask import Flask, render_template_string
import os

app = Flask(__name__)


PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#10152b">
  <title>Demo App · Live on Minikube</title>
  <style>
    :root {
      color-scheme: dark;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #10152b;
      color: #f7f7ff;
    }

    * { box-sizing: border-box; }

    body {
      min-height: 100vh;
      margin: 0;
      display: grid;
      place-items: center;
      overflow: hidden;
      background:
        radial-gradient(ellipse at 18% 18%, #5727a855, transparent 36%),
        radial-gradient(ellipse at 84% 78%, #00c9a755, transparent 34%),
        #10152b;
    }

    .glow {
      position: fixed;
      width: 18rem;
      aspect-ratio: 1;
      border-radius: 50%;
      background: linear-gradient(135deg, #ff4ecd, #6c63ff 55%, #00e0b8);
      filter: blur(2px);
      opacity: .7;
      animation: float 9s ease-in-out infinite alternate;
    }

    .glow.one { top: -10rem; left: -7rem; }
    .glow.two {
      right: -9rem;
      bottom: -11rem;
      width: 25rem;
      animation-delay: -4s;
    }

    main {
      position: relative;
      width: min(90vw, 42rem);
      padding: clamp(2rem, 7vw, 4.5rem);
      border: 1px solid #ffffff24;
      border-radius: 2rem;
      background: #171d35d9;
      box-shadow: 0 2rem 7rem #05071288, inset 0 1px #ffffff18;
      backdrop-filter: blur(18px);
      animation: arrive .8s cubic-bezier(.2, .8, .2, 1) both;
    }

    .eyebrow {
      display: inline-flex;
      align-items: center;
      gap: .55rem;
      margin: 0 0 1.8rem;
      color: #a9f5dc;
      font-size: .75rem;
      font-weight: 750;
      letter-spacing: .14em;
      text-transform: uppercase;
    }

    .dot {
      width: .55rem;
      aspect-ratio: 1;
      border-radius: 50%;
      background: #43f0ae;
      box-shadow: 0 0 1rem #43f0ae;
      animation: pulse 1.8s ease-in-out infinite;
    }

    h1 {
      max-width: 10ch;
      margin: 0;
      font-size: clamp(3rem, 10vw, 5.5rem);
      line-height: .96;
      letter-spacing: -.075em;
    }

    h1 span {
      color: transparent;
      background: linear-gradient(100deg, #ff70d4, #a795ff 52%, #70f4ce);
      background-clip: text;
      -webkit-background-clip: text;
    }

    .intro {
      max-width: 31rem;
      margin: 1.6rem 0 2.4rem;
      color: #bec5dd;
      font-size: 1.05rem;
      line-height: 1.7;
    }

    .version {
      display: inline-flex;
      align-items: center;
      gap: .7rem;
      padding: .8rem 1rem;
      border: 1px solid #ffffff1c;
      border-radius: 1rem;
      background: #ffffff0a;
      color: #e7e9f7;
      font-size: .9rem;
    }

    .version strong { color: #70f4ce; }

    .metadata {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(9rem, 1fr));
      gap: .75rem;
      margin-top: 1.25rem;
    }

    .metadata-item {
      min-width: 0;
      padding: 1rem;
      border: 1px solid #ffffff1c;
      border-radius: 1rem;
      background: #ffffff08;
    }

    .metadata-item span {
      display: block;
      margin-bottom: .5rem;
      color: #9da7c5;
      font-size: .72rem;
      line-height: 1.4;
    }

    .metadata-item strong {
      display: block;
      overflow-wrap: anywhere;
      color: #e7e9f7;
      font-size: 1rem;
    }

    footer {
      margin-top: 2.5rem;
      color: #7f89a8;
      font-size: .8rem;
      letter-spacing: .04em;
    }

    @keyframes float {
      to { transform: translate(3rem, 2rem) scale(1.12); }
    }

    @keyframes pulse {
      50% { opacity: .55; transform: scale(.78); }
    }

    @keyframes arrive {
      from { opacity: 0; transform: translateY(1.2rem) scale(.98); }
      to { opacity: 1; transform: translateY(0) scale(1); }
    }

    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: .01ms !important;
        animation-iteration-count: 1 !important;
        scroll-behavior: auto !important;
      }
    }
  </style>
</head>
<body>
  <div class="glow one" aria-hidden="true"></div>
  <div class="glow two" aria-hidden="true"></div>
  <main>
    <p class="eyebrow"><span class="dot" aria-hidden="true"></span> Live on Minikube</p>
    <h1>Small app.<br><span>Big energy.</span></h1>
    <p class="intro">
      A little Flask demo, delivered by Jenkins and now happily running in your cluster.
      The best kind of deployment is the one you can see.
    </p>
    <div class="version">
      <span aria-hidden="true">✦</span>
      Deployed version <strong>{{ version }}</strong>
    </div>
    <section class="metadata" aria-label="Deployment metadata">
      <div class="metadata-item">
        <span>Jenkins build number</span>
        <strong>{{ build_number }}</strong>
      </div>
      <div class="metadata-item">
        <span>Helm revision</span>
        <strong>{{ helm_revision }}</strong>
      </div>
      <div class="metadata-item">
        <span>Helm history version</span>
        <strong>{{ helm_history_version }}</strong>
      </div>
      <div class="metadata-item">
        <span>Helm chart version</span>
        <strong>{{ chart_version }}</strong>
      </div>
      <div class="metadata-item">
        <span>Helm chart appVersion</span>
        <strong>{{ chart_app_version }}</strong>
      </div>
    </section>
    <footer>BUILT WITH FLASK · SHIPPED WITH HELM</footer>
  </main>
</body>
</html>"""


@app.route("/")
def hello():
    return render_template_string(
        PAGE,
        version=os.getenv("APP_VERSION", "dev"),
        build_number=os.getenv("JENKINS_BUILD_NUMBER", "local"),
        helm_revision=os.getenv("HELM_REVISION", "local"),
        helm_history_version=os.getenv("HELM_HISTORY_VERSION", "local"),
        chart_version=os.getenv("HELM_CHART_VERSION", "local"),
        chart_app_version=os.getenv("HELM_CHART_APP_VERSION", "local"),
    )

@app.route("/health")
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
