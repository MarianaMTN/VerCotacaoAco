# ⚙️ Cotação Rápida e Inteligente para Fornecedores

## 📄 Introdução

A comunicação eficiente entre clientes e fornecedores é vital no setor de suprimentos industriais. Pensando nisso, este aplicativo foi desenvolvido com o objetivo de ajudar pessoas e empresas a encontrarem fornecedores de confiança com facilidade, de acordo com o tipo de material ou produto que necessitam. A solução moderniza e centraliza o processo de cotação ao substituir formulários estáticos ou e-mails manuais por uma interface dinâmica e funcional, permitindo ao usuário cadastrar suas necessidades e receber indicações de fornecedores confiáveis.

## 🎯 Objetivo do Projeto

Desenvolver um sistema (ou aplicativo) que auxilie pessoas ou empresas a encontrarem fornecedores de com facilidade, de acordo com o tipo de material.
O sistema buscará otimizar o processo de pesquisa e seleção do fornecedor, permitindo o usuário receber indicações precisas 

## 📐 Documentação Técnica

### 1. Fluxograma do Aplicativo (Mermaid)

O diagrama abaixo ilustra o fluxo completo do aplicativo, desde a inicialização até o resultado do envio do e-mail.

![Fluxograma Completo do Aplicativo de Cotação](https://raw.githubusercontent.com/MarianaMTN/VerCotacaoAco/refs/heads/main/Fluxograma.svg)

### 2. Pseudocódigo

#### A. Lógica Principal (`streamlit_app.py`)

\`\`\`pseudocode
INICIO PROGRAMA PRINCIPAL

    // 1. Configuração e Segurança
    IMPORTAR streamlit, pandas, email_sender
    TENTAR
        LER SENDER_EMAIL E SENDER_PASSWORD DE st.secrets
    SE ERRO StreamlitSecretNotFoundError
        EXIBIR ERRO "Credenciais não encontradas"
        PARAR

    // 2. Dados e Estilização
    DEFINIR DADOS_FORNECEDORES (DataFrame)
    DEFINIR DESCRICOES_ACO (Dicionário)
    APLICAR ESTILOS CSS CUSTOMIZADOS

    // 3. Interface do Usuário
    EXIBIR TÍTULO
    SELECIONAR selected_steel_type EM DADOS_FORNECEDORES
    
    // 4. Exibir Informações do Fornecedor
    BUSCAR supplier_info BASEADO EM selected_steel_type
    BUSCAR descricao_do_aco EM DESCRICOES_ACO
    EXIBIR supplier_name
    EXIBIR supplier_info E descricao_do_aco EM BLOCO INFORMATIVO

    // 5. Formulário de Envio
    INICIAR FORMULÁRIO 'email_form'
        user_email = CAMPO_TEXTO "Seu E-mail (Para Resposta)"
        assunto = CAMPO_TEXTO
        mensagem = CAMPO_AREA_TEXTO
        uploaded_file = CAMPO_UPLOAD
        send_button = BOTÃO "Enviar E-mail"
    FIM FORMULÁRIO

    // 6. Lógica de Envio
    SE send_button FOR PRESSIONADO
        SE user_email ESTIVER VAZIO
            EXIBIR ERRO "Preencha seu e-mail"
        SENÃO
            TENTAR
                SE uploaded_file EXISTIR
                    SALVAR uploaded_file TEMPORARIAMENTE
                    file_path = CAMINHO_DO_ARQUIVO
                SENÃO
                    file_path = NULO

                // Chamada da Função de Envio
                result = email_sender.send_email(
                    SENDER_EMAIL, SENDER_PASSWORD, recipient_email, 
                    assunto, mensagem, file_path, user_email
                )
                EXIBIR SUCESSO result
                SE file_path EXISTIR
                    REMOVER file_path
            SE ERRO (e)
                EXIBIR ERRO "Erro ao enviar: " + e
            FIM TENTAR

FIM PROGRAMA PRINCIPAL
\`\`\`

#### B. Função de Envio (`email_sender.py`)

\`\`\`pseudocode
FUNÇÃO send_email(sender_email, sender_password, recipient_email, subject, body, file_path, reply_to_email)

    // 1. Construção da Mensagem
    CRIAR mensagem (MIMEMultipart)
    DEFINIR message['From'] = sender_email
    DEFINIR message['To'] = recipient_email
    DEFINIR message['Subject'] = subject
    DEFINIR message['Reply-To'] = reply_to_email // Permite que o destinatário responda ao usuário final
    ANEXAR body (MIMEText)

    // 2. Anexo Opcional
    SE file_path NÃO FOR NULO
        LER arquivo EM MODO BINÁRIO
        ANEXAR arquivo À mensagem (MIMEImage)

    // 3. Envio SMTP
    TENTAR
        CONECTAR AO SERVIDOR SMTP DO GMAIL (smtp.gmail.com:587)
        INICIAR TLS (Criptografia)
        LOGIN COM sender_email E sender_password
        ENVIAR mensagem DE sender_email PARA recipient_email
        FECHAR CONEXÃO
        RETORNAR MENSAGEM DE SUCESSO
    SE ERRO SMTPAuthenticationError (e)
        LEVANTAR EXCEÇÃO "Falha na autenticação: " + e
    SE ERRO QUALQUER_OUTRO_ERRO (e)
        LEVANTAR EXCEÇÃO "Erro ao enviar email: " + e
    FIM TENTAR

FIM FUNÇÃO
\`\`\`

### 3. Narrativa Técnica

O aplicativo de cotação é uma solução de software de duas camadas que adere aos princípios de separação de responsabilidades e segurança.

#### Camada de Apresentação e Lógica (Frontend - `streamlit_app.py`)

Esta camada gerencia a interação com o usuário e a lógica de negócios:

*   **Segurança e Configuração:** O aplicativo inicia carregando as credenciais de envio (`SENDER_EMAIL` e `SENDER_PASSWORD`) através do `st.secrets`. Este método é crucial, pois evita que dados sensíveis sejam expostos no código-fonte, garantindo a segurança da aplicação em ambientes de nuvem.
*   **Fluxo de Dados:** Os dados de fornecedores e as descrições de aços são definidos e gerenciados por estruturas de dados Python (`DataFrame` e `Dicionário`). A seleção do usuário (`st.selectbox`) atua como um filtro, definindo o fornecedor e o aço para a cotação.
*   **Interface:** A interface é construída com Streamlit e aprimorada com CSS customizado para um visual moderno e profissional. O formulário de envio é o ponto central, onde o usuário insere seu e-mail (para resposta), o assunto, a mensagem e, opcionalmente, anexa um arquivo.
*   **Orquestração:** Ao pressionar o botão "Enviar E-mail", o aplicativo orquestra a chamada para a função de backend, passando todos os parâmetros necessários, incluindo o caminho do arquivo temporário (se houver) e o e-mail do usuário para o campo `Reply-To`.

#### Camada de Comunicação (Backend - `email_sender.py`)

Esta camada é dedicada exclusivamente à comunicação via protocolo SMTP:

*   **Função `send_email`:** A função é o ponto de contato com o servidor SMTP do Gmail. Ela utiliza a biblioteca `smtplib` para estabelecer uma conexão segura (via TLS) e autenticar-se usando as credenciais fornecidas.
*   **Construção da Mensagem:** A mensagem é construída usando a classe `MIMEMultipart`, que permite a inclusão de texto e anexos. A inclusão do cabeçalho `Reply-To` com o e-mail do usuário final é uma funcionalidade chave, garantindo que o destinatário responda diretamente ao usuário, mesmo que o e-mail tenha sido enviado pelo e-mail de serviço do aplicativo.
*   **Robustez:** A função é robusta, pois trata o anexo como opcional, evitando erros de tipo (`NoneType`). Além disso, ela implementa um tratamento de exceção específico para `SMTPAuthenticationError`, que captura falhas de login e as reporta de forma clara ao usuário, resolvendo os problemas de depuração iniciais.

## 💡 Conclusão

O aplicativo de Cotação Rápida e Inteligente é uma prova de conceito funcional e segura, pronta para ser utilizada em um ambiente de produção. A separação clara entre a lógica de interface (`streamlit_app.py`) e a lógica de comunicação (`email_sender.py`) garante a manutenibilidade e a escalabilidade do código. O uso de práticas de segurança modernas, como o `st.secrets` e o `Reply-To`, o torna uma solução confiável para a gestão de cotações.

## 🔗 Anexos e Instruções de Deploy

Para implantar este aplicativo no Streamlit Cloud, siga os passos abaixo:

1.  **Arquivos Essenciais:** Certifique-se de que os seguintes arquivos estejam no seu repositório GitHub:
    *   `streamlit_app.py` (Lógica principal e UI)
    *   `email_sender.py` (Função de envio de e-mail)
    *   `requirements.txt` (Contendo: `streamlit`, `pandas`, `pytz`)
2.  **Segredos (NÃO ENVIAR PARA O GITHUB):** O arquivo `.streamlit/secrets.toml` **NÃO** deve ser enviado para o GitHub. Você deve copiar o conteúdo dele e colá-lo na seção **Advanced Settings -> Secrets** do Streamlit Cloud durante o deploy.
    \`\`\`toml
    [gmail]
    email = "seu_email_de_servico@gmail.com"
    password = "sua_senha_de_app_de_16_caracteres"
    \`\`\`
3.  **Deploy:** Conecte o Streamlit Cloud ao seu repositório, defina `streamlit_app.py` como o arquivo principal e adicione os segredos. O aplicativo estará pronto para uso.
