from _class.Player import *
from _class.Game import *
from _class.Daft import *
from RiotAPI import *
from DataAnalyse import *
from AddSupabase import *

#game1 = GameEnd(6317145488)
game1 = Game(6300818823,teamBlue='Bluereal',teamRed='BDS',win='B')

add_value_supabase(game1)