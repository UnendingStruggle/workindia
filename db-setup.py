from databaseManagement import DB

db = DB()
db.query("CREATE TABLE Users(id INT AUTO_INCREMENT PRIMARY KEY,Username varchar(16) NOT NULL, Password varchar(32) NOT NULL)")
db.query("CREATE TABLE Notes(note_id INT,notes TEXT,FOREIGN KEY (note_id) REFERENCES Users(id))")
result = db.query("DESC Notes")
for row in result:
    print(row)
