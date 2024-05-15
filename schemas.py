from marshmallow import Schema, fields




class ItemPlainSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class StorePlainSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class StoreSchema(StorePlainSchema):
    items = fields.List(fields.Nested(ItemPlainSchema()), dump_only=True)

class StoreUpdateSchema(Schema):
    name = fields.Str()


class ItemSchema(ItemPlainSchema):
    store_id = fields.Int(required=True)
    store = fields.Nested(StorePlainSchema(), dump_only=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()



