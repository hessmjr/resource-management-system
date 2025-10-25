-- -----------------------------------------------------
-- Table `user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `user` ;


CREATE TABLE IF NOT EXISTS `user` (
  `username` VARCHAR(50) NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  `password` VARCHAR(32) NOT NULL,
  PRIMARY KEY (`username`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `company`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `company` ;


CREATE TABLE IF NOT EXISTS `company` (
  `username` VARCHAR(50) NOT NULL,
  `headquarters` VARCHAR(50) NULL,
  PRIMARY KEY (`username`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC),
  UNIQUE INDEX `headquarters_UNIQUE` (`headquarters` ASC),
  CONSTRAINT `FK_company_user_username`
    FOREIGN KEY (`username`)
    REFERENCES `user` (`username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `individual`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `individual` ;


CREATE TABLE IF NOT EXISTS `individual` (
  `username` VARCHAR(50) NOT NULL,
  `job_title` VARCHAR(50) NOT NULL,
  `hired_date` DATETIME NOT NULL,
  PRIMARY KEY (`username`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC),
  CONSTRAINT `FK_individual_user_username`
    FOREIGN KEY (`username`)
    REFERENCES `user` (`username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `municipality`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `municipality` ;


CREATE TABLE IF NOT EXISTS `municipality` (
  `username` VARCHAR(50) NOT NULL,
  `population_size` BIGINT NOT NULL,
  PRIMARY KEY (`username`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC),
  CONSTRAINT `FK_municipality_user_username`
    FOREIGN KEY (`username`)
    REFERENCES `user` (`username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `government_agency`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `government_agency` ;


CREATE TABLE IF NOT EXISTS `government_agency` (
  `username` VARCHAR(50) NOT NULL,
  `jurisdiction` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`username`),
  CONSTRAINT `FK_government_agency_user_username`
    FOREIGN KEY (`username`)
    REFERENCES `user` (`username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `incident`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `incident` ;


CREATE TABLE IF NOT EXISTS `incident` (
  `incident_id` CHAR(10) NOT NULL,
  `username` VARCHAR(50) NOT NULL,
  `description` VARCHAR(50) NOT NULL,
  `latitude` DECIMAL NOT NULL,
  `longitude` DECIMAL NOT NULL,
  `incident_date` DATE NOT NULL,
  PRIMARY KEY (`incident_id`),
  INDEX `FK_incident_user_idx` (`username` ASC),
  CONSTRAINT `FK_incident_user`
    FOREIGN KEY (`username`)
    REFERENCES `user` (`username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cost_time_period`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cost_time_period` ;


CREATE TABLE IF NOT EXISTS `cost_time_period` (
  `cost_time_period_id` INT NOT NULL AUTO_INCREMENT,
  `time_period` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`cost_time_period_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `esf`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `esf` ;


CREATE TABLE IF NOT EXISTS `esf` (
  `esf_id` INT NOT NULL,
  `description` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`esf_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `resource`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `resource` ;


CREATE TABLE IF NOT EXISTS `resource` (
  `resource_id` CHAR(10) NOT NULL,
  `cost_time_period_id` INT NOT NULL,
  `username` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `model` VARCHAR(45) NULL,
  `latitude` DECIMAL NOT NULL,
  `longitude` DECIMAL NOT NULL,
  `amount` DECIMAL NOT NULL,
  `primary_esf_id` INT NOT NULL,
  CHECK(latitude >= -90 and latitude <= 90),
  CHECK(longitude >= -180 and longitude <= 180),
  PRIMARY KEY (`resource_id`),
  INDEX `FK_resource_cost_time_period_id_idx` (`cost_time_period_id` ASC),
  INDEX `FK_resource_user_idx` (`username` ASC),
  INDEX `FK_resource_primary_esf_id_idx` (`primary_esf_id` ASC),
  CONSTRAINT `FK_resource_primary_esf_id`
    FOREIGN KEY (`primary_esf_id`)
    REFERENCES `esf` (`esf_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_resource_cost_time_period_id`
    FOREIGN KEY (`cost_time_period_id`)
    REFERENCES `cost_time_period` (`cost_time_period_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_resource_user`
    FOREIGN KEY (`username`)
    REFERENCES `user` (`username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `resource_esf`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `resource_esf` ;


CREATE TABLE IF NOT EXISTS `resource_esf` (
  `resource_id` CHAR(16) NOT NULL,
  `esf_id` INT NOT NULL,
  PRIMARY KEY (`resource_id`, `esf_id`),
  INDEX `FK_resource_esf_esf_idx` (`esf_id` ASC),
  CONSTRAINT `FK_resource_esf_resource`
    FOREIGN KEY (`resource_id`)
    REFERENCES `resource` (`resource_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_resource_esf_esf`
    FOREIGN KEY (`esf_id`)
    REFERENCES `esf` (`esf_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `resource_request_status`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `resource_request_status` ;


CREATE TABLE IF NOT EXISTS `resource_request_status` (
  `resource_request_status_id` INT NOT NULL AUTO_INCREMENT,
  `status` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`resource_request_status_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `resource_request`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `resource_request` ;


CREATE TABLE IF NOT EXISTS `resource_request` (
  `resource_request_id` INT NOT NULL AUTO_INCREMENT,
  `resource_request_status_id` INT NOT NULL,
  `incident_id` CHAR(16) NOT NULL,
  `resource_id` CHAR(16) NOT NULL,
  `start_date` DATE NOT NULL,
  `return_by_date` DATE NOT NULL,
  PRIMARY KEY (`resource_request_id`),
  INDEX `FK_resource_request_resource_request_status_idx` (`resource_request_status_id` ASC),
  INDEX `FK_resource_request_incident_idx` (`incident_id` ASC),
  INDEX `FK_resource_request_resource_idx` (`resource_id` ASC),
  CONSTRAINT `FK_resource_request_resource_request_status`
    FOREIGN KEY (`resource_request_status_id`)
    REFERENCES `resource_request_status` (`resource_request_status_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_resource_request_incident`
    FOREIGN KEY (`incident_id`)
    REFERENCES `incident` (`incident_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_resource_request_resource`
    FOREIGN KEY (`resource_id`)
    REFERENCES `resource` (`resource_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `resource_repair`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `resource_repair` ;


CREATE TABLE IF NOT EXISTS `resource_repair` (
  `resource_repair_id` INT NOT NULL AUTO_INCREMENT,
  `resource_id` VARCHAR(45) NOT NULL,
  `status` VARCHAR(45) NOT NULL,
  `start_date` DATE NOT NULL,
  `ready_by_date` DATE NOT NULL,
  PRIMARY KEY (`resource_repair_id`),
  CONSTRAINT `FK_resource_resource_repair`
    FOREIGN KEY (`resource_id`)
    REFERENCES `resource` (`resource_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `capability`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `capability` ;


CREATE TABLE IF NOT EXISTS `capability` (
  `resource_id` CHAR(16) NOT NULL,
  `capability` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`resource_id`, `capability`),
  CONSTRAINT `FK_resource_capability`
    FOREIGN KEY (`resource_id`)
    REFERENCES `resource` (`resource_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Data for table `cost_time_period`
-- -----------------------------------------------------
START TRANSACTION;


INSERT INTO `cost_time_period` (`cost_time_period_id`, `time_period`) VALUES (1, 'Hour');
INSERT INTO `cost_time_period` (`cost_time_period_id`, `time_period`) VALUES (2, 'Day');
INSERT INTO `cost_time_period` (`cost_time_period_id`, `time_period`) VALUES (3, 'Week');

COMMIT;


-- -----------------------------------------------------
-- Data for table `resource_request_status`
-- -----------------------------------------------------
START TRANSACTION;


INSERT INTO `resource_request_status` (`resource_request_status_id`, `status`) VALUES (1, 'New');
INSERT INTO `resource_request_status` (`resource_request_status_id`, `status`) VALUES (2, 'Deployed');
INSERT INTO `resource_request_status` (`resource_request_status_id`, `status`) VALUES (3, 'Rejected');
INSERT INTO `resource_request_status` (`resource_request_status_id`, `status`) VALUES (4, 'Returned');

COMMIT;


-- -----------------------------------------------------
-- Data for table `esf`
-- -----------------------------------------------------
START TRANSACTION;


INSERT INTO `esf` (`esf_id`, `description`) VALUES (1, 'Transportation');
INSERT INTO `esf` (`esf_id`, `description`) VALUES (2, 'Communications');
INSERT INTO `esf` (`esf_id`, `description`) VALUES (3, 'Public Works and Engineering');
INSERT INTO `esf` (`esf_id`, `description`) VALUES (4, 'Firefighting');
INSERT INTO `esf` (`esf_id`, `description`) VALUES (5, 'Emergency Management');
INSERT INTO `esf` (`esf_id`, `description`) VALUES (6, 'Mass Care, Emergency Assistance, Housing, and Human Services');
INSERT INTO `esf` (`esf_id`, `description`) VALUES (7, 'Logistics Management and Resource Support');
INSERT INTO `esf` (`esf_id`, `description`) VALUES (8, 'Public Health and Medical Services');
INSERT INTO `esf` (`esf_id`, `description`) VALUES (9, 'Search and Rescue');
INSERT INTO `esf` (`esf_id`, `description`) VALUES (10, 'Oil and Hazardous Materials Response');
INSERT INTO `esf` (`esf_id`, `description`) VALUES (11, 'Agriculture and Natural Resources');
INSERT INTO `esf` (`esf_id`, `description`) VALUES (12, 'Energy');
INSERT INTO `esf` (`esf_id`, `description`) VALUES (13, 'Public Safety and Security');
INSERT INTO `esf` (`esf_id`, `description`) VALUES (14, 'Long-Term Community Recovery');
INSERT INTO `esf` (`esf_id`, `description`) VALUES (15, 'External Affairs');

COMMIT;


-- -----------------------------------------------------
-- Haversine distance formula
-- -----------------------------------------------------
DELIMITER $$
DROP FUNCTION IF EXISTS distance_formula$$

CREATE FUNCTION distance_formula(
        lat_one FLOAT, long_one FLOAT,
        lat_two FLOAT, long_two FLOAT
    ) RETURNS FLOAT
    NO SQL DETERMINISTIC

BEGIN
    RETURN 111.045 * DEGREES(ACOS(
        COS(RADIANS(lat_one)) *
        COS(RADIANS(lat_two)) *
        COS(RADIANS(long_one) - RADIANS(long_two)) +
        SIN(RADIANS(lat_one)) * SIN(RADIANS(lat_two))
    ));

END$$
DELIMITER ;
