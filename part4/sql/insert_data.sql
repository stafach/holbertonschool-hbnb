-- Insert Admin user
INSERT INTO User (id, email, first_name, last_name, password, is_admin) VALUES ("36c9050e-ddd3-4c3b-9731-9f487208bbc1", "admin@hbnb.io", "Admin", "HBnB", "$2b$12$rd6eohZP9Q7Pc0/PppgyI.gGcNFl7fMrt.lmC0DawC38O1QpImL6S", TRUE);

-- Insert 3 amenities
INSERT INTO Amenity (id, name) VALUES ("298cd0f9-9713-479f-b14b-ac4f5a9d97fe", "WiFi");
INSERT INTO Amenity (id, name) VALUES ("8f83ec02-93f9-4085-8090-3137ad57fdcb", "Swimming Pool");
INSERT INTO Amenity (id, name) VALUES ("f47dceb5-5804-4c58-aaf5-1051c1f9fee2", "Air Conditioning");
