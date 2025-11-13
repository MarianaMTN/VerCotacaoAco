# ⚙️ Cotação Rápida e Inteligente para Fornecedores de Aço

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
| **Documentação** | ✅ Completa | Pseudocódigo e narrativa técnica criados para a lógica do aplicativo. |

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
