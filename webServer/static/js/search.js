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
                                <h5 class="title is-5 simpleText">${model.modelId}</h5>
                                <div class="info-item">
                                    <i class="fas fa-thumbs-up has-text-info title" style ="color:rgb(13, 255, 1);"></i>
                                    <strong>Likes:</strong> ${model.likes || 0}
                                </div>
                                <div class="info-item">
                                    <i class="fas fa-book has-text-success title" style ="color:rgb(255, 175, 1);"></i>
                                    <strong>Library:</strong> ${model.library_name || "N/A"}
                                </div>
                                <div class="info-item">
                                    <i class="fas fa-project-diagram has-text-primary title"></i>
                                    <strong>Pipeline:</strong> ${model.pipeline_tag || "N/A"}
                                </div>
                                <div class="info-item">
                                    <i class="fas fa-download has-text-warning title" style ="color:rgb(1, 204, 255);"></i>
                                    <strong>Downloads:</strong> ${model.downloads || 0}
                                </div>
                                <div class="info-item">
                                    <i class="fas fa-scroll has-text-danger title" style ="color:rgb(204, 209, 65);"></i>
                                    <strong>License:</strong> ${model.license || "Unknown"}
                                </div>
                                <div class="info-item">
                                    <i class="fas fa-calendar-alt has-text-warning title" style ="color:rgb(255, 0, 0);"></i>
                                    <strong>Created At:</strong> ${model.createdAt ? model.createdAt.slice(0, 10) : "N/A"}
                                </div>
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
