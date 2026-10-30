document.addEventListener("DOMContentLoaded", () => {
    fetch('data/catalog.json')
        .then(response => response.json())
        .then(data => montarCatalogo(data))
        .catch(error => console.error("Erro ao carregar o catálogo:", error));
});

function montarCatalogo(filmes) {
    const container = document.getElementById("catalog-container");
    container.innerHTML = "";

    // Agrupar por categoria
    const categorias = {};
    filmes.forEach(filme => {
        if (!categorias[filme.categoria]) {
            categorias[filme.categoria] = [];
        }
        categorias[filme.categoria].push(filme);
    });

    // Criar seções para cada categoria
    for (const [categoria, itens] of Object.entries(categorias)) {
        const secaoDiv = document.createElement("div");
        secaoDiv.classList.add("categoria-secao");

        const tituloSecao = document.createElement("h2");
        tituloSecao.textContent = categoria;
        secaoDiv.appendChild(tituloSecao);

        const rowDiv = document.createElement("div");
        rowDiv.classList.add("cards-row");

        itens.forEach(filme => {
            const card = document.createElement("div");
            card.classList.add("media-card");
            card.innerHTML = `
                <img src="${filme.imagem}" alt="${filme.titulo}" onerror="this.src='https://via.placeholder.com/200x280?text=Sem+Imagem'">
                <div class="media-card-info">
                    <h3>${filme.titulo}</h3>
                </div>
            `;
            
            // Evento de clique para abrir o player passando os dados por parâmetro na URL
            card.addEventListener("click", () => {
                const params = new URLSearchParams({
                    titulo: filme.titulo,
                    descricao: filme.descricao,
                    video: filme.video
                });
                window.location.href = `player.html?${params.toString()}`;
            });

            rowDiv.appendChild(card);
        });

        secaoDiv.appendChild(rowDiv);
        container.appendChild(secaoDiv);
    }
}