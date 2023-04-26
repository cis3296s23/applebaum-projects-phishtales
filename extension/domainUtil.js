
async function getFromStorage(key) {
  return new Promise((resolve, reject) => {

    chrome.storage.local.get(key, async function(result) {
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
}




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
   return new Promise((resolve, reject) => {
    getFromStorage().then(
      result => {
        resolve(new Map(Object.entries(result)));
      }
    );
    
    }); 
  }