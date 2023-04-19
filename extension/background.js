var whitelistMap = new Map();

// const { getDomain, updateIgnoreList, loadWhitelist, getIgnore } = require('./domainUtil')
import {getDomain, updateIgnoreList, loadWhitelist, getIgnore} from './domainUtil.js'







function ignoreListContains(websiteURL) {
  let domain = getDomain(websiteURL);
  return getIgnore(domain) == 0 || (whitelistMap.get(websiteURL) ?? 1) == 0;
  
}

chrome.runtime.onStartup.addListener(
  function() {
    loadWhitelist();
  }
);



chrome.webNavigation.onCommitted.addListener((callback) => {
  if (callback.transitionType && callback.transitionType != 'auto_toplevel' && callback.transitionType != 'auto_subframe' ) {
    console.log(`${callback.url} ${callback.frameId} ${callback.tabId} ${callback.parentFrameId} ${callback.transitionType}`);
  
    
    //send call to model to see if phishing
    var phishing = callback.url == "https://www.google.com/";
    var isWhitelisted = ignoreListContains(callback.url);
    console.log(`whitelsited : ${isWhitelisted}`);

    if (phishing && !isWhitelisted) {
        chrome.action.setIcon({path: "/warning.png"});
        chrome.tabs.update(callback.tabId, {url: (chrome.runtime.getURL("blocked.html") + "?url=" + callback.url)});
        
    } else if (!isWhitelisted) {
        chrome.action.setIcon({path: "/PhishTales.png"});
    }

  }
});


chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {

  
    if (sender.tab && sender.tab.url.startsWith(chrome.runtime.getURL("blocked.html")) && request.action == "whitelist") {
      console.log(sender.tab ?
        "from a content script:" + sender.tab.url :
        "from the extension");
      whitelistMap.set(request.url, 0)
    } else if (request.action == 'updateIgnore') {
      updateIgnoreList(request.url, request.add);
    } else if (request.action == 'getIgnore') {
     // return domainWhitelist;
    }
  }
);

