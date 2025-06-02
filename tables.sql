CREATE TABLE IF NOT EXISTS bundles_list(
	id SERIAL PRIMARY KEY,
	bundle VARCHAR(25) NOT NULL,
	CONSTRAINT bundles_list_unique UNIQUE (bundle)
);
INSERT INTO bundles_list (bundle)
VALUES ('magic'),
('generic scene'),
('tearing'),
('flames'),
('flame thrower'),
('dust'),
('explosion'),
('fog'),
('shockwave'),
('skies'),
('cloud'),
('tornado'),
('smoke'),
('environment'),
('water Bomb'),
('debris'),
('lighting'),
('jelly slice'),
('dop setups') 


CREATE TABLE IF NOT EXISTS tags(
	id SERIAL PRIMARY KEY,
	tag VARCHAR(35) NOT NULL,
	CONSTRAINT tag_unique UNIQUE (tag)
);
INSERT INTO tags (tag)
VALUES ('water'),
('volumetrics'),
('destructions'),
('render'),
('hair'),
('fur'),
('softbody'),
('material'), 
('fx'),
('cfx'),
('ground breaking'),
('atmosphere'),
('misc')


CREATE TABLE IF NOT EXISTS categories(
	id SERIAL PRIMARY KEY,
	category VARCHAR(35) NOT NULL,
	CONSTRAINT category_unique UNIQUE (category)
);
INSERT INTO categories (category)
VALUES ('surfacing'),
('pyro'),
('flip'),
('particles'),
('rbds'),
('vellum'),
('ocean'),
('whitewater'),
('mist'),
('foam')

CREATE TABLE IF NOT EXISTS contexts(
	id SERIAL PRIMARY KEY,
	context VARCHAR(35) NOT NULL,
	CONSTRAINT context_unique UNIQUE (context)
);
INSERT INTO contexts (context)
VALUES ('Sop'),
('vop'),
('dop'),
('top'),
('out'),
('pop'),
('chop'),
('mat'),
('lops')

CREATE TABLE IF NOT EXISTS versions(
	id SERIAL PRIMARY KEY,
	version VARCHAR(35) NOT NULL,
	CONSTRAINT version_unique UNIQUE (version)
);
INSERT INTO versions (version)
VALUES ('20.5'),
('20.0'),
('19.5')

CREATE TABLE IF NOT EXISTS bundle_types(
	id SERIAL PRIMARY KEY,
	bundle_type VARCHAR(35) NOT NULL,
	CONSTRAINT bundle_type_unique UNIQUE (bundle_type)
);
INSERT INTO bundle_types (bundle_type)
VALUES ('templates'),
('node snippets')

