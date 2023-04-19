const urlString = window.location.search;
const urlParams = new URLSearchParams(urlString);
var currentTabId;


//display website name to user
infoLabel = document.getElementById('info');
infoLabel.innerHTML = `PhishTales has blocked ${getPhishingURL()}<br> This website is most likely phishing.`;

//get current tab id for whitelisting when clicking continue - website may redirect and prevent you from loading the next webpage
chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
    console.log(tabs[0]);
    currentTabId = tabs[0].id
});



function goBack() {
    chrome.tabs.goBack();
}

function continueToURL() {
    
    chrome.runtime.sendMessage({action: "whitelist", url: getPhishingURL(), tabId: currentTabId});
    chrome.tabs.update({url: getPhishingURL()});
}

function getPhishingURL() {
    return urlParams.get('url');
}

document.getElementById("continueToURL").addEventListener("click", continueToURL);
document.getElementById("goBack").addEventListener("click", goBack);
