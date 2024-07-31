import streamlit as st
import pandas as pd
import openpyxl as xl

st.set_page_config(page_title="acaocidada", layout='wide')

st.markdown("""
            <style>
            .st-emotion-cache-czk5ss.e16jpq800{
                visibility:hidden;
            }
            .stDeployButton{
                visibility:hidden;
            }
            </style>
            """,unsafe_allow_html=True)

#tutores
arq_carioca = pd.read_csv('relat_fs01_carioca01_tutor.csv')
arq_rio1 = pd.read_csv('relat_fs01_rio01_tutor.csv')
carioca_df = pd.DataFrame(arq_carioca)
rio01_df = pd.DataFrame(arq_rio1)
# Agendamento
planilha = xl.load_workbook("relatorio_fase01_acaocidada.xlsx")
c_genero = planilha['resultados_generos_fase01']
atendimentos_df = pd.read_excel('relatorio_fase01_acaocidada.xlsx', sheet_name='resultados_atendimentos_fase01')
meses_df = pd.read_excel('relatorio_fase01_acaocidada.xlsx', sheet_name='resultados_meses_fase01')
genero_df = pd.DataFrame(list(c_genero.values)[1:], columns=list(c_genero.values)[0]).fillna(0)

def intro():
    import streamlit as st
    st.title("Relatório Fase 01")
    st.image("logo_azul_preto.jpeg",output_format='JPEG')

def tutores():
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    from scipy import stats
    tab1,tab2,tab3 = st.tabs(['Escolha das Análises','Gráficos', 'Tabelas Resumo'])
    #col1,col2, col3 = st.columns([2,2,8],)    
