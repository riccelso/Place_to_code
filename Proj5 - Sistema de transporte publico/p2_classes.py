# BIBLIOTECAS IMPORTADAS
from typing import Union
import re
from datetime import datetime
from pyodbc import connect
import toml


# CLASSES:
class Objeto_incorreto(Exception):
	def __init__(self, value: str, message: str) -> None:
		self.value = value
		self.message = message
		super().__init__(message)


class Usuario:
	# ID: int
	# Nome: string
	# Sobrenome: string
	# E-mail: string
	# Bairro: string
	# Data de nascimento: date
	
	cabecalho = {
		'ID' : 'ID',
		'Nome' : 'NOME',
		'Sobrenome' : 'SOBRENOME',
		'E-mail' : 'EMAIL',
		'Bairro' : 'BAIRRO',
		'Data de nascimento' : 'DATA_NASC',
	}
	
	# CREATE TABLE[dbo].[ricardo_celso.Usuario](
	# ID INT IDENTITY(1, 1) PRIMARY KEY,
	# NOME VARCHAR(255) NOT NULL,
	# SOBRENOME VARCHAR(255) NOT NULL,
	# EMAIL VARCHAR(255) NOT NULL,
	# BAIRRO VARCHAR(255) NOT NULL,
	# DATA_NASC DATE NOT NULL,
	# )
	def __init__(self, nome: str, sobrenome: str, email: str, bairro: str, data_nasc: str):
		self.__nome = nome
		self.__sobrenome = sobrenome
		self.__email = email
		self.__bairro = bairro
		self.__data_nasc = data_nasc

	@property
	def __nome(self):
		return self._sobrenome

	
	@__nome.setter
	def __nome(self, value):
		if not re.findall(r'[A-Za-z ]+', value):
			raise ValueError("O nome deve conter somente letras")
		self._nome = value

	@property
	def __sobrenome(self):
		return self._sobrenome

	@__sobrenome.setter
	def __sobrenome(self, value):
		if not re.findall(r'[A-Za-z ]+', value):
			raise ValueError("O sobrenome deve conter somente letras")
		self._sobrenome = value

	@property
	def __email(self):
		return self._email

	@__email.setter
	def __email(self, value):
		result = re.findall('^.+?@.+?\.com(?:.br)?$', value)
		if not result:
			raise ValueError("Parece haver algo de errado com o e-mail")
		self._email = value

	@property
	def __bairro(self):
		return self._bairro

	@__bairro.setter
	def __bairro(self, value):		
		# substituir bairro por CEP?
		if str(value).isnumeric():
			raise ValueError("Bairro deve conter pelo menos letras")
		self._bairro = value

	@property
	def __data_nasc(self):
		return self._data_nasc

	@__data_nasc.setter
	def __data_nasc(self, value):
		result = re.findall(r"^\d{1,2}[-/]{1}\d{1,2}[-/]{1}\d\d(?:\d\d)?$", value)
		if not result:
			raise ValueError("Formatação de data não reconhecida")
		
		result = re.findall(r"(?:^(\d{1,2})[-/]{1}(\d{1,2})[-/]{1}(\d\d(?:\d\d)?)$)", value)[0]

		if re.findall(r'[-/]{1}\d\d\d\d', value):
			data_digitada = datetime(int(result[2]), int(result[1]), int(result[0]))
		else:
			if int(result[-1]) > int(str(datetime.today().year)[2:]):
				data_digitada = datetime(int(f'19{result[2]}'), int(result[1]), int(result[0]))
			else:
				data_digitada = datetime(
					int(f'20{result[2]}'), int(result[1]), int(result[0]))


		idade = (datetime.today() - data_digitada).days / 360
		
		if idade < 16:
			raise ValueError(
				"Idade mínima exigida: 16 anos"
			)
		
		if idade > 130:
			raise ValueError(
				"mais que 130 anos? tem certeza disso?"
            )

		self._data_nasc = value
	

