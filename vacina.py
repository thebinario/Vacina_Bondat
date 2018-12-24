import os
import re
import psutil
from prettytable import PrettyTable




class Monitor_de_Processos(object):
    def __init__(self):

        self.padrao_regex = re.compile(r'wscript.exe')


    def procura_info_processo_decorrer_sistema(self):
        for processo in psutil.process_iter():
            try:
                codigo_execucao = 0
                atributos_processo = processo.as_dict(attrs=['pid','name','username']) #Devolve dicionario com info do processo wscript.exe(pid , name, username)
                if self.padrao_regex.match(atributos_processo['name']): #Expressão regular para encontrar processo wscript.exe no resultado da linha anterior
                    return atributos_processo['pid'], atributos_processo['name'], atributos_processo['username'], codigo_execucao  # retorna info do dicionário
            except:
                # Se o processo wscript.exe não estiver ativo o programa sai no ultimo ( except ) no fim do código
                pass
            
    def info_processo_descendente(self, processo_id):
        numero_key = 0
        lista_processos_child = {}
        for x in psutil.Process(processo_id).children():# Verifica processos child
            """
             A variável (numero_key) com valor zero aparece porque o dicionário (lista_processos_child)
             recebe o valor de X também enquanto dicionário, uma vez que as keys do dicionário (pid,name)
             são constantes, e em python os dicionários quando recebem Keys iguais às que já lá se encontram,
             a cada update são subscritas as keys anteriores com o mesmo nome, ficando apenas a ùltima key e o seu valor, a entrar.
             Usei a variável (numero_key) a incrementar a cada iteração para criar um dicionário aninhado, assim
             é criado uma key com número 1 que recebe como valor o dicionario de x... esse valor é incrementado a cada itereção
             dependendo do número de processos filho encontrados, assim sendo todos os processos são adicionados ao dicionário e nenhum
             é subscrito.
            """
            numero_key += 1
            lista_processos_child[numero_key] = (x.as_dict(attrs=['pid','name']))# Dicionário lista_processos_child, recebe valor de x como dicionário
                                                                                 # ficando dicionários aninhados
        return lista_processos_child, numero_key 

    # Esta função testa se os processos child do prcesso wscript.exe, têm processos descendentes
    def descendente_processo_descendente(self, descendente_processo_id):
        numero_key = 0
        child_processos_child = {}
        for x in psutil.Process(descendente_processo_id).children():
            numero_key += 1
            child_processos_child[numero_key] = (x.as_dict(attrs=['pid','name']))
            
        return child_processos_child, numero_key    
        
    def termina_processos(self, atributos_processo_id):   
        wscript_id = psutil.Process(atributos_processo_id) #Identifica processo wscript.exe
        for child in wscript_id.children(recursive=True):
            child.kill() # Termina processos filho antes de terminar processos wscript.exe
        wscript_id.kill() # Termina processo wscript.exe




class Gestor_de_Ficheiros(object):

    #def __init__(self):

    #    self.extencao_exe = '.exe'
    #    self.extencao_js = '.js'
    #    self.extencao_txt = '.txt'

    def localiza_ficheiros_diretorios_childs(self, processo_child):
        """
        ESTA FUNÇÃO NECESSITA SER TRABALHADA MEDIANTE CONCLUSÕES FUTURAS SOBRE O COMPORTAMENTO DOS PROCESSOS DETETADOS...
        Os agurmento que esta função recebe estão armazenados na lista ( lista_ficheiros_localizar),
        são os childs do processo wscript.exe...
        
        ATENÇÃO: (Aparentemente) O mesmo ficheiro dá origem a dois processos diferentes a trabalhar em simultâneo,
        essa é a razão pela qual a lista contém dois processos com o mesmo nome.

        O RESULTADO DESTA FUNÇÃO DUPLICA O MESMO RESULTADO, DEVE SER CONSIDERADA UMA SOLUÇÃO PARA ESSE EFEITO.
        
        """
        
        for root,diretorios,ficheiros in os.walk("c:\\"):
            for ficheiros in ficheiros:
                if ficheiros == processo_child:
                    print("Caminho para ficheiro\n-> ",os.path.join(root,ficheiros)) # Devolve a localização do ficheiro child de wscript.exe
                    """
                    A linha que segue deve ser tida em conta na altura de fazer a função que elemina a pasta que contém
                    os ficheiros que devem ser eleminados.
                    """
                    # Devove o nome do diretório onde se encontra o ficheiro child anterior
                    print("Diretório onde se situa o ficheiro\n-> ",os.path.basename(os.path.dirname(os.path.join(root,ficheiros))))                       
        
        

        
        
    def elemina_ficheiros_e_diretorios(self, nome_ficheiro, nome_diretorio):
        """
        Esta função deve ser feita depois de perceber que ficheiros são gerados
        e onde estão localizados no sistema.

        ATENÇÃO: Os parâmetros desta função não devem ser considerados, são apenas considerações
        para alterações futuras.
        """
        pass
        

