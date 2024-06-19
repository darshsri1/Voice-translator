const btn = document.getElementById("translate");
const inputQuestion = document.getElementById("language");

btn.addEventListener("click", function() {
    btn.disabled = true;
    btn.innerHTML = "Getting audio...";
    btn.style.boxShadow = 'None';

    chrome.tabs.query({ currentWindow: true, active: true }, function(tabs) {
        var url = tabs[0].url;
        var question = inputQuestion.value;
        var xhr = new XMLHttpRequest();

        xhr.open("GET", "http://127.0.0.1:5000/answer?url=" + url + "&question=" + encodeURIComponent(question), true);

        xhr.onload = function() {
            var answer = xhr.responseText;
            const p = document.getElementById("output");
            p.innerHTML = "Audio: " + answer;
            btn.disabled = false;
            btn.innerHTML = "Translate Audio";
            btn.style.boxShadow = '5px 5px 5px rgba(0, 0, 0, 0.3)';
        };

        xhr.send();
    });
});