
//window.domainWhitelist  = new Map();
//window.loaded = false;


async function getFromStorage(key) {
  return new Promise((resolve, reject) => {

    chrome.storage.local.get(key, async function(result) {
      console.log("result: " + new Map(Object.entries(result)));
      resolve(result);
    });

  });
}




function addToStorage(key) {
  chrome.storage.local.set(
    { [key]: 1 }
  );
}

function removeFromStorage(key) {
  chrome.storage.local.remove(key);
}

export function getDomain(websiteURL) {
    let domain = (new URL(websiteURL));
    return domain.hostname;
  }

export  function updateIgnoreList(domain, add) {
  if (add == true) {
    addToStorage(domain);
  } else {
    removeFromStorage(domain);
  }
    /*if (window.loaded == true) {
      chrome.storage.local.set(
        { "ignoreList": Object.fromEntries(domainWhitelist) }
      );
    }*/
    
    
  
}


 /*export function loadWhitelist() {
    chrome.storage.local.get("ignoreList", function(result) {
        if (result != undefined && result.ignoreList != undefined) {
          let tempdomainWhitelist = new Map(Object.entries(result.ignoreList));
          window.domainWhitelist = new Map([window.domainWhitelist, tempdomainWhitelist]);
          window.loaded = true;
          console.log("loaded");
        }
      });
  }*/

  export async function getIgnore(domain) {
    return new Promise((resolve, reject) => {
      getFromStorage(domain).then(
        result => {
          resolve(result[domain] ?? 0);
        }
      );
      
      }); 
  }

  export async function getIgnoreList() {
   // console.log("result1: " + getFromStorage());
   return new Promise((resolve, reject) => {
    getFromStorage().then(
      result => {
        resolve(new Map(Object.entries(result)));
      }
    );
    
    }); 
  }


// export {getDomain, updateIgnoreList, loadWhitelist, getIgnore};