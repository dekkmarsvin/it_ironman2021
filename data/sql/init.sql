BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Users" (
	"UID"	INTEGER NOT NULL UNIQUE,
	"TYPE"	INTEGER NOT NULL,
	"NAME"	TEXT NOT NULL,
	"PWDHASH"	TEXT NOT NULL,
	PRIMARY KEY("UID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Cards" (
	"CID"	INTEGER NOT NULL UNIQUE,
	"Bind_User"	INTEGER,
	"Balance"	INTEGER NOT NULL DEFAULT 0,
	"Frozen"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("CID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "transmit_logs" (
	"ID"	INTEGER NOT NULL UNIQUE,
	"TYPE"	INTEGER NOT NULL DEFAULT 0,
	"STATUS"	INTEGER NOT NULL DEFAULT 0,
	"Remark"	TEXT,
	PRIMARY KEY("ID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Order_logs" (
	"ID"	INTEGER NOT NULL UNIQUE,
	"TID"	INTEGER,
	"Valid"	INTEGER NOT NULL DEFAULT 0,
	"Shipment_Status"	INTEGER NOT NULL DEFAULT 0,
	"Order_INFO"	TEXT,
	PRIMARY KEY("ID" AUTOINCREMENT)
);
COMMIT;