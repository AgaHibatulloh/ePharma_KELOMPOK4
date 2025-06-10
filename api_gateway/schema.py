import graphene
import requests

class Obat(graphene.ObjectType):
    id = graphene.Int()
    nama_obat = graphene.String()
    stok = graphene.Int()

class Pesanan(graphene.ObjectType):
    id = graphene.Int()
    nama_pemesan = graphene.String()
    jumlah = graphene.Int()
    status = graphene.String()

class Query(graphene.ObjectType):
    obat = graphene.List(Obat)
    pesanan = graphene.List(Pesanan)
    
    def resolve_obat(self, info):
        try:
            response = requests.get('http://inventory-service:5002/api/obat')
            return response.json()
        except Exception as e:
            print(f"Error fetching obat: {e}")
            return []
    
    def resolve_pesanan(self, info):
        try:
            response = requests.get('http://order-service:5003/api/orders')
            return response.json()
        except Exception as e:
            print(f"Error fetching pesanan: {e}")
            return []

schema = graphene.Schema(query=Query)