const API_URL = 'http://127.0.0.1:5000/api';
let meuGrafico = null;

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('data').value = new Date().toISOString().split('T')[0];
    
    // Seleciona o mes atual por padrao no filtro
    const mesAtual = new Date().getMonth() + 1;
    document.getElementById('filtroMes').value = mesAtual;
    
    aplicarFiltros();
});

function aplicarFiltros() {
    const mes = document.getElementById('filtroMes').value;
    const ano = document.getElementById('filtroAno').value;

    carregarResumo(mes, ano);
    carregarTransacoes(mes, ano);
}

// CARREGAR RESUMO COM FILTROS
async function carregarResumo(mes = '', ano = '') {
    try {
        const url = `${API_URL}/resumo?mes=${mes}&ano=${ano}`;
        const resposta = await fetch(url);
        const dados = await resposta.json();

        document.getElementById('totalReceitas').innerText = formatarMoeda(dados.total_receitas);
        document.getElementById('totalDespesas').innerText = formatarMoeda(dados.total_despesas);
        document.getElementById('saldoTotal').innerText = formatarMoeda(dados.saldo);

        renderizarGrafico(dados.despesas_por_categoria);
    } catch (erro) {
        console.error('Erro ao carregar resumo:', erro);
    }
}

// CARREGAR LISTA DE TRANSACOES COM FILTROS
async function carregarTransacoes(mes = '', ano = '') {
    try {
        const url = `${API_URL}/transacoes?mes=${mes}&ano=${ano}`;
        const resposta = await fetch(url);
        const transacoes = await resposta.json();

        const tbody = document.getElementById('tabelaTransacoes');
        tbody.innerHTML = '';

        transacoes.forEach(t => {
            const tr = document.createElement('tr');
            const classeValor = t.tipo === 'receita' ? 'valor-receita' : 'valor-despesa';
            const sinal = t.tipo === 'receita' ? '+' : '-';

            tr.innerHTML = `
                <td>${formatarData(t.data)}</td>
                <td><strong>${t.descricao}</strong></td>
                <td>${t.categoria}</td>
                <td>${t.tipo === 'receita' ? '🟢 Receita' : '🔴 Despesa'}</td>
                <td class="${classeValor}">${sinal} ${formatarMoeda(t.valor)}</td>
                <td>
                    <button class="btn-deletar" onclick="deletarTransacao(${t.id})">❌</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (erro) {
        console.error('Erro ao carregar transações:', erro);
    }
}

// SALVAR TRANSACAO (POST)
async function salvarTransacao(event) {
    event.preventDefault();

    const novaTransacao = {
        descricao: document.getElementById('descricao').value,
        valor: parseFloat(document.getElementById('valor').value),
        tipo: document.getElementById('tipo').value,
        categoria: document.getElementById('categoria').value,
        data: document.getElementById('data').value
    };

    try {
        const resposta = await fetch(`${API_URL}/transacoes`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(novaTransacao)
        });

        if (resposta.ok) {
            document.getElementById('descricao').value = '';
            document.getElementById('valor').value = '';
            aplicarFiltros();
        }
    } catch (erro) {
        console.error('Erro ao salvar transação:', erro);
    }
}

// DELETAR TRANSACAO (DELETE)
async function deletarTransacao(id) {
    if (!confirm('Deseja realmente remover este registro?')) return;

    try {
        const resposta = await fetch(`${API_URL}/transacoes/${id}`, { method: 'DELETE' });
        if (resposta.ok) aplicarFiltros();
    } catch (erro) {
        console.error('Erro ao deletar:', erro);
    }
}

// EXPORTAR RELATORIO PARA CSV
function exportarCSV() {
    window.location.href = `${API_URL}/exportar/csv`;
}

// RENDERIZAR GRAFICO (CHART.JS)
function renderizarGrafico(dadosCategorias) {
    const ctx = document.getElementById('graficoCategorias').getContext('2d');

    const labels = dadosCategorias.map(item => item.categoria);
    const valores = dadosCategorias.map(item => item.total);

    if (meuGrafico) {
        meuGrafico.destroy();
    }

    meuGrafico = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels.length ? labels : ['Sem despesas'],
            datasets: [{
                data: valores.length ? valores : [1],
                backgroundColor: [
                    '#e74c3c', '#e67e22', '#f1c40f', 
                    '#9b59b6', '#3498db', '#95a5a6'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });
}

function formatarMoeda(valor) {
    return Number(valor).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

function formatarData(dataISO) {
    const partes = dataISO.split('-');
    return `${partes[2]}/${partes[1]}/${partes[0]}`;
}