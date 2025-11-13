--  CREATE TEST DATA

-- Create Admin
INSERT INTO User (id, email, first_name, last_name, password, is_admin) VALUES
('bff3a936-7e41-44af-b347-b1a27d20391b', 'admin1@hbnbtest.uk', 'Admin', 'HBnB', '$2b$12$rd6eohZP9Q7Pc0/PppgyI.gGcNFl7fMrt.lmC0DawC38O1QpImL6S', TRUE);

-- Create regular users
INSERT INTO User (id, email, first_name, last_name, password, is_admin) VALUES
('d7b9a4f4-1796-42cc-98d9-b7f5e3e1bcf1', 'johndoe1@test.uk', 'John', 'Doe', '$2b$12$Hk9gX5wXv/N9Kp0sLqZ1OuyjS0gV7Qv1k5xHl4IhBfGZ8qZbE4T16', FALSE),
('9d2a7b21-0df9-4a14-a7c2-5b5d0d7de4e3', 'annebo1@test.uk', 'Anne', 'Bo', '$2b$12$HyYE5JjK1Y54CjNNOo0H0.keKsLQWKZ6tOF1EMG7hpRPjJNZBy0a6', FALSE);

-- Create Places
INSERT INTO Place (id, title, description, price, latitude, longitude, owner_id) VALUES
('f9d7a2a0-351a-4621-bb62-4d12e244ab9c', 'Charming Cottage', 'A cozy little cottage in the countryside.', 120.00, 48.8566, 2.3522, 'bff3a936-7e41-44af-b347-b1a27d20391b'),
('c3a5f0c8-317d-438b-8d2e-f0c0f945d902', 'City Apartment', 'Modern apartment in the city center.', 200.00, 48.8566, 2.3522, 'd7b9a4f4-1796-42cc-98d9-b7f5e3e1bcf1');

-- Create Reviews
INSERT INTO Review (id, text, rating, user_id, place_id) VALUES
('f08c5c7d-3d24-4a89-b4a4-372dff5421fa', 'Amazing stay!', 5, '9d2a7b21-0df9-4a14-a7c2-5b5d0d7de4e3', 'f9d7a2a0-351a-4621-bb62-4d12e244ab9c'),
('1b7d84d9-fb7d-4022-97a4-12cd5f5792e9', 'Very clean and comfortable!', 4, '9d2a7b21-0df9-4a14-a7c2-5b5d0d7de4e3', 'c3a5f0c8-317d-438b-8d2e-f0c0f945d902');

-- Create Amenities
INSERT INTO Amenity (id, name) VALUES
('6a3cc56e-6824-42b5-a44d-6f1f02d22b74', 'WiFi'),
('b7ff49b5-3621-40d7-bb0e-19c54f53c5f7', 'Swimming Pool'),
('e2b7f1c5-31df-4d32-9b28-1a8a5eecf96a', 'Air Conditioning');

-- Add amenities to places
INSERT INTO Place_Amenity (place_id, amenity_id) VALUES
('f9d7a2a0-351a-4621-bb62-4d12e244ab9c', '6a3cc56e-6824-42b5-a44d-6f1f02d22b74'),
('f9d7a2a0-351a-4621-bb62-4d12e244ab9c', 'b7ff49b5-3621-40d7-bb0e-19c54f53c5f7'),
('c3a5f0c8-317d-438b-8d2e-f0c0f945d902', 'e2b7f1c5-31df-4d32-9b28-1a8a5eecf96a');


-- READ TESTS


-- List all users
SELECT * FROM User;

-- List all places with their owner
SELECT Place.id, Place.title, Place.price, User.first_name AS owner
FROM Place
JOIN User ON Place.owner_id = User.id
ORDER BY Place.title ASC;

-- List all reviews for a given place
SELECT Review.text, Review.rating, User.first_name AS reviewer
FROM Review
JOIN User ON Review.user_id = User.id
JOIN Place ON Review.place_id = Place.id
WHERE Place.title = 'Charming Cottage'
ORDER BY Review.rating DESC;

-- List amenities of a specific place
SELECT Place.title, Amenity.name
FROM Place
JOIN Place_Amenity ON Place_Amenity.place_id = Place.id
JOIN Amenity ON Amenity.id = Place_Amenity.amenity_id
WHERE Place.title = 'Charming Cottage'
ORDER BY Amenity.name;


--  UPDATE TESTS

-- Update place price
UPDATE Place SET price = 100.00 WHERE id = 'f9d7a2a0-351a-4621-bb62-4d12e244ab9c';

-- Update user first name
UPDATE User SET first_name = 'Jonathan' WHERE id = 'd7b9a4f4-1796-42cc-98d9-b7f5e3e1bcf1';

-- Update amenity name
UPDATE Amenity SET name = 'High-Speed WiFi' WHERE id = '6a3cc56e-6824-42b5-a44d-6f1f02d22b74';


-- DELETE TESTS

-- Delete a review
DELETE FROM Review WHERE id = '1b7d84d9-fb7d-4022-97a4-12cd5f5792e9';

-- Delete an amenity from a place
DELETE FROM Place_Amenity WHERE place_id = 'f9d7a2a0-351a-4621-bb62-4d12e244ab9c' AND amenity_id = 'b7ff49b5-3621-40d7-bb0e-19c54f53c5f7';

-- Delete a place (cascade removes related reviews + place_amenity)
DELETE FROM Place WHERE id = 'c3a5f0c8-317d-438b-8d2e-f0c0f945d902';

-- Delete a user (cascade removes owned places, reviews, etc.)
DELETE FROM User WHERE id = '9d2a7b21-0df9-4a14-a7c2-5b5d0d7de4e3';
