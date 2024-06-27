FROM nikolaik/python-nodejs:python3.10-nodejs18

# تثبيت ntpdate
RUN apt-get update && apt-get install -y ntpdate

# مزامنة الوقت
RUN ntpdate -s time.nist.gov

# تثبيت المتطلبات
COPY requirements.txt .
RUN pip3 install --no-cache-dir -U -r requirements.txt

# نسخ الكود إلى الحاوية
COPY . .

# الأوامر الافتراضية
CMD ["python", "main.py"]
