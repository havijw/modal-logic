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
in the main directory. From here, you can choose a modal logic to work in and type a proposition to check if it is valid in that logic. The system used is based on the method of tableau. Note that it is possible to generate an infinite tableau from a proposition, in which case the program will just hang indefinitely. Please just kill the program, as it will never finish.

Currently, the following logics are supported:
* K
* KT
