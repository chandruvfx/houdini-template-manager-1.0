CREATE TABLE IF NOT EXISTS bundles_list(
	id SERIAL PRIMARY KEY,
	bundle VARCHAR(25) NOT NULL,
	CONSTRAINT bundles_list_unique UNIQUE (bundle)
);
CREATE TABLE IF NOT EXISTS tags(
	id SERIAL PRIMARY KEY,
	tag VARCHAR(35) NOT NULL,
	CONSTRAINT tag_unique UNIQUE (tag)
);
CREATE TABLE IF NOT EXISTS categories(
	id SERIAL PRIMARY KEY,
	category VARCHAR(35) NOT NULL,
	CONSTRAINT category_unique UNIQUE (category)
);
CREATE TABLE IF NOT EXISTS contexts(
	id SERIAL PRIMARY KEY,
	context VARCHAR(35) NOT NULL,
	CONSTRAINT context_unique UNIQUE (context)
);
CREATE TABLE IF NOT EXISTS versions(
	id SERIAL PRIMARY KEY,
	version VARCHAR(35) NOT NULL,
	CONSTRAINT version_unique UNIQUE (version)
);
CREATE TABLE IF NOT EXISTS bundle_types(
	id SERIAL PRIMARY KEY,
	bundle_type VARCHAR(35) NOT NULL,
	CONSTRAINT bundle_type_unique UNIQUE (bundle_type)
);
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
CREATE TABLE IF NOT EXISTS bundles_tag(
	id SERIAL PRIMARY KEY,
	bundle_id INT NOT NULL,
	tag_id INT NOT NULL,
	CONSTRAINT fk_bundle_con_id FOREIGN KEY(bundle_id) REFERENCES bundles(id),
	CONSTRAINT fk_tag_con_id FOREIGN KEY(tag_id) REFERENCES tags(id)
);
