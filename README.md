# Modal Logic
## Purpose
This is a collection of tool developed to help study modal logics.
## GUI
One such tool is a graphical user interface for creating a modal logic. To use this, run
```python3 gui.py```
in the main directory. Once the program is open, click anywhere to create a world, drag between worlds to create accessibility relations (including dragging from a world to itself), and type in expressions to evaluate at a particular world. To delete a world, click the x button, and to delete an arrow, simply click the arrow (it is recommended that you turn off world creation when editing arrows so you don't accidentally create new worlds).
## Proof Generation
Another tool is a general program for checking propositions in a given modal logic. To use this, run
```python3 proof_generation.py```
in the main directory. From here, you can choose which logic you want to work in by specifying properties it should have, then enter a proposition to check. The program uses a system based on modal taleaux to see if the given formula is valid in an arbitrary logic with the given properties. There are some formulas that induce an infinitely long tree, and to protect against this the program exits if the model it builds has more than 50 worlds at any point. In this case, it is extremely likely that the formula is invalid, but the maiximum number of worlds can be increased by modifying the MAX_WORLDS variable in the code. Currently, the following properties are supported:
* Reflexivity (the T axiom)
* Transitivity (the 4 axiom)
* Symmetry (the B axiom)
