/*
 Copyright (c) 2023 Karoly Molnar
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
*/
include <mounting_pad_cfg.scad>

$fn=40;

height = thickness; // Height of the box
cylinder_height = max(c_height,height);
mountpad_radius = max(mh_drill, thickness);

internal_radius = sqrt(radius^2 + thickness^2);

mountingholes =[[mh_distance,mh_distance],
                [mh_distance, depth-mh_distance],
                [width-mh_distance, mh_distance],
                [width-mh_distance, depth-mh_distance]
];

// Main box with internal corner cylinders
difference() {
    // Outer shape of the box
    union(){
        hull() {
            for (x=[radius, width - radius])
                for (y=[radius, depth - radius])
                    translate([x, y, 0])
                        cylinder(r=radius, h=height);
        }
        for (a = [ 0 : len(mountingholes) - 1 ]) {
            point=mountingholes[a];
            translate([point[0],point[1],0]){
                cylinder(r=mountpad_radius, h=cylinder_height+thickness);
            }
        }

    }
    for (a = [ 0 : len(mountingholes) - 1 ]) {
        point=mountingholes[a];
        translate([point[0],point[1],-thickness]){
            cylinder(r=mh_drill/2, h=cylinder_height+3*thickness);
        }
    }


    // Inner shape (to create the wall thickness and accommodate cylinders)
    translate([0, 0, -thickness]) { // Offset downwards
        hull() {
            for (x=[thickness*1.5, width -thickness*1.5])
                for (y=[mh_distance+2*mountpad_radius, depth - (mh_distance+2*mountpad_radius)])
                    translate([x, y, 0])
                        cylinder(r=thickness/2 , h=height + 2 * thickness);
        }
    }

    translate([0, 0, -thickness]) { // Offset downwards
        hull() {
            for (x=[mh_distance+2*mountpad_radius, width -(mh_distance+2*mountpad_radius)])
                for (y=[thickness*1.5, depth - thickness*1.5])
                    translate([x, y, 0])
                        cylinder(r=thickness/2 , h=height + 2 * thickness);
        }
    }
}