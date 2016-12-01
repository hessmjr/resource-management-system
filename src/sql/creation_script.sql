-- -----------------------------------------------------
-- Schema emergency_response_system
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `emergency_response_system` ;


-- -----------------------------------------------------
-- Schema emergency_response_system
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `emergency_response_system` DEFAULT CHARACTER SET utf8 ;
USE `emergency_response_system` ;


-- -----------------------------------------------------
-- Table `emergency_response_system`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `emergency_response_system`.`user` ;


CREATE TABLE IF NOT EXISTS `emergency_response_system`.`user` (
  `username` VARCHAR(50) NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  `password` VARCHAR(32) NOT NULL,
  PRIMARY KEY (`username`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC))
ENGINE = InnoDB;




-- -----------------------------------------------------
-- Table `emergency_response_system`.`company`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `emergency_response_system`.`company` ;


CREATE TABLE IF NOT EXISTS `emergency_response_system`.`company` (
  `username` VARCHAR(50) NOT NULL,
  `headquarters` VARCHAR(50) NULL,
  PRIMARY KEY (`username`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC),
  UNIQUE INDEX `headquarters_UNIQUE` (`headquarters` ASC),
  CONSTRAINT `FK_company_user_username`
    FOREIGN KEY (`username`)
    REFERENCES `emergency_response_system`.`user` (`username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;




-- -----------------------------------------------------
-- Table `emergency_response_system`.`individual`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `emergency_response_system`.`individual` ;


CREATE TABLE IF NOT EXISTS `emergency_response_system`.`individual` (
  `username` VARCHAR(50) NOT NULL,
  `job_title` VARCHAR(50) NOT NULL,
  `hired_date` DATETIME NOT NULL,
  PRIMARY KEY (`username`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC),
  CONSTRAINT `FK_individual_user_username`
    FOREIGN KEY (`username`)
    REFERENCES `emergency_response_system`.`user` (`username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;




-- -----------------------------------------------------
-- Table `emergency_response_system`.`municipality`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `emergency_response_system`.`municipality` ;


CREATE TABLE IF NOT EXISTS `emergency_response_system`.`municipality` (
  `username` VARCHAR(50) NOT NULL,
  `population_size` BIGINT NOT NULL,
  PRIMARY KEY (`username`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC),
  CONSTRAINT `FK_municipality_user_username`
    FOREIGN KEY (`username`)
    REFERENCES `emergency_response_system`.`user` (`username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;




-- -----------------------------------------------------
-- Table `emergency_response_system`.`government_agency`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `emergency_response_system`.`government_agency` ;


CREATE TABLE IF NOT EXISTS `emergency_response_system`.`government_agency` (
  `username` VARCHAR(50) NOT NULL,
  `jurisdiction` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`username`),
  CONSTRAINT `FK_government_agency_user_username`
    FOREIGN KEY (`username`)
    REFERENCES `emergency_response_system`.`user` (`username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;




-- -----------------------------------------------------
-- Table `emergency_response_system`.`incident`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `emergency_response_system`.`incident` ;


CREATE TABLE IF NOT EXISTS `emergency_response_system`.`incident` (
  `incident_id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL,
  `description` VARCHAR(50) NOT NULL,
  `latitude` DECIMAL NOT NULL,
  `longitude` DECIMAL NOT NULL,
  `incident_date` DATETIME NOT NULL,
  PRIMARY KEY (`incident_id`),
  INDEX `FK_incident_user_idx` (`username` ASC),
  CONSTRAINT `FK_incident_user`
    FOREIGN KEY (`username`)
    REFERENCES `emergency_response_system`.`user` (`username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;




-- -----------------------------------------------------
-- Table `emergency_response_system`.`cost_time_period`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `emergency_response_system`.`cost_time_period` ;


CREATE TABLE IF NOT EXISTS `emergency_response_system`.`cost_time_period` (
  `cost_time_period_id` INT NOT NULL AUTO_INCREMENT,
  `time_period` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`cost_time_period_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `emergency_response_system`.`esf`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `emergency_response_system`.`esf` ;


CREATE TABLE IF NOT EXISTS `emergency_response_system`.`esf` (
  `esf_id` INT NOT NULL,
  `description` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`esf_id`))
ENGINE = InnoDB;






-- -----------------------------------------------------
-- Table `emergency_response_system`.`resource`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `emergency_response_system`.`resource` ;


CREATE TABLE IF NOT EXISTS `emergency_response_system`.`resource` (
  `resource_id` CHAR(16) NOT NULL,
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
    REFERENCES `emergency_response_system`.`esf` (`esf_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_resource_cost_time_period_id`
    FOREIGN KEY (`cost_time_period_id`)
    REFERENCES `emergency_response_system`.`cost_time_period` (`cost_time_period_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_resource_user`
    FOREIGN KEY (`username`)
    REFERENCES `emergency_response_system`.`user` (`username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;



-- -----------------------------------------------------
-- Table `emergency_response_system`.`resource_esf`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `emergency_response_system`.`resource_esf` ;


CREATE TABLE IF NOT EXISTS `emergency_response_system`.`resource_esf` (
  `resource_id` CHAR(16) NOT NULL,
  `esf_id` INT NOT NULL,
  PRIMARY KEY (`resource_id`, `esf_id`),
  INDEX `FK_resource_esf_esf_idx` (`esf_id` ASC),
  CONSTRAINT `FK_resource_esf_resource`
    FOREIGN KEY (`resource_id`)
    REFERENCES `emergency_response_system`.`resource` (`resource_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_resource_esf_esf`
    FOREIGN KEY (`esf_id`)
    REFERENCES `emergency_response_system`.`esf` (`esf_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `emergency_response_system`.`resource_request_status`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `emergency_response_system`.`resource_request_status` ;


CREATE TABLE IF NOT EXISTS `emergency_response_system`.`resource_request_status` (
  `resource_request_status_id` INT NOT NULL AUTO_INCREMENT,
  `status` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`resource_request_status_id`))
ENGINE = InnoDB;




-- -----------------------------------------------------
-- Table `emergency_response_system`.`resource_request`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `emergency_response_system`.`resource_request` ;


CREATE TABLE IF NOT EXISTS `emergency_response_system`.`resource_request` (
  `resource_request_id` INT NOT NULL AUTO_INCREMENT,
  `resource_request_status_id` INT NOT NULL,
  `incident_id` INT NOT NULL,
  `resource_id` CHAR(16) NOT NULL,
  `start_date` DATE NOT NULL,
  `return_by_date` DATE NOT NULL,
  PRIMARY KEY (`resource_request_id`),
  INDEX `FK_resource_request_resource_request_status_idx` (`resource_request_status_id` ASC),
  INDEX `FK_resource_request_incident_idx` (`incident_id` ASC),
  INDEX `FK_resource_request_resource_idx` (`resource_id` ASC),
  CONSTRAINT `FK_resource_request_resource_request_status`
    FOREIGN KEY (`resource_request_status_id`)
    REFERENCES `emergency_response_system`.`resource_request_status` (`resource_request_status_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_resource_request_incident`
    FOREIGN KEY (`incident_id`)
    REFERENCES `emergency_response_system`.`incident` (`incident_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_resource_request_resource`
    FOREIGN KEY (`resource_id`)
    REFERENCES `emergency_response_system`.`resource` (`resource_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `emergency_response_system`.`resource_repair`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `emergency_response_system`.`resource_repair` ;


CREATE TABLE IF NOT EXISTS `emergency_response_system`.`resource_repair` (
  `resource_repair_id` INT NOT NULL AUTO_INCREMENT,
  `resource_id` VARCHAR(45) NOT NULL,
  `status` VARCHAR(45) NOT NULL,
  `start_date` DATE NOT NULL,
  `ready_by_date` DATE NOT NULL,
  PRIMARY KEY (`resource_repair_id`),
  CONSTRAINT `FK_resource_resource_repair`
    FOREIGN KEY (`resource_id`)
    REFERENCES `emergency_response_system`.`resource` (`resource_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;





-- -----------------------------------------------------
-- Table `emergency_response_system`.`capability`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `emergency_response_system`.`capability` ;


CREATE TABLE IF NOT EXISTS `emergency_response_system`.`capability` (
  `resource_id` CHAR(16) NOT NULL,
  `capability` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`resource_id`, `capability`),
  CONSTRAINT `FK_resource_capability`
    FOREIGN KEY (`resource_id`)
    REFERENCES `emergency_response_system`.`resource` (`resource_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Data for table `emergency_response_system`.`cost_time_period`
-- -----------------------------------------------------
START TRANSACTION;
USE `emergency_response_system`;
INSERT INTO `emergency_response_system`.`cost_time_period` (`cost_time_period_id`, `time_period`) VALUES (1, 'Hour');
INSERT INTO `emergency_response_system`.`cost_time_period` (`cost_time_period_id`, `time_period`) VALUES (2, 'Day');
INSERT INTO `emergency_response_system`.`cost_time_period` (`cost_time_period_id`, `time_period`) VALUES (3, 'Week');


COMMIT;

-- -----------------------------------------------------
-- Data for table `emergency_response_system`.`resource_request_status`
-- -----------------------------------------------------
START TRANSACTION;
USE `emergency_response_system`;
INSERT INTO `emergency_response_system`.`resource_request_status` (`resource_request_status_id`, `status`) VALUES (1, 'New');
INSERT INTO `emergency_response_system`.`resource_request_status` (`resource_request_status_id`, `status`) VALUES (2, 'Deployed');
INSERT INTO `emergency_response_system`.`resource_request_status` (`resource_request_status_id`, `status`) VALUES (3, 'Rejected');
INSERT INTO `emergency_response_system`.`resource_request_status` (`resource_request_status_id`, `status`) VALUES (4, 'Returned');


COMMIT;




-- -----------------------------------------------------
-- Data for table `emergency_response_system`.`esf`
-- -----------------------------------------------------
START TRANSACTION;
USE `emergency_response_system`;
INSERT INTO `emergency_response_system`.`esf` (`esf_id`, `description`) VALUES (1, 'Transportation');
INSERT INTO `emergency_response_system`.`esf` (`esf_id`, `description`) VALUES (2, 'Communications');
INSERT INTO `emergency_response_system`.`esf` (`esf_id`, `description`) VALUES (3, 'Public Works and Engineering');
INSERT INTO `emergency_response_system`.`esf` (`esf_id`, `description`) VALUES (4, 'Firefighting');
INSERT INTO `emergency_response_system`.`esf` (`esf_id`, `description`) VALUES (5, 'Emergency Management');
INSERT INTO `emergency_response_system`.`esf` (`esf_id`, `description`) VALUES (6, 'Mass Care, Emergency Assistance, Housing, and Human Services');
INSERT INTO `emergency_response_system`.`esf` (`esf_id`, `description`) VALUES (7, 'Logistics Management and Resource Support');
INSERT INTO `emergency_response_system`.`esf` (`esf_id`, `description`) VALUES (8, 'Public Health and Medical Services');
INSERT INTO `emergency_response_system`.`esf` (`esf_id`, `description`) VALUES (9, 'Search and Rescue');
INSERT INTO `emergency_response_system`.`esf` (`esf_id`, `description`) VALUES (10, 'Oil and Hazardous Materials Response');
INSERT INTO `emergency_response_system`.`esf` (`esf_id`, `description`) VALUES (11, 'Agriculture and Natural Resources');
INSERT INTO `emergency_response_system`.`esf` (`esf_id`, `description`) VALUES (12, 'Energy');
INSERT INTO `emergency_response_system`.`esf` (`esf_id`, `description`) VALUES (13, 'Public Safety and Security');
INSERT INTO `emergency_response_system`.`esf` (`esf_id`, `description`) VALUES (14, 'Long-Term Community Recovery');
INSERT INTO `emergency_response_system`.`esf` (`esf_id`, `description`) VALUES (15, 'External Affairs');


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
