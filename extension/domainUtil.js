
var domainWhitelist = new Map();

export function getDomain(websiteURL) {
    let domain = (new URL(websiteURL));
    return domain.hostname;
  }

  export  function updateIgnoreList(website, add) {
    domain = getDomain(website);
  
    if (add == true) {
      domainWhitelist.delete(domain)
    } else {
      domainWhitelist.set(domain, 0)
    }
    chrome.storage.local.set(
      { "ignoreList": Object.fromEntries(domainWhitelist) }
    );
    
  }


  export function loadWhitelist() {
    chrome.storage.local.get(["ignoreList"]).then((result) => {
        if (result) {
          domainWhitelist = new Map(Object.fromEntries(result.ignoreList));
        } else {
          domainWhitelist = new Map();
        }
      });
  }

  export  function getIgnore(domain) {
    return (domainWhitelist.get(domain) ?? 1);
  }


// export {getDomain, updateIgnoreList, loadWhitelist, getIgnore};