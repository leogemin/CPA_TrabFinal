import json
import os

def clean_data():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    deputados_path = os.path.join(project_root, 'assets', 'deputados.json')
    profissoes_path = os.path.join(project_root, 'assets', 'deputadosProfissoes.json')
    legislaturas_path = os.path.join(project_root, 'assets', 'legislaturas.json')

    with open(deputados_path, 'r', encoding='utf-8') as f:
        deputados = json.load(f)
    with open(profissoes_path, 'r', encoding='utf-8') as f:
        profissoes = json.load(f)
    with open(legislaturas_path, 'r', encoding='utf-8') as f:
        legislaturas = json.load(f)

    profissoes_dict = {prof['id']: prof for prof in profissoes['dados']}

    legislaturas_dict = {leg['idLegislatura']: leg for leg in legislaturas['dados']}

    cleaned_data = []
    for dep in deputados['dados']:
        dep_id = int(dep['uri'].split('/')[-1])
        profissao_info = profissoes_dict.get(dep_id, {})

        id_legislatura_inicial = dep.get('idLegislaturaInicial')
        id_legislatura_final = dep.get('idLegislaturaFinal')

        ano_entrada = None
        if id_legislatura_inicial and legislaturas_dict.get(id_legislatura_inicial):
            ano_entrada = legislaturas_dict[id_legislatura_inicial]['dataInicio'].split('-')[0]

        ano_saida = None
        if id_legislatura_final and legislaturas_dict.get(id_legislatura_final):
            ano_saida = legislaturas_dict[id_legislatura_final]['dataFim'].split('-')[0]

        cleaned_dep = {
            'nome': dep.get('nome'),
            'idLegislaturaInicial': id_legislatura_inicial,
            'idLegislaturaFinal': id_legislatura_final,
            'nomeCivil': dep.get('nomeCivil'),
            'id': dep_id,
            'siglaSexo': dep.get('siglaSexo'),
            'dataNascimento': dep.get('dataNascimento'),
            'ufNascimento': dep.get('ufNascimento'),
            'codTipoProfissao': profissao_info.get('codTipoProfissao'),
            'tituloProfissao': profissao_info.get('titulo'),
            'anoEntrada': ano_entrada,
            'anoSaida': ano_saida,
        }
        cleaned_data.append(cleaned_dep)

    output_path = os.path.join(project_root, 'assets', 'cleanedData.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    clean_data()