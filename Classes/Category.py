from flask_jwt_extended.view_decorators import jwt_required
from sqlalchemy import ForeignKey

from header import *

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoryName = db.Column(db.String(250))
    # userId = db.Column(db.Interger)
    # createdAt = db.Column(db.DateTime,default=datetime.datetime.now())

    @staticmethod
    def Index():
        db.create_all()
        message = {"message": "Table Created"}
        return jsonify(message)
    
    @staticmethod
    def GetAll():
        __tablename__ = "category"
        dataRest = Category.query.all()
        result = []
        apiRest = {}
        myRest = {}

        for obj in dataRest:
            myRest = {}

            myRest["id"] = obj.id
            myRest["categoryName"] = obj.categoryName
            result.append(myRest)

        if result.count(myRest) > 0:
            apiRest["code"] ="0000"
            apiRest["message"] = "Fect data successfully"
        else:
            apiRest["code"] ="9999"
            apiRest["message"] = "There no data"

        apiRest["data"] = result
        return json.dumps(apiRest)
        

    @staticmethod
    @jwt_required()
    def createCategory():
        __tablename__ = "category"
        data = request.get_json()
        category = Category()
        category.categoryName = data['categoryName']
        db.session.add(category)
        message = {"message": "category Created"}
        db.session.commit()
        return jsonify(message)

    @staticmethod
    @jwt_required()
    def deleteCategoryByPublicId(id):
        objUser = Category.query.filter_by(id=id).first()

        if not objUser:
            return jsonify({"message": "No user found"})
        db.session.delete(objUser)
        db.session.commit()
        return "User has been deleted"