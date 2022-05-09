import buscador
import indexador
import processador
from datetime import datetime

now = datetime.now()
if __name__ == "__main__":
  print('O programa está sendo executado ás ',now)
  indexador()
  buscador()
