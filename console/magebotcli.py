# MageBot CLI - Console version of MageBot
# Notes: When a duel starts, the system activates MageBot AI since CLI mode is against AI.

# Import necessary modules
import asyncio
import random
from colorama import Fore, Style, init as colorama_init

# Initialize Colorama for colored text in the terminal
colorama_init(autoreset=True)

# Valeurs globales (utilisées par l'heuristique)
MAX_HP = 20
MAX_MANA = 25


# ---- Gestion des fonctions du jeu ----

# Utility functions for readable duel display
def print_duel_state(player_hp, player_res, player_mana, magebot_hp, magebot_res, magebot_mana, player_effects=None, magebot_effects=None):
    print(f"\n{Fore.YELLOW}--- Duel State ---{Style.RESET_ALL}")
    effects_str = ""
    if player_effects:
        active_effects = [k for k, v in player_effects.items() if v > 0]
        if active_effects:
            effects_str += f" | Effects: {', '.join(active_effects)}"
    print(f"{Fore.GREEN}You      : {player_hp} HP | Resistance : {player_res} | Mana : {player_mana}{effects_str}{Style.RESET_ALL}")
    effects_str = ""
    # Display MageBot effects
    if magebot_effects:
        active_effects = [k for k, v in magebot_effects.items() if v > 0]
        if active_effects:
            effects_str += f" | Effects: {', '.join(active_effects)}"
    print(f"{Fore.MAGENTA}MageBot  : {magebot_hp} HP | Resistance : {magebot_res} | Mana : {magebot_mana}{effects_str}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}---------------------{Style.RESET_ALL}\n")
# Log actions during the duel
def print_action_log(actor, spell_name, spell, effect_value, target):
    if "damage" in spell:
        ascii = f"{Fore.RED}>>>>>" if actor == "You" else f"{Fore.MAGENTA}<<<<<"
        print(f"{ascii} {actor} casts {spell_name} (Attack) : {Fore.RED}{effect_value} magical damage dealt to {target} !{Style.RESET_ALL}")
    elif "healing" in spell:
        ascii = f"{Fore.GREEN}+++++"
        print(f"{ascii} {actor} casts {spell_name} (Healing) : {Fore.GREEN}{effect_value} HP restored.{Style.RESET_ALL}")
    elif "resistance_boost" in spell:
        ascii = f"{Fore.CYAN}====="
        print(f"{ascii} {actor} casts {spell_name} (Resistance) : {Fore.CYAN}Magical resistance +{effect_value} this turn.{Style.RESET_ALL}")


# Dictionary of spells in Latin (attack, healing, resistance)
attack_spells = {
    "Ignis": {"description": "Deals fire damage and may burn the enemy.", "damage": 3, "mana_cost": 3, "effect": "burn", "duration": 2, "chance": 0.6},
    "Glacies": {"description": "Deals ice damage and may freeze the enemy.", "damage": 4, "mana_cost": 2, "effect": "freeze", "duration": 1, "chance": 0.3},
    "Fulmen": {"description": "Deals lightning damage and may paralyze the enemy.", "damage": 2, "mana_cost": 2, "effect": "paralyze", "duration": 1, "chance": 0.4},
}
resistance_spells = {
    "Fortitudo": {"description": "Increases the caster's magical resistance.", "resistance_boost": 3, "mana_cost": 2},
    "Praesidium": {"description": "Temporary magical shield.", "resistance_boost": 2, "mana_cost": 1},
    "Tutela": {"description": "Light magical protection.", "resistance_boost": 1, "mana_cost": 1},
}
healing_spells = {
    "Vitalis": {"description": "Heals the caster's wounds.", "healing": 6, "mana_cost": 4},
    "Vitae": {"description": "Restores some of the caster's health.", "healing": 4, "mana_cost": 3},
    "Sanare": {"description": "Light healing.", "healing": 2, "mana_cost": 1},
}


# Heuristic evaluation function for Minimax
def evaluate_state(player_hp, player_res, player_mana, magebot_hp, magebot_res, magebot_mana,
                   w_hp=1.0, w_res=0.5, w_mana=0.4):
    # Positive score favors MageBot
    hp_score = (magebot_hp - player_hp) * w_hp
    res_score = (magebot_res - player_res) * w_res
    # Normalize mana between 0..1 and weight (multiplied by MAX_HP to keep similar scale)
    mana_score = ((magebot_mana - player_mana) / MAX_MANA) * w_mana * MAX_HP
    return hp_score + res_score + mana_score

