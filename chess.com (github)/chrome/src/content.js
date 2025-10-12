/* --  Initialisation  --*/
let movesList = [];

let adPlace = document.getElementById("board-layout-ad");
  adPlace.innerHTML = "<div id='suggestbox'><span id='bestmove_n'>Best Move</span><br><span id='bestmove_v'></span></div>";
  let bestmovebox = document.getElementById("bestmove_v");

  let infoBox = document.createElement("div");
  infoBox.id = "infobox";

    let mystatus = document.createElement("div");
    mystatus.id = "mystatus";
    mystatus.innerText = "Stopped..";

    let mybtn = document.createElement("button");
    mybtn.id = "mybtn";
    mybtn.innerText = "Start";

    let resetGameBtn = document.createElement("button");
    resetGameBtn.id = "myresetGameBtn";
    resetGameBtn.innerHTML = "Reset Game Data";
    resetGameBtn.onclick = (event) => { sendToServer("ResetGame: "); }

    let myServerEle = document.createElement("div");
    myServerEle.id = "myServerEle";
        let myServerInfo = document.createElement("span");
        myServerInfo.id = "myServerInfoEle";
        myServerInfo.innerHTML = "&#x1F600;" //😀

            function myServerInfoErrorLog(errorMessage, onClick_callback){
              myServerInfo.innerHTML = "&#x1F608;" //😈
              myServerInfo.setAttribute("title", errorMessage + "\n" + "Click to take action.");
              myServerInfo.onclick = onClick_callback;
            }
            function myServerInfoErrorReset(){
              myServerInfo.innerHTML = "&#x1F600;" //😀
              myServerInfo.setAttribute("title", "Connected to Server");
              myServerInfo.onclick = null;
            }

        let myServerInput = document.createElement("input");
        myServerInput.value = WS_SERVER_URL;
        myServerInput.onchange = (event) => { WS_SERVER_URL = event.target.value; }

      myServerEle.appendChild(myServerInfo);
      myServerEle.appendChild(myServerInput);


    infoBox.appendChild(mystatus);
    infoBox.appendChild(mybtn);
    infoBox.appendChild(resetGameBtn);
    infoBox.appendChild(myServerEle);


  adPlace.appendChild(infoBox);


mybtn.onclick = () => {
  if(mystatus.innerText === "Stopped.."){
    main("start");
    mybtn.innerText = "Stop";
    mystatus.innerText = "Running..";
  }
  else if(mystatus.innerText === "Running.."){
    main("stop");
    mybtn.innerText = "Start";
    mystatus.innerText = "Stopped..";
  }
}

let pieces;
const observer = new MutationObserver(callbackListner);
const mutationConfig = {
  attributes: true,
  attributeFilter: ["class"],
  attributeOldValue: true
}
function main(ok){
  if(ok==="start"){
    pieces = getPieceObjects();
    //Set the listner for every object with class "piece" to track their location
    for(let i=0; i<pieces.length; i++){
      observer.observe(pieces[i], mutationConfig);
    }
  }
  else if(ok==="stop"){
    observer.disconnect();
  }
}


/**Message Passing */
// chrome.runtime.onConnect.addListener(function(port) {
//   console.assert(port.name === "knockknock");
//   port.onMessage.addListener(function(msg) {
//     if(msg.action === "start" || msg.action === "stop"){
//       console.log("Received Action: ",msg.action);
//       main(msg.action);
//       port.postMessage({status: msg.action==="start" ? "running" : "stopped"});
//     }
//   });
// });

// let port;
// chrome.tabs.query( {active : true}, main);

// function main(tabsList){
//   currentTab = tabsList[0];
//   port = chrome.tabs.connect(currentTab.id, {name: "knockknock"});
//   port.onMessage.addListener(function(msg) {
//     if(msg.status==="running" || msg.status==="stopped"){
//       console.log("Status: ", msg.status);
//       statusEl.innerText = msg.status;
//     }
//   });
// }