class Cartao:
	# ID: int
	# ID do proprietário: int
	# Quantidade de créditos disponível: double
	# Tipo (comum, estudante, vale-transporte ou idoso): string
	# Data de emissão: date

	cabecalho = {
		'ID': 'ID',
		'ID do proprietário': 'ID_PROPRIETARIO',
		'Quantia de créditos disponível': 'QTD_CREDITO',
		'Tipo': 'TIPO',
		'Data de emissão': 'DATA_EMISSAO',
	}

	# CREATE TABLE [dbo].[ricardo_celso.Cartao](
	# ID INT IDENTITY(1, 1) PRIMARY KEY,
	# ID_PROPRIETARIO INT NOT NULL,
	# QTD_CREDITO FLOAT DEFAULT 0,
	# TIPO VARCHAR(15) NOT NULL CHECK(tipo IN('comum', 'estudante', 'vale-transporte', 'idoso')),
	# DATA_EMISSAO date DEFAULT GETDATE()
	# )

	def __init__(self, id_proprietario, qtd_credito, tipo):
		self.__id_proprietario = id_proprietario
		self.__qtd_credito = qtd_credito
		self.__tipo = tipo

	@property
	def __id_proprietario(self):
		return self._id_proprietario

	@__id_proprietario.setter
	def __id_proprietario(self, value):
		self._id_proprietario = value

	@property
	def __qtd_credito(self):
		return self._qtd_credito

	@__qtd_credito.setter
	def __qtd_credito(self, value):
		if not str(value).isnumeric():
			raise ValueError("O valor digitado deve conter somente números")
		self._qtd_credito = value

	@property
	def __tipo(self):
		return self._tipo

	@__tipo.setter
	def __tipo(self, value):
		if not str(value) in ["comum", "estudante", "vale-transporte", "idoso"]:
			raise ValueError(
				'O valor digitado deve ser "comum", "estudante", "vale-transporte" ou "idoso"')
		self._tipo = value


class Onibus:
	# Número da placa: string
	# Número da linha: string
	# Modelo do ônibus: string
	# Ano de fabricação: int
	# ID motorista: int

	cabecalho = {
		'ID': 'ID',
		'Número da placa': 'PLACA',
		'Número da linha': 'LINHA',
		'Modelo do ônibus': 'MODELO',
		'Ano de fabricação': 'ANO_FABRIC',
		'ID motorista': 'ID_MOTORISTA',
	}
	
	# CREATE TABLE [dbo].[ricardo_celso.Onibus](
    #         ID INT IDENTITY(1, 1) PRIMARY KEY,
    #         PLACA VARCHAR(255) NOT NULL,
    #         LINHA VARCHAR(255) NOT NULL,
    #         MODELO VARCHAR(255) NOT NULL,
    #         ANO_FABRIC INT NOT NULL,
    #         ID_MOTORISTA INT,
    #     )

	def __init__(self, placa, linha, modelo, ano_fabric, id_motorista):
		self.__placa = placa
		self.__linha = linha
		self.__modelo = modelo
		self.__ano_fabric = ano_fabric
		self.__id_motorista = id_motorista

	@property
	def __placa(self):
		return self._placa

	@__placa.setter
	def __placa(self, value):
		# Fonte: 
		# https://www.minamimotors.com.br/blog/como-funciona-e-o-que-muda-no-sistema-de-emplacamento-de-veiculos-aqui-no-brasil
		placa_tipo1 = re.findall(r'^[A-Za-z]{3}[ -/][a-zA-Z0-9]{4}$', value)
		placa_tipo2 = re.findall(r'^[A-Za-z]{2,4}[ -/][a-zA-Z0-9]{3,4}[ -/]?[a-zA-Z]{0,2}$', value)
		if not (placa_tipo1 or placa_tipo2):
			raise ValueError("A placa do carro parece estar incorreta")
		self._placa = value

	@property
	def __linha(self):
		return self._linha

	@__linha.setter
	def __linha(self, value):
		self._linha = value

	@property
	def __modelo(self):
		return self._modelo

	@__modelo.setter
	def __modelo(self, value):
		self._modelo = value

	@property
	def __ano_fabric(self):
		return self._ano_fabric

	@__ano_fabric.setter
	def __ano_fabric(self, value):
		if len(value) != 4 and (not isinstance(value, int)):
			raise ValueError("Ano deve conter 4 dígitos inteiros")
		self._ano_fabric = value

	@property
	def __id_motorista(self):
		return self._id_motorista

	@__id_motorista.setter
	def __id_motorista(self, value):
		self._id_motorista = value


