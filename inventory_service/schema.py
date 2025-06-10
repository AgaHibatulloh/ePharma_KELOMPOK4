import graphene

from models import get_all_obat, get_all_kategori

class Obat(graphene.ObjectType):
    id = graphene.Int()
    nama_obat = graphene.String()
    stok = graphene.Int()
    nama_kategori = graphene.String()

class Kategori(graphene.ObjectType):
    id = graphene.Int()
    nama_kategori = graphene.String()

class Query(graphene.ObjectType):
    obat = graphene.List(Obat)
    kategori = graphene.List(Kategori)
    
    def resolve_obat(self, info):
        return get_all_obat()
    
    def resolve_kategori(self, info):
        return get_all_kategori()

schema = graphene.Schema(query=Query)