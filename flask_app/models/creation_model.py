from flask_app.config.mysql_connection import connectToMySQL
from flask import flash

class Creation:
    DB = "creations_db"


    def __init__(self, data) -> None:
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.quantity = data['quantity']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.first_name = data['first_name']
        self.last_name = data['last_name']


    @classmethod 
    def add_new_creation(cls,data):
        query = """
        INSERT INTO creations (title, description, price, quantity, user_id)
        VALUES (%(title)s, %(description)s,%(price)s, %(quantity)s, %(user_id)s)
        """
        return connectToMySQL(Creation.DB).query_db(query,data)
    
    @classmethod
    def get_all_creations(cls):
        query = """
        SELECT c.id, c.title, c.description, c.price, c.quantity, c.created_at, c.updated_at, u.first_name, u.last_name, c.user_id FROM creations AS c
        JOIN users AS u ON u.id = c.user_id
        """
        results = connectToMySQL(Creation.DB).query_db(query)
        creations = []
        for row in results:
            creations.append(cls(row))
        return creations
    
    @classmethod 
    def get_creation_by_id(cls,data):
        query = """
        SELECT c.id, c.title, c.description, c.price, c.quantity, c.created_at, c.updated_at, c.user_id, u.first_name, u.last_name FROM creations AS c
        JOIN users AS u ON u.id = c.user_id
        WHERE c.id = %(id)s;
        """
        results = connectToMySQL(Creation.DB).query_db(query, data)
        creations = []
        for row in results:
            creations.append(cls(row))
        return creations
    
    @classmethod
    def edit_by_id(cls,data):
        query = """
        UPDATE creations SET title = %(title)s, description = %(description)s, price = %(price)s, quantity = %(quantity)s
        WHERE id = %(id)s
        """
        return connectToMySQL(Creation.DB).query_db(query,data)
    
    @classmethod 
    def delete_by_id(cls, data):
        query = """
        DELETE FROM creations
        WHERE id = %(id)s
        """
        return connectToMySQL(Creation.DB).query_db(query,data)
    
    @classmethod
    def get_creation_by_title(cls, data):
        query = """
        SELECT * FROM creations
        WHERE  title = %(title)s
        """
        return connectToMySQL(Creation.DB).query_db(query,data)
    
    @classmethod
    def get_creations_by_user(cls, data):
        query = """
        SELECT * FROM creations AS c
        JOIN users AS u ON u.id = c.user_id
        WHERE c.user_id LIKE %(user_id)s;
        """
        results = connectToMySQL(Creation.DB).query_db(query, data)
        creations = []
        for row in results:
            creations.append(cls(row))
        return creations
    
    @staticmethod
    def validate_creation(data):
        print("This is print:",data)
        is_valid = True
        current_creation = Creation.get_creation_by_id(data)
        creations = Creation.get_creation_by_title(data)
        if len(creations) > 0 and current_creation[0].title != data['title']:
            is_valid = False
            flash('Title must be unique.')
        if len(data['title']) <= 2:
            is_valid = False
            flash('Title must be 2 or more characters.')
        if len(data['description']) <= 10:
            print("This is print 5:",data)
            is_valid = False
            flash('Description must be 10 or more characters.')
        if len(data['price']) <= 0:
            print("This is print 6:",data)
            is_valid = False
            flash('Price field must not be blank.')
        if len(data['quantity']) <= 0:
            print("This is print 6:",data)
            is_valid = False
            flash('Quantity field must not be blank.')
        print('You have hit End Of Validation')
        return is_valid
    
    @classmethod
    def delete_one_from_quantity(cls,data):
        query = """
        UPDATE creations SET quantity = %(quantity)s
        WHERE id = %(id)s
        """
        return connectToMySQL(Creation.DB).query_db(query, data)