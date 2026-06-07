from src.database.config import supabase
import bcrypt

def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(),bcrypt.gensalt()).decode()


def check_pass(pwd,hashed):
    return bcrypt.checkpw(pwd.encode(),hashed.encode())


def check_teacher_exists(username):
    #check for unique username ,return false when username is already taken
    response =supabase.table("teachers").select("username").eq("username",username).execute()
    return len(response.data)>0

def create_teacher(username,passward,name):
    data={ "username":username,"passward":hash_pass(passward),"name":name}
    response=supabase.table("teachers").insert(data).execute()
    return response.data

def teacher_login(username,passward):
    response=supabase.table("teachers").select("*").eq("username",username).execute()
    if response.data:
        teacher=response.data[0]
        if check_pass(passward,teacher['passward']):
            return teacher
    return None


def get_all_students():
    response= supabase.table('students').select('*').execute()
    return response.data