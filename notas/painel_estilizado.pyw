import os
import xmltodict
import tkinter as tk
from tkinter import filedialog, scrolledtext
from datetime import datetime

def valor_float(valor_str):
    try:
        if not valor_str:
            return 0.0
        return float(valor_str)
    except:
        return 0.0

def processar_xmls():
    caminho_pasta = filedialog.askdirectory(title="Selecione a pasta com XMLs")
    if not caminho_pasta:
        return

    total_geral = 0.0
    notas_autorizadas = 0
    notas_canceladas = 0
    arquivos_lidos = 0
    datas_emissao = []

    icms_total = 0.0
    ipi_total = 0.0
    pis_total = 0.0
    cofins_total = 0.0

    log_texto.delete(1.0, tk.END)

    for nome_arquivo in os.listdir(caminho_pasta):
        if nome_arquivo.lower().endswith('.xml'):
            caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)
            try:
                with open(caminho_arquivo, encoding='utf-8') as f:
                    conteudo = xmltodict.parse(f.read())

                    if arquivos_lidos == 0:
                        try:
                            emitente = conteudo['nfeProc']['NFe']['infNFe']['emit']
                            nome_empresa = emitente.get('xNome', 'Nome não encontrado')
                            cnpj = emitente.get('CNPJ', 'CNPJ não encontrado')
                            if cnpj and len(cnpj) == 14:
                                cnpj_formatado = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
                            else:
                                cnpj_formatado = cnpj
                            empresa_var.set(f"Empresa: {nome_empresa}")
                            cnpj_var.set(f"CNPJ: {cnpj_formatado}")
                        except:
                            empresa_var.set("Empresa: erro na leitura")
                            cnpj_var.set("CNPJ: erro na leitura")

                    try:
                        dhEmi = conteudo['nfeProc']['NFe']['infNFe']['ide']['dhEmi']
                        data_emissao = datetime.fromisoformat(dhEmi.replace("Z", "+00:00"))
                        datas_emissao.append(data_emissao)
                    except:
                        log_texto.insert(tk.END, f"⚠️ Falha ao ler data de emissão em {nome_arquivo}\n")

                    status = conteudo['nfeProc']['protNFe']['infProt']['cStat']

                    if status == '100':
                        totais = conteudo['nfeProc']['NFe']['infNFe']['total']['ICMSTot']

                        valor_nf = valor_float(totais.get('vNF'))
                        total_geral += valor_nf
                        notas_autorizadas += 1

                        icms_total += valor_float(totais.get('vICMS'))
                        ipi_total += valor_float(totais.get('vIPI'))
                        pis_total += valor_float(totais.get('vPIS'))
                        cofins_total += valor_float(totais.get('vCOFINS'))

                        log_texto.insert(tk.END, f"✅ {nome_arquivo} AUTORIZADA → R$ {valor_nf:.2f}\n")
                    elif status in ['101', '135', '151']:
                        notas_canceladas += 1
                        log_texto.insert(tk.END, f"❌ {nome_arquivo} CANCELADA\n")
                    else:
                        log_texto.insert(tk.END, f"⚠️ {nome_arquivo} STATUS DESCONHECIDO: {status}\n")

                    arquivos_lidos += 1
            except Exception as e:
                log_texto.insert(tk.END, f"Erro ao processar {nome_arquivo}: {e}\n")

    valor_total_var.set(f"R$ {total_geral:,.2f}")
    arquivos_lidos_var.set(str(arquivos_lidos))
    autorizadas_var.set(str(notas_autorizadas))
    canceladas_var.set(str(notas_canceladas))

    icms_var.set(f"R$ {icms_total:,.2f}")
    ipi_var.set(f"R$ {ipi_total:,.2f}")
    pis_var.set(f"R$ {pis_total:,.2f}")
    cofins_var.set(f"R$ {cofins_total:,.2f}")

    if datas_emissao:
        data_inicial = min(datas_emissao).strftime('%d/%m/%Y')
        data_final = max(datas_emissao).strftime('%d/%m/%Y')
        intervalo_data_var.set(f"📅 De {data_inicial} até {data_final}")
    else:
        intervalo_data_var.set("📅 Nenhuma data encontrada")

