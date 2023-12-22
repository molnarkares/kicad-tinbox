#!/bin/bash

rm -rf kicad-tinbox
rm -rf kicad-tinbox.zip
mkdir kicad-tinbox
mkdir kicad-tinbox/plugins
cp *.py kicad-tinbox/plugins
cp *.png kicad-tinbox/plugins
mkdir kicad-tinbox/resources
cp icon.png kicad-tinbox/resources
cp metadata.json kicad-tinbox
cd kicad-tinbox || exit
zip -r ../kicad-tinbox.zip .
cd .. || exit
