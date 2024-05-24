# ベースイメージを指定
FROM python:3.9-alpine

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコードをコピー
COPY . .

# コンテナを起動する際のコマンドを指定
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--access-logfile", "-", "--error-logfile", "-"]

# 必要なポートを公開
EXPOSE 5000

