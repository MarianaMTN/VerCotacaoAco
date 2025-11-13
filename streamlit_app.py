import streamlit as st
import pandas as pd
import os
from email_sender import send_email 

# --- 1. CONFIGURAÇÃO DE SEGURANÇA 
try:
    SENDER_EMAIL = st.secrets["gmail"]["email"]
    SENDER_PASSWORD = st.secrets["gmail"]["password"]
except KeyError:
    st.error("As credenciais do Gmail não foram encontradas. Por favor, crie o arquivo .streamlit/secrets.toml.")
    st.stop()


# --- 2. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(layout="wide")

# --- 3. DADOS DOS FORNECEDORES 
df = pd.DataFrame({
    'Tipo de Aço': ['Aço Carbono 1020', 'Aço Inox 304', 'Aço Ferramenta D2', 'Aço Liga 4140'],
    'Fornecedor': ['Metalúrgica Alfa', 'Inox Beta', 'Aços Gama', 'Ligas Delta'],
    'Email': ['alfametalurgica@gmail.com', 'beta@fornecedor.com.br', 'gama@fornecedor.com.br', 'deltaliga@gmail.com'],
    'Telefone': ['(11) 98765-4321', '(21) 91234-5678', '(31) 99876-5432', '(41) 97654-3210']
})
DESCRICOES_ACO = {
    'Aço Carbono 1020': 'Versátil e fácil de usinar, ideal para peças mecânicas simples.',
    'Aço Inox 304': 'Resistente à corrosão, perfeito para ambientes úmidos ou alimentícios.',
    'Aço Ferramenta D2': 'Alta dureza e resistência ao desgaste, usado em matrizes e facas industriais.',
    'Aço Liga 4140': 'Forte e tenaz, excelente para eixos, engrenagens e componentes estruturais.'
}

# --- 4. ESTILIZAÇÃO (CSS)
st.markdown("""
<style>
    /* Cor de fundo do Streamlit */
    .stApp {
        background-color: #2F4F4F;
        color: #87CEEB; /* Cor do texto principal */
    }
    /* Título Principal */
    .main-header {
        color: #008080; /* Teal */
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 20px;
    }
    /* Títulos Secundários (h2) */
    h2 {
        color: #333333;
    }
    /* Garante que todos os textos de labels e inputs sejam escuros */
    label, .st-b9, .st-b6, .st-b3 {
        color: #ADD8E6 !important;
    }
    
    /* Cards de Informação */
    .card {
        background-color: #FFF0F5; /* Cor de fundo dos cards  */
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: transform 0.4s, box-shadow 0.3s;
        margin-bottom: 15px;
        border-left: 10px solid #F0E68C; 
        color: #333333;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }
    /* Título dentro do Card */
    .card-title {
        color: #008080; /* Teal */
        font-weight: bold;
        font-size: 1.2em;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header"><b>🏗️Cotação de Aços para Fornecedores🏗️</b></h1>', unsafe_allow_html=True)

# --- 5. SELEÇÃO DE AÇO ---
steel_types = df['Tipo de Aço'].unique()
selected_steel_type = st.selectbox("Selecione o Tipo de Aço para Cotação:", steel_types)

# --- 6. EXIBIÇÃO DO FORNECEDOR ---
supplier_info = df[df['Tipo de Aço'] == selected_steel_type].iloc[0]
supplier_name = supplier_info['Fornecedor']
recipient_email = supplier_info['Email']

# NOVO: Obter a descrição do aço
descricao_do_aco = DESCRICOES_ACO.get(selected_steel_type, "Descrição não disponível.")

st.markdown(f"## Fornecedor Selecionado: {supplier_name}")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="card">
        <p class="card-title">Fornecedor</p>
        <p><b>{supplier_name}</b></p>
        <p><i>"{descricao_do_aco}"</i></p>   
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        <p class="card-title">Contato</p>
        <p>Email: {recipient_email}</p>
        <p>Telefone: {supplier_info['Telefone']}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- 7. FORMULÁRIO DE ENVIO DE E-MAIL ---
st.subheader(f"Enviar Solicitação de Cotação para {supplier_name}")

# Variável para o anexo (inicialmente None)
file_path = None

# O Streamlit lida com o upload do arquivo
uploaded_file = st.file_uploader("Anexar Documento (Opcional - PNG, JPG, JPEG, PDF)", type=['png', 'jpg', 'jpeg', 'pdf'])

if uploaded_file is not None:
    # Salva o arquivo temporariamente para obter o caminho
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, uploaded_file.name)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

# Formulário de envio
with st.form(key='email_form'):
    
    # CAMPO DE ENTRADA PARA O E-MAIL DO USUÁRIO (Reply-To)
    user_email = st.text_input("Seu E-mail (Para o Fornecedor Responder):")
    
    assunto = st.text_input("Assunto:", value=f"Cotação de Aço - {selected_steel_type}")
    
    mensagem = st.text_area("Mensagem:", value=f"Prezado(a) {supplier_name},\n\nSolicito a cotação para o aço {selected_steel_type}. Por favor, envie os detalhes de preço e prazo de entrega.\n\nAtenciosamente,\n[Seu Nome]")
    
    send_button = st.form_submit_button("Enviar E-mail")

# --- 8. LÓGICA DE ENVIO ---
if send_button:
    if not user_email:
        st.error("Por favor, preencha o seu e-mail para que o fornecedor possa responder.")
    else:
        try:
            # CHAMADA DA FUNÇÃO send_email (FINAL)
            result = send_email(
                sender_email=SENDER_EMAIL,
                sender_password=SENDER_PASSWORD,
                recipient_email=recipient_email,
                subject=assunto,
                body=mensagem,
                file_path=file_path, # Passa o caminho (ou None)
                reply_to_email=user_email # Novo parâmetro para o e-mail do usuário
            )
            st.success(f"E-mail enviado com sucesso! {result}")
            
            # Limpa o arquivo temporário após o envio
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
                
        except Exception as e:
            st.error(f"Erro ao enviar: {e}")