def obter_resposta_utilizador(pergunta):
    while True:
        resposta = input(pergunta).strip().lower()
        # Se a resposta for "s" termina processos filho e processo pai
        if resposta  == 's':
            Monitora_processo.termina_processos(atributos_processo_id)
            print("Processos Terminados!")
            break
        # Se resposta for "n" termina o programa, processos continuam ativos
        elif resposta == 'n':
            print("Programa terminado pelo utilizador, processos continuam ativos...")
            break
        else:
            print("Resposta de ser s/n...")
    
   
if __name__ == '__main__':

    Monitora_processo = Monitor_de_Processos() # Inicia Objecto
    Gestor_ficheiros = Gestor_de_Ficheiros()

    lista_ficheiros_localizar = [] # Recebe nome dos processos (ficheiros), para apagar

    # PrettyTable é uma biblioteca que posiciona, valores em células("Planilhas") 
    
    tabela_processo = PrettyTable() 
    tabela_processo.field_names = ["Nome Proc.", "Proc ID", "Usuário"]

    tabela_processo_child = PrettyTable()
    tabela_processo_child.field_names = ["Proc. child", "child ID", "  ", "Nome Proc.", "Proc ID"]

    tabela_child_processo_child = PrettyTable()
    tabela_child_processo_child.field_names = ["Proc. child", "child ID", "  ", "Proc. descendente de child", "descendente ID"]


    try:
        atributos_processo_id, atributos_processo_name, atributos_processo_username, codigo_execucao = Monitora_processo.procura_info_processo_decorrer_sistema()

        lista_processos_child, numero_key = Monitora_processo.info_processo_descendente(atributos_processo_id)

        

        
        if codigo_execucao == 0:
             
            tabela_processo.add_row([atributos_processo_name, atributos_processo_id, atributos_processo_username])

            for child in lista_processos_child:
                lista_ficheiros_localizar.append(lista_processos_child[child]['name'])
                tabela_processo_child.add_row([lista_processos_child[child]['name'], lista_processos_child[child]['pid'], " de ", atributos_processo_name, atributos_processo_id])
                
                
            try:
                for child_id in lista_processos_child:
                    child_processos_child, _ = Monitora_processo.descendente_processo_descendente(lista_processos_child[child_id]['pid'])
                    
                    if len(child_processos_child) == 0:
                        tabela_child_processo_child.add_row([lista_processos_child[child_id]['name'], lista_processos_child[child_id]['pid'], "  ",
                                                                                                                                 "NÃO EXISTE", "---"])
                    else:
                        
                         tabela_child_processo_child.add_row([lista_processos_child[child_id]['name'], lista_processos_child[child_id]['pid'], "  ",
                                                             child_processos_child[child_id]['name'], child_processos_child[child_id]['pid']  ])
            except:
                pass

        
              
            print(tabela_processo)
            print(tabela_processo_child)
            print(tabela_child_processo_child)
            
            for processo_child in lista_ficheiros_localizar:
                Gestor_ficheiros.localiza_ficheiros_diretorios_childs(processo_child) 

            # A ação da linha que segue, mediante a resposta do utilizador,
            # está posicionada na função (obter_resposta_utilizador)   
            obter_resposta_utilizador("Queres terminar processos e apagar os ficheiros?[s/n] ")
  
            
        
    except :
        print("Processo wscript.exe não foi encontrado")
