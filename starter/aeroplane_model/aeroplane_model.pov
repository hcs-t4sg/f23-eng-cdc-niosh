#version 3.7; // 3.6
global_settings { assumed_gamma 1.0 }
#default { finish { ambient 0.2 diffuse 0.9 } }
#default { pigment { rgb <0.800, 0.800, 0.800> } }

//------------------------------------------
#include "colors.inc"
#include "textures.inc"

//------------------------------------------
#include "aeroplane_model_textures.inc"

//------------------------------------------
// Camera ----------------------------------
#declare CamUp = < 0, 0, 31.18>;
#declare CamRight = <41.58, 0, 0>;
#declare CamRotation = <-35.264385748209804, 3.109193303150473e-05, 44.999983741532446>;
#declare CamPosition = <28.325950622558594, -25.40311050415039, 24.36869239807129>;
camera {
	orthographic
	location <0, 0, 0>
	direction <0, 1, 0>
	up CamUp
	right CamRight
	rotate CamRotation
	translate CamPosition
}

// FreeCAD Light -------------------------------------
light_source { CamPosition color rgb <0.5, 0.5, 0.5> }

// Background ------------------------------

polygon {
	5, <-20.789137522379555, -15.591853141784668>, <-20.789137522379555, 15.591853141784668>, <20.789137522379555, 15.591853141784668>, <20.789137522379555, -15.591853141784668>, <-20.789137522379555, -15.591853141784668>
	pigment {
		gradient y
		color_map {
			[ 0.00  color rgb<0.592, 0.592, 0.667> ]
			[ 0.05  color rgb<0.592, 0.592, 0.667> ]
			[ 0.95  color rgb<0.200, 0.200, 0.396> ]
			[ 1.00  color rgb<0.200, 0.200, 0.396> ]
		}
		scale <1,31.183706283569336,1>
		translate <0,-15.591853141784668,0>
	}
	finish { ambient 1 diffuse 0 }
	rotate <54.735614251790196, 3.109193303150473e-05, 44.999983741532446>
	translate <28.325950622558594, -25.40311050415039, 24.36869239807129>
	translate <-57735.0378036499, 57735.02588272095, -57735.01992225647>
}
sky_sphere {
	pigment {
		gradient z
		color_map {
			[ 0.00  color rgb<0.592, 0.592, 0.667> ]
			[ 0.30  color rgb<0.592, 0.592, 0.667> ]
			[ 0.70  color rgb<0.200, 0.200, 0.396> ]
			[ 1.00  color rgb<0.200, 0.200, 0.396> ]
		}
		scale 2
		translate -1
		rotate<-35.264385748209804, 3.109193303150473e-05, 44.999983741532446>
	}
}

//------------------------------------------

#include "aeroplane_model_user.inc"

// Objects in Scene ------------------------

//----- Aeroplane -----
merge {

	//----- Fusion -----
	merge {
	
		//----- Cube -----
		box { <0,0,0>, <5.0, 20.0, 1.0>
			translate <3.0, -10.0, -1.0>
		}
		
		//----- Cylinder -----
		cylinder { <0, 0, 0>, <0, 0, 20.0>, 2.0
			rotate <0.0, 90.0, 0.0>
		}
		
	}
	
	//----- Cube001 -----
	box { <0,0,0>, <3.0, 1.0, 5.0>
		translate <0.0, -0.5, 0.0>
	}
	
}

//----- PointLight -----
light_source { <0, 0, 0>
	color rgb<1.0, 1.0, 1.0>
	translate <10.0, 10.0, 10.0>
}
