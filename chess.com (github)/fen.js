let nullcount;


FEN_STRING = "";

//RANKS 8 -> 1
for(let i=8; i>=1; i--){
  nullcount = 0;
  //FILES a -> h
  for(let j=1; j<=8; j++){
    let className = ".piece.square-" + j.toString() + i.toString();
    let squareji = document.querySelector(className);

    //NO PIECE FOUND
    if(squareji === null){ nullcount += 1; }
    else{ //PIECE FOUND
      //IF EMPTY PIECE BEFORE : APPEND
      if(nullcount!==0){ FEN_STRING += nullcount.toString(); }
      //MAKE IT ZERO
      nullcount = 0;

      let pieceName;
      squareji.classList.forEach( element => { if(element.length === 2){ pieceName = element; return;} });

      if(pieceName[0]==="w"){ FEN_STRING += pieceName[1].toUpperCase(); }
      else if(pieceName[0]==="b"){ FEN_STRING += pieceName[1]; }
    }
  }
  if(nullcount!==0){FEN_STRING += nullcount.toString(); }
  FEN_STRING += "/";
}

FEN_STRING += " ";

//TO MOVE "w" | "b"
FEN_STRING += "w";

FEN_STRING += " ";

//CASTLING "KQkq" | "-"
FEN_STRING += "KQkq";

FEN_STRING += " ";

//ENPASSANT MOVE <algebraic-location> | "-"
FEN_STRING += "-";

FEN_STRING += " ";

//HALFMOVE CLOCK
FEN_STRING += "0";

FEN_STRING += " ";

//FULLMOVE NUMBER ∈ [1,∞)
FEN_STRING += "1";

console.log(FEN_STRING);