# Minimax algorithm for MageBot's decision-making
def minimax(player_hp, player_res, player_mana, magebot_hp, magebot_res, magebot_mana, depth, maximizing):
    if player_hp <= 0:
        return 100  # MageBot wins
    if magebot_hp <= 0:
        return -100  # Player wins
    if depth == 0:
        return evaluate_state(player_hp, player_res, player_mana, magebot_hp, magebot_res, magebot_mana)
    # MageBot's turn (maximizing) or Player's turn (minimizing)
    if maximizing:
        max_eval = -float('inf')
        # MageBot plays: only consider spells it can afford
        for name, spell in all_spells.items():
            cost = spell.get("mana_cost", 0)
            if cost > magebot_mana:
                continue
            if "damage" in spell:
                dmg = max(0, spell["damage"] - player_res)
                eval = minimax(player_hp - dmg, 0, player_mana, magebot_hp, magebot_res, magebot_mana - cost, depth-1, False)
            elif "healing" in spell:
                new_hp = min(MAX_HP, magebot_hp + spell["healing"])
                eval = minimax(player_hp, player_res, player_mana, new_hp, magebot_res, magebot_mana - cost, depth-1, False)
            elif "resistance_boost" in spell:
                new_res = magebot_res + spell["resistance_boost"]
                eval = minimax(player_hp, player_res, player_mana, magebot_hp, new_res, magebot_mana - cost, depth-1, False)
            else:
                eval = evaluate_state(player_hp, player_res, player_mana, magebot_hp, magebot_res, magebot_mana)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        # Player plays: only consider spells they can afford
        for name, spell in all_spells.items():
            cost = spell.get("mana_cost", 0)
            if cost > player_mana:
                continue
            if "damage" in spell:
                dmg = max(0, spell["damage"] - magebot_res)
                eval = minimax(player_hp, player_res, player_mana - cost, magebot_hp - dmg, 0, magebot_mana, depth-1, True)
            elif "healing" in spell:
                new_hp = min(MAX_HP, player_hp + spell["healing"])
                eval = minimax(new_hp, player_res, player_mana - cost, magebot_hp, magebot_res, magebot_mana, depth-1, True)
            elif "resistance_boost" in spell:
                new_res = player_res + spell["resistance_boost"]
                eval = minimax(player_hp, new_res, player_mana - cost, magebot_hp, magebot_res, magebot_mana, depth-1, True)
            else:
                eval = evaluate_state(player_hp, player_res, player_mana, magebot_hp, magebot_res, magebot_mana)
            min_eval = min(min_eval, eval)
        return min_eval
# Spell choice by MageBot using Minimax
def magebot_choose_spell(player_hp, player_res, player_mana, magebot_hp, magebot_res, magebot_mana, magebot_max_hp, possible_spells):
    best_score = -float('inf')
    best_spell = None
    # Filter healing spells if MageBot is already at max HP
    filtered_spells = []
    for name in possible_spells:
        spell = all_spells[name]
        if "healing" in spell and magebot_hp >= magebot_max_hp:
            continue
        filtered_spells.append(name)
    # If all are filtered, fall back to original list
    if not filtered_spells:
        filtered_spells = possible_spells

    for name in filtered_spells:
        spell = all_spells[name]
        cost = spell.get("mana_cost", 0)
        if cost > magebot_mana:
            continue
        if "damage" in spell:
            dmg = max(0, spell["damage"] - player_res)
            score = minimax(player_hp - dmg, 0, player_mana, magebot_hp, magebot_res, magebot_mana - cost, 2, False)
        elif "healing" in spell:
            new_hp = min(MAX_HP, magebot_hp + spell["healing"])
            score = minimax(player_hp, player_res, player_mana, new_hp, magebot_res, magebot_mana - cost, 2, False)
        elif "resistance_boost" in spell:
            new_res = magebot_res + spell["resistance_boost"]
            score = minimax(player_hp, player_res, player_mana, magebot_hp, new_res, magebot_mana - cost, 2, False)
        else:
            score = evaluate_state(player_hp, player_res, player_mana, magebot_hp, magebot_res, magebot_mana)
        if score > best_score:
            best_score = score
            best_spell = name
    return best_spell

