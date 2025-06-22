# Model
```collatz.py``` models the mathematics described in the tex paper under ```latex/```. It generates the inverse tree graph using the anytree NodeMixin for some tree logic. The model will automatically keep track on a few key metrics like depth, transformations and potential loops (none found so far unforutately).  

Use ```controller.py``` as a playground to test different scenarios, visualize the graph, collect data etc.

# Requirements
Python requirements are listed in ```requirements.txt``` but you also need to install graphviz. On a mac: ```brew install graphviz```.