-- ============================================================================
-- seed.sql  — Seed data for Real-Time Traffic Sign Recognition System
-- Run AFTER schema.sql
-- ============================================================================

USE traffic_sign_db;

-- ============================================================================
-- Sign Meaning Dictionary — Indian Traffic Signs
-- Categories: mandatory | cautionary | informatory
-- ============================================================================

INSERT INTO sign_meaning_dictionary (sign_name, sign_description, category) VALUES
-- MANDATORY
('Stop',                    'All vehicles must stop completely before proceeding.',                                   'mandatory'),
('Give Way',                'Yield to vehicles on the major road.',                                                   'mandatory'),
('No Entry',                'Entry of all vehicles prohibited in the direction of sign.',                            'mandatory'),
('No Left Turn',            'Turning left is prohibited.',                                                           'mandatory'),
('No Right Turn',           'Turning right is prohibited.',                                                          'mandatory'),
('No U-Turn',               'U-turn is not permitted.',                                                              'mandatory'),
('No Overtaking',           'Overtaking of vehicles is prohibited.',                                                 'mandatory'),
('No Parking',              'Parking of vehicles is prohibited at this location.',                                   'mandatory'),
('No Stopping or Standing', 'Vehicles must not stop or stand at this location.',                                     'mandatory'),
('Speed Limit 20',          'Maximum speed allowed is 20 km/h.',                                                     'mandatory'),
('Speed Limit 30',          'Maximum speed allowed is 30 km/h.',                                                     'mandatory'),
('Speed Limit 40',          'Maximum speed allowed is 40 km/h.',                                                     'mandatory'),
('Speed Limit 50',          'Maximum speed allowed is 50 km/h.',                                                     'mandatory'),
('Speed Limit 60',          'Maximum speed allowed is 60 km/h.',                                                     'mandatory'),
('Speed Limit 70',          'Maximum speed allowed is 70 km/h.',                                                     'mandatory'),
('Speed Limit 80',          'Maximum speed allowed is 80 km/h.',                                                     'mandatory'),
('Speed Limit 100',         'Maximum speed allowed is 100 km/h.',                                                    'mandatory'),
('Keep Left',               'Vehicles must keep to the left side of the road.',                                      'mandatory'),
('Keep Right',              'Vehicles must keep to the right side of the road.',                                     'mandatory'),
('Horn Prohibited',         'Use of horn is prohibited in this zone.',                                               'mandatory'),
('Compulsory Ahead',        'Vehicles must proceed in the forward direction only.',                                   'mandatory'),
('Compulsory Turn Left',    'Vehicles must turn left at this junction.',                                              'mandatory'),
('Compulsory Turn Right',   'Vehicles must turn right at this junction.',                                             'mandatory'),
('Pedestrians Only',        'Road or path reserved exclusively for pedestrians.',                                    'mandatory'),
('Cycle Track',             'Lane or track reserved for cyclists only.',                                             'mandatory'),

-- CAUTIONARY
('School Ahead',            'School zone — drive carefully and watch for children.',                                 'cautionary'),
('Pedestrian Crossing',     'Pedestrian crossing ahead — give way to pedestrians.',                                  'cautionary'),
('Children Crossing',       'Children crossing the road — exercise extreme caution.',                                'cautionary'),
('Cattle Crossing',         'Animals may be crossing the road — slow down.',                                         'cautionary'),
('Sharp Bend Left',         'Sharp left curve ahead — reduce speed.',                                                'cautionary'),
('Sharp Bend Right',        'Sharp right curve ahead — reduce speed.',                                               'cautionary'),
('Winding Road',            'Series of curves ahead — slow down and drive carefully.',                               'cautionary'),
('Steep Ascent',            'Steep uphill gradient ahead.',                                                          'cautionary'),
('Steep Descent',           'Steep downhill gradient ahead — use lower gear.',                                       'cautionary'),
('Narrow Road',             'Road narrows ahead — pass with care.',                                                  'cautionary'),
('Narrow Bridge',           'Bridge ahead is narrower than the road — proceed cautiously.',                          'cautionary'),
('Slippery Road',           'Road surface is slippery — reduce speed and avoid sudden braking.',                     'cautionary'),
('Road Under Construction', 'Road work in progress — reduce speed and follow instructions.',                         'cautionary'),
('Rough Road',              'Rough or uneven road surface ahead.',                                                    'cautionary'),
('Speed Breaker',           'Speed breaker (bump) ahead — slow down.',                                               'cautionary'),
('Ferry',                   'Ferry crossing ahead — vehicles may board a ferry.',                                    'cautionary'),
('Cross Road',              'Cross road intersection ahead — proceed with caution.',                                  'cautionary'),
('T-Junction',              'T-shaped junction ahead.',                                                              'cautionary'),
('Y-Junction',              'Y-shaped junction ahead.',                                                              'cautionary'),
('Staggered Junction',      'Staggered junction (offset roads) ahead — use caution.',                                'cautionary'),
('Major Road Ahead',        'Major or priority road meets this road ahead.',                                         'cautionary'),
('Roundabout',              'Roundabout ahead — give way to traffic from the right.',                                 'cautionary'),
('Falling Rocks',           'Risk of falling rocks from hillside — drive with caution.',                             'cautionary'),
('Hump Bridge',             'Hump bridge ahead — reduce speed.',                                                     'cautionary'),
('Gap in Median',           'Opening in central median ahead — watch for turning vehicles.',                         'cautionary'),

-- INFORMATORY
('Hospital',                'Hospital nearby — maintain silence and drive carefully.',                               'informatory'),
('Parking',                 'Parking area available ahead.',                                                         'informatory'),
('Fuel Station',            'Fuel / petrol station ahead.',                                                          'informatory'),
('First Aid Post',          'First aid / medical post nearby.',                                                      'informatory'),
('Rest Area',               'Rest area / picnic spot ahead.',                                                        'informatory'),
('Hotel',                   'Hotel or accommodation facility ahead.',                                                'informatory'),
('Restaurant',              'Restaurant or food facility ahead.',                                                    'informatory'),
('Telephone',               'Public telephone available nearby.',                                                    'informatory'),
('Bus Stop',                'Public bus stop location.',                                                             'informatory'),
('Public Toilet',           'Public toilet / restroom facility nearby.',                                             'informatory'),
('Direction Sign',          'Directional sign indicating route to a destination.',                                   'informatory'),
('One Way Street',          'Traffic flows in one direction only.',                                                  'informatory'),
('Expressway Start',        'Expressway / highway begins here.',                                                     'informatory'),
('Expressway End',          'Expressway / highway ends here.',                                                       'informatory'),
('Priority Road',           'This road has priority over intersecting roads.',                                       'informatory'),
('No Through Road',         'Road is a dead end — no exit at far end.',                                             'informatory'),
('Pedestrian Zone',         'Pedestrian-priority zone — vehicles may be restricted.',                                'informatory'),
('Bicycle Route',           'Recommended cycling route.',                                                            'informatory'),
('Truck Route',             'Designated route for heavy goods vehicles.',                                            'informatory'),
('Tourist Site',            'Tourist attraction or point of interest nearby.',                                       'informatory');

-- ============================================================================
-- Default admin user placeholder
-- NOTE: Replace <bcrypt-hash-here> with a real bcrypt hash generated at
--       application startup (never store plaintext passwords).
-- ============================================================================
-- INSERT INTO users (username, email, password_hash, role, email_verified)
-- VALUES ('admin', 'admin@nitk.edu.in', '<bcrypt-hash-here>', 'admin', 1);
