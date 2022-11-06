from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask_bcrypt import Bcrypt 
from flask_app import app
bcrypt = Bcrypt(app)
from flask_app.models import job

class User:
    db_name = "users_jobs_schema"   


    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.jobs = []



    @classmethod
    def register_user(cls,data):
        query = """
        INSERT INTO users
        (first_name, last_name, email, password)
        VALUES
        (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    
    @classmethod
    def get_user_by_id(cls,data):
        query = """
        SELECT * FROM users
        WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data) 
        if len(results) == 0:
            return None
        else:
            return cls(results[0]) 


    @classmethod
    def get_user_by_email(cls,data):
        query = """ 
        SELECT * FROM users
        WHERE email = %(email)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            return cls(results[0])
        

    @classmethod
    def get_all_user_jobs(cls, data):
        query = """
        SELECT * FROM users LEFT JOIN 
        jobs ON users.id = jobs.pro_id
        WHERE pro_id = %(id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) == 0:
            return []  
        else:
            user_obj = cls(results[0])
            for one_user_list in results:
                job_dictionary = {
                    "id" : one_user_list["jobs.id"],
                    "title" : one_user_list["title"],
                    "description" : one_user_list["description"],
                    "location" : one_user_list["location"],
                    "created_at" : one_user_list["jobs.created_at"],
                    "updated_at": one_user_list["jobs.updated_at"],
                    "user_id": one_user_list["user_id"],
                    "pro_id": one_user_list["pro_id"]
                }
                job_obj = job.Job(job_dictionary)
                user_obj.jobs.append(job_obj)
            return user_obj


    
    @staticmethod
    def validate_registration(form_data):
        is_valid = True
        if len(form_data["first_name"]) < 2:
            flash("First name must be 2 or more character", "register")
            is_valid = False
        if len(form_data["last_name"]) < 2:
            flash("Last name must be 2 or more character", "register")
            is_valid = False
        if not EMAIL_REGEX.match(form_data["email"]): 
            flash("Invalid email address!")
            is_valid = False
        data = {           
            "email" : form_data["email"]
        }
        found_user_or_None = User.get_user_by_email(data)
        if found_user_or_None != None:  
            flash("Email already taken","register")
            return False  
        if len(form_data["password"]) < 8:
            flash("Password must be 8 or more character", "register")
            is_valid = False
        if form_data["password"] !=  form_data["confirm_password"]:
            flash("Password don't agree", "register")
            is_valid = False
        return is_valid


    @staticmethod
    def validate_login(form_data):
        if not EMAIL_REGEX.match(form_data["email"]): 
            flash("Invalid login credentials!", "login")  
            return False
        data = {
            "email" : form_data["email"]
        }
        found_user_or_None = User.get_user_by_email(data)
        if found_user_or_None == None:
            flash("Invalid login credentials!","login") 
            return False  
        if not bcrypt.check_password_hash(found_user_or_None.password, form_data["password"]): 
            flash("Invalid login credentials!", "login")
            return False  
        return found_user_or_None





