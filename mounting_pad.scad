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

$fn=60;

height = thickness; // Height of the base frame
cylinder_height = max(c_height,height);
mountpad_radius = max(mh_drill, thickness);
internal_radius = sqrt(radius^2 + thickness^2);

// Additional parameter for bottom rounding
round_radius = 1; // Radius for the rounding at the bottom

mountingholes =[[mh_distance,mh_distance],
                [mh_distance, depth-mh_distance],
                [width-mh_distance, mh_distance],
                [width-mh_distance, depth-mh_distance]
];


// Rounded bottomed  cylinder
module rounded_bottom_cylinder(radius, round_radius, height) {
    translate([0,0,-(height-round_radius)])
    hull(){
        cylinder(h = height-round_radius, r = radius);
        // Adding rounded bottom edge
        rotate_extrude()
            translate([radius-round_radius, 0, 0])
                circle(r = round_radius);
    }
}

// Function to create a rounded rectangle
module rounded_rectangle(length, width, height, radius) {
    hull() {
        translate([radius, radius, 0])
            cylinder(r=radius, h=height);
        translate([length - radius, radius, 0])
            cylinder(r=radius, h=height);
        translate([radius, width - radius, 0])
            cylinder(r=radius, h=height);
        translate([length - radius, width - radius, 0])
            cylinder(r=radius, h=height);
    }
}

// Function to create a inward concave roounding
module inward_rounding(radius, height, x,y) {
    difference() {
        cube([radius*2,radius*2,height], center = true);
        translate([x*radius,y*radius,0]){
            cylinder(r=radius, h=2 * height,  center=true);
        }
    }
}

// Function to create a rounded cross
module rounded_cross(x_length,x_width,y_length,y_width,z_width,round_radius){
    // Horizontal arm
    translate([-x_length/2, -x_width/2, 0])
        rounded_rectangle(x_length, x_width, z_width, round_radius);

    // Vertical arm
    rotate([0,0,90])
        translate([-y_length/2, -y_width/2, 0])
            rounded_rectangle(y_length, y_width, z_width, round_radius);

    // Roundings in inward corners
    for (dx=[-1, 1])
        for (dy=[-1, 1])
            translate([dx*y_width/2,dy*x_width/2, z_width/2])
                inward_rounding(round_radius,z_width,dx,dy);
}

// Main box with internal corner cylinders
difference() {
    // Outer shape of the box
    union(){
        hull() {
            for (x=[radius, width - radius]){
                for (y=[radius, depth - radius]) {
                    translate([x, y, 0])
                        rounded_bottom_cylinder(radius, round_radius, height);
                }
            }
        }

        //add the mounting pads
        for (a = [ 0 : len(mountingholes) - 1]) {
            point=mountingholes[a];
            translate([point[0],point[1],(cylinder_height)/2]){
                cylinder(r=mountpad_radius, h=cylinder_height, center = true);
            }
        }
    }

    //make the mounting pad holes
    for (a = [ 0 : len(mountingholes) - 1]) {
        point=mountingholes[a];
        translate([point[0],point[1],0]){
            cylinder(r=mh_drill/2, h=2*(cylinder_height+height), center = true);
        }
    }

    //make internal cut-out
    translate([width/2,depth/2,-2*height])
        rounded_cross(width-thickness*2,
                      depth - 2*(mh_distance+mountpad_radius)-thickness ,
                      depth-thickness*2,
                      width - 2*(mh_distance+mountpad_radius)-thickness ,
                      3*height,round_radius);

}