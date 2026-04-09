import mlbstatsapi
import json
json_name = 'player_data.json'
mlb = mlbstatsapi.Mlb()
# grabbing player names
player_names = ["Mike Trout", "Freddie Freeman","Shohei Ohtani", "Mookie Betts"]
data_for_stan = {"N": len(player_names), "y": [], "K": []}

for name in player_names:
    # 1. Get Player ID
    ids = mlb.get_people_id(name)
    if ids:
        p_id = ids[0]
        # 2. Get 2025 Season Stats
        stats = mlb.get_player_stats(p_id, stats=['season'], groups=['hitting'],season=2025)
        
        # 3. Extract H and AB
        hitting_stats = stats['hitting']['season'].splits[0].stat
        data_for_stan["y"].append(hitting_stats.hits)
        data_for_stan["K"].append(hitting_stats.at_bats)

# Save as JSON for your Stan terminal command
print("Saving player data to ", json_name)
with open(json_name, 'w') as f:
    json.dump(data_for_stan, f)

