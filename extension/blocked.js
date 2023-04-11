const urlString = window.location.search;
const urlParams = new URLSearchParams(urlString);
console.log(urlParams.get('url'));

infoLabel = document.getElementById('info');

infoLabel.innerHTML = `PhishTales has blocked ${urlParams.get('url')}<br> This website is most likely phishing.`;


function goBack() {
    chrome.tabs.goBack();
}

function continueToURL() {
    chrome.runtime.sendMessage({action: "whitelist", url: urlParams.get('url')});
    chrome.tabs.update({url: urlParams.get('url')});
}

function getPhishingURL() {
    return urlParams.get('url');
}

document.getElementById("continueToURL").addEventListener("click", continueToURL);
document.getElementById("goBack").addEventListener("click", goBack);
