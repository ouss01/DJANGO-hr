BEGIN;
--
-- Alter field date_fin on tache
--
CREATE TABLE "new__EmployeeApp_tache" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "date_fin" date NULL, "titre" varchar(100) NOT NULL, "description" text NOT NULL, "budget" decimal NOT NULL, "budget_min" decimal NOT NULL, "date_debut" date NOT NULL, "presence" bool NULL, "poste_id" bigint NOT NULL REFERENCES "EmployeeApp_poste" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "new__EmployeeApp_tache" ("id", "titre", "description", "budget", "budget_min", "date_debut", "presence", "poste_id", "date_fin") SELECT "id", "titre", "description", "budget", "budget_min", "date_debut", "presence", "poste_id", "date_fin" FROM "EmployeeApp_tache";
DROP TABLE "EmployeeApp_tache";
ALTER TABLE "new__EmployeeApp_tache" RENAME TO "EmployeeApp_tache";
CREATE INDEX "EmployeeApp_tache_poste_id_369aaac4" ON "EmployeeApp_tache" ("poste_id");
--
-- Create model Affectation
--
CREATE TABLE "EmployeeApp_affectation" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "ratio" decimal NOT NULL, "employee_id" bigint NOT NULL REFERENCES "EmployeeApp_employee" ("id") DEFERRABLE INITIALLY DEFERRED, "poste_id" bigint NOT NULL REFERENCES "EmployeeApp_poste" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE UNIQUE INDEX "EmployeeApp_affectation_employee_id_poste_id_ef150874_uniq" ON "EmployeeApp_affectation" ("employee_id", "poste_id");
CREATE INDEX "EmployeeApp_affectation_employee_id_7b1cbea3" ON "EmployeeApp_affectation" ("employee_id");
CREATE INDEX "EmployeeApp_affectation_poste_id_223ef3da" ON "EmployeeApp_affectation" ("poste_id");
COMMIT;
