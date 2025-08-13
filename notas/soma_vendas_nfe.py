import os
import xmltodict
from datetime import datetime

caminho_pasta = "C:\\Users\\La Pimienta\\Documents\\Leitor xml\\notas\\XMLS"

if not os.path.exists(caminho_pasta):
    print("🚨 ERRO: Caminho da pasta não encontrado.")
    exit()

total_geral = 0.0
notas_autorizadas = 0
notas_canceladas = 0
notas_desconhecidas = 0
arquivos_lidos = 0
datas_emissao = []

# Impostos totais
icms_total = 0.0
ipi_total = 0.0
pis_total = 0.0
cofins_total = 0.0

nome_empresa = None
cnpj_formatado = None

def valor_float(valor_str):
    try:
        if valor_str is None or valor_str == '':
            return 0.0
        return float(valor_str)
    except:
        return 0.0

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
                        if cnpj != 'CNPJ não encontrado' and len(cnpj) == 14:
                            cnpj_formatado = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
                        else:
                            cnpj_formatado = cnpj
                    except:
                        nome_empresa = "Erro ao ler nome da empresa"
                        cnpj_formatado = "Erro ao ler CNPJ"

                try:
                    dhEmi = conteudo['nfeProc']['NFe']['infNFe']['ide']['dhEmi']
                    data_emissao = datetime.fromisoformat(dhEmi.replace("Z", "+00:00"))
                    datas_emissao.append(data_emissao)
                except:
                    print(f"⚠️ Falha ao ler data de emissão em {nome_arquivo}")

                status = conteudo['nfeProc']['protNFe']['infProt']['cStat']

                if status == '100':
                    totais = conteudo['nfeProc']['NFe']['infNFe']['total']['ICMSTot']
                    valor_nf = valor_float(totais.get('vNF'))

                    icms_total += valor_float(totais.get('vICMS'))
                    ipi_total += valor_float(totais.get('vIPI'))
                    pis_total += valor_float(totais.get('vPIS'))
                    cofins_total += valor_float(totais.get('vCOFINS'))

                    total_geral += valor_nf
                    notas_autorizadas += 1

                    print(f"✅ {nome_arquivo} AUTORIZADA → R$ {valor_nf:.2f}")
                elif status in ['101', '135', '151']:
                    notas_canceladas += 1
                    print(f"❌ {nome_arquivo} CANCELADA")
                else:
                    notas_desconhecidas += 1
                    print(f"⚠️ {nome_arquivo} STATUS DESCONHECIDO: {status}")

                arquivos_lidos += 1
        except Exception as e:
            print(f"Erro ao processar {nome_arquivo}: {e}")

print("\n🔍 RESUMO:")
if nome_empresa and cnpj_formatado:
    print(f"🏢 Empresa: {nome_empresa}")
    print(f"🔢 CNPJ: {cnpj_formatado}")

print(f"📄 Arquivos XML lidos: {arquivos_lidos}")
print(f"✅ Notas autorizadas: {notas_autorizadas}")
print(f"❌ Notas canceladas: {notas_canceladas}")
print(f"❓ Notas com status desconhecido: {notas_desconhecidas}")
print(f"💰 Total em vendas autorizadas: R$ {total_geral:.2f}")

if datas_emissao:
    print(f"📆 Período de emissão: de {min(datas_emissao).strftime('%d/%m/%Y')} até {max(datas_emissao).strftime('%d/%m/%Y')}")
else:
    print("📆 Nenhuma data de emissão encontrada.")

print("\n💸 IMPOSTOS SOMADOS:")
print(f"🧾 ICMS: R$ {icms_total:.2f}")
print(f"🏭 IPI: R$ {ipi_total:.2f}")
print(f"📌 PIS: R$ {pis_total:.2f}")
print(f"📎 COFINS: R$ {cofins_total:.2f}")
