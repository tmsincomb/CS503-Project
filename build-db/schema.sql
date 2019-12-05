# SHOW DATABASES;

# CREATE DATABASE S_aureus;
# USE S_aureus;
# SHOW TABLES;

SET FOREIGN_KEY_CHECKS = 0; # removes FK rules (FALSE)
DROP TABLE IF EXISTS STRAINS CASCADE; 
DROP TABLE IF EXISTS METADATA CASCADE;
DROP TABLE IF EXISTS GENES CASCADE;
DROP TABLE IF EXISTS MECHANISMS CASCADE;
SET FOREIGN_KEY_CHECKS = 1; # activates FK rules (TRUE)

CREATE TABLE IF NOT EXISTS STRAINS(
  strain_id VARCHAR(255) NOT NULL, 
	strain_name VARCHAR(255) NOT NULL, 
	PRIMARY KEY (strain_id)
);

CREATE TABLE IF NOT EXISTS METADATA(
  biosample_id VARCHAR(255) NOT NULL,
  strain_id VARCHAR(255) NOT NULL,
	gene_count INT NOT NULL,
	protein_count INT NOT NULL,
  genome_release_date DATE NOT NULL,
  genome_modify_date DATE NOT NULL,
  organism VARCHAR(255) NOT NULL,
	PRIMARY KEY (biosample_id, strain_id),
  FOREIGN KEY (strain_id) REFERENCES STRAINS(strain_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS GENES(
	gene_name VARCHAR(255) NOT NULL,
  strain_id VARCHAR(255) NOT NULL,
	PRIMARY KEY (gene_name, strain_id),
  FOREIGN KEY (strain_id) REFERENCES STRAINS(strain_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS GENE_INFO(
  gene_description VARCHAR(255) NOT NULL,
  gene_name VARCHAR(255) NOT NULL,
	PRIMARY KEY (gene_description, gene_name),
  FOREIGN KEY (gene_name) REFERENCES GENES(gene_name) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS MECHANISMS(
	gene_name VARCHAR(255) NOT NULL,
	gene_qualifier VARCHAR(255) NOT NULL,
  gene_ontology_term VARCHAR(255) NOT NULL,
  gene_ontology_source VARCHAR(255) NOT NULL,
	PRIMARY KEY (gene_name),
  FOREIGN KEY (gene_name) REFERENCES GENES(gene_name) ON DELETE CASCADE ON UPDATE CASCADE
);


ALTER TABLE STRAINS
  ADD COLUMN strain_resistance_status VARCHAR(255) NOT NULL AFTER strain_name;

INSERT INTO STRAINS
  VALUES
  ('CP033506', 'ATCC BAA-39', 'MRSA'),
  ('NZ_CP007176', 'USA300-ISMMS1', 'MRSA'),
  ('CP000253', 'NCTC8325', 'MSSA');

UPDATE STRAINS SET strain_resistance_status = 'MSSA' WHERE strain_id = 'CP000253';


INSERT INTO METADATA
  VALUES
  ('SAMN09635551', 'CP033506', 2975, 2411, '2018-11-26', '2019-01-30', 'Staphylococcus aureus'),
  ('SAMN03081531', 'NZ_CP007176', 3054, 2889, '2014-02-12', '2019-08-27', 'Staphylococcus aureus'),
  ('SAMN02604235', 'CP000253', 2872, 2767, '2006-02-13', '2016-08-03', 'Staphylococcus aureus');

INSERT INTO GENES
  VALUES
  ('mecA', 'CP033506'),
  ('mecA', 'NZ_CP007176'),
  ('mecR1', 'CP033506'),
  ('mecR1', 'NZ_CP007176'),
  ('iscS', 'CP033506'),
  ('iscS', 'NZ_CP007176'),
  ('dnaA', 'CP033506'),
  ('dnaA', 'NZ_CP007176'),
  ('dnaA', 'CP000253'),
  ('gltB', 'NZ_CP007176'),
  ('gltB', 'CP000253');


INSERT INTO GENE_INFO
  VALUES
  ('Adapter protein', 'mecA'),
  ('Methicillin resistance/beta-lactam signal transducer', 'mecR1'),
  ('Cysteine desulfurase', 'mecR1'),
  ('chromosomal replication initiator', 'dnaA'),
  ('glutamate synthase large subunit', 'gltB');

UPDATE GENE_INFO SET gene_name = 'iscS' WHERE gene_description = 'Cysteine desulfurase';


INSERT INTO MECHANISMS
  VALUES
  ('mecA', 'enables penicillin binding', 'GO:0008658', 'InterPro'),
  ('mecR1', 'involved_in response to antibiotic', 'GO:0046677', 'UniProt'),
  ('iscS', 'enables cysteine desulfurase activity', 'GO:0031071', 'UniProt'),
  ('dnaA', 'involved_in DNA replication initiation', 'GO:0006270', 'InterPro'),
  ('gltB', 'enables glutamate synthase activity', 'GO:0015930', 'InterPro');



# EXPLAIN STRAINS; # DESCRIBE STRAINS;
# SELECT * FROM MECHANISMS;
# SELECT * FROM STRAINS as S JOIN METADATA as M ON S.strain_id = M.strain_id;

