var mainMenu = document.getElementById("mainMenu")
var domainWhitelist;
var currentURL;

chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
    console.log(tabs[0]);
  });




function getDomain(websiteURL) {
    let domain = (new URL(websiteURL));
    return domain.hostname;
  }

function addIgnoreList(website) {
    domain = getDomain(website);
    domainWhitelist = chrome.runtime.sendMessage({action: "updateIgnore", url: website, add: true });
    domainWhitelist.set(domain)
}


function showIgnoreList() {
    mainMenu.style.display = "none";
    if (domainWhitelist == undefined) {
        domainWhitelist = chrome.runtime.sendMessage({action: "getIgnore" });
    }
    
}

ignoreButton = document.getElementById('btnIgnore');

if (currentURL == undefined) {
    document.getElementById("lowerMenu").style.display = "none"
} else {
    ignoreButton.innerText = `Ignore ${currentURL.domain}`;
}







document.getElementById("btnIgnore").addEventListener("click", showIgnoreList);