async def activate_magebot_ai(): # Activates an LLM and not a simulation. (To be updated in future versions)
    print("MageBot AI: activated.")
    await asyncio.sleep(1)  # Simulate an asynchronous operation

# Merge all spells into a single dictionary
all_spells = {}
all_spells.update(attack_spells)
all_spells.update(resistance_spells)
all_spells.update(healing_spells)

def print_spells_ui():
    print("\n=== Available Spells ===")
    print("\n[Attack Spells]")
    for name, spell in attack_spells.items():
        effect_str = ""
        if "effect" in spell:
            effect_str = f" | Effect: {spell['effect']} ({spell['chance']*100:.0f}% chance, {spell['duration']} turn(s))"
        print(f"  {name} : {spell['description']} (Damage : {spell['damage']}, Mana : {spell['mana_cost']}){effect_str}")
    print("\n[Healing Spells]")
    for name, spell in healing_spells.items():
        print(f"  {name} : {spell['description']} (Healing : {spell['healing']}, Mana : {spell['mana_cost']})")
    print("\n[Resistance Spells]")
    for name, spell in resistance_spells.items():
        print(f"  {name} : {spell['description']} (Resistance : +{spell['resistance_boost']}, Mana : {spell['mana_cost']})")
    print("========================\n")

async def duel_vs_magebot():
    await activate_magebot_ai()
    print("The duel begins!")
    player_hp = 10
    player_res = 5
    player_mana = 15
    player_max_hp = 20
    player_max_mana = 25
    magebot_hp = 10
    magebot_res = 5
    magebot_mana = 15
    magebot_max_hp = 20
    magebot_max_mana = 25
    player_effects = {"frozen": 0, "paralyzed": 0, "burned": 0}
    magebot_effects = {"frozen": 0, "paralyzed": 0, "burned": 0}

    while player_hp > 0 and magebot_hp > 0:
        print_duel_state(player_hp, player_res, player_mana, magebot_hp, magebot_res, magebot_mana, player_effects, magebot_effects)
        print_spells_ui()
        print(f"{Fore.CYAN}=== Your Turn ==={Style.RESET_ALL}")

        # Apply player effects
        if player_effects["burned"] > 0:
            burn_damage = 1
            player_hp -= burn_damage
            print(f"{Fore.RED}[Burn] You take {burn_damage} burn damage!{Style.RESET_ALL}")
            player_effects["burned"] -= 1
        if player_effects["frozen"] > 0 or player_effects["paralyzed"] > 0:
            effect_name = "frozen" if player_effects["frozen"] > 0 else "paralyzed"
            print(f"{Fore.BLUE}[Effect] You are {effect_name} and skip your turn!{Style.RESET_ALL}")
            player_effects["frozen"] = max(0, player_effects["frozen"] - 1)
            player_effects["paralyzed"] = max(0, player_effects["paralyzed"] - 1)
            # Skip to mana regen
        else:
            action = input("Your turn! Type a spell name: ").strip()
            if action in all_spells:
                spell = all_spells[action]
                mana_cost = spell.get("mana_cost", 0)
                if player_mana < mana_cost:
                    print(f"{Fore.RED}[Error] Not enough mana to cast {action}! Required mana: {mana_cost}, Current mana: {player_mana}{Style.RESET_ALL}")
                else:
                    player_mana -= mana_cost
                    if "damage" in spell:
                        # Special message if enemy resistance is broken
                        if magebot_res > 0 and spell["damage"] >= magebot_res:
                            print(f"{Fore.YELLOW}[Info] Enemy resistance broken! (RES:0){Style.RESET_ALL}")
                        dmg = max(0, spell["damage"] - magebot_res)
                        magebot_hp -= dmg
                        print_action_log("You", action, spell, dmg, "MageBot")
                        magebot_res = 0
                        # Apply effect if present
                        if "effect" in spell and random.random() < spell["chance"]:
                            magebot_effects[spell["effect"]] = spell["duration"]
                            print(f"{Fore.YELLOW}[Effect] MageBot is now {spell['effect']} for {spell['duration']} turn(s)!{Style.RESET_ALL}")
                    elif "healing" in spell:
                        player_hp += spell["healing"]
                        if player_hp > player_max_hp:
                            player_hp = player_max_hp
                            print(f"{Fore.GREEN}[Info] You have reached your maximum HP!{Style.RESET_ALL}")
                        print_action_log("You", action, spell, spell["healing"], "You")
                    elif "resistance_boost" in spell:
                        player_res += spell["resistance_boost"]
                        print_action_log("You", action, spell, spell["resistance_boost"], "You")
            else:
                print(f"{Fore.RED}Unknown spell. Turn lost.{Style.RESET_ALL}")

        # Player mana regeneration
        regen = 2
        if player_mana < player_max_mana:
            player_mana += regen
            if player_mana > player_max_mana:
                player_mana = player_max_mana
            print(f"{Fore.BLUE}[Mana] You recover {regen} mana. (Mana: {player_mana}/{player_max_mana}){Style.RESET_ALL}")

        if magebot_hp <= 0:
            print_duel_state(player_hp, player_res, player_mana, magebot_hp, magebot_res, magebot_mana, player_effects, magebot_effects)
            print(f"{Fore.GREEN}Congratulations, you defeated MageBot!{Style.RESET_ALL}")
            break

        # MageBot plays with Minimax
        await asyncio.sleep(1)
        print(f"{Fore.MAGENTA}=== MageBot's Turn ==={Style.RESET_ALL}")

        # Apply magebot effects
        if magebot_effects["burned"] > 0:
            burn_damage = 1
            magebot_hp -= burn_damage
            print(f"{Fore.RED}[Burn] MageBot takes {burn_damage} burn damage!{Style.RESET_ALL}")
            magebot_effects["burned"] -= 1
        if magebot_effects["frozen"] > 0 or magebot_effects["paralyzed"] > 0:
            effect_name = "frozen" if magebot_effects["frozen"] > 0 else "paralyzed"
            print(f"{Fore.BLUE}[Effect] MageBot is {effect_name} and skips its turn!{Style.RESET_ALL}")
            magebot_effects["frozen"] = max(0, magebot_effects["frozen"] - 1)
            magebot_effects["paralyzed"] = max(0, magebot_effects["paralyzed"] - 1)
            # Skip to mana regen
        else:
            # MageBot chooses a spell it can afford
            magebot_possible_spells = [name for name, s in all_spells.items() if s.get("mana_cost", 0) <= magebot_mana]
            if not magebot_possible_spells:
                print(f"{Fore.MAGENTA}MageBot doesn't have enough mana to cast a spell! It passes its turn...{Style.RESET_ALL}")
                magebot_mana += 2
                if magebot_mana > magebot_max_mana:
                    magebot_mana = magebot_max_mana
                print(f"{Fore.MAGENTA}[Mana] MageBot recovers 2 mana. (Mana: {magebot_mana}/{magebot_max_mana}){Style.RESET_ALL}")
            else:
                magebot_action = magebot_choose_spell(player_hp, player_res, player_mana, magebot_hp, magebot_res, magebot_mana, magebot_max_hp, magebot_possible_spells)
                spell = all_spells[magebot_action]
                mana_cost = spell.get("mana_cost", 0)
                magebot_mana -= mana_cost
                # MageBot dialogue
                # MageBot no longer has random comments, everything is deterministic
                print(f"{Fore.MAGENTA}[MageBot] MageBot acts deterministically.{Style.RESET_ALL}")
                if "damage" in spell:
                    if player_res > 0 and spell["damage"] >= player_res:
                        print(f"{Fore.YELLOW}[Info] Your resistance is broken! (RES:0){Style.RESET_ALL}")
                    dmg = max(0, spell["damage"] - player_res)
                    player_hp -= dmg
                    print_action_log("MageBot", magebot_action, spell, dmg, "You")
                    player_res = 0
                    # Apply effect if present
                    if "effect" in spell and random.random() < spell["chance"]:
                        player_effects[spell["effect"]] = spell["duration"]
                        print(f"{Fore.YELLOW}[Effect] You are now {spell['effect']} for {spell['duration']} turn(s)!{Style.RESET_ALL}")
                elif "healing" in spell:
                    magebot_hp += spell["healing"]
                    if magebot_hp > magebot_max_hp:
                        magebot_hp = magebot_max_hp
                        print(f"{Fore.GREEN}[Info] MageBot has reached its maximum HP!{Style.RESET_ALL}")
                    print_action_log("MageBot", magebot_action, spell, spell["healing"], "MageBot")
                elif "resistance_boost" in spell:
                    magebot_res += spell["resistance_boost"]
                    print_action_log("MageBot", magebot_action, spell, spell["resistance_boost"], "MageBot")

        # MageBot mana regeneration
        if magebot_mana < magebot_max_mana:
            magebot_mana += regen
            if magebot_mana > magebot_max_mana:
                magebot_mana = magebot_max_mana
            print(f"{Fore.MAGENTA}[Mana] MageBot recovers {regen} mana. (Mana: {magebot_mana}/{magebot_max_mana}){Style.RESET_ALL}")

        if player_hp <= 0:
            print_duel_state(player_hp, player_res, player_mana, magebot_hp, magebot_res, magebot_mana, player_effects, magebot_effects)
            print(f"{Fore.RED}You lost against MageBot...{Style.RESET_ALL}")
            break

