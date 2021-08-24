instructions = [
    'SET FOREIGN_KEY_CHECKS=0;',
    'DROP TABLE IF EXISTS user;',
    'DROP TABLE IF EXISTS rol;',
    'SET FOREIGN_KEY_CHECKS=1;',
    """
        CREATE TABLE rol (
            id INT PRIMARY KEY AUTO_INCREMENT,
            rol_name VARCHAR(50) UNIQUE NOT NULL
        )
    """,
    """
        CREATE TABLE user (
            id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(200) NOT NULL,
            position INT NOT NULL,
            FOREIGN KEY (position) REFERENCES rol (id)
        )
    """
]