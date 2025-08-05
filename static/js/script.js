async function convertTextToSpeech() {
    const text = document.getElementById("text-input").value;

    const response = await fetch("/speak", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
    });

    if (response.ok) {
        const audioURL = URL.createObjectURL(await response.blob());
        const audio = new Audio(audioURL);
        audio.play();
    } else {
        alert("Failed to generate audio");
    }
}