class Motorista:
	# ID motorista: int
	# Número CNH: int
	# Nome: string
	# Sobrenome: stirng
	# Data de nascimento: date

	cabecalho = {
		'ID motorista': 'ID',
		'Número CNH': 'N_CNH',
		'Nome': 'NOME',
		'Sobrenome': 'SOBRENOME',
		'Data de nascimento': 'DATA_NASC',
	}

	# CREATE TABLE [dbo].[ricardo_celso.Motorista](
    #         ID INT IDENTITY(1, 1) PRIMARY KEY,
    #         N_CNH BIGINT NOT NULL,
    #         NOME VARCHAR(255) NOT NULL,
    #         SOBRENOME VARCHAR(255) NOT NULL,
	# 		  DATA_NASC DATE NOT NULL,
    #     )


	def __init__(self, n_cnh, nome, sobrenome, data_nasc):
		self.__n_cnh = n_cnh
		self.__nome = nome
		self.__sobrenome = sobrenome
		self.__data_nasc = data_nasc
	

	@property
	def __n_cnh(self):
		return self._n_cnh

	@__n_cnh.setter
	def __n_cnh(self, value):
		pure_cnh = re.sub(r'[.-]', '', value)

		cond =[
			len(pure_cnh) == 11,
			len(re.findall(r'[0-9\.\-]+', value)) == 1,
			len(set(pure_cnh)) > 1,
		]

		if not all(cond):
			raise ValueError("CNH deve conter 11 números, somente '.' e '-' são aceitos além disso")

		self._n_cnh = pure_cnh

	@property
	def __nome(self):
		return self._nome

	@__nome.setter
	def __nome(self, value):
		if not re.findall(r'[A-Za-z ]+', value):
			raise ValueError("Nome deve conter somente letras")
		self._nome = value

	@property
	def __sobrenome(self):
		return self._sobrenome

	@__sobrenome.setter
	def __sobrenome(self, value):
		if not re.findall(r'[A-Za-z ]+', value):
			raise ValueError("Sobrenome deve conter somente letras")
		self._sobrenome = value

	@property
	def __data_nasc(self):
		return self._data_nasc

	@__data_nasc.setter
	def __data_nasc(self, value):
		result = re.findall(r"^\d{1,2}[-/]{1}\d{1,2}[-/]{1}\d\d(?:\d\d)?$", value)
		if not result:
			raise ValueError("Formatação de data não reconhecida")

		result = re.findall(
			r"(?:^(\d{1,2})[-/]{1}(\d{1,2})[-/]{1}(\d\d(?:\d\d)?)$)", value)[0]

		if re.findall(r'[-/]{1}\d\d\d\d', value):
			data_digitada = datetime(int(result[2]), int(result[1]), int(result[0]))
		else:
			if int(result[-1]) > int(str(datetime.today().year)[2:]):
				data_digitada = datetime(
					int(f'19{result[2]}'), int(result[1]), int(result[0]))
			else:
				data_digitada = datetime(
					int(f'20{result[2]}'), int(result[1]), int(result[0]))

		idade = (datetime.today() - data_digitada).days / 360

		if idade < 16:
			raise ValueError(
				"Idade mínima exigida: 16 anos"
			)

		if idade > 130:
			raise ValueError(
                    "mais que 130 anos? tem certeza disso?"
                )

		self._data_nasc = value


