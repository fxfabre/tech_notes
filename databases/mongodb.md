```yaml
version: '3.7'

services:
  mongodb_container:
    image: mongo:4.2.9
    container_name: mongo_name
    env_file:
      - .env
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: rootpassword
    ports:
      - 27017:27017
    volumes:
      - ./mongo_data/mongo_db:/data/db
```

apt install mongodb-clients
mongo admin -u root -p rootpassword

Show databases: `show dbs`

Create / use database : `use mydatabase`

Show collections : `show collections`

select * : `db.your_collection_name.find()`

insert : `db.your_collection_name.save({"name":"Sony AK"})`
