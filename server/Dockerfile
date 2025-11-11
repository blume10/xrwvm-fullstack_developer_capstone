# -------------------------------
# 1️⃣ Basisimage
# -------------------------------
    FROM python:3.12.0-slim-bookworm

    # -------------------------------
    # 2️⃣ Environment-Variablen
    # -------------------------------
    ENV PYTHONUNBUFFERED=1
    ENV PYTHONWRITEBYTECODE=1
    ENV APP=/app
    
    # -------------------------------
    # 3️⃣ Arbeitsverzeichnis ändern
    # -------------------------------
    WORKDIR $APP
    
    # -------------------------------
    # 4️⃣ Abhängigkeiten installieren
    # -------------------------------
    COPY requirements.txt $APP/
    RUN pip install --upgrade pip
    RUN pip install -r requirements.txt
    
    # -------------------------------
    # 5️⃣ Restliche Dateien kopieren
    # -------------------------------
    COPY . $APP
    
    # -------------------------------
    # 6️⃣ Port öffnen
    # -------------------------------
    EXPOSE 8000
    
    # -------------------------------
    # 7️⃣ Entrypoint & Startbefehl
    # -------------------------------
    RUN chmod +x /app/entrypoint.sh
    ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
    CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]
    