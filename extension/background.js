const whitelistMap = new Map()

chrome.webNavigation.onCommitted.addListener((callback) => {
  if (callback.transitionType && callback.transitionType != 'auto_toplevel' && callback.transitionType != 'auto_subframe' ) {
    console.log(`${callback.url} ${callback.frameId} ${callback.tabId} ${callback.parentFrameId} ${callback.transitionType}`);
  
    
    //send call to model to see if phishing
    var phishing = callback.url == "https://www.google.com/";

    if (phishing && (whitelistMap.get(callback.url) ?? 1) == 1) {


        chrome.action.setIcon({path: "/warning.png"});
        chrome.tabs.update(callback.tabId, {url: (chrome.runtime.getURL("blocked.html") + "?url=" + callback.url)});
    } else {
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
    }
  }
);

