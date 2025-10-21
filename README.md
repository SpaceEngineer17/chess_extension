# chess_extension
A Browser extension for chess.com.

# Disclaimer
This entire project done for the purpose of challenge and education.
Not for the purpose of cheating.

*⚠ USE AT YOUR OWN RISK. YOUR ACCOUNT WILL GET BANNED IF CHEATED ON REAL PLAYERS WHICH VIOLATES CHESS.COM's FAIR PLAY POLICY. ⚠*

# Usage
Download the Source.
--------------------
 - ```git clone URL```

Load the Extension in Browser.
------------------------------
> Chrome
 - GOTO `chrome://extensions` (Type in URL bar)
 - SELECT `Load Unpacked` and OPEN the `manifest.json` file (`chess.com (github)/chrome/manifest.json`)

> Firefox:
 - GOTO `about:debugging` (Type in URL bar) and then CLICK `This Firefox`
 - CLICK `Load Temporary Add-On`
 - OPEN the `manifest.json` file

Start the Server and Connect.
-----------------------------
 - `cd 'chess.com (github)/engine'`
 - `python server.py`

Using the Extension.
--------------------
- The Extension loads when you go to `chess.com/play/computer`
- Next, you need to Connect to the Server from Extension's `Connection Info Element`
   - 😈 == Connection is Down...
   - Click on it.
   - 😀 == Connection is connected on the connection channel so that the connector can communicate to the other connecting side.
- Click `Start`
- It will show the next best move for both armies.

 Tips:
   > On First Run of Extension, Clicking 😈 won't change to 😀, as connection if failed to establish. <br>
   To solve this, visit "https://localhost:9999" once and procede to `Trust the Certificate` as this makes your browser trust the
   self-signed certs and is is necessary to establish as secure websocket connection
   Now 😈 onclick --> 😀.
   Citations: Since we are running on a HTTPS website, we cannot use HTTP for websockets as of [this](https://stackoverflow.com/a/50861413/31419782) and hence forced to      use Secure WebSockets.

   But note it can work with HTTP WebSocket in FireFox, all you need to do change is one line in `server.py`.

# Credits
 - [WebSocket Server](https://github.com/Pithikos/python-websocket-server.git)
 - [Python](https://www.python.org/)
 - [Stockfish](https://github.com/official-stockfish/Stockfish.git)
 - All opensource softwares and developers.
