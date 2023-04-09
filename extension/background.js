var newId = 1;

chrome.declarativeNetRequest.getDynamicRules((callback) => { 
    console.log(callback.length);
    newId = callback.length + 1;
});


/*
chrome.webNavigation.onBeforeNavigate.addListener((callback) => {
    console.log(callback.url);
    //send call to model to see if phishing
    var phishing = true;

    if (phishing) {
        chrome.action.setIcon({path: "/warning.png"});
        chrome.declarativeNetRequest.updateDynamicRules(
            {
              addRules: [
                {
                  action: {
                    type: "block",
                  },
                  condition: {
                    urlFilter: callback.url, // block URLs that starts with this
                    
                  },
                  id: newId,
                  priority: 1,
                },
              ],
            },
            () => {
              newId += 1;
              console.log("block rule added");
            }
          );
    } else {
        chrome.action.setIcon({path: "/PhishTales.png"});
    }


  });*/

  chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    console.log("changed");
    console.log(changeInfo.url);
    if (changeInfo.url) {
        
        var phishing = true;

        if (phishing) {
            chrome.action.setIcon({path: "/warning.png"});
            chrome.declarativeNetRequest.updateDynamicRules(
                {
                addRules: [
                    {
                    action: {
                        type: "block",
                    },
                    condition: {
                        urlFilter: changeInfo.url, // block URLs that starts with this
                        
                    },
                    id: newId,
                    priority: 1,
                    },
                ],
                },
                () => {
                newId += 1;
                console.log("block rule added");
                }
            );
        } else {
            chrome.action.setIcon({path: "/PhishTales.png"});
        }
    }
  });