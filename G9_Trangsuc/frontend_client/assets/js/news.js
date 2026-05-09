async function loadNews() {
    const response = await fetch(`${API_BASE_URL}/bdh/news/`);
    const news = await response.json();

    let html = "";

    news.forEach(item => {
        html += `
            <div class="col-md-3 mb-4">
                <div class="card h-100">
                    <img src="assets/img/${item.image}" class="card-img-top" style="height:160px; object-fit:cover;">

                    <div class="card-body">
                        <h6>${item.title}</h6>
                        <p>${item.shortDescription}</p>
                        <small>${item.category}</small>
                    </div>
                </div>
            </div>
        `;
    });

    const newsList = document.getElementById("news-list");

    if (newsList) {
        newsList.innerHTML = html;
    }
}

loadNews();