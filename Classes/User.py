from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

from header import *


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean)

    @staticmethod
    def Indexs():
        db.create_all()
        return jsonify({"message": "Table Created"})


    @staticmethod
    @jwt_required()
    def GetUserAll():
        __tablename__ = "user"
        objUser = User.query.all()
        result = []
        for col in objUser:
            user_dict = {}
            user_dict["id"] = col.id
            user_dict["public_id"] = col.public_id
            user_dict["name"] = col.name
            user_dict["admin"] = col.admin
            result.append(user_dict)
        return json.dumps(result)

    @staticmethod
    def CreateUser():
        data = request.get_json()
        objUser = User()
        objUser.public_id = str(uuid.uuid4())
        objUser.name = data['name']
        hashed_password = generate_password_hash(data["password"], method="sha256")
        objUser.password = hashed_password
        objUser.admin = True
        db.session.add(objUser)
        db.session.commit()
        message = {"message": "User Created"}
        return jsonify(message)

    @staticmethod
    def deleteUserByPublicId(public_id):
        objUser = User.query.filter_by(public_id=public_id).first()

        if not objUser:
            return jsonify({"message": "No user found"})
        db.session.delete(objUser)
        db.session.commit()
        return "User has been deleted"

    @staticmethod
    def SearchByName():
        data = request.get_json()
        objUser = User.query.filter_by(name=data['name'])
        if not objUser:
            message = {"message": "Not Found User"}
            return jsonify(message)
        result = []
        for col in objUser:
            user_dict = {}
        user_dict["id"] = col.id
        user_dict["public_id"] = col.public_id
        user_dict["name"] = col.name
        user_dict["password"] = col.password
        user_dict["admin"] = col.admin
        result.append(user_dict)
        return json.dumps(result)

    @staticmethod
    def updateUserById(id):
        try:
            if request.method =="PUT":
                objUser = User.query.filter_by(id=id).first()
                if not objUser:
                    return  jsonify({"message": "not found id="+ id})
                if objUser:
                    objUser
                    data = request.get_json()
                    objUser.name = data['name']
                    objUser.password = generate_password_hash(data["password"], method="sha256")
                    db.session.add(objUser)
                    db.session.commit()
                    return jsonify({"message:": "user update"})
        except Exception as ex:
            return jsonify({"message": "user updated"})

    @staticmethod
    def Login():
        User.message = []
        data = request.get_json()
        objUser1 = User()
        objUser1.name = data["name"]
        objUser1.password = data["password"]
        objUser = User.query.filter_by(name=objUser1.name, admin=True).first()
        if not objUser:
            User.message_dict = {"message": "Username and password is invalid"}
            User.message.append(User.message_dict)
            return json.dumps(User.message), 401
        if not check_password_hash(objUser.password, objUser1.password):
            User.message_dict = {"message": "Username and password is invalid"}
            User.message.append(User.message_dict)
            return json.dumps(User.message), 401

        ret = {
            'access_token': create_access_token(identity=objUser1.public_id),
            'refresh_token': create_refresh_token(identity=objUser1.public_id)
        }
        return json.dumps(ret), 200

    @staticmethod
    @jwt_required()
    def refresh():
        current_user = get_jwt_identity()
        ret = {
            'access_token': create_access_token(identity=current_user)
        }
        return jsonify(ret), 200

    @staticmethod
    @jwt_required
    def protected():
        username = get_jwt_identity()
        return jsonify(logged_in_as=username), 200




