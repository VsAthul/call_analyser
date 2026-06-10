let currentPage = 1;
const pageSize = 10;

const params =
    new URLSearchParams(
        window.location.search
    );

const callId =
    params.get("call_id");

async function loadSummaries(
    page = 1
) {

    try {

        let url =
            `/api/summaries?page=${page}&size=${pageSize}`;

        if (callId) {
            url += `&call_id=${callId}`;
        }

        const response =
            await fetch(url);

        const data =
            await response.json();

        const tbody =
            document.getElementById(
                "summaryTableBody"
            );

        tbody.innerHTML = "";

        if (
            !data.items ||
            data.items.length === 0
        ) {

            tbody.innerHTML = `
                <tr>
                    <td
                        colspan="4"
                        class="
                            px-6
                            py-8
                            text-center
                            text-gray-500
                        "
                    >
                        No summaries found
                    </td>
                </tr>
            `;

            return;
        }

        data.items.forEach(
            (row, index) => {

                const tr =
                    document.createElement(
                        "tr"
                    );

                tr.className =
                    "hover:bg-gray-50";

                tr.innerHTML = `
                    <td class="px-6 py-4 text-center">
                        ${
                            ((page - 1) * pageSize)
                            + index
                            + 1
                        }
                    </td>

                    <td class="px-6 py-4">
                        ${row.call_type || "-"}
                    </td>

                    <td class="px-6 py-4 text-sm">
                        ${row.summary_text || "-"}
                    </td>

                    <td class="px-6 py-4">
                        ${
                            row.audio_path
                            ?
                            `
                            <audio
                                controls
                                class="w-64"
                            >
                                <source
                                    src="${row.audio_path}"
                                    type="audio/mpeg"
                                >
                            </audio>
                            `
                            :
                            `
                            <span
                                class="text-gray-400"
                            >
                                -
                            </span>
                            `
                        }
                    </td>
                `;

                tbody.appendChild(tr);
            }
        );

        currentPage = page;

        document.getElementById(
            "pageInfo"
        ).innerText =
            `Page ${page}`;

        document.getElementById(
            "prevBtn"
        ).disabled =
            page <= 1;

        document.getElementById(
            "nextBtn"
        ).disabled =
            (page * pageSize)
            >= data.total;

    }
    catch (error) {

        console.error(error);

        alert(
            "Failed to load summaries"
        );
    }
}

function prevPage() {

    if (currentPage > 1) {

        loadSummaries(
            currentPage - 1
        );
    }
}

function nextPage() {

    loadSummaries(
        currentPage + 1
    );
}

function goBack() {

    sessionStorage.removeItem(
        "navigatingToSummaries"
    );

    window.location.href = "/";
}

window.addEventListener(
    "DOMContentLoaded",
    () => {

        loadSummaries();
    }
);