const params =
    new URLSearchParams(
        window.location.search
    );

let currentCallId =params.get("call_id");

const statusDiv =
    document.getElementById("status");

const chatWindow =
    document.getElementById("chatWindow");

document
.getElementById("uploadBtn")
.addEventListener(
    "click",
    async () => {

        const file =
            document.getElementById(
                "audioFile"
            ).files[0];

        if (!file) {
            alert("Select audio file");
            return;
        }

        const allowedExt =
            [".wav", ".mp3", ".m4a", ".aac"];

        const ext =
            file.name
                .substring(
                    file.name.lastIndexOf(".")
                )
                .toLowerCase();

        if (!allowedExt.includes(ext)) {

            alert(
                "Unsupported file type. Please upload a .wav, .mp3, or .m4a file."
            );

            return;
        }

        const formData =
            new FormData();

        formData.append(
            "audio_file",
            file
        );

        statusDiv.innerText =
            "Processing audio...";

        const response =
            await fetch(
                "/api/calls/upload",
                {
                    method: "POST",
                    body: formData
                }
            );

        const data =
            await response.json();

        currentCallId =
            data.call_id;

        statusDiv.innerHTML = `
            <div style="margin-top:8px;">
                <p style="color:#16a34a;font-weight:600;">
                    ✅ Processing complete
                </p>

                <p style="margin-top:4px;">
                    📞 Call Type:
                    <strong>${data.call_type}</strong>
                </p>

                <p style="margin-top:2px;">
                    🆔 Call ID:
                    <strong>${data.call_id}</strong>
                </p>
            </div>
        `;
    }
);

document
.getElementById("summaryBtn")
.addEventListener(
    "click",
    async () => {

        if (!currentCallId) {

            alert(
                "Upload audio first"
            );

            return;
        }

        const response =
            await fetch(
                `/api/calls/${currentCallId}/summary`
            );

        const data =
            await response.json();

        showChatView();

        addMessage(
            "Summary",
            data.summary
        );

        if (data.audio_path) {

            const wrapper =
                document.createElement(
                    "div"
                );

            wrapper.innerHTML = `
                <div
                    style="
                        background:white;
                        padding:12px;
                        border-radius:12px;
                        border:1px solid #e5e7eb;
                    "
                >
                    <p
                        style="
                            font-size:12px;
                            font-weight:600;
                            margin-bottom:8px;
                        "
                    >
                        Audio Summary
                    </p>

                    <audio controls>
                        <source
                            src="${data.audio_path}"
                            type="audio/mpeg"
                        >
                    </audio>
                </div>
            `;

            chatWindow.appendChild(
                wrapper
            );

            chatWindow.scrollTop =
                chatWindow.scrollHeight;
        }
    }
);

document
.getElementById("summaryListBtn")
.addEventListener(
    "click",
    () => {

        console.log(
            "currentCallId:",
            currentCallId
        );

        if (!currentCallId) {

            alert(
                "Upload audio first"
            );

            return;
        }

        window.location.href =
            `/summaries?call_id=${currentCallId}`;
    }
);

document
.getElementById("transcriptBtn")
.addEventListener(
    "click",
    async () => {

        if (!currentCallId) {

            alert(
                "Upload audio first"
            );

            return;
        }

        const response =
            await fetch(
                `/api/calls/${currentCallId}/transcript`
            );

        const data =
            await response.json();

        let transcriptText = "";

        data.transcript.forEach(
            item => {

                transcriptText +=
                    `${item.speaker}: ${item.text}\n`;
            }
        );

        showChatView();

        addMessage(
            "Transcript",
            transcriptText
        );
    }
);

document
.getElementById("askBtn")
.addEventListener(
    "click",
    async () => {

        if (!currentCallId) {

            alert(
                "Upload audio first"
            );

            return;
        }

        const question =
            document.getElementById(
                "questionInput"
            ).value;

        if (!question.trim()) {

            alert(
                "Please enter a question"
            );

            return;
        }

        showChatView();

        addMessage(
            "You",
            question
        );

        const response =
            await fetch(
                `/api/calls/${currentCallId}/ask`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                        "application/json"
                    },

                    body: JSON.stringify(
                        {
                            question
                        }
                    )
                }
            );

        const data =
            await response.json();

        addMessage(
            "Assistant",
            data.answer
        );

        document.getElementById(
            "questionInput"
        ).value = "";
    }
);

function showChatView() {

    chatWindow.style.display =
        "flex";
}

function addMessage(
    sender,
    text
) {

    const isUser =
        sender === "You";

    const wrapper =
        document.createElement(
            "div"
        );

    wrapper.style.display =
        "flex";

    wrapper.style.justifyContent =
        isUser
        ? "flex-end"
        : "flex-start";

    wrapper.style.marginBottom =
        "12px";

    const bubble =
        document.createElement(
            "div"
        );

    bubble.style.maxWidth =
        "70%";

    bubble.style.padding =
        "12px 16px";

    bubble.style.borderRadius =
        "18px";

    bubble.style.boxShadow =
        "0 1px 3px rgba(0,0,0,0.1)";

    bubble.style.backgroundColor =
        isUser
        ? "#2563eb"
        : "#ffffff";

    bubble.style.color =
        isUser
        ? "#ffffff"
        : "#1f2937";

    bubble.style.border =
        isUser
        ? "none"
        : "1px solid #e5e7eb";

    bubble.style.borderBottomRightRadius =
        isUser
        ? "4px"
        : "18px";

    bubble.style.borderBottomLeftRadius =
        isUser
        ? "18px"
        : "4px";

    bubble.innerHTML = `
        <p
            style="
                font-size:11px;
                font-weight:600;
                margin-bottom:4px;
                opacity:0.7;
            "
        >
            ${sender}
        </p>

        <pre
            style="
                white-space:pre-wrap;
                font-size:14px;
                font-family:inherit;
                margin:0;
            "
        >
${text}
        </pre>
    `;

    wrapper.appendChild(
        bubble
    );

    chatWindow.appendChild(
        wrapper
    );

    chatWindow.scrollTop =
        chatWindow.scrollHeight;
}