#seleção das páginas:
    if opcoes_tutores == "Carioca":
        with tab1:
            col1,col2, col3 = st.columns([2,2,8],)
            # Escolha da variavel X
            with col1:
                x_carioca_lista = list(carioca_df.columns[1:])
                var_c_x = st.radio(
                    "*Escolha o valor das linhas*",
                    x_carioca_lista,
                )
                figx = px.pie(
                    carioca_df[var_c_x], 
                    values=list(carioca_df[var_c_x].value_counts()),
                    names=list(carioca_df[var_c_x].unique()),
                    title=f'Variável {var_c_x}')
                x_carioca_lista.pop(x_carioca_lista.index(var_c_x))
                y_carioca_lista = x_carioca_lista
            # Escolha da variavel Y
            with col2:
                var_c_y = st.radio(
                    "*Escolha o valor das colunas*",
                    y_carioca_lista,
                )
                figy = px.pie(
                    carioca_df[var_c_y],
                    values=list(carioca_df[var_c_y].value_counts()),
                    names=list(carioca_df[var_c_y].unique()),
                    title=f'Variavel {var_c_y}')
            # Criação da tabela de contingência                    
            with col3:
                st.title("Escolha as variáveis")
                st.plotly_chart(figx)
                st.plotly_chart(figy)

        #tabela de contingencia
        c_ctab = pd.crosstab(carioca_df[var_c_x],carioca_df[var_c_y])
        res = stats.chi2_contingency(c_ctab)

        with tab2:
            fig_c = px.bar(
                c_ctab,
                x=c_ctab.index,
                y=c_ctab.columns,
                title='Gráfico de barras',
                color_discrete_sequence=px.colors.qualitative.Plotly,
                labels={'value':f'{var_c_y}'},
                barmode='group',
            )
            st.plotly_chart(fig_c)
        with tab3:
            c_ctab_n = pd.crosstab(carioca_df[var_c_x],carioca_df[var_c_y], normalize=True)*100
            #c_ctab_n.style.background_gradient(cmap='coolwarm').format(precision=2)
            fig_heatmap = px.imshow(c_ctab_n, text_auto=True, aspect='auto')
            st.plotly_chart(fig_heatmap)
            st.title("Tabela de relativa (%)")
            st.table(c_ctab_n)
            if min(c_ctab.min())>4:
                if float(res.pvalue) > 0.05:
                    st.markdown("---")
                    st.markdown("### As variáveis escolhidas não são *Associadas*.")
                    st.write("pvalue:", round(float(res.pvalue),3))
                    st.table(c_ctab)
                else:
                    st.markdown("---")
                    st.markdown("### As variáveis escolhidas são *dependentes*")
                    st.write("pvalue:", round(float(res.pvalue),3))
                    st.table(c_ctab)
            elif min(c_ctab.min())<5:
                st.markdown("---")
                st.markdown(
                    """ As Variáveis escolhidas possuem
                    *Células* com valores menores que 5
                    não sendo possível realizar o teste de hipótese
                    escolhido.""")
                st.table(c_ctab)

    if opcoes_tutores == 'Rio':
        with tab1:
            col1,col2, col3 = st.columns([2,2,8],)
            # Escolha da variavel X
            with col1:
                x_rio_lista = list(rio01_df.columns[1:])
                var_r_x = st.radio(
                    "*Escolha o valor das linhas*",
                    x_rio_lista)
                figx = px.pie(
                    rio01_df[var_r_x], 
                    values=list(rio01_df[var_r_x].value_counts()),
                    names=list(rio01_df[var_r_x].unique()),
                    title=f'Variável {var_r_x}')
                x_rio_lista.pop(x_rio_lista.index(var_r_x))
                #y_rio_lista = x_rio_lista
            # Escolha da variavel Y
            with col2:
                y_rio_lista = x_rio_lista
                var_r_y = st.radio(
                    "*Escolha o valor das colunas*",
                    y_rio_lista)
                figy = px.pie(
                    rio01_df[var_r_y],
                    values=list(rio01_df[var_r_y].value_counts()),
                    names=list(rio01_df[var_r_y].unique()),
                    title=f'Variavel {var_r_y}')
            # Criação da tabela de contingência                    
            r_ctab = pd.crosstab(rio01_df[var_r_x],rio01_df[var_r_y])
            res = stats.chi2_contingency(r_ctab)
            with col3:
                st.title("Escolha as variáveis")
                st.plotly_chart(figx)
                st.plotly_chart(figy)
                if min(r_ctab.min())>4:
                    if float(res.pvalue) > 0.05:
                        st.markdown("### As variáveis escolhidas não são *Associadas*.")
                        st.write("pvalue:", round(float(res.pvalue),3))
                        st.table(r_ctab)
                    else:
                        st.markdown("### As variáveis escolhidas são *dependentes*")
                        st.write("pvalue:", round(float(res.pvalue),3))
                        st.table(r_ctab)
                elif min(r_ctab.min())<5:
                    st.markdown(
                        """ As Variáveis escolhidas possuem
                        *Células* com valores menores que 5
                        não sendo possível realizar o teste de hipótese
                                escolhido.""")
                    st.table(r_ctab)          
        with tab2:
            fig_r = px.bar(
                r_ctab,
                x=r_ctab.index,
                y=r_ctab.columns,
                labels={'value':f'{var_r_y}'},
                color_discrete_sequence=px.colors.qualitative.Plotly,
                title='Gráfico de barras',
                barmode='group',
            )
            st.plotly_chart(fig_r)

        with tab3:
            r_ctab_n = pd.crosstab(rio01_df[var_r_x],rio01_df[var_r_y], normalize=True)*100
            r_fig_heatmap = px.imshow(r_ctab_n, text_auto=True, aspect='auto')
            st.plotly_chart(r_fig_heatmap)
            st.title("Tabela de relativa (%)")
            st.table(r_ctab_n)
            if min(r_ctab.min())>4:
                if float(res.pvalue) > 0.05:
                    st.markdown("---")
                    st.markdown("### As variáveis escolhidas não são *Associadas*.")
                    st.write("pvalue:", round(float(res.pvalue),3))
                    st.table(r_ctab)
                else:
                    st.markdown("---")
                    st.markdown("### As variáveis escolhidas são *dependentes*")
                    st.write("pvalue:", round(float(res.pvalue),3))
                    st.table(r_ctab)
            elif min(r_ctab.min())<5:
                st.markdown("---")
                st.markdown(
                    """ As Variáveis escolhidas possuem
                    *Células* com valores menores que 5
                    não sendo possível realizar o teste de hipótese
                    escolhido.""")
                st.table(r_ctab)
                
