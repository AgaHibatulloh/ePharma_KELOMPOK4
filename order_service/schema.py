import graphene
from models import get_all_pesanan

class Pesanan(graphene.ObjectType):
    id = graphene.Int()
    nama_pemesan = graphene.String()
    jumlah = graphene.Int()
    status = graphene.String()

class Query(graphene.ObjectType):
    pesanan = graphene.List(Pesanan)
    
    def resolve_pesanan(self, info):
        return get_all_pesanan()

schema = graphene.Schema(query=Query)