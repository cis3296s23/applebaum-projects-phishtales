import { getDomain, getIgnore, getIgnoreList, loadWhitelist, updateIgnoreList } from "./domainUtil.js";

var mainMenu = document.getElementById("mainMenu")
var ignoreButton = document.getElementById('btnIgnoreList');
var lblCurrentDomain = document.getElementById('lblCurrentDomain');
var ignoreListMenu = document.getElementById('ignoreListMenu');
var ignoreListContainer = document.getElementById('ignoreList');
var ignoreListItem = document.getElementById('ignoreListItem');
var btnAddToIgnoreList = document.getElementById('btnAddWhitelist');
var btnExitIgnoreList = document.getElementById('btnExitIgnoreList');
var btnWebsite = document.getElementById('btnWebsite');

var currentURL;
var defaultHeight = document.body.offsetHeight;





var result = await loadWhitelist();
checkCurrentURL();




function checkCurrentURL() {
    chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
        currentURL = tabs[0].url;
        if (currentURL == undefined) {
            document.getElementById("lowerMenu").style.display = "none"
            lblCurrentDomain.textContent = "";
        } else {
            var currDomain = getDomain(currentURL);

            lblCurrentDomain.textContent = currDomain;
            if (getIgnore(currDomain) == 0) {
                btnAddToIgnoreList.style.color = "#bababa";

            } else {
                btnAddToIgnoreList.style.color = "green";
            }
            document.getElementById("lowerMenu").style.display = "inline";
        }
      });
}


function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

function goToWebsite() {
    parent.open('https://www.phishtales.net/');
}



function exitIgnoreList() {
    ignoreListMenu.style.display = "none";
    checkCurrentURL();
    mainMenu.style.display = "inline";
    console.log(defaultHeight);
    document.body.style.height = defaultHeight + 'px';
}

function addCurrentWebsite() {
    var currentlyAdded = getIgnore(getDomain(currentURL));
    updateIgnoreList(getDomain(currentURL), (currentlyAdded == 1) ? false : true);
    if (currentlyAdded == 1) {
        btnAddToIgnoreList.style.color = "#bababa";
    } else {
        btnAddToIgnoreList.style.color = "green";
    }
}


function showIgnoreList() {
    mainMenu.style.display = "none";

    removeAllChildNodes(ignoreListContainer);
    

    var domainWhitelist = getIgnoreList();
    for (let [key, value] of domainWhitelist) {
        (function() {
            console.log(key + ": " + value);

            var newItem = ignoreListItem.cloneNode();
    
            var lblWebsite = document.createElement("p");
            lblWebsite.className = 'leftfatext';
            lblWebsite.innerText = key;
    
            var btnDelete = document.createElement("button");
            btnDelete.className = 'fa-solid fa-trash fabutton';
    
            newItem.appendChild(lblWebsite);
            newItem.appendChild(btnDelete);
    
            newItem.style.display = "inline";
    
            btnDelete.addEventListener("click",
            function() {
                console.log("removing " + key);
                updateIgnoreList(key, false);
                newItem.remove();
            });
    
            ignoreListContainer.appendChild(newItem);
        }());
        
    }
    ignoreListMenu.style.display = "inline";
}









ignoreButton.addEventListener("click", showIgnoreList);
btnAddToIgnoreList.addEventListener("click", addCurrentWebsite);

btnExitIgnoreList.addEventListener("click", exitIgnoreList);

btnWebsite.addEventListener("click", goToWebsite)