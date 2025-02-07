### Process
- `Attacker` attacks `Target` with a `Weapon` ability
- See if `Attacker` hits `Target` (Accuracy vs Dodge)
- If the `Attacker` hits `Target`:
	- `Attacker` calculates `Weapon` Damage:
	  `weapon_damage = attacker.calculate_base_damage()`
		- This asks `Weapon` for damage scaling based on `Attacker`
		  `weapon_damage = attacker.equipment[WEAPON].get_damage(attacker)`
		- We take that `Weapon` damage, and run it through each effect on `Attacker`
		  `for e in attacker.effects: see if e affects damage`
		- Then we return result
	- We calculate how much damage `Target` should take from this
	  `damage = attacker.calculate_total_damage(target, weapon_damage)`
		- This checks the `Target` resistances
		- This also runs through each effect on `Target` to see if it should take bonus damage
	- Then we need to calculate the actual damage and type
	  `result, type = random.randint(damage.min, damage.max), damage.type`
	- Then `Attacker` deals that damage to `Target`
	  `target.take_damage(result, type)`
		- This checks to see if `Target` dies