def agendamento():
    import openpyxl as xl
    import pandas as pd
    import altair as alt
    import plotly.express as px
    
    tab1,tab2 = st.tabs(['valores absolutos', 'valores relativos (%)'])
    #col1, col2 =st.columns([1,4])
                
    #atendimentos
    abs_plt_atendimentos = (atendimentos_df.drop([3]).drop(['endereço não encontrado', 'chipagem','total'],axis=1).fillna(0).set_index('trailer')).T
    rel_plt_atendimentos = abs_plt_atendimentos/abs_plt_atendimentos.sum()*100
    at_fig_abs = px.bar(abs_plt_atendimentos, 
                        x=abs_plt_atendimentos.columns, 
                        y=abs_plt_atendimentos.index,
                        labels={'value':'trailers','index':'atendimentos'}, 
                        color_discrete_sequence = px.colors.qualitative.G10, 
                        barmode='group')
    at_fig_rel = px.bar(rel_plt_atendimentos, 
                        x=rel_plt_atendimentos.index,
                        y=rel_plt_atendimentos.columns,
                        labels={'value':'trailers','index':'atendimentos'},
                        barmode='group')

    
    #meses
    abs_plt_meses = (meses_df.drop([3]).drop(['total', 'inicio_fase-01','fim_fase-01'],axis=1).fillna(0).set_index('trailer')).T
    rel_plt_meses = abs_plt_meses/abs_plt_meses.sum()*100
    m_fig_abs = px.line(abs_plt_meses, x=abs_plt_meses.index, y=abs_plt_meses.columns, markers=True)
    m_fig_rel = px.line(rel_plt_meses, x=rel_plt_meses.index, y=rel_plt_meses.columns, markers=True)
    
    #genero
    abs_plt_genero = genero_df[['trailer', 'canino_f', 'canino_m', 'felino_f', 'felino_m']][:-1]
    rel_plt_genero = abs_plt_genero[['trailer']].join(round(genero_df[['canino_f', 'canino_m', 'felino_f', 'felino_m']][:-1]/genero_df['total'].max()*100,2))
    g_fig_rel = px.bar(rel_plt_genero, x='trailer',y=rel_plt_genero.columns[1:],barmode='group')
    g_fig_abs = px.bar(abs_plt_genero, x='trailer', y=abs_plt_genero.columns[1:],barmode='group')
    
    with tab1:
        if opcoes_agendamento == 'atendimentos':
            st.plotly_chart(at_fig_abs,theme="streamlit")
            st.markdown("<h1 style='text-align: center;'>Frequências Absolutas</h1>", unsafe_allow_html=True)
            st.table(atendimentos_df)
            
        elif opcoes_agendamento == 'meses':
            st.plotly_chart(m_fig_abs,theme="streamlit")
            st.markdown("<h1 style='text-align: center;'>Frequências Absolutas</h1>", unsafe_allow_html=True)
            st.table(meses_df)
            
        elif opcoes_agendamento == 'genero':
            st.plotly_chart(g_fig_abs,theme="streamlit")
            st.markdown("<h1 style='text-align: center;'>Frequências Absolutas</h1>", unsafe_allow_html=True)
            st.table(genero_df)
    
    with tab2:
        if opcoes_agendamento == 'atendimentos':
            st.plotly_chart(at_fig_rel, theme='streamlit')
            st.markdown("<h1 style='text-align: center;'>Frequências Relativas (%)</h1>", unsafe_allow_html=True)
            st.table(atendimentos_df[['trailer']].join(round(atendimentos_df[atendimentos_df.columns[1:]]/atendimentos_df['total'].max()*100,2)))
        
        elif opcoes_agendamento == 'meses':
            st.plotly_chart(m_fig_rel, theme='streamlit')
            st.markdown("<h1 style='text-align: center;'>Frequências Relativas (%)</h1>", unsafe_allow_html=True)
            st.table(meses_df[['trailer']].join(round(meses_df[meses_df.columns[1:7]]/meses_df['total'].max()*100,2)))
        
        elif opcoes_agendamento == 'genero':
            st.plotly_chart(g_fig_rel, theme='streamlit')
            st.markdown("<h1 style='text-align: center;'>Frequências Relativas (%)</h1>", unsafe_allow_html=True)
            st.table(genero_df[['trailer']].join(round(genero_df[genero_df.columns[1:]]/meses_df['total'].max()*100,2)))
            
# estrutura das paginas

paginas = {
    "---":intro,
    "relatorio censo tutor":tutores,
    "relatorio agendamentos":agendamento, 
}

st.logo('logo1.jpeg')
selecao = st.sidebar.selectbox("Selecione:", paginas.keys())

with st.sidebar:
    if selecao == "relatorio agendamentos":
        opcoes_agendamento = st.radio(
        "*Escolha qual grupo deseja verificar*",
        ['atendimentos','meses','genero'])
    elif selecao == "relatorio censo tutor":
        opcoes_tutores = st.radio(
            "*Escolha qual trailer deseja verificar*",
            ['Carioca','Rio'])
        
    else:
        st.success("Escolha a base de deseja")

paginas[selecao]()