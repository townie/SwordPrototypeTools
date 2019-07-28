#!/bin/bash

# remove old

rm -rf  ~/.config/blender/2.79/scripts/modules


virtualenv -p python blendenv
source blendenv/bin/activate

############

pip install beautifulsoup4

pip install ipython






###############
mkdir -p ~/.config/blender/2.79/scripts/modules/
cp -r blendenv/lib/python3.5/site-packages/* ~/.config/blender/2.79/scripts/modules/




# cp -r blendenv/lib/python3.5/site-packages/bs4/ ~/.config/blender/2.79/scripts/modules
# cp -r blendenv/lib/python3.5/site-packages/IPython/ ~/.config/blender/2.79/scripts/modules
