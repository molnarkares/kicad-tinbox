#!/bin/bash

rm -rf kicad-tinbox
rm -rf kicad-tinbox.zip
mkdir kicad-tinbox
mkdir kicad-tinbox/plugins
mkdir kicad-tinbox/resources
cp *.py kicad-tinbox/plugins
cp images/tinbox_measure.png kicad-tinbox/plugins
cp images/icon.png kicad-tinbox/plugins
cp images/icon.png kicad-tinbox/resources
cp mounting_pad.scad kicad-tinbox/plugins
cp metadata.json kicad-tinbox
cd kicad-tinbox || exit
zip -r ../kicad-tinbox.zip .
cd .. || exit

