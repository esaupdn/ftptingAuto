# 🕵️‍♂️ Footprinting Automático com Python

Ferramenta simples e eficiente para realizar footprinting (reconhecimento inicial) de um domínio, utilizando consultas DNS e verificação de portas abertas. O projeto gera automaticamente um relatório TXT com todos os resultados obtidos.

## 📌 Sobre o Projeto
Este projeto realiza um levantamento de informações públicas (OSINT) sobre um domínio alvo, executando consultas DNS (A, MX, NS, TXT), verificação de portas comuns e geração automática de relatório em TXT. Ele é ideal para estudos de cibersegurança, portfólio, demonstrações no LinkedIn e treinos de técnicas de footprinting.

## 🧠 Tecnologias Utilizadas
- Python 3  
- dnspython (consultas DNS)  
- socket (port scanning)  
- datetime (timestamp no relatório)

## 🚀 Funcionalidades
O script executa:
- Consulta dos principais registros DNS: A, MX, NS, TXT.  
- Scan das portas mais utilizadas: 80, 443, 21, 22, 25, 3306 e 8080.  
- Geração automática do arquivo `relatorio_footprinting.txt`, contendo domínio analisado, data, registros DNS e portas abertas.

## 🔐 Aviso 
Este projeto é destinado exclusivamente a fins educacionais. Só utilize para analisar domínios que você tenha permissão explícita para testar.

## ⭐ Contribuições
Contribuições são bem-vindas! Sinta-se livre para abrir issues e sugerir melhorias.

## 📎 Autor
Desenvolvido por **Esaú Paiva**.
