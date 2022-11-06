from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user


class Job:
    db_name = "users_jobs_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.description = data["description"]
        self.location = data["location"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.pro_id = data["pro_id"]
        self.user = None  
        self.pro = None 


    
    @classmethod
    def add_pro(cls, data):
        query = """
        UPDATE jobs SET
        pro_id = %(pro_id)s
        WHERE jobs.id = %(job_id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def add_job(cls, data):
        query = """
        INSERT INTO jobs(title, description,
        location, user_id)
        VALUES (%(title)s, %(description)s,
        %(location)s, %(user_id)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)  

    

    @classmethod
    def get_all_jobs(cls):
        query = """
        SELECT * FROM jobs JOIN users
        ON jobs.user_id = users.id;
        """
        results = connectToMySQL(cls.db_name).query_db(query)
        if len(results) == 0:
            return []
        else:  
            all_job_objects = [] 
            for job_dictionary in results:
                job_obj = cls(job_dictionary) 
                user_dictionary = {
                    "id" : job_dictionary["users.id"],
                    "first_name" : job_dictionary["first_name"],
                    "last_name" : job_dictionary["last_name"],
                    "email": job_dictionary["email"],
                    "password" : job_dictionary["password"],
                    "created_at" : job_dictionary["users.created_at"],
                    "updated_at" : job_dictionary["users.updated_at"]
                }
                user_obj = user.User(user_dictionary)
                job_obj.user = user_obj
            
                all_job_objects.append(job_obj)
            return all_job_objects
        
    @classmethod
    def update_job(cls, data):
        query = """
        UPDATE jobs SET
        title = %(title)s,
        description = %(description)s,
        location = %(location)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query,data)
    

    @classmethod
    def delete_job(cls, data):
        query = """
        DELETE FROM jobs WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query,data)

    

    @classmethod
    def get_one_job(cls, data):
        query = """
        SELECT * FROM jobs JOIN
        users ON jobs.user_id = users.id 
        WHERE jobs.id = %(id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) == 0:
            return None  
        else:
            job_dictionary =results[0]
            job_obj = cls(job_dictionary)  
            user_dictionary = {
                "id" : job_dictionary["users.id"],
                "first_name" : job_dictionary["first_name"],
                "last_name" : job_dictionary["last_name"],
                "email": job_dictionary["email"],
                "password" : job_dictionary["password"],
                "created_at" : job_dictionary["users.created_at"],
                "updated_at" : job_dictionary["users.updated_at"]
            }
            user_obj = user.User(user_dictionary) 
            job_obj.user = user_obj   
        return job_obj  

    

    @classmethod
    def edit_job(cls, data):
        query = """
        INSERT INTO jobs (title,
        description, location, user_id)
        VALUES (%(title)s, %(description)s, 
        %(location)s, %(user_id)s, %(pro_id)s);
        """
        return connectToMySQL(cls.db_name).query_db(query,data)
    


    @staticmethod
    def validate_job(form_data):
        is_valid = True
        if len(form_data["title"]) < 3:
            flash("title must be 2 or more characters")
            is_valid = False
        if len(form_data["description"]) < 8:
            flash("description must be 2 or more characters")
            is_valid = False
        if len(form_data["location"]) < 3:
            flash("location must be 3 or more characters")
            is_valid = False
        return is_valid
