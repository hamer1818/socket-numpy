uvicorn main:app --reload --port 8081

pm2 da python komut satırı penceresi açmaması için:
main.py dosyasının eklentsi pyw yapılarak 
pm2 start main.pyw --interpreter=pythonw
ile çalıştırılır..
----------------------------------------
ENVIRONMENT DEKİ PAKETLERİN SAKLANMASIS
environment de kullanılan modullerden requiremenets oluşturma
pip freeze > requiremenets.txt
---------------------------------
KURULUM

python -m venv venv 
ile virtual environtment oluşturulduktan sonra aktif edilir
venv\Scripts\activate

geri yükleme
pip install -r requirements.txt

Nodejs kurulumuna gerek yok