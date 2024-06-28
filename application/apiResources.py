from flask_restful import Resource, output_json
from application.models import *
from application.validation import *
from flask_restful import reqparse
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import marshal
import requests


product_parser = reqparse.RequestParser()
product_parser.add_argument("name", type=str)
product_parser.add_argument("img_name", type=str)
product_parser.add_argument("mgf_date", type=str)
product_parser.add_argument("exp_date", type=str)
product_parser.add_argument("description", type=str)
product_parser.add_argument("price", type=float)
product_parser.add_argument("quantity", type=int)
product_parser.add_argument("view_type", type=str)
product_parser.add_argument("category_id", type=int)


product= {
    "id": fields.Integer,
    "name": fields.String,
    "img_name":fields.String,
    "mgf_date":fields.String,
    "exp_date":fields.Integer,
    "description": fields.String,
    "price": fields.Float,
    "quantity":fields.Integer,
    "view_type":fields.String,
    "category_id":fields.Integer
}

productList={
    "products":fields.List(fields.Nested(product)),
}

class productApi(Resource):
    @marshal_with(productList)
    def get(self):
        try:
            products=Product.query.all()
            if products:
                return products
            else:
                raise NotFoundError(status_code=400)
        except requests.exceptions.RequestException as e:
            raise NetworkError(status_code=405, message="Error: {}".format(e) )
    @marshal_with(product)
    def put(self, product_id):
        args=product_parser.parse_args()
        name=args.get("name", None)
        img_name=args.get("img_name", None)
        mgf_date=args.get("mgf_date", None)
        exp_date=args.get("exp_date", None)
        description=args.get("description", None)
        price=args.get("price", None)
        quantity=args.get("quantity", None)
        view_type=args.get("view_type", None)
        category_id=args.get("category_id", None)
        if product_id is None:
            raise NotFoundError(status_code=400)
        elif name is None:
            NotFoundError(status_code=400)
        elif img_name is None:
            NotFoundError(status_code=400)
        elif mgf_date is None:
            NotFoundError(status_code=400)
        elif exp_date is None:
            NotFoundError(status_code=400)
        elif description is None:
            NotFoundError(status_code=400)
        elif price is None:
            NotFoundError(status_code=400)
        elif quantity is None:
            NotFoundError(status_code=400)
        elif view_type is None:
            NotFoundError(status_code=400)
        elif category_id is None:
            NotFoundError(status_code=400)
        else:
            try:
                product=Product.query.filter_by(id=product_id).first()
                product.name=name
                product.img_name=img_name
                product.mgf_date=mgf_date
                product.exp_date=exp_date
                product.description=description
                product.price=price
                product.quantity=quantity
                product.view_type=view_type
                product.category_id=category_id
                db.session.commit()
                return product
            except requests.exceptions.RequestException as e:
                db.session.rollback()
                raise NetworkError(status_code=405, message="Error: {}".format(e))
            
    def delete(self, product_id):
        product=Product.query.filter_by(id=product_id).first()
        if product is None:
            raise NotFoundError(status_code=400)            
        else:
            try:
                userproducts = UserProduct.query.filter_by(product_id=product_id).all()
                for userproduct in userproducts:
                    db.session.delete(userproduct)
                    db.session.commit()
                db.session.delete(product)
                db.session.commit()
                return output_json(data={"message":"successfully deleted"}, code=200)
            except requests.exceptions.RequestException as e:
                db.session.rollback()
                raise NetworkError(status_code=405, message="Error: {}".format(e))

    @marshal_with(product)
    def post(self):
        args=product_parser.parse_args()
        name=args.get("name", None)
        img_name=args.get("img_name", None)
        mgf_date=args.get("mgf_date", None)
        exp_date=args.get("exp_date", None)
        description=args.get("description", None)
        price=args.get("price", None)
        quantity=args.get("quantity", None)
        view_type=args.get("view_type", None)
        category_id=args.get("category_id", None)
        if name is None:
            NotFoundError(status_code=400)
        elif img_name is None:
            NotFoundError(status_code=400)
        elif mgf_date is None:
            NotFoundError(status_code=400)
        elif exp_date is None:
            NotFoundError(status_code=400)
        elif description is None:
            NotFoundError(status_code=400)
        elif price is None:
            NotFoundError(status_code=400)
        elif quantity is None:
            NotFoundError(status_code=400)
        elif view_type is None:
            NotFoundError(status_code=400)
        elif category_id is None:
            NotFoundError(status_code=400)
        else:
            try:
                product = Product(name, description, price, category_id, view_type, img_name, mgf_date, exp_date, quantity)
                db.session.add(product)
                db.session.commit()
                return product
            except requests.exceptions.RequestException as e:
                db.session.rollback()
                raise NetworkError(status_code=405, message="Error: {}".format(e))