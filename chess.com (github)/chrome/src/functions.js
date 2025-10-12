const names = {
  "c" : {  'w' : "White", 'b' : "Black"},

  'r' : "Rook",
  'n' : "Knight",
  'b' : "Bishop",
  'q' : "Queen",
  'k' : "King",
  'p' : "Pawn"
}
function map_name(move){
  return names["c"][move[0]] + " " + names[move[1]];
}

//TODO: Optimise with predefined map of all 64 locations for both map & reverse map and names too.
//to reduce function calling??
let map = { 1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'};
let mapInverted = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8};
function map_location(pos){
  return map[Number(pos[0])] + pos[1];
}
function map_locationInverted(pos){
  return mapInverted[pos[0]] + pos[1];
}

/**
 * Return a list of HTML Element's of Chess Pieces (class 'piece')
 */
function getPieceObjects() {
    return document.getElementsByClassName("piece");
}


/**
 * @param {String} className
 * @returns [ Location, Name ]
 */
function getPieceData(className){
  if(className.includes("element-pool")){
    return ["Void Space","Eliminated"];
  }
  let pieceLocation = "";
  let pieceName = "";
  // CLASS LIST WONT BE IN ORDER (sometimes) "piece wp square-42"
  // but after a pawn promotion "piece square-48 wq" //piece name is appended at last of list by chess.com scripts.
  //so use for loop
  let classList = className.split(" ");
  for(let i=0; i<classList.length; i++){
    if (classList[i].includes("square-")) { pieceLocation = classList[i].split("square-")[1]; }
    else if(classList[i].length == 2) { pieceName = classList[i]; }
  }
  pieceLocation = map_location(pieceLocation);
  pieceName = pieceName; //= map_name(pieceName); //Keep int short for fast Checking in onPieceMoved().

  return [pieceLocation, pieceName];
}


// MutationObserver Listner function for pieces.
function callbackListner(mutationList) {
  for(const mutation of mutationList){
    if(mutation.type === 'attributes' && mutation.attributeName === "class"){
      // mutation.target is the DOM HtmlElement
      if(
          ( mutation.oldValue.includes("square-") && !mutation.oldValue.includes("dragging") )
          &&
          ( ( mutation.target.className.includes("square-") && !mutation.target.className.includes("dragging") )
          || mutation.target.className.includes("element-pool") )
        ){
        let oldData = getPieceData(mutation.oldValue);
        let newData = getPieceData(mutation.target.className);

        if(oldData[0] === newData[0]){ continue; } //SAME PIECE after dragging } <--😂
        onPieceMoved(oldData, newData);
      }
    }
  }
}

function onPieceMoved(oldPieceData, newPieceData){
  // pieceData = [loc, name]
  move = oldPieceData[0]+newPieceData[0];
  if(newPieceData[0] === "Void Space"){ return; }
  //THE TRANSFORMATION 🔥
  else if(oldPieceData[1][1] == "p" && newPieceData[1][1]!="p"){
    move += newPieceData[1][1];
    console.log("Promotion: ",move);
  }
  else if ( //CASTLING
    (move === "h1f1" && movesList.at(-1) == "e1g1") ||
    (move === "a1d1" && movesList.at(-1) === "e1c1") ||
    (move === "h8f8" && movesList.at(-1) === "e8g8" ) ||
    (move === "a8d8" && movesList.at(-1) === "e8c8")
  ){ return; }

  movesList.push(move);
  console.log("Piece Moved: ", move);
  sendToServer("Move: " + move);
}

/* -- CONNECTION MANAGER -- */
function sendToServer(message){
  if(ws.readyState === ws.OPEN){ ws.send(message); }
  else{ wsErrorReconnect("Server Disconnected."); };
}

/* --- Initialisation --- */
  /* --- WebSockets --- */
let WS_SERVER_URL = "wss://localhost:9999"
let ws = new WebSocket(WS_SERVER_URL);
wsConfigureListners(ws);

function wsConfigureListners(websocket){
  websocket.onerror = (event) => { wsErrorReconnect("Can't connect to Server."); }
  websocket.onopen = (event) => { console.info("WebSocket initiated.", event.data);}
  websocket.onmessage = (event) => {
    if (event.data.includes("BestMove: ") ){
      let bestmove = event.data.split("BestMove: ")[1];
      bestmovebox.innerText = bestmove;
    }
    else if(event.data.includes("ping")){
      sendToServer("pong");
    }
  }
}

/**
 * Ask user input for creating a `new WebSocket` using `myServerInfoErrorLog`.
*/
function wsErrorReconnect(userMsg){
  myServerInfoErrorLog( userMsg,
    () => {
      ws = new WebSocket(WS_SERVER_URL);
      wsConfigureListners(ws);
      myServerInfoErrorReset();
  });
}

