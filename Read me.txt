# Painel e Analisador de Notas Fiscais XML

Este projeto é um conjunto de ferramentas em Python para leitura, análise e soma de vendas a partir de arquivos XML de Notas Fiscais Eletrônicas (NF-e).Inclui uma interface gráfica com Tkinter, um script de soma rápida via terminal e um inicializador automático para Windows.

----------------------------------------------------------------------

# Funcionalidades

📂 Leitura de pastas contendo múltiplos arquivos XML de NF-e.
📊 Cálculo automático de:

* Total em vendas
* Totais de ICMS, IPI, PIS e COFINS
* Quantidade de notas autorizadas e canceladas

🗓️ Detecção automática do intervalo de datas de emissão das notas.
📜 Log detalhado de cada arquivo processado.
🔄 Opção para limpar e reiniciar a análise.
⚡ Inicialização automática no Windows via .bat com instalação de dependências.
📈 Script adicional para somar vendas sem interface gráfica.

----------------------------------------------------------------------

# Estrutura do Projeto

📁 Painel-XML
├── iniciar_painel.bat
├── painel_estilizado.pyw  
├── Soma_vendas_nfe.py    
└── README.md       

----------------------------------------------------------------------

# Requisitos

* Windows
* Python 3.8+
* Bibliotecas Python:
   * xmltodict
   * tkinter (incluso no Python padrão)

----------------------------------------------------------------------

# Como Executar

## Modo Automático (Windows)

Clone ou baixe este repositório:

git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git

Execute o arquivo iniciar_painel.bat com duplo clique.

O script irá:

   * Verificar se o Python está instalado
   * Instalar automaticamente xmltodict (se necessário)
   * Iniciar a aplicação painel_estilizado.pyw

⚠️ Importante: Se o Python não estiver no caminho configurado no .bat, edite a linha: set "PYTHON_DIR=C:\CAMINHO\DO\PYTHON"

## Modo Manual — Painel Gráfico

   * Instale as dependências:
   * pip install xmltodict

Execute o painel:

   * python painel_estilizado.pyw

## Modo Manual — Soma de Vendas via Terminal

   * Instale as dependências:
   * pip install xmltodict

Execute o script:

   * python Soma_vendas_nfe.py

Informe o caminho da pasta contendo os arquivos XML quando solicitado.

----------------------------------------------------------------------

# Interface (painel_estilizado.pyw)

   * Cartões com valores totais e impostos.

   * Informações da empresa e CNPJ.

   * Intervalo de datas automaticamente detectado.

   * Log detalhado de cada nota processada.