class Gestor_de_bd:

	def dados_conn(self):
		# CONSTANTES:
		CONFIG = toml.load('base_dados_info.toml')['config']
		AUTHENTICATION = 'ActiveDirectoryInteractive'
		
		# STRING P/ CONEXÃO EM BD:
		txt_conexao = \
		f"DRIVER={CONFIG['driver']};\
		SERVER={CONFIG['server']};\
		PORT={CONFIG['port']};\
		DATABASE={CONFIG['database']};\
		UID={CONFIG['username']};\
		PWD={CONFIG['password']};\
		AUTHENTICATION={AUTHENTICATION};"

		return txt_conexao

	def validacao(self, objeto: Union[Usuario, Onibus, Cartao, Motorista]):
		if isinstance(objeto, (Usuario, Onibus, Cartao, Motorista)):
			return objeto
		else:
			raise Objeto_incorreto(value=objeto, message="O objeto enviado ao banco de dados deve ser:\n\
				Motorista, Usuario, Onibus ou Cartao")
		
	def enviar_dados(self, objeto):
		objeto = self.validacao(objeto)
		
		campos = str(tuple(str(x).strip('_').upper()
		             for x in tuple(objeto.__dict__.keys()))).replace("'", "")
		valores = str(tuple(str(x).strip('_') for x in tuple(objeto.__dict__.values())))

		sql_cmd = \
			f'insert into [ricardo_celso.{objeto.__class__.__name__}] {campos} values {valores}'
		
		# CONVERTENDO PARA SEQUENCIA Y-M-D
		sql_cmd = re.sub(r'(?:(\d{1,2})[-/]{1}(\d{1,2})[-/]{1}(\d\d(?:\d\d)?))', r'\3-\2-\1', sql_cmd)

		# Lidando com dias e meses com somente 1 digito:
		data_corrigida = None
		grupos = re.findall(r'(?:\'(\d\d\d\d)[/-](\d{1,2})[/-](\d{1,2}))', sql_cmd)
		if grupos:
			grupos = grupos[0]
			ano, mes, dia = tuple( int(x) for x in grupos )
			data_corrigida = f'{ano}-{mes:02d}-{dia:02d}'
		
		# Tratando datas que possuem ano com 2 dígitos
		grupos = re.findall(r'(?:\'(\d\d)[/-](\d{1,2})[/-](\d{1,2}))', sql_cmd)
		if grupos:
			grupos = grupos[0]
			ano, mes, dia = tuple(int(x) for x in grupos)
			pos_ano_atual = int(str(datetime.today().year)[2:])
			pre_ano_atual = int(str(datetime.today().year)[:2])
			if int(ano) > pos_ano_atual:
				data_corrigida = f'{pre_ano_atual-1}{ano}-{mes:02d}-{dia:02d}'
			else:
				data_corrigida = f'{pre_ano_atual}{ano}-{mes:02d}-{dia:02d}'

		# Substituir data da string para data corrigida no formato sql
		if data_corrigida:
			sql_cmd = re.sub(r'\d{2,4}[-/]{1}\d{1,2}[-/]{1}\d{1,2}', data_corrigida, sql_cmd)

		# print('\nAguarde a conexão...')
		# print('\n', sql_cmd, '\n')

		with connect(self.dados_conn()) as cursor:
			cursor.execute(sql_cmd)
	
	def ver_dados(self, tabela, colunas=None, limit=None, desc=False, onde=None):
		sql_cmd = \
		f'select * from [ricardo_celso.{str(tabela).capitalize()}]'

		if limit != None:
			sql_cmd = sql_cmd.replace('*', f'TOP {limit} *')

		if colunas != None:
			if isinstance(colunas, (list, tuple, set)):
				l = tuple(x.upper() for x in colunas)
				l = str(l).replace("(", "").replace(")", "").replace("'", "")
				if len(colunas) == 1:
					l = l.replace(',', '')
				sql_cmd = sql_cmd.replace('*', l)
			else:
				raise Objeto_incorreto(
					colunas, 
					"O objeto da variável \"colunas\" deve ser: list, tuple ou set"
					)
		
		if onde != None:
			regex1 = re.findall(r'\w+=[\w\d]+', onde)
			if regex1:
				sql_cmd += '\nWHERE '
				for i, v in enumerate(regex1):
					if i == 0: sql_cmd += v; continue
					sql_cmd += f', {v}'
			else:
				regex2 = re.findall(r"\w+\s+like\s+'%.+%'", onde, flags=re.IGNORECASE)
				if regex2:
					sql_cmd += '\nWHERE '
					for i, v in enumerate(regex2):
						if i == 0: sql_cmd += v; continue
						sql_cmd += f', {v}'

		
		sql_cmd = re.sub(
			r'(?:(\d\d)[-/]{1}(\d\d)[-/]{1}(\d\d(?:\d\d)?))', r'\3-\2-\1', sql_cmd)

		if desc == True:
			sql_cmd += f'\nORDER BY ID DESC'

		# print('\nAguarde a conexão...')
		# print('\n', sql_cmd, '\n')

		with connect(self.dados_conn()) as cursor:
			r = cursor.execute(sql_cmd)
			return r.fetchall()
	
	def atualizar_dados(self, tabela: str, identificador: int, coluna_mudar: str, valor_novo: str):

		sql_cmd = \
			f"UPDATE [ricardo_celso.{tabela.capitalize()}] SET {coluna_mudar}={valor_novo} WHERE ID={identificador};"
		
		sql_cmd = re.sub(
			r'(?:(\d\d)[-/]{1}(\d\d)[-/]{1}(\d\d(?:\d\d)?))', r'\3-\2-\1', sql_cmd) # Melhorar isso

		# print('\nAguarde a conexão...')
		# print('\n', sql_cmd, '\n')

		with connect(self.dados_conn()) as cursor:
			cursor.execute(sql_cmd)