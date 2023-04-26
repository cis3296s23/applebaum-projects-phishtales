
var domainWhitelist = new Map();

export function getDomain(websiteURL) {
    let domain = (new URL(websiteURL));
    return domain.hostname;
  }

  export  function updateIgnoreList(domain, add) {
  
    if (add == true) {
      domainWhitelist.set(domain, 1)
    } else {
      domainWhitelist.delete(domain)
    }
    chrome.storage.local.set(
      { "ignoreList": Object.fromEntries(domainWhitelist) }
    );
    
  }


  export async function loadWhitelist() {
    chrome.storage.local.get("ignoreList", function(result) {
        if (result != undefined && result.ignoreList != undefined) {
          domainWhitelist = new Map(Object.entries(result.ignoreList));
        } else {
          domainWhitelist = new Map();
        }
        return Promise.all;
      });
  }

  export  function getIgnore(domain) {
    return (domainWhitelist.get(domain) ?? 0);
  }

  export function getIgnoreList() {
    return new Map(domainWhitelist);
  }


// export {getDomain, updateIgnoreList, loadWhitelist, getIgnore};