CREATE TABLE IF NOT EXISTS bundles(
	id SERIAL PRIMARY KEY,
	name VARCHAR(200) NOT NULL,
	description TEXT NOT NULL,
	version INT NOT NULL,
	artist VARCHAR(100) NOT NULL,
	file_path VARCHAR(100) NOT NULL,
	file_type VARCHAR(10) NOT NULL,
	frame_start BIGINT,
	frame_end BIGINT,
	frame_count BIGINT,
	img_path VARCHAR(300),
	favorite BOOLEAN NOT NULL,
	bundle_type_id INT NOT NULL,
	bundle_list_id INT NOT NULL,
	category_id INT,
	context_id INT,
	houdini_version_id INT NOT NULL,
	CONSTRAINT fk_bundle_type_id FOREIGN KEY(bundle_type_id) REFERENCES bundle_types(id),
	CONSTRAINT fk_bundle_list_id FOREIGN KEY(bundle_list_id) REFERENCES bundles_list(id),
	CONSTRAINT fk_category_id FOREIGN KEY(category_id) REFERENCES categories(id),
	CONSTRAINT fk_context_id FOREIGN KEY(context_id) REFERENCES contexts(id),
	CONSTRAINT fk_houdini_version_id FOREIGN KEY(houdini_version_id) REFERENCES versions(id),
	created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO bundles(name, description, version, artist, file_path, file_type, frame_start,
					frame_end, img_path, favorite, bundle_type_id, bundle_list_id, category_id,
					context_id, houdini_version_id)
VALUES('tourch fire', 
		'Burning Tgas torch with an intensely hot flame produced using sparse solver with high density, seperation 0.02, substeps 3',
		1, 'Chandrakanth', 'D:\houdini_bundles\flames\torch_fire\v001\hip\ezgif-frame.hip', '.hip', 1, 138, 138
		'D:\houdini_bundles\flames\torch_fire\v001\img\ezgif-frame-001.jpg', FALSE, 1, 4, 2, null, 3),
	  ('perlin noise', 'noise pattern to a volume field in order to create a cloud like appearance. Various noise shaping options are available as well as masking controls',
	  	1, 'James Won', 'D:\houdini_bundles\cloud\perlin_noise\v001\snip\ezgif-frame.snip', '.snip', null, null, null
	  	'D:\houdini_bundles\cloud\perlin_noise\v001\img\ezgif-frame.jpg', FALSE, 2, 10, null, 2, 3)
INSERT INTO bundles(name, description, version, artist, file_path, file_type, frame_start,
					frame_end, img_path, favorite, bundle_type_id, bundle_list_id, category_id,
					context_id, houdini_version_id, frame_count)
VALUES('flames', 
		'A detailed close-up shot of burning detailed fire, with combination of yellow and light red flames',
		1, 'trishit pradhan', 'D:\houdini_bundles\flames\flames_big\v001\hip\flames.hip', '.hip', 1, 98,
		'\media\flames\flames_big\v001\img\flames_big_001.jpg', FALSE, 1, 4, 2, null, 1, 98), 
        ('flame thrower', 
		'flamethrower effect tweaked with Density, Temperature, Velocity, and Fuel to simulate a realistic behavior. Karma render tested with production shader',
		1, 'murali', 'D:\houdini_bundles\flame_thrower\flame_thrower\v001\hip\flame_thrower.hip', '.hip', 1, 62,
		'\media\flame_thrower\flame_thrower\v001\img\flames_thrower_001.jpg', FALSE, 1, 5, 2, null, 2, 62), 
        ('dust explosion', 
		'Large scale explosion of dust explosion. The particles to drive the motion of fluids and add lots of bursts to the overall reaction',
		1, 'bruce wayne', 'D:\houdini_bundles\explosion\dust_explosion\v001\hip\dust_explosion.hip', '.hip', 1, 48,
		'\media\explosion\dust_explosion\v001\img\dust_explosion_001.jpg', FALSE, 1, 7, 2, null, 1, 48), 
        ('blood splash', 
		'Dynamic Sprouts with animated emission. Approved and archived from tan2 project. Particle counts should increased if gonna rescaled',
		1, 'james won', 'D:\houdini_bundles\blood\blood_splash\v001\hip\blood_splash.hip', '.hip', 1, 60,
		'\media\blood\blood_splash\v001\img\blood_splash_001.jpg', FALSE, 1, 14, 3, null, 2, 60), 
        ('blood splash', 
		'Dynamic and realistic splatter with tweaked viscosity. midium scale. Approved in tan2 project. Retimed in Sop level',
		1, 'james won', 'D:\houdini_bundles\blood\blood_splash\v002\hip\blood_splash.hip', '.hip', 1, 15,
		'\media\blood\blood_splash\v002\img\blood_splash_001.jpg', FALSE, 1, 14, 3, null, 2, 15), 
        ('solver sop sky', 
		'Procedural cloud  sky and evolving cloud containers with simple physical lighting setup in karma',
		1, 'mural ramachari', 'D:\houdini_bundles\skies\solver_sop_sky\v001\snip\solver_sop_sky.snip', '.snip', null, null,
		'D:\houdini_bundles\skies\solver_sop_sky\v001\img\solver_sop_sky.jpg', FALSE, 2, 9, null, 1, 1, null), 
        ('cloth tear setup', 
		'Cloth setup using vellum. animated the collider geometry to drive the main deformations of our cloth. custom growth solver we will be able to manually delete constraints from the vellum object, causing the cloth to tear.',
		1, 'peter parker', 'D:\houdini_bundles\tearing\cloth_tearing_setup\v001\hip\cloth_tearing_setup.hip', '.hip', 1, 40,
		'\media\houdini_bundles\tearing\cloth_tearing_setup\v001\img\cloth_tearing_setup_001.jpg', FALSE, 1, 3, 6, null, 2, 40),
         ('solver sop sky', 
        'Dop setup for POP Drag Spin with RBD Packed. Used for standard RBD construction.  ',
        1, 'peter parker', 'D:\houdini_bundles\dop_setups\rbd_custom_setup\v001\snip\rbd_custom_setup.snip', '.snip', null, null,
        '\media\dop_setups\rbd_custom_setup\v001\img\rbd_custom_setup.jpg', FALSE, 2, 18, null, 3, 1, null),
        ('dust shockwave', 
		'shockwave variation 1',
		1, 'shang chi', 'D:\houdini_bundles\shockwave\dust_shockwave\v001\hip\dust_shockwave.hip', '.hip', 1, 102,
		'\media\houdini_bundles\shockwave\dust_shockwave\v001\img\dust_shockwave_001.jpg', FALSE, 1, 8, 2, null, 1, 102),
		('dust shockwave', 
		'shockwave variation 2',
		2, 'shang chi', 'D:\houdini_bundles\shockwave\dust_shockwave\v002\hip\dust_shockwave.hip', '.hip', 1, 103,
		'\media\houdini_bundles\shockwave\dust_shockwave\v002\img\dust_shockwave_001.jpg', FALSE, 1, 8, 2, null, 1, 103),
		('dust shockwave', 
		'shockwave variation 3',
		3, 'shang chi', 'D:\houdini_bundles\shockwave\dust_shockwave\v003\hip\dust_shockwave.hip', '.hip', 1, 111,
		'\media\houdini_bundles\shockwave\dust_shockwave\v003\img\dust_shockwave_001.jpg', FALSE, 1, 8, 2, null, 1, 111),
		('dust shockwave', 
		'shockwave variation 4',
		4, 'shang chi', 'D:\houdini_bundles\shockwave\dust_shockwave\v004\hip\dust_shockwave.hip', '.hip', 1, 100,
		'\media\houdini_bundles\shockwave\dust_shockwave\v004\img\dust_shockwave_001.jpg', FALSE, 1, 8, 2, null, 1, 100),
		('dust shockwave', 
		'shockwave variation 5',
		5, 'shang chi', 'D:\houdini_bundles\shockwave\dust_shockwave\v005\hip\dust_shockwave.hip', '.hip', 1, 45,
		'\media\houdini_bundles\shockwave\dust_shockwave\v005\img\dust_shockwave_001.jpg', FALSE, 1, 8, 2, null, 1, 45),
		('dust shockwave', 
		'shockwave variation 6',
		6, 'shang chi', 'D:\houdini_bundles\shockwave\dust_shockwave\v006\hip\dust_shockwave.hip', '.hip', 1, 60,
		'\media\houdini_bundles\shockwave\dust_shockwave\v006\img\dust_shockwave_001.jpg', FALSE, 1, 8, 2, null, 1, 60)


CREATE TABLE IF NOT EXISTS bundles_tag(
	id SERIAL PRIMARY KEY,
	bundle_id INT NOT NULL,
	tag_id INT NOT NULL,
	CONSTRAINT fk_bundle_con_id FOREIGN KEY(bundle_id) REFERENCES bundles(id),
	CONSTRAINT fk_tag_con_id FOREIGN KEY(tag_id) REFERENCES tags(id)
);
INSERT INTO bundles_tag(bundle_id, tag_id)
VALUES(1, 2),
(1, 9),
(1,13)

-- Query MANY -to -MANY relation ship for bundles and tags
SELECT name,tags.tag  FROM bundles
JOIN bundles_tag ON bundles_tag.bundle_id = bundles.id
JOIN tags ON tags.id = bundles_tag.tag_id;

-- RESET the primary key  to latest one
ALTER SEQUENCE bundles_id_seq RESTART WITH 20;
ALTER SEQUENCE bundles_tag_id_seq RESTART WITH 39;
