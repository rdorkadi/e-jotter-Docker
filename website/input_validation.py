# This file is for signup userfields creation validation

# check if the password contains special char
# return type = True or False 
# Eg : password = "afdsaas" return "false"
# password = "@#afads" retrun "true"
def contains_chr(_password):
    password = _password
    return (not password.isalnum())

# check if string contains uppercase letters
# Retrun Type = True or Flase
def contains_upper(_password):
    password = _password
    return (any(x.isupper() for x in password))

# check if string contains lowercase letters
# Return Type = True or Flase
def contains_lower(_password):
    password = _password
    return (any(x.islower() for x in password))

# check if string start with special chr or Number
# Return type = True or False
# eg : #asflkj or 9sadfkj return True
def sw_ChrNum(_password):
    password = _password
    
# password with special characters

# password without special characters

# password with uppercase

# password without uppercase

# password with lowercase

# password without lowercase

# password starting with special characters

# password starting with numbers

