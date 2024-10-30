# a


about the number of start of the repository,
I disided that is unnecessary to fetch all the repository but to ....

Swagger UI


http://127.0.0.1:8000/docs



sync type to frontend:
pip install datamodel-code-generator
curl -o openapi.json http://localhost:8000/openapi.json
datamodel-codegen --input openapi.json --output src/app/models.ts --input-file-type openapi
