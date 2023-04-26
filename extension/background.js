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
  
    //send call to model to see if phishing
    var response = await fetch("https://www.phishtales.net/extension", {
      method: "POST",
      body: JSON.stringify({
          url: callback.url
      }),
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }
    });

    let phishing = await response.text();

    console.log("phishing:" + phishing);


    ignoreListContains(callback.url).then(
      isWhitelisted => {
    
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
      //allow loading of pages that users continue to
      whitelistMap.set(request.url, 1)
      whitelistTabs[request.tabId] = true
    }
  }
);

