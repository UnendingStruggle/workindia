from databaseManagement import DB

db = DB()
db.query("CREATE TABLE Users(id INT AUTO_INCREMENT PRIMARY KEY,Username varchar(16) NOT NULL, Password varchar(32) NOT NULL, Email varchar(20) NOT NULL)")
db.query("""CREATE TABLE Shorts (id INT PRIMARY KEY AUTO_INCREMENT,
    category VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(100),
    publish_date DATETIME,
    content TEXT,
    actual_content_link VARCHAR(255),
    image VARCHAR(255),
    upvote INT DEFAULT 0,
    downvote INT DEFAULT 0
)AUTO_INCREMENT=10000;""")
result = db.query("DESC Shorts")
for row in result:
    print(row)
