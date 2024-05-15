from marshmallow import Schema, fields


class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Int(required=True)



class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()




class StoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)



class StoreUpdateSchema(Schema):
    name = fields.Str()