def limpar_dados():
    valor_total_var.set("R$ 0,00")
    arquivos_lidos_var.set("0")
    autorizadas_var.set("0")
    canceladas_var.set("0")
    icms_var.set("R$ 0,00")
    ipi_var.set("R$ 0,00")
    pis_var.set("R$ 0,00")
    cofins_var.set("R$ 0,00")
    intervalo_data_var.set("📅 Nenhuma data carregada")
    empresa_var.set("Empresa: —")
    cnpj_var.set("CNPJ: —")
    log_texto.delete(1.0, tk.END)

# Interface
janela = tk.Tk()
janela.title("Painel de Notas Fiscais XML")
janela.geometry("950x700")
janela.configure(bg="#f4f6f8")

# Variáveis
valor_total_var = tk.StringVar(value="R$ 0,00")
arquivos_lidos_var = tk.StringVar(value="0")
autorizadas_var = tk.StringVar(value="0")
canceladas_var = tk.StringVar(value="0")
icms_var = tk.StringVar(value="R$ 0,00")
ipi_var = tk.StringVar(value="R$ 0,00")
pis_var = tk.StringVar(value="R$ 0,00")
cofins_var = tk.StringVar(value="R$ 0,00")
intervalo_data_var = tk.StringVar(value="📅 Nenhuma data carregada")
empresa_var = tk.StringVar(value="Empresa: —")
cnpj_var = tk.StringVar(value="CNPJ: —")

# Botões
botoes_frame = tk.Frame(janela, bg="#f4f6f8")
botoes_frame.pack(pady=15)

tk.Button(
    botoes_frame, text="📂 Selecionar Pasta com XMLs", command=processar_xmls,
    bg="#007acc", fg="white", font=("Segoe UI", 12, "bold"),
    padx=20, pady=10, bd=0, activebackground="#005f99", cursor="hand2"
).pack(side="left", padx=10)

tk.Button(
    botoes_frame, text="🔄 Limpar e Recomeçar", command=limpar_dados,
    bg="#e0e0e0", fg="#333", font=("Segoe UI", 12),
    padx=20, pady=10, bd=0, activebackground="#c0c0c0", cursor="hand2"
).pack(side="left", padx=10)

# Labels empresa e datas
tk.Label(janela, textvariable=empresa_var, bg="#f4f6f8", fg="#111", font=("Segoe UI", 11, "bold")).pack()
tk.Label(janela, textvariable=cnpj_var, bg="#f4f6f8", fg="#555", font=("Segoe UI", 10)).pack()
tk.Label(janela, textvariable=intervalo_data_var, bg="#f4f6f8", fg="#444", font=("Segoe UI", 11, "italic")).pack()

# Cards
cards_frame = tk.Frame(janela, bg="#f4f6f8")
cards_frame.pack()

def criar_card(titulo, variavel, cor_fundo="#ffffff"):
    card = tk.Frame(cards_frame, bg=cor_fundo, width=200, height=90, bd=1, relief="ridge")
    card.pack_propagate(False)
    card.pack(side="left", padx=12, pady=5)
    tk.Label(card, text=titulo, font=("Segoe UI", 10, "bold"), bg=cor_fundo, fg="#333").pack(pady=(10, 0))
    tk.Label(card, textvariable=variavel, font=("Segoe UI", 14, "bold"), bg=cor_fundo, fg="#007acc").pack()

criar_card("💰 Total em Vendas", valor_total_var)
criar_card("📄 Arquivos Lidos", arquivos_lidos_var)
criar_card("✅ Notas Autorizadas", autorizadas_var)
criar_card("❌ Notas Canceladas", canceladas_var)
criar_card("🧾 ICMS", icms_var)
criar_card("🏭 IPI", ipi_var)
criar_card("📌 PIS", pis_var)
criar_card("📎 COFINS", cofins_var)

# Log
frame_log = tk.Frame(janela, bg="#f4f6f8")
frame_log.pack(padx=10, pady=20, fill="both", expand=True)

tk.Label(frame_log, text="📋 Detalhes das Notas:", font=("Segoe UI", 11, "bold"), bg="#f4f6f8", fg="#444").pack(anchor="w", padx=5, pady=(0, 5))

log_texto = scrolledtext.ScrolledText(frame_log, width=105, height=20, font=("Courier New", 9),
                                      bg="white", fg="#222", bd=1, relief="solid")
log_texto.pack(fill="both", expand=True)

janela.mainloop()
