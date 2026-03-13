1. docker exec -it configsvr1 mongosh --eval "rs.initiate({_id:'cfgrs',configsvr:true,members:[{_id:0,host:'configsvr1:27017'},{_id:1,host:'configsvr2:27017'},{_id:2,host:'configsvr3:27017'}]})"
2. docker exec -it shard1 mongosh --eval "rs.initiate({_id:'shard1rs',members:[{_id:0,host:'shard1:27017'}]})"
docker exec -it shard2 mongosh --eval "rs.initiate({_id:'shard2rs',members:[{_id:0,host:'shard2:27017'}]})"
3. docker exec -it mongos mongosh --eval "sh.addShard('shard1rs/shard1:27017')"
docker exec -it mongos mongosh --eval "sh.addShard('shard2rs/shard2:27017')"
4. docker exec -it mongos mongosh --eval "sh.enableSharding('UniversityDB')"
5. docker exec -it mongos mongosh --eval "db.students.createIndex({ student_id: 'hashed' })"
docker exec -it mongos mongosh --eval "db.grades.createIndex({ student_id: 'hashed', discipline_id: 1 })"
6. docker exec -it mongos mongosh --eval "sh.shardCollection('UniversityDB.students', { student_id: 'hashed' })"
docker exec -it mongos mongosh --eval "sh.shardCollection('UniversityDB.grades', { student_id: 'hashed', discipline_id: 1 })"
7. docker exec -it mongos mongoimport --db UniversityDB --collection students --drop --jsonArray /data/import/students.json
docker exec -it mongos mongoimport --db UniversityDB --collection disciplines --drop --jsonArray /data/import/disciplines.json
docker exec -it mongos mongoimport --db UniversityDB --collection professors --drop --jsonArray /data/import/professors.json
docker exec -it mongos mongoimport --db UniversityDB --collection grades --drop --jsonArray /data/import/grades.json
8. docker exec -it mongos mongosh UniversityDB --eval "db.students.createIndex({ student_id: 1 }, { unique: true })"
docker exec -it mongos mongosh UniversityDB --eval "db.students.createIndex({ group: 1 })"
docker exec -it mongos mongosh UniversityDB --eval "db.students.createIndex({ last_name: 1, first_name: 1 })"
docker exec -it mongos mongosh UniversityDB --eval "db.disciplines.createIndex({ name: 1 })"
docker exec -it mongos mongosh UniversityDB --eval "db.professors.createIndex({ last_name: 1, first_name: 1 })"
docker exec -it mongos mongosh UniversityDB --eval "db.grades.createIndex({ student_id: 1, discipline_name: 1 })"
docker exec -it mongos mongosh UniversityDB --eval "db.grades.createIndex({ student_id: 1, grade: 1 })"
