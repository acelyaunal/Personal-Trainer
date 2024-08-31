BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "user" (
	"id"	INTEGER NOT NULL,
	"firstname"	VARCHAR(150) NOT NULL,
	"lastname"	VARCHAR(150) NOT NULL,
	"email"	VARCHAR(150) NOT NULL,
	"gender"	VARCHAR(50) NOT NULL,
	"height"	INTEGER NOT NULL,
	"weight"	INTEGER NOT NULL,
	"dob"	DATE NOT NULL,
	"password"	VARCHAR(150) NOT NULL,
	"created_at"	DATETIME,
	PRIMARY KEY("id"),
	UNIQUE("email")
);
CREATE TABLE IF NOT EXISTS "exercise_type" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(100) NOT NULL,
	"description"	TEXT NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "user_history" (
	"id"	INTEGER NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"attribute_name"	VARCHAR(50) NOT NULL,
	"old_value"	VARCHAR(150) NOT NULL,
	"new_value"	VARCHAR(150) NOT NULL,
	"updated_at"	DATETIME,
	FOREIGN KEY("user_id") REFERENCES "user"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "exercise" (
	"id"	INTEGER NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"exercise_type_id"	INTEGER NOT NULL,
	"repetitions"	INTEGER,
	"timestamp"	DATETIME,
	"duration"	INTEGER,
	FOREIGN KEY("user_id") REFERENCES "user"("id"),
	FOREIGN KEY("exercise_type_id") REFERENCES "exercise_type"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "session" (
	"session_id"	INTEGER NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"start_time"	DATETIME NOT NULL,
	"end_time"	DATETIME,
	FOREIGN KEY("user_id") REFERENCES "user"("id"),
	PRIMARY KEY("session_id")
);
CREATE TABLE IF NOT EXISTS "weight_height_update" (
	"id"	INTEGER NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"height"	INTEGER NOT NULL,
	"weight"	INTEGER NOT NULL,
	"bmi"	FLOAT NOT NULL,
	"updated_at"	DATETIME,
	FOREIGN KEY("user_id") REFERENCES "user"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "password_reset" (
	"id"	INTEGER NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"token"	VARCHAR(100) NOT NULL,
	"created_at"	DATETIME,
	FOREIGN KEY("user_id") REFERENCES "user"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "feedback" (
	"id"	INTEGER NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"message"	TEXT NOT NULL,
	"created_at"	DATETIME,
	FOREIGN KEY("user_id") REFERENCES "user"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "email_log" (
	"id"	INTEGER NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"recipient_email"	VARCHAR(150) NOT NULL,
	"subject"	VARCHAR(255) NOT NULL,
	"message"	TEXT NOT NULL,
	"sent_at"	DATETIME,
	FOREIGN KEY("user_id") REFERENCES "user"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "session_exercise" (
	"id"	INTEGER NOT NULL,
	"session_id"	INTEGER NOT NULL,
	"exercise_id"	INTEGER NOT NULL,
	FOREIGN KEY("session_id") REFERENCES "session"("session_id"),
	FOREIGN KEY("exercise_id") REFERENCES "exercise"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "user_session" (
	"id"	INTEGER NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"login_time"	DATETIME NOT NULL,
	"logout_time"	DATETIME,
	FOREIGN KEY("user_id") REFERENCES "user"("id"),
	PRIMARY KEY("id")
);
INSERT INTO "user" VALUES (1,'Açelya','Ünal','acelyaunal1@hotmail.com','female',178,50,'2000-07-19','Sifre.yenilensin','2024-05-21 02:22:39.973267');
INSERT INTO "exercise_type" VALUES (1,'squat','Squat strengthens the legs, hips, and back muscles. Feet are shoulder-width apart, body leans back, and knees bend. It improves balance and supports calorie burning.');
INSERT INTO "exercise_type" VALUES (2,'plank','Plank strengthens the abdominal and core muscles. The body is held in a straight line and elbows are placed on the ground. It tightens the abdominal muscles and improves posture.');
INSERT INTO "exercise_type" VALUES (3,'birddog','BirdDog works the back and abdominal muscles. Hands and knees are on the ground, one arm and the opposite leg are raised straight. It strengthens core muscles and balanced movements.');
INSERT INTO "exercise_type" VALUES (4,'dumbbellcurl','Dumbbell Curl strengthens arm muscles. Dumbbells are held with palms facing up while standing, and arms are bent. It works the biceps muscles.');
INSERT INTO "exercise_type" VALUES (5,'kneetouch','Knee Touch works the abdominal and hip muscles. While lying on the ground, hands are raised towards the knees. It strengthens core muscles and improves flexibility.');
INSERT INTO "user_history" VALUES (1,1,'height','170','168','2024-05-21 02:40:15.160967');
INSERT INTO "user_history" VALUES (2,1,'dob','2000-07-18','2000-07-18','2024-05-21 02:40:15.160983');
INSERT INTO "user_history" VALUES (3,1,'weight','65','66','2024-05-21 02:41:02.423267');
INSERT INTO "user_history" VALUES (4,1,'dob','2000-07-18','2000-07-18','2024-05-21 02:41:02.423275');
INSERT INTO "user_history" VALUES (5,1,'dob','2000-07-18','2000-07-19','2024-05-21 02:41:19.429410');
INSERT INTO "user_history" VALUES (6,1,'gender','female','other','2024-05-21 02:41:28.686728');
INSERT INTO "user_history" VALUES (7,1,'dob','2000-07-19','2000-07-19','2024-05-21 02:41:28.686740');
INSERT INTO "user_history" VALUES (8,1,'weight','66','67','2024-05-21 02:45:05.415964');
INSERT INTO "user_history" VALUES (9,1,'dob','2000-07-19','2000-07-19','2024-05-21 02:45:05.415978');
INSERT INTO "user_history" VALUES (10,1,'height','168','169','2024-05-21 02:45:16.698012');
INSERT INTO "user_history" VALUES (11,1,'dob','2000-07-19','2000-07-19','2024-05-21 02:45:16.698021');
INSERT INTO "user_history" VALUES (12,1,'gender','other','female','2024-05-21 03:04:35.805149');
INSERT INTO "user_history" VALUES (13,1,'weight','67','69','2024-05-21 03:04:41.689899');
INSERT INTO "user_history" VALUES (14,1,'height','169','168','2024-05-21 03:05:12.116325');
INSERT INTO "user_history" VALUES (15,1,'password','Acelya.12345','Acelya.123456','2024-05-21 03:05:37.268189');
INSERT INTO "user_history" VALUES (16,1,'height','168','150','2024-05-21 03:06:11.347772');
INSERT INTO "user_history" VALUES (17,1,'weight','69','80','2024-05-21 03:06:11.347782');
INSERT INTO "user_history" VALUES (18,1,'height','150','168','2024-05-21 03:23:27.110226');
INSERT INTO "user_history" VALUES (19,1,'weight','80','69','2024-05-21 03:23:27.110231');
INSERT INTO "user_history" VALUES (20,1,'dob','2000-07-19','2000-07-19','2024-05-21 03:23:27.110231');
INSERT INTO "user_history" VALUES (21,1,'password','Acelya.12345','Acelya.123456','2024-05-21 03:23:27.110232');
INSERT INTO "user_history" VALUES (22,1,'height','168','190','2024-05-21 03:23:37.018665');
INSERT INTO "user_history" VALUES (23,1,'weight','69','50','2024-05-21 03:23:37.018720');
INSERT INTO "user_history" VALUES (24,1,'dob','2000-07-19','2000-07-19','2024-05-21 03:23:37.018722');
INSERT INTO "user_history" VALUES (25,1,'height','190','178','2024-05-21 04:22:32.504369');
INSERT INTO "user_history" VALUES (26,1,'dob','2000-07-19','2000-07-19','2024-05-21 04:22:32.504374');
INSERT INTO "user_history" VALUES (27,1,'password','Yeter.Kafayı.Yedim','Sifre.yenilensin','2024-05-21 04:22:32.504375');
INSERT INTO "exercise" VALUES (1,1,1,0,'2024-05-21 02:22:46.767414',NULL);
INSERT INTO "exercise" VALUES (2,1,2,0,'2024-05-21 02:22:46.770566',NULL);
INSERT INTO "exercise" VALUES (3,1,1,0,'2024-05-21 02:32:05.346800',NULL);
INSERT INTO "exercise" VALUES (4,1,2,0,'2024-05-21 02:32:05.351195',NULL);
INSERT INTO "exercise" VALUES (5,1,1,0,'2024-05-21 02:57:23.571692',NULL);
INSERT INTO "exercise" VALUES (6,1,2,0,'2024-05-21 02:57:23.576800',NULL);
INSERT INTO "exercise" VALUES (7,1,1,0,'2024-05-21 02:57:54.744370',NULL);
INSERT INTO "exercise" VALUES (8,1,2,0,'2024-05-21 02:57:54.747381',NULL);
INSERT INTO "exercise" VALUES (9,1,1,0,'2024-05-21 03:27:56.172568',NULL);
INSERT INTO "exercise" VALUES (10,1,2,0,'2024-05-21 03:27:56.176224',NULL);
INSERT INTO "exercise" VALUES (11,1,1,0,'2024-05-21 03:32:55.543723',NULL);
INSERT INTO "exercise" VALUES (12,1,2,0,'2024-05-21 03:32:55.544533',NULL);
INSERT INTO "exercise" VALUES (13,1,1,0,'2024-05-21 03:52:21.635827',NULL);
INSERT INTO "exercise" VALUES (14,1,2,0,'2024-05-21 03:52:21.639850',NULL);
INSERT INTO "exercise" VALUES (15,1,1,0,'2024-05-21 04:00:23.377810',NULL);
INSERT INTO "exercise" VALUES (16,1,2,0,'2024-05-21 04:00:23.393917',NULL);
INSERT INTO "exercise" VALUES (17,1,1,0,'2024-05-21 04:00:39.288395',NULL);
INSERT INTO "exercise" VALUES (18,1,2,0,'2024-05-21 04:00:39.294581',NULL);
INSERT INTO "exercise" VALUES (19,1,1,0,'2024-05-21 04:00:45.196760',NULL);
INSERT INTO "exercise" VALUES (20,1,2,0,'2024-05-21 04:00:45.203332',NULL);
INSERT INTO "exercise" VALUES (21,1,1,0,'2024-05-21 04:00:46.104924',NULL);
INSERT INTO "exercise" VALUES (22,1,2,0,'2024-05-21 04:00:46.107259',NULL);
INSERT INTO "exercise" VALUES (23,1,1,0,'2024-05-21 04:00:49.098219',NULL);
INSERT INTO "exercise" VALUES (24,1,2,0,'2024-05-21 04:00:49.100884',NULL);
INSERT INTO "exercise" VALUES (25,1,1,0,'2024-05-21 04:00:56.620928',NULL);
INSERT INTO "exercise" VALUES (26,1,2,0,'2024-05-21 04:00:56.626683',NULL);
INSERT INTO "exercise" VALUES (27,1,1,0,'2024-05-21 04:00:59.843058',NULL);
INSERT INTO "exercise" VALUES (28,1,2,0,'2024-05-21 04:00:59.847034',NULL);
INSERT INTO "exercise" VALUES (29,1,1,0,'2024-05-21 04:01:06.610872',NULL);
INSERT INTO "exercise" VALUES (30,1,2,0,'2024-05-21 04:01:06.617932',NULL);
INSERT INTO "exercise" VALUES (31,1,1,0,'2024-05-21 04:01:09.749014',NULL);
INSERT INTO "exercise" VALUES (32,1,2,0,'2024-05-21 04:01:09.751656',NULL);
INSERT INTO "exercise" VALUES (33,1,1,0,'2024-05-21 04:01:23.291707',NULL);
INSERT INTO "exercise" VALUES (34,1,2,0,'2024-05-21 04:01:23.295001',NULL);
INSERT INTO "exercise" VALUES (35,1,1,0,'2024-05-21 04:08:47.759567',NULL);
INSERT INTO "exercise" VALUES (36,1,2,0,'2024-05-21 04:08:47.771158',NULL);
INSERT INTO "exercise" VALUES (37,1,1,0,'2024-05-21 04:09:31.773704',NULL);
INSERT INTO "exercise" VALUES (38,1,2,0,'2024-05-21 04:09:31.784076',NULL);
INSERT INTO "session" VALUES (1,1,'2024-05-21 04:00:23.365669','2024-05-21 04:00:23.365674');
INSERT INTO "session" VALUES (2,1,'2024-05-21 04:08:47.745157','2024-05-21 04:08:47.745163');
INSERT INTO "session" VALUES (3,1,'2024-05-21 04:09:31.764214','2024-05-21 04:09:31.764218');
INSERT INTO "weight_height_update" VALUES (1,1,168,69,24.4,'2024-05-21 03:23:27.114768');
INSERT INTO "weight_height_update" VALUES (2,1,190,50,13.9,'2024-05-21 03:23:37.025325');
INSERT INTO "weight_height_update" VALUES (3,1,178,50,15.8,'2024-05-21 04:22:32.509090');
INSERT INTO "password_reset" VALUES (1,1,'ImFjZWx5YXVuYWwxQGhvdG1haWwuY29tIg.ZkwfwQ.DDIR7ponVjOJOU_Dnd-rnsVxFRI','2024-05-21 04:14:59.215549');
INSERT INTO "feedback" VALUES (1,1,'deneme mail','2024-05-21 03:29:50.529822');
INSERT INTO "feedback" VALUES (2,1,'deneme mail','2024-05-21 03:30:03.702038');
INSERT INTO "email_log" VALUES (1,1,'acelyaunal1@hotmail.com','Password Reset Request','Hi Açelya,

To reset your password, please click the link below:
http://127.0.0.1:8085/reset_password/ImFjZWx5YXVuYWwxQGhvdG1haWwuY29tIg.ZkwYzg.I1JVPJvr2yZfeKEUODXDKPyfNVE

If you did not make this request, please ignore this email.','2024-05-21 03:45:19.398280');
INSERT INTO "email_log" VALUES (2,1,'acelyaunal1@hotmail.com','Password Reset Request','Hi Açelya,

To reset your password, please click the link below:
http://127.0.0.1:8085/reset_password/ImFjZWx5YXVuYWwxQGhvdG1haWwuY29tIg.ZkwY7A.hrvg5ZJMVkO7GLZHtfAcQYhcvcU

If you did not make this request, please ignore this email.','2024-05-21 03:45:49.923699');
INSERT INTO "session_exercise" VALUES (1,1,15);
INSERT INTO "session_exercise" VALUES (2,1,16);
INSERT INTO "session_exercise" VALUES (3,2,35);
INSERT INTO "session_exercise" VALUES (4,2,36);
INSERT INTO "session_exercise" VALUES (5,3,37);
INSERT INTO "session_exercise" VALUES (6,3,38);
INSERT INTO "user_session" VALUES (1,1,'2024-05-21 02:31:30.081004',NULL);
INSERT INTO "user_session" VALUES (2,1,'2024-05-21 02:31:59.875957',NULL);
INSERT INTO "user_session" VALUES (3,1,'2024-05-21 02:44:58.280012',NULL);
INSERT INTO "user_session" VALUES (4,1,'2024-05-21 02:57:18.481270',NULL);
INSERT INTO "user_session" VALUES (5,1,'2024-05-21 03:13:07.117522',NULL);
INSERT INTO "user_session" VALUES (6,1,'2024-05-21 03:24:16.296167',NULL);
INSERT INTO "user_session" VALUES (7,1,'2024-05-21 03:27:34.136245','2024-05-21 03:27:57.272953');
INSERT INTO "user_session" VALUES (8,1,'2024-05-21 03:29:42.478490',NULL);
INSERT INTO "user_session" VALUES (9,1,'2024-05-21 03:41:55.251320',NULL);
INSERT INTO "user_session" VALUES (10,1,'2024-05-21 03:46:10.194888',NULL);
INSERT INTO "user_session" VALUES (11,1,'2024-05-21 03:52:15.582184','2024-05-21 03:53:10.392934');
INSERT INTO "user_session" VALUES (12,1,'2024-05-21 04:00:18.044442','2024-05-21 04:08:49.095994');
INSERT INTO "user_session" VALUES (13,1,'2024-05-21 04:08:51.712956',NULL);
INSERT INTO "user_session" VALUES (14,1,'2024-05-21 04:15:24.233325',NULL);
COMMIT;
