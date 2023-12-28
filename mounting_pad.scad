include <mounting_pad_cfg.scad>

$fn=40;

height = thickness; // Height of the box
cylinder_height = max(c_height,height);

reduced_width = width - radius;
reduced_depth = depth - radius;

// Main box with internal corner cylinders
difference() {
    // Outer shape of the box
    hull() {
        for (x=[0, reduced_width-radius])
            for (y=[0,reduced_depth-radius])
                translate([x, y, 0])
                    cylinder(r=radius, h=height);
    }

    // Inner shape (to create the wall thickness and accommodate cylinders)
    translate([0, 0, -thickness]) { // Offset downwards
        hull() {
            for (x=[thickness, reduced_width- thickness-radius])
                for (y=[thickness, reduced_depth - thickness-radius])
                    translate([x, y, 0])
                        cylinder(r=radius - thickness, h=height + 2 * thickness);
        }
    }
    
}

// Adding internal cylinders
difference(){
    union() {
        translate([0, 0, 0]) // Positioning cylinders inside the box
            for (x=[mh_distance/2,reduced_width-mh_distance])
                for (y=[mh_distance/2,reduced_depth-mh_distance])
                    translate([x, y, 0])
                        cylinder(r=mh_distance-thickness, h=height);

        translate([0, 0, height]) // Positioning cylinders inside the box
            for (x=[mh_distance/2,reduced_width-mh_distance])
                for (y=[mh_distance/2,reduced_depth-mh_distance])
                    translate([x, y, 0])
                        cylinder(r=mh_drill/2+2*thickness, h=cylinder_height-height);

    }

    translate([0, 0, 0]) // Positioning cylinders inside the box
        for (x=[mh_distance/2,reduced_width-mh_distance])
            for (y=[mh_distance/2,reduced_depth-mh_distance])
                translate([x, y, 0])
                    cylinder(r=mh_drill/2, h=cylinder_height);

}



// Uncomment the line below to visualize the cutting shape
// translate([0, 0, height/2]) cube([reduced_width, reduced_depth, height], center=true);