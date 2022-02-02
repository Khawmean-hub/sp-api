from flask_jwt_extended.view_decorators import jwt_required
from sqlalchemy.orm import relationship
from werkzeug.wrappers import response
from Classes.Category import Category
from header import *

class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    barcode = db.Column(db.String(100))
    unitPrice = db.Column(db.String(100))
    sellPrice = db.Column(db.String(100))
    qty = db.Column(db.String(100))
    categoryId = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    # categoryName = relationship("Category", foreign_keys=[categoryId])

    @staticmethod
    def Index():
        db.create_all()
        message = {"message": "Table Created"}
        return jsonify(message)

    @staticmethod
    def GetProductAll():
        __tablename__ = "product"
        myObjProduct = db.session.query(Product.id, Product.name, Product.barcode, Product.unitPrice, Product.sellPrice, Product.qty, Product.categoryId, Category.categoryName).filter(
            Product.categoryId == Category.id
        )
                                #  .filter_by(userid=2) \
                                #  .order_by(Product.price).first()
        result = []
        apiRest = {}
        if myObjProduct.count() > 0:
            apiRest["code"] ="0000"
            apiRest["message"] = "Fect data successfully"
        else:
            apiRest["code"] ="9999"
            apiRest["message"] = "There no data"

        for col in myObjProduct:
            product_dict = {}
            product_dict["id"] = col.id
            product_dict["name"] = col.name
            product_dict["barcode"] = col.barcode
            product_dict["unitPrice"] = col.unitPrice
            product_dict["sellPrice"] = col.sellPrice
            product_dict["qty"] = col.qty
            product_dict["categoryId"] = col.categoryId
            product_dict["categoryName"] = col.categoryName
            result.append(product_dict)
        apiRest["data"] =result
        return json.dumps(apiRest)

    @staticmethod
    @jwt_required()
    def CreateProduct():
        data = request.get_json()
        objProduct = Product()
        objProduct.name = data['name']
        objProduct.barcode = data['barcode']
        objProduct.unitPrice = data['unitPrice']
        objProduct.sellPrice = data['sellPrice']
        objProduct.qty = data['qty']
        objProduct.categoryId = data['categoryId']
        db.session.add(objProduct)
        message = {"message": "User Created"}
        db.session.commit()
        return jsonify(message)

    @staticmethod
    @jwt_required()
    def deleteProductByPublicId(id):
        objUser = Product.query.filter_by(id=id).first()

        if not objUser:
            return jsonify({"message": "No user found"})
        db.session.delete(objUser)
        db.session.commit()
        return "User has been deleted"

    @staticmethod
    def SearchProductByName():
        data = request.get_json()
        objUser = db.session.query(Product.id, Product.name, Product.barcode, Product.unitPrice, Product.sellPrice, Product.qty, Product.categoryId, Category.categoryName).filter(
            Product.categoryId == Category.id,
            Product.name.contains(data["name"]) 
        )

        apiRest = {}
        if objUser.count() > 0:
            apiRest["code"] ="0000"
            apiRest["message"] = "Fect data successfully"
        else:
            apiRest["code"] ="9999"
            apiRest["message"] = "Data not found"
        rename_dict = {}

        for col in objUser:
            rename_dict = {}
            rename_dict["id"] = col.id
            rename_dict["name"] = col.name
            rename_dict["barcode"] = col.barcode
            rename_dict["sellPrice"] = col.sellPrice
            rename_dict["qty"] = col.qty
            rename_dict["categoryId"] = col.categoryId
            rename_dict["categoryName"] = col.categoryName
        apiRest["data"] = rename_dict
        return json.dumps(apiRest)

    @staticmethod
    @jwt_required()
    def updateProductById(id):
        try:
            if request.method == "PUT":
                objProduct = Product.query.filter_by(id=id).first()
                if not objProduct:
                    return jsonify({"message": "not found id=" + id})
                if objProduct:
                    objProduct
                    data = request.get_json()
                    objProduct.name = data['name']
                    objProduct.barcode = data['barcode']
                    objProduct.unitPrice = data['unitPrice']
                    objProduct.sellPrice = data['sellPrice']
                    objProduct.qty = data['qty']
                    objProduct.categoryId = data['categoryId']

                    db.session.add(objProduct)
                    db.session.commit()
                    return jsonify({"message:": "product update"})
        except Exception as ex:
            return jsonify({"message": "product updated"})

