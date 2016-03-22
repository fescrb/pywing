# pywing

This library serves as a quick and easy way to calculate, compare and 
plot dice probabilities in the X-Wing Miniatures game. It is designed to
be used with the python interactive shell. It is flexible enough to 
describe all existing dice modification rules. Hopefully all future ones
too.

The main way to interact with this code is via the **get_hit_chances**
and **get_evade_chances** function. Both of these return an array of 
decimals which reflect the chances of obtaining the number of results 
equal to its index. 

For example:

```
>>> import pywing
>>> pywing.get_hit_chances(3)
array([ 0.124265,  0.3749  ,  0.37552 ,  0.125315,  0.      ,  0.      ,  0.      ,  0.      ])
```

This array tells us that rolling 3 unmodified attack dice has a ~12% 
chance of returning 0 hit results, ~37% chance of resulting in 1 hit and
etcetera. These are not exact results (we have exactly the same chance 
of rolling 1 or 2 hits). This is because the library simulates many dice 
rolls and gets the statistics from those. This means that the same 
function run twice does not return the same exact numbers. However they 
should be accurate to 2 decimal places. 

Pywing provides functions to compare and plot these probabilities. Below
their usage is exemplified with increasingly complex examples.

## Going over concrete examples

### Should I boost into range 1 with my T-70 X-Wing, target lock or 
focus agaisnt my oponent's tokenless TIE Bomber?

Let's begin with the easy stuff. Our opponent's evade chances. No 
variables, no dice modifications.

```
>>> import pywing
>>> bomber_evade_chances = pywing.get_evade_chances(2)
```

Now we'd like to compare that with our unmodified range 1 shot. To start
with, we store the probabilities.

```
>>> xwing_range_one_attack  = pywing.get_hit_chances(4)
```

We can already try and evaluate these chances somewhat. The function 
**average_chance** returns the average result from an array of chances:

```
>>> pywing.average_chance(bomber_evade_chances)
0.75014999999999998
>>> pywing.average_chance(xwing_range_one_attack)
1.9959449999999999
```

Comparing these two doesn't help much, however. This is because rolling 
two evades against the X-Wing's zero hits will not recover hull. A 
function is provided to properly compare hits vs evades, cleverly called 
**hits_vs_evade**:

```
>>> range_one_vs_bomber = pywing.hits_vs_evades(xwing_range_one_attack,bomber_evade_chances)
>>> range_one_vs_bomber
[0.2688081753999999, 0.30879635650000004, 0.27180276515000001, 0.12639285575, 0.024199847199999999, 0.0, 0.0, 0.0]
```

Time to talk about modifying dice. Pywing is quite flexible with regards
to dice modifications if you're willing to create custom python objects.
But for now we will just go over the provided ones.

To describe when we want to reroll our dice, we must provide two things:
*which* results we would like to reroll and *how many* rerolls we can 
perform. The class **reroll** is contructed with these parameters:

```
>>> target_lock = pywing.reroll(pywing.perform.FOR_ALL, pywing.result.FOCUS | pywing.result.BLANK)
```

The object **target_lock** will reroll all results which are FOCUS or 
BLANK. It is also in charge of doing so in accordance with the rules! In
this case, a single die will not be rerolled more than once, even if it 
could be rerolled by multiple objects.

Let's apply this to our roll:

```
>>> xwing_target_lock_attack = pywing.get_hit_chances(3, friendly_modifications=[target_lock])
>>> xwing_target_lock_attack
array([ 0.01549 ,  0.141225,  0.421785,  0.4215  ,  0.      ,  0.      ,  0.      ,  0.      ])

```

Still TODO
 
