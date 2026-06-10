let currentPage = 1;
const pageSize = 10;

const params =
    new URLSearchParams(
        window.location.search
    );

const callId =
    params.get(
        "call_id"
    );

document
.getElementById("backBtn")
.addEventListener(
    "click",
    () => {

        window.location.href =
            `/?call_id=${callId}`;
    }
);

document
.getElementById("prevBtn")
.addEventListener(
    "click",
    () => {

        if (currentPage > 1) {

            loadSummaries(
                currentPage - 1
            );
        }
    }
);

document
.getElementById("nextBtn")
.addEventListener(
    "click",
    () => {

        loadSummaries(
            currentPage + 1
        );
    }
);

async function loadSummaries(
    page = 1
) {

    try {

        const response =
            await fetch(
                `/api/summaries?page=${page}&size=${pageSize}`
            );

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
                            border
                            p-4
                            text-center
                        "
                    >
                        No summaries found
                    </td>
                </tr>
            `;

            return;
        }

        data.items.forEach(
            (
                row,
                index
            ) => {

                const tr =
                    document.createElement(
                        "tr"
                    );

                tr.innerHTML = `

                    <td
                        class="
                            border
                            p-2
                            text-center
                        "
                    >
                        ${
                            (
                                (page - 1)
                                * pageSize
                            )
                            + index
                            + 1
                        }
                    </td>

                    <td
                        class="
                            border
                            p-2
                        "
                    >
                        ${
                            row.call_type
                            || "-"
                        }
                    </td>

                    <td
                        class="
                            border
                            p-2
                        "
                    >
                        ${
                            row.summary_text
                            || "-"
                        }
                    </td>

                    <td
                        class="
                            border
                            p-2
                        "
                    >

                        ${
                            row.audio_path
                            ?
                            `
                            <audio controls>
                                <source
                                    src="${row.audio_path}"
                                    type="audio/mpeg"
                                >
                            </audio>
                            `
                            :
                            "-"
                        }

                    </td>
                `;

                tbody.appendChild(
                    tr
                );
            }
        );

        currentPage =
            page;

        document
        .getElementById(
            "pageInfo"
        )
        .innerText =
            `Page ${page}`;

        document
        .getElementById(
            "prevBtn"
        )
        .disabled =
            page <= 1;

        document
        .getElementById(
            "nextBtn"
        )
        .disabled =
            (
                page
                * pageSize
            )
            >= data.total;

    } catch (error) {

        console.error(
            error
        );

        alert(
            "Failed to load summaries"
        );
    }
}

loadSummaries();