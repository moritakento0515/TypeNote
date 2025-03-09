# Pythonの公式イメージを使用
FROM python:3.10

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
COPY requirements.txt requirements-dev.txt .  
RUN pip install --no-cache-dir -r requirements.txt  

# アプリケーションファイルをコピー
COPY . .

# collectstatic を実行
RUN python manage.py collectstatic --noinput

# ポートを開放
EXPOSE 8000

# Gunicornを起動してDjangoを実行
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
