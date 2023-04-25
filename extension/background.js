let whitelistMap = new Map();
let whitelistTabs = {};

import {getDomain, getIgnore, updateIgnoreList} from './domainUtil.js'







async function ignoreListContains(websiteURL) {
  let domain = getDomain(websiteURL);
  return new Promise((resolve, reject) => {
    getIgnore(domain).then(
      result => {
        resolve(result == 1 || (whitelistMap.get(websiteURL) ?? 0) == 1);
      }
    );
    
    }); 
  
}

/*chrome.runtime.onStartup.addListener(
  function() {
    loadWhitelist();
  }
);*/



chrome.webNavigation.onCommitted.addListener(async (callback) => {
  if (callback.transitionType && callback.transitionType != 'auto_toplevel' && callback.transitionType != 'auto_subframe' ) {
    
    if (callback.url.startsWith(chrome.runtime.getURL("blocked.html"))) {
      return; // ignore blocked page
    }
  
    var phishing;
    //send call to model to see if phishing
    var response = await fetch("http://127.0.0.1:5000/extension", {//https://www.phishtales.net
      method: "POST",
      body: JSON.stringify({
          url: callback.url
      }),
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }
    });

    phishing = await response.text();

  


    console.log(phishing);
    //var phishing = callback.url == "https://www.google.com/";
    ignoreListContains(callback.url).then(
      isWhitelisted => {
        if (isWhitelisted == 0) {
          updateIgnoreList(getDomain(callback.url), 1)
        }
        console.log(`whitelisted : ${isWhitelisted}`);
    
        if (phishing == 'phishing' && !isWhitelisted && whitelistTabs[callback.tabId] == undefined) {
            chrome.action.setIcon({path: "/warning.png"});
            chrome.tabs.update(callback.tabId, {url: (chrome.runtime.getURL("blocked.html") + "?url=" + callback.url)});
            
        } else {
            chrome.action.setIcon({path: "/PhishTales.png"});
        }
    
        whitelistTabs[callback.tabId] = undefined;
      }
    );
    

  }
});


chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {

  
    if (sender.tab && sender.tab.url.startsWith(chrome.runtime.getURL("blocked.html")) && request.action == "whitelist") {
      whitelistMap.set(request.url, 1)
      whitelistTabs[request.tabId] = true
    }
  }
);

