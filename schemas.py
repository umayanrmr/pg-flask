from marshmallow import Schema, fields




class TagPlainSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

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
    tags = fields.List(fields.Nested(TagPlainSchema()) , dump_only=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()





class TagSchema(TagPlainSchema):
    store_id = fields.Int(required=True)
    store = fields.Nested(StorePlainSchema(), dump_only=True)
    items = fields.List(fields.Nested(ItemPlainSchema()) , dump_only=True)



class TagItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    # load_only=True tells python to not return this property to user
    password = fields.Str(required=True, load_only=True)