import __init__ as pywing

# Rules given
focus_token = pywing.change(pywing.perform.FOR_ALL, pywing.result.FOCUS, pywing.result.HIT | pywing.result.EVADE)

# Moficications
modification_autothrusters = pywing.change(pywing.perform.ONCE, pywing.result.BLANK, pywing.result.EVADE)
modification_guidance_chips_two_attack = pywing.change(pywing.perform.ONCE, pywing.result.BLANK|pywing.result.FOCUS, pywing.result.HIT)
modification_guidance_chips_three_attack = pywing.change(pywing.perform.ONCE, pywing.result.BLANK|pywing.result.FOCUS, pywing.result.CRIT)

# Pilot abilities
ability_poe_focus = pywing.change(pywing.perform.ONCE, pywing.result.FOCUS, pywing.result.HIT | pywing.result.EVADE)

# Elite pilot talent
ept_wired = pywing.reroll(pywing.perform.ONCE, pywing.result.FOCUS)
ept_calculation = pywing.change(pywing.perform.ONCE, pywing.result.FOCUS, pywing.result.CRIT)

# Ordnance
ordnance_proton_torpedoes = pywing.change(pywing.perform.ONCE, pywing.result.FOCUS, pywing.result.CRIT)