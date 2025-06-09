import requests
import sqlite3
import re
import smtplib
from email.message import EmailMessage

print("Coletando piadas da API do Chuck Norris...")

url = "https://api.chucknorris.io/jokes/random"
piadas = []

for _ in range(10):
    response = requests.get(url)
    data = response.json()
    piadas.append((data["id"], data["value"]))

print("Piadas coletadas com sucesso! Exemplos:")
for piada in piadas[:3]:
    print(piada)

conn = sqlite3.connect("projeto_rpa.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS piadas_chuck (
        id TEXT PRIMARY KEY,
        texto TEXT
    )
''')
print("Tabela 'piadas_chuck' criada/verificada com sucesso!")

cursor.executemany('''
    INSERT OR REPLACE INTO piadas_chuck (id, texto) VALUES (?, ?)
''', piadas)
conn.commit()
print("Piadas inseridas na tabela 'piadas_chuck' com sucesso!")

regex = r'\bCh\w+'
piadas_processadas = []

for piada in piadas:
    if re.search(regex, piada[1]):
        piadas_processadas.append(piada)

print("Piadas processadas (contendo palavras iniciadas por 'Ch'):")
for piada in piadas_processadas[:3]:
    print(piada)

cursor.execute('''
    CREATE TABLE IF NOT EXISTS dados_processados (
        id TEXT PRIMARY KEY,
        texto TEXT
    )
''')
print("Tabela 'dados_processados' criada/verificada com sucesso!")

cursor.executemany('''
    INSERT OR REPLACE INTO dados_processados (id, texto) VALUES (?, ?)
''', piadas_processadas)
conn.commit()
print("Dados inseridos na tabela 'dados_processados' com sucesso!")


EMAIL = "tomazzandrey@gmail.com"
SENHA = "djymxmrfqqqrzuvl"
DESTINATARIO = "tomazzandrey@gmail.com"

mensagem = EmailMessage()
mensagem["Subject"] = "Relatório RPA - Chuck Norris API"
mensagem["From"] = EMAIL
mensagem["To"] = DESTINATARIO

resumo = f'''
Relatório de Piadas do Chuck Norris

Total de piadas coletadas: {len(piadas)}
Total de piadas com palavras iniciadas por "Ch": {len(piadas_processadas)}

Exemplos:
'''
for piada in piadas_processadas[:3]:
    resumo += f"- {piada[1]}\n\n"

mensagem.set_content(resumo)

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL, SENHA)
        smtp.send_message(mensagem)
    print("E-mail enviado com sucesso!")
except Exception as e:
    print(f"Erro ao enviar e-mail: {e}")

conn.close()