# Duel startup function

def main():
    try:
        asyncio.run(init())
    except KeyboardInterrupt:
        print("\nClosing MageBot CLI.")

async def init():
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}███╗   ███╗ █████╗  ██████╗ ███████╗    ██████╗  ██████╗ ████████╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}████╗ ████║██╔══██╗██╔════╝ ██╔════╝    ██╔══██╗██╔═══██╗╚══██╔══╝{Style.RESET_ALL}")
    print(f"{Fore.CYAN}██╔████╔██║███████║██║  ███╗█████╗      ██████╔╝██║   ██║   ██║   {Style.RESET_ALL}")
    print(f"{Fore.CYAN}██║╚██╔╝██║██╔══██║██║   ██║██╔══╝      ██╔══██╗██║   ██║   ██║   {Style.RESET_ALL}")
    print(f"{Fore.CYAN}██║ ╚═╝ ██║██║  ██║╚██████╔╝███████╗    ██████╔╝╚██████╔╝   ██║   {Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝    ╚═════╝  ╚═════╝    ╚═╝   {Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Welcome to MageBot CLI{Style.RESET_ALL}")
    print("Type 'help' to see available commands.")
    print(f'Version: 1.1.7')
    while True:
        print(f"{Fore.YELLOW}{'='*40}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}MageBot CLI - Main Menu{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'='*40}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1.{Style.RESET_ALL} Help")
        print(f"{Fore.GREEN}2.{Style.RESET_ALL} About")
        print(f"{Fore.GREEN}3.{Style.RESET_ALL} Start Duel")
        print(f"{Fore.GREEN}4.{Style.RESET_ALL} Exit")
        print(f"{Fore.YELLOW}{'-'*40}{Style.RESET_ALL}")
        command = input(f"{Fore.CYAN}Select an option (1-4): {Style.RESET_ALL}").strip()
        if command == "1" or command.lower() == "help":
            print(f"{Fore.YELLOW}Available commands: help, about, start_dual, exit{Style.RESET_ALL}")
        elif command == "2" or command.lower() == "about":
            print(f"{Fore.MAGENTA}About MageBot:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Created by the ZIOS team.{Style.RESET_ALL}")
            print(f"{Fore.CYAN}MageBot is a console-based magical duel game where you face an AI using various spells.{Style.RESET_ALL}")
            print(f"{Fore.CYAN}The goal is to defeat MageBot by reducing its HP to 0 while managing your own resources (HP, Resistance, Mana).{Style.RESET_ALL}")
        elif command == "3" or command.lower() == "start_dual":
            print(f"{Fore.YELLOW}Starting duel mode...{Style.RESET_ALL}")
            await asyncio.sleep(2)
            print(f"{Fore.YELLOW}You are about to face MageBot AI! Prepare for battle!{Style.RESET_ALL}")
            await duel_vs_magebot()
        elif command == "4" or command.lower() == "exit":
            print(f"{Fore.YELLOW}Closing MageBot CLI.{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Unknown command: {command}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
