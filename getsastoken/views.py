from rest_framework.decorators import api_view
from rest_framework.response import Response
from azure.storage.blob import generate_blob_sas, BlobSasPermissions, BlobServiceClient
from datetime import datetime, timedelta

@api_view(['POST'])
def generate_sas_token(request):
    container_name = request.data.get('container_name')
    blob_name = request.data.get('blob_name')

    if not container_name or not blob_name:
        return Response({'error': 'Container name and blob name are required'}, status=400)

    account_key = request.data.get('storage_key')
    account_url = 'https://allrestorage1.blob.core.windows.net/'

    blob_service_client = BlobServiceClient(account_url=account_url, credential=account_key)

    sas_token = generate_blob_sas(
        blob_service_client.account_name,
        container_name=container_name,
        blob_name=blob_name,
        account_key=blob_service_client.credential.account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=2),  # Expires in 2 hours
        protocol="https"
    )

    sas_url = f"https://allrestorage1.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"
    return Response({'sas_url': sas_url})
