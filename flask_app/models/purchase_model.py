from flask_app.config.mysql_connection import connectToMySQL

class Purchase:
    DB = 'creations_db'

    def __init__(self, data) -> None:
        self.user_id = data['user_id']
        self.creation_id = data['creation_id']

    @classmethod
    def add_purchase(cls, data):
        query = """
        INSERT INTO purchases (user_id, creation_id)
        VALUES(%(user_id)s, %(creation_id)s)
        """
        return connectToMySQL(Purchase.DB).query_db(query, data)

    @classmethod 
    def get_all_purchases_by_user_id(cls,data):

        query = """
        SELECT p.user_id, p.creation_id FROM purchases as p
        JOIN users as u ON p.user_id = u.id
        WHERE user_id = %(user_id)s;
        """
        results = connectToMySQL(Purchase.DB).query_db(query, data)
        purchases = []
        for row in results:
            purchases.append(cls(row))
        return purchases
    
    @classmethod
    def delete_purchases_by_creation_id(cls,data):
        query = """
        DELETE FROM purchases 
        WHERE creation_id = %(id)s
        """
        return connectToMySQL(Purchase.DB).query_db(query, data)