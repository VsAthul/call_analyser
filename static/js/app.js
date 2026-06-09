let currentCallId = null;

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

        const callType =
            document.getElementById(
                "callType"
            ).value;

        if (!file) {
    alert("Select audio file");
    return;
}

const allowed = ["audio/wav", "audio/mpeg", "audio/mp4", "audio/x-m4a", "audio/mp3"];
const allowedExt = [".wav", ".mp3", ".m4a"];
const ext = file.name.substring(file.name.lastIndexOf(".")).toLowerCase();

if (!allowed.includes(file.type) && !allowedExt.includes(ext)) {
    alert("Unsupported file type. Please upload a .wav, .mp3, or .m4a file.");
    return;
}

        const formData =
            new FormData();

        formData.append(
            "audio_file",
            file
        );

        formData.append(
            "call_type",
            callType
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

        statusDiv.innerText =
            data.message;
    }
);

document
.getElementById("summaryBtn")
.addEventListener(
    "click",
    async () => {

        if (!currentCallId) {
            alert("Upload audio first");
            return;
        }

        const response =
            await fetch(
                `/api/calls/${currentCallId}/summary`
            );

        const data =
            await response.json();

        addMessage(
            "Summary",
            data.summary
        );
    }
);

document
.getElementById("transcriptBtn")
.addEventListener(
    "click",
    async () => {

        if (!currentCallId) {
            alert("Upload audio first");
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
            alert("Upload audio first");
            return;
        }

        const question =
            document.getElementById(
                "questionInput"
            ).value;

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

function addMessage(
    sender,
    text
) {

    const message =
        document.createElement("div");

    message.className =
        "bg-white p-4 rounded shadow";

    message.innerHTML =
        `
        <strong>${sender}</strong>
        <br>
        <pre class="whitespace-pre-wrap">
${text}
        </pre>
        `;

    chatWindow.appendChild(
        message
    );

    chatWindow.scrollTop =
        chatWindow.scrollHeight;
}