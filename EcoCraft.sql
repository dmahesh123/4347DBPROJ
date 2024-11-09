CREATE TABLE Users (
    UserID INT PRIMARY KEY,
    UserType VARCHAR(50),
    UserName VARCHAR(100),
    Email VARCHAR(100)
);

CREATE TABLE Craft (
    CraftID INT PRIMARY KEY,
    UserID INT,
    CraftName VARCHAR(100),
    DifficultyLevel VARCHAR(50),
    EstimatedTime INT,
    AgeRange VARCHAR(50),
    CraftType VARCHAR(50),
    Theme VARCHAR(50),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE Instructions (
    CraftID INT,
    StepNumber INT,
    Description TEXT,
    PRIMARY KEY (CraftID, StepNumber),
    FOREIGN KEY (CraftID) REFERENCES Craft(CraftID)
);

CREATE TABLE Material (
    MaterialID INT PRIMARY KEY,
    MaterialName VARCHAR(100),
    Quantity INT,
    Price DECIMAL(10, 2),
    MaterialType VARCHAR(50) 
);


CREATE TABLE Tool (
    ToolID INT PRIMARY KEY,
    ToolName VARCHAR(100),
    Price DECIMAL(10, 2),
    ToolType VARCHAR(50)
);

CREATE TABLE CraftMaterialRelation (
    CraftID INT,
    MaterialID INT,
    Quantity INT,
    PRIMARY KEY (CraftID, MaterialID),
    FOREIGN KEY (CraftID) REFERENCES Craft(CraftID),
    FOREIGN KEY (MaterialID) REFERENCES Material(MaterialID)
);

CREATE TABLE CraftToolRelation (
    CraftID INT,
    ToolID INT,
    QuantityRequired INT,
    PRIMARY KEY (CraftID, ToolID),
    FOREIGN KEY (CraftID) REFERENCES Craft(CraftID),
    FOREIGN KEY (ToolID) REFERENCES Tool(ToolID)
);



CREATE TABLE SeasonalCraft (
    CraftID INT PRIMARY KEY,
    FOREIGN KEY (CraftID) REFERENCES Craft(CraftID)
);



CREATE TABLE DecorativeCraft (
    CraftID INT PRIMARY KEY,
    FOREIGN KEY (CraftID) REFERENCES Craft(CraftID)
);

CREATE TABLE EducationalCraft (
    CraftID INT PRIMARY KEY,
    FOREIGN KEY (CraftID) REFERENCES Craft(CraftID)
);
Select * from EducationalCraft;

INSERT INTO Users (UserID, UserType, UserName, Email)
VALUES
(1, 'Teacher', 'Alice Johnson', 'alice.johnson@example.com'),
(2, 'Student', 'Bob Smith', 'bob.smith@example.com'),
(3, 'Parent', 'Carol White', 'carol.white@example.com'),
(4, 'Teacher', 'David Green', 'david.green@example.com'),
(5, 'Student', 'Eve Brown', 'eve.brown@example.com'),
(6, 'Teacher', 'Frank Thomas', 'frank.thomas@example.com'),
(7, 'Parent', 'Grace Kelly', 'grace.kelly@example.com'),
(8, 'Student', 'Henry Adams', 'henry.adams@example.com'),
(9, 'Teacher', 'Ivy Martin', 'ivy.martin@example.com'),
(10, 'Student', 'Jake Turner', 'jake.turner@example.com');

INSERT INTO Craft (CraftID, UserID, CraftName, DifficultyLevel, EstimatedTime, AgeRange)
VALUES
(1, 1, 'Paper Airplane', 'Easy', 15, '5-10'),
(2, 2, 'Origami Crane', 'Medium', 30, '10-15'),
(3, 3, 'Beaded Bracelet', 'Easy', 20, '8-12'),
(4, 4, 'Wooden Birdhouse', 'Hard', 90, '12-18'),
(5, 5, 'Clay Sculpture', 'Medium', 60, '10-16'),
(6, 6, 'Knitted Scarf', 'Hard', 120, '12-18'),
(7, 7, 'Paper Mache Mask', 'Medium', 45, '10-15'),
(8, 8, 'DIY Picture Frame', 'Easy', 30, '8-12'),
(9, 9, 'Christmas Ornament', 'Easy', 20, '5-10'),
(10, 10, 'Lego Robot', 'Medium', 60, '10-15');



INSERT INTO Instructions (CraftID, StepNumber, Description)
VALUES
(1, 1, 'Fold the paper in half lengthwise.'),
(1, 2, 'Fold the corners into triangles.'),
(1, 3, 'Fold the wings down.'),
(2, 1, 'Fold the paper into a square.'),
(2, 2, 'Fold diagonally to form a triangle.'),
(2, 3, 'Bring the edges together to form a crane shape.'),
(3, 1, 'Thread the beads onto the string.'),
(3, 2, 'Tie a knot at the end of the string.'),
(4, 1, 'Cut the wooden pieces according to the measurements.'),
(4, 2, 'Assemble the pieces to form the birdhouse.');


INSERT INTO Material (MaterialID, MaterialName, Quantity, Price, MaterialType)
VALUES
(1, 'Paper', 100, 0.10, 'Paper'),
(2, 'Beads', 200, 0.05, 'Plastic'),
(3, 'Wood', 50, 1.50, 'Wood'),
(4, 'Clay', 30, 2.00, 'Plastic'),
(5, 'Yarn', 40, 1.20, 'Fabric'),
(6, 'Paint', 25, 3.00, 'Glass'),
(7, 'Glue', 50, 0.50, 'Plastic'),
(8, 'Lego Bricks', 500, 0.15, 'Plastic'),
(9, 'Wire', 100, 0.75, 'Metal'),
(10, 'Fabric', 60, 1.00, 'Fabric');

INSERT INTO Tool (ToolID, ToolName, Price, ToolType)
VALUES
(1, 'Scissors', 2.00, 'Cutting'),
(2, 'Paintbrush', 1.50, 'Painting'),
(3, 'Needle', 1.00, 'Sewing'),
(4, 'Hammer', 5.00, 'Building'),
(5, 'Screwdriver', 3.50, 'Building'),
(6, 'Hot Glue Gun', 7.00, 'Adhesive'),
(7, 'Saw', 8.00, 'Cutting'),
(8, 'Pliers', 4.50, 'Bending'),
(9, 'Lego Separator', 2.00, 'Building'),
(10, 'Measuring Tape', 1.75, 'Measuring');


INSERT INTO CraftMaterialRelation (CraftID, MaterialID, Quantity)
VALUES
(1, 1, 1),
(2, 1, 1),
(3, 2, 20),
(4, 3, 5),
(5, 4, 1),
(6, 5, 2),
(7, 1, 3),
(8, 10, 2),
(9, 6, 1),
(10, 8, 50);


INSERT INTO CraftToolRelation (CraftID, ToolID, QuantityRequired)
VALUES
(1, 1, 1),
(2, 2, 1),
(3, 3, 1),
(4, 4, 1),
(5, 2, 1),
(6, 3, 1),
(7, 6, 1),
(8, 1, 1),
(9, 2, 1),
(10, 9, 1);

INSERT INTO Supervises (SupervisorID, SupervisedID)
VALUES
(1, 2),
(3, 5),
(4, 6),
(1, 8),
(7, 10),
(1, 9),
(6, 8),
(9, 10),
(4, 7),
(3, 4);

INSERT INTO RecyclingCenter (CenterID, CenterName, Location)
VALUES
(1, 'City Recycling Center', 'Downtown'),
(2, 'Green Earth Recycling', 'Suburbs'),
(3, 'Eco Friendly Recycling', 'Uptown'),
(4, 'Neighborhood Recycling', 'Residential Area'),
(5, 'Community Recycling', 'Park Area'),
(6, 'Reclaim and Recycle', 'Industrial Zone'),
(7, 'Planet Care Recycling', 'City Outskirts'),
(8, 'GreenCycle', 'Main Street'),
(9, 'Future Earth Recycling', 'Town Center'),
(10, 'Clean Earth Recycling', 'Rural Area');

INSERT INTO Recycles (MaterialID, CenterID)
VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);

