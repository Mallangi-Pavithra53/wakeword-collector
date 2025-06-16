let recorder;
let audioChunks = [];

function startRecording() {
  console.log("Start button clicked");

  navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
      recorder = new MediaRecorder(stream);
      audioChunks = [];

      recorder.ondataavailable = e => {
        audioChunks.push(e.data);
      };

      recorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const audioUrl = URL.createObjectURL(audioBlob);
        document.getElementById("player").src = audioUrl;

        const form = document.getElementById("metaForm");
        const formData = new FormData(form);
        const username = formData.get("username") || "anonymous";
        formData.append("file", audioBlob, `${username}_hey_pavs.wav`);

        fetch("/upload", {
          method: "POST",
          body: formData
        })
        .then(response => response.text())
        .then(data => alert(" " + data))
        .catch(err => alert(" Upload failed: " + err));
      };

      recorder.start();
      console.log("Recording started...");
    })
    .catch(err => {
      console.error("Microphone access error:", err);
      alert("Microphone permission denied or not supported.");
    });
}

function stopRecording() {
  console.log("Stop button clicked");
  if (recorder && recorder.state === "recording") {
    recorder.stop();
  } else {
    alert("Recording is not active.");
  }
}
