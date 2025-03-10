$(document).ready(function () {
    let currentPage = 1;
    const resultsPerPage = 20;

    function fetchResults(query = "", page = 1) {
        $.get(`/search?query=${query}&page=${page}&limit=${resultsPerPage}`, function (data) {
            const resultsDiv = $("#results");
            resultsDiv.empty();

            if (!data.models || data.models.length === 0) {
                resultsDiv.append("<p class='text-center'>No models found.</p>");
                return;
            }

            data.models.forEach((model) => {
                resultsDiv.append(`
                    <div class="col-md-4">
                        <div class="card mb-3">
                            <div class="card-body">
                                <h5 class="card-title">${model.modelId}</h5>
                                <p><strong>Library:</strong> ${model.library_name || "N/A"}</p>
                                <p><strong>Pipeline:</strong> ${model.pipeline_tag || "N/A"}</p>
                                <p><strong>Downloads:</strong> ${model.downloads || 0}</p>
                                <p><strong>Likes:</strong> ${model.likes || 0}</p>
                                <p><strong>License:</strong> ${model.license || "Unknown"}</p>
                                <p><strong>Created:</strong> ${model.createdAt ? model.createdAt.slice(0, 10) : "N/A"}</p>
                                <a href="https://huggingface.co/${model.modelId}" class="btn btn-info" target="_blank">View Model</a>
                            </div>
                        </div>
                    </div>
                `);
            });

            renderPagination(data.totalPages, page);
        });
    }

    function renderPagination(totalPages, currentPage) {
        const pagination = $("#pagination");
        pagination.empty();

        if (totalPages > 1) {
            for (let i = 1; i <= totalPages; i++) {
                pagination.append(`
                    <li class="page-item ${i === currentPage ? 'active' : ''}">
                        <a class="page-link" href="#" data-page="${i}">${i}</a>
                    </li>
                `);
            }
        }
    }

    $("#searchButton").click(function () {
        currentPage = 1;
        const query = $("#query").val();
        fetchResults(query, currentPage);
    });

    $("#pagination").on("click", "a", function (e) {
        e.preventDefault();
        currentPage = parseInt($(this).data("page"));
        fetchResults($("#query").val(), currentPage);
    });

    // Load initial models without a query
    fetchResults();
});