INSERT INTO SeasonalCraft (CraftID)
VALUES
(1), (4), (9);

INSERT INTO DecorativeCraft (CraftID)
VALUES
(3), (6), (8);

INSERT INTO EducationalCraft (CraftID)
VALUES
(2), (5), (10);

Select * from Craft;

SELECT CraftID, CraftName, DifficultyLevel, AgeRange
FROM Craft
WHERE DifficultyLevel = 'Easy';

Insert into Tool 
Values 
(11, 'Wrench', 2.00, 'Building'),
(12, 'Pen', 1.50, 'Drawing');

Select * from Tool;

DELETE FROM SeasonalCraft
WHERE CraftID = 1;
Select * from SeasonalCraft;

UPDATE CraftMaterialRelation
SET Quantity = 3
WHERE CraftID = 1 AND MaterialID = 1;

Select * from CraftMaterialRelation;

SELECT Material.MaterialName, CraftMaterialRelation.Quantity
FROM Material
JOIN CraftMaterialRelation
    ON Material.MaterialID = CraftMaterialRelation.MaterialID
WHERE CraftMaterialRelation.CraftID = 1;


CREATE VIEW CraftDetailsView AS
SELECT
c.CraftID,
c.CraftName,
c.DifficultyLevel,
c.EstimatedTime,
c.AgeRange,
u.UserName AS CreatorName,
u.UserType AS CreatorType
FROM
Craft c
JOIN
Users u ON c.UserID = u.UserID;

SELECT * FROM CraftDetailsView;


Select * from Craft;
INSERT INTO Craft (CraftID, UserID, CraftName, DifficultyLevel, EstimatedTime, AgeRange)
VALUES
(11, 5, 'Bottle Rocket', 'Easy', 15, '5-10');

Select * from Craft;
