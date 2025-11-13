# ⚙️ Cotação Rápida e Inteligente para Fornecedores

## 💡 Resumo da Ideia

Este projeto consiste em um aplicativo web interativo, desenvolvido com **Streamlit**, que simplifica o processo de solicitação de cotações de aço. A ferramenta permite que o usuário selecione o tipo de aço desejado, visualize informações detalhadas do fornecedor e envie um e-mail de cotação personalizado e seguro, com a opção de anexar arquivos. O foco principal é a **segurança** das credenciais e a **rastreabilidade** da comunicação, garantindo que as respostas dos fornecedores sejam direcionadas diretamente ao e-mail do usuário final.

## 📄 Introdução

A comunicação eficiente entre clientes e fornecedores é vital no setor de suprimentos industriais. Este aplicativo foi criado para modernizar e centralizar o processo de cotação, substituindo formulários estáticos ou e-mails manuais por uma interface dinâmica e funcional. A solução utiliza o poder do Python e do Streamlit para criar uma experiência de usuário rica, enquanto emprega bibliotecas padrão para garantir um envio de e-mail robusto e seguro via protocolo SMTP.

## 🎯 Objetivos do Projeto

Os principais objetivos alcançados durante o desenvolvimento foram:

1.  **Desenvolver uma Interface Intuitiva:** Criar um frontend amigável e visualmente agradável (utilizando o esquema de cores Teal e Roxo) com o Streamlit.
2.  **Garantir a Segurança das Credenciais:** Implementar o uso de `st.secrets` para armazenar o e-mail e a senha de aplicativo do Gmail, evitando a exposição de dados sensíveis no código-fonte.
3.  **Implementar a Funcionalidade `Reply-To`:** Configurar o cabeçalho do e-mail para que as respostas dos fornecedores sejam enviadas diretamente para o e-mail do usuário que solicitou a cotação, e não para o e-mail de serviço.
4.  **Suportar Anexos Opcionais:** Permitir que o usuário anexe arquivos (como especificações técnicas) à solicitação de cotação, garantindo que o envio funcione perfeitamente mesmo sem anexo.
5.  **Tratamento de Erros Robusto:** Incluir tratamento de exceções específico para falhas de autenticação SMTP (código 535), fornecendo feedback claro ao usuário.
6.  **Preparação para Deploy:** Estruturar o projeto para fácil implantação no Streamlit Cloud.

## ✅ Resultados Alcançados

O projeto foi concluído com sucesso, atendendo a todos os requisitos e resolvendo os desafios técnicos iniciais:

| Funcionalidade | Status | Detalhes da Implementação |
| :--- | :--- | :--- |
| **Envio de E-mail** | ✅ Funcional | Utiliza `smtplib` e `email.mime` para comunicação segura via Gmail (SMTP/SSL). |
| **Segurança de Credenciais** | ✅ Implementada | Credenciais armazenadas em `st.secrets` (Arquivo `.streamlit/secrets.toml`). |
| **`Reply-To`** | ✅ Implementado | Garante que o fornecedor responda ao e-mail do usuário final. |
| **Anexos** | ✅ Funcional | Suporta upload de arquivos e envia e-mail com ou sem anexo (tratamento de `NoneType` resolvido). |
| **Estilização** | ✅ Personalizada | Aplicação de CSS customizado com o esquema de cores Teal e Roxo. |

## 📐 Documentação Técnica

### 1. Fluxograma do Aplicativo (Mermaid)

O diagrama abaixo ilustra o fluxo completo do aplicativo, desde a inicialização até o resultado do envio do e-mail.

\`\`\`mermaid
graph TD
    A[Inicio: Inicializacao do App Streamlit] --> B[Carregar Dados: Fornecedores e Descricoes de Aco];
    B --> C[Configurar UI: Titulo e CSS Personalizado];
    C --> D[Sidebar: Selecao do Tipo de Aco];
    
    D --> E[Exibir Descricao do Aco Selecionado];
    E --> F[Exibir Tabela de Fornecedores];
    
    F --> G[Formulario de Cotacao: Nome, Email, Mensagem];
    G --> H[Upload de Arquivo Opcional];
    
    H --> I{Botao Enviar Clicado};
    
    I -- Sim --> J{Email do Usuario Preenchido};
    I -- Nao --> G;
    
    J -- Nao --> K[Exibir Erro: Preencha Email];
    J -- Sim --> L[Chamar send_email];
    
    L --> M[send_email: Construir Mensagem MIME com Reply-To];
    
    M --> N{Anexo Existe};
    N -- Sim --> O[Anexar Arquivo Temp];
    N -- Nao --> P[Continuar];
    
    O --> Q[Tentar Conexao SMTP e Login com st.secrets];
    P --> Q;
    
    Q --> R{Envio Bem-Sucedido};
    
    R -- Sim --> S[Exibir Sucesso];
    R -- Sim --> T{Anexo Existia};
    
    R -- Nao --> U[Capturar Erro Autenticacao];
    U --> V[Exibir Erro Informativo];
    V --> W[Fim];
    
    T -- Sim --> X[Remover Arquivo Temp];
    T -- Nao --> W;
    
    X --> W;
    S --> W;
    K --> W;
\`\`\`

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

---
*Desenvolvido com Python e Streamlit.*


```mermaid graph TD A[Inicio: Inicializacao do App Streamlit] --> B[Carregar Dados: Fornecedores e Descricoes de Aco]; B --> C[Configurar UI: Titulo e CSS Personalizado]; C --> D[Sidebar: Selecao do Tipo de Aco];

D --> E[Exibir Descricao do Aco Selecionado];
E --> F[Exibir Tabela de Fornecedores];

F --> G[Formulario de Cotacao: Nome, Email, Mensagem];
G --> H[Upload de Arquivo Opcional];

H --> I{Botao Enviar Clicado};

I -- Sim --> J{Email do Usuario Preenchido};
I -- Nao --> G;

J -- Nao --> K[Exibir Erro: Preencha Email];
J -- Sim --> L[Chamar send_email];

L --> M[send_email: Construir Mensagem MIME com Reply-To];

M --> N{Anexo Existe};
N -- Sim --> O[Anexar Arquivo Temp];
N -- Nao --> P[Continuar];

O --> Q[Tentar Conexao SMTP e Login com st.secrets];
P --> Q;

Q --> R{Envio Bem-Sucedido};

R -- Sim --> S[Exibir Sucesso];
R -- Sim --> T{Anexo Existia};

R -- Nao --> U[Capturar Erro Autenticacao];
U --> V[Exibir Erro Informativo];
V --> W[Fim];

T -- Sim --> X[Remover Arquivo Temp];
T -- Nao --> W;

X --> W;
S --> W;
K --> W;
```
