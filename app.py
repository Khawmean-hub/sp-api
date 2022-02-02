from header import *
from Classes.Product import *
from Classes.User import *
from Classes.Category import *


#route
app.add_url_rule("/",view_func=User.Indexs)
app.add_url_rule("/user/create",view_func=User.CreateUser,methods=["POST"])
app.add_url_rule("/user/get",view_func=User.GetUserAll,methods=["GET"],endpoint="/user/get")
app.add_url_rule("/user/<public_id>",view_func=User.deleteUserByPublicId, methods=["DELETE"])
app.add_url_rule("/user/name",view_func=User.SearchByName, methods=["GET"])
app.add_url_rule("/user/update/<id>",view_func=User.updateUserById, methods=["PUT"],endpoint="/user/update")
app.add_url_rule("/login",view_func=User.Login, methods=["POST"])

app.add_url_rule("/",view_func=Product.Index)
app.add_url_rule("/product/create",view_func=Product.CreateProduct, methods=["POST"])
app.add_url_rule("/product/get",view_func=Product.GetProductAll, methods=["GET"])
app.add_url_rule("/product/<id>",view_func=Product.deleteProductByPublicId, methods=["DELETE"])
app.add_url_rule("/product/name",view_func=Product.SearchProductByName, methods=["GET"])
app.add_url_rule("/product/update/<id>",view_func=Product.updateProductById, methods=["PUT"],endpoint="/product/update")

#-------------------------------------category---------------------------------
app.add_url_rule("/category/create", view_func=Category.createCategory, methods=["POST"])
app.add_url_rule("/category/get", view_func=Category.GetAll, methods=["GET"])
app.add_url_rule("/category/<id>",view_func=Category.deleteCategoryByPublicId, methods=["DELETE"])


