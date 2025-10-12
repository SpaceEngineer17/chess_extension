import subprocess

class Engine:
  def __init__(self, engine_path):
    self.engine = subprocess.Popen(
                    [engine_path],
                    stdin = subprocess.PIPE,
                    stdout = subprocess.PIPE,
                    stderr = subprocess.STDOUT
                  )

    self._STDOUT_DELIMETERS = {
      "go" : "bestmove",
      "isready" : "readyok",
      "uci" : "uciok",
      "position" : 0,
      "d" : "Checkers:"
      #for 'setoptions ' use function params
    }
    self.moves = {0 : []}

    ## CREATED FROM STDOUT(stockfish < uci) manually 😂 ##
    ## Create from data( self._readEngineParameters() )
    self._ENGINE_PARAMETERS = {
      # 'Clear Hash': { 'type' : 'button'},
      'Debug Log File'   : { 'type' : 'string', 'default' : '<empty>'              },
      'EvalFile'         : { 'type' : 'string', 'default' : 'nn-1c0000000000.nnue' },
      'EvalFileSmall'    : { 'type' : 'string', 'default' : 'nn-37f18f62d772.nnue' },
      'NumaPolicy'       : { 'type' : 'string', 'default' : 'auto'                 },
      'SyzygyPath'       : { 'type' : 'string', 'default' : '<empty>'              },

      'Hash'             : { 'type' : 'spin', 'default' : 16,   'min': 1,     'max' : 33554432  },
      'Move Overhead'    : { 'type' : 'spin', 'default' : 10,   'min': 0,     'max' : 5000      },
      'MultiPV'          : { 'type' : 'spin', 'default' : 1,   'min': 1,     'max' : 256        },
      'Skill Level'      : { 'type' : 'spin', 'default' : 20,   'min': 0,     'max' : 20        },
      'SyzygyProbeDepth' : { 'type' : 'spin', 'default' : 1,   'min': 1,     'max' : 100        },
      'SyzygyProbeLimit' : { 'type' : 'spin', 'default' : 7,    'min': 0,     'max' : 7         },
      'Threads'          : { 'type' : 'spin', 'default' : 1,    'min': 1,     'max' : 1024      },
      'UCI_Elo'          : { 'type' : 'spin', 'default' : 1320, 'min' : 1320, 'max' : 3190      },
      'nodestime'        : { 'type' : 'spin', 'default' : 0,    'min': 0,     'max' : 10000     },

      'Ponder'           : { 'type' : 'check', 'default' : 'false' },
      'Syzygy50MoveRule' : { 'type' : 'check', 'default' : 'true'  },
      'UCI_Chess960'     : { 'type' : 'check', 'default' : 'false' },
      'UCI_LimitStrength': { 'type' : 'check', 'default' : 'false' },
      'UCI_ShowWDL'      : { 'type' : 'check', 'default' : 'false' }
    }

  def getEngineParamater(self, optionName):
    return self._ENGINE_PARAMETERS.get(optionName)

  def getEngineParameters(self):
    ret = {}
    for k,v in self._ENGINE_PARAMETERS.items():
      ret[k] = v.get('current_value', v.get('default'))
    return ret

  def setEngineParameter(self, optionName, value):
    if not optionName in self._ENGINE_PARAMETERS:
      raise KeyError("Unknown Engine Parameter: " + optionName)

    engineParam = self._ENGINE_PARAMETERS[optionName]
    if engineParam['type'] == 'string':
      pass

    elif engineParam['type'] == 'spin':
      if not engineParam['min'] <= value <= engineParam['max']:
        raise ValueError(f"{optionName} must be between {engineParam['min']} and {engineParam['max']}")

    elif engineParam['type'] == 'check':
      pass

    self._ENGINE_PARAMETERS[optionName]['current_value'] = value # if verified but no way to!

    return self._writeEngineParameter(optionName, value)


  def setEngineParameters(self, options: dict) -> str:
    """
    Update Engine Parameters.
    Returns the output(aka `stdout`).
    """
    out = ""
    for k,v in options.items():
      try:
        ret = self.setEngineParameter(k, v)
        out += f'{k} : {v} : {ret}\n'
      except KeyError as err:
        print(err)

    return out #use Logger

  def _readEngineParameters(self):
    return self.command("uci")

  def _writeEngineParameter(self, optionName, value):
    """
    Writes uci `setoption` command to STDIN and returns expected output.
    """
    cmd = "setoption name %s value %s" % (optionName, value)
    breaker = None
    linecount = None

    if optionName == "Threads": breaker = "info string"
    elif optionName == "NumaPolicy": breaker = "binding"

    #self.verifyEngineParameters()
    return self.command(cmd, breaker=breaker, linecount=linecount) #Write to STDIN


  ## STANDARD I/O Functions - read(), write() ##
  def read(self):
    return self.engine.stdout.readline().decode("utf-8")

  def write(self, data):
    self.engine.stdin.write(data.encode("utf-8") + b"\n")
    self.engine.stdin.flush()


  ## HIGH-LEVEL STANDARD I/O Functions - get_output(), command() ##
  def get_output(self, breaker=None, linecount=None):
    data = []
    if breaker!=None:
      while True:
        buff = self.read()
        data.append(buff)
        if breaker in buff:
          break
      return data

    elif linecount!=None:
      c = 0
      while c<linecount:
        buff = self.read()
        data.append(buff)
        c += 1
      return data

  def command(self, inpu: str, breaker: str=None, linecount: int=None) -> list:
    if breaker==None and linecount==None:
      for k,v in self._STDOUT_DELIMETERS.items():
        if k in inpu:
          if(isinstance(v, str)):
            breaker = v
            break
          elif(isinstance(v, int)):
            linecount = v
            break

    self.write(inpu)
    return self.get_output(breaker=breaker, linecount=linecount)

  ## ENGINE CHESS functions ##
  # USER-LEVEL   - addMove(), addMoves(), getMoves(), getMove(), resetMoves()
  # ENGINE-LEVEL - setPosition(), go()

  def addMove(self, move: str, gameid: int=0):
    self.moves[gameid].append(move)

  def addMoves(self, moves: list | str, gameid=0):
    if isinstance(moves, str):
      moves = moves.split(" ")
    self.moves[gameid].extend(moves)

  def getMoves(self, gameid=0):
    return self.moves[gameid]

  def getMove(self, index, gameid=0):
    return self.moves[gameid][index]

  def resetMoves(self, gameid=0):
    self.moves[gameid] = []

  def setPosition(self, movesList=None, fen=None):
    """
    Set the position data for the engine. \n
    `movesList` = None <==> `self.moves[0]`. \n
    Uses `fen` if given.
    """
    if movesList==None:
      movesList = self.moves[0]
      self.command("position startpos moves " + " ".join(movesList))
    elif fen:
      self.command("position fen " + fen)

  def go(self, str):
    out = self.command(f"go {str}")
    return out



if __name__ == "__main__":
  fish = Engine("/usr/local/games/stockfish")
  print(fish.read())
  print(fish.setEngineParameters({"Threads" : 16, "Hash" : 256, "UCI_Elo": 3190}))
  fish.addMoves("e2e4 e7e5 a2a4")
  fish.setPosition()
  bestmove = fish.go("movetime 5000")[-1].split(" ")[1]
  print(bestmove)


"""
PROTIP: Add doc strings everywhere.
"""
