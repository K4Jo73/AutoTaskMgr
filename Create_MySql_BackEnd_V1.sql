-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema atm
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema atm
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `atm` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `atm` ;

-- -----------------------------------------------------
-- Table `atm`.`task_status`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `atm`.`task_status` (
  `status_id` INT NOT NULL AUTO_INCREMENT,
  `status_name` VARCHAR(100) NOT NULL,
  `status_desc` LONGTEXT NULL DEFAULT NULL,
  `status_active` TINYINT NOT NULL DEFAULT '1',
  `is_open` TINYINT NOT NULL DEFAULT '0',
  `is_hold` TINYINT NOT NULL DEFAULT '0',
  `is_error` TINYINT NOT NULL DEFAULT '0',
  `is_progress` TINYINT NOT NULL DEFAULT '0',
  PRIMARY KEY (`status_id`),
  UNIQUE INDEX `status_name_UNIQUE` (`status_name` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 10
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `atm`.`task_type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `atm`.`task_type` (
  `type_id` INT NOT NULL AUTO_INCREMENT,
  `type_name` VARCHAR(100) NOT NULL,
  `type_desc` LONGTEXT NULL DEFAULT NULL,
  `type_active` TINYINT NOT NULL DEFAULT '1',
  PRIMARY KEY (`type_id`),
  UNIQUE INDEX `type_name_UNIQUE` (`type_name` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `atm`.`task_queue`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `atm`.`task_queue` (
  `task_id` INT NOT NULL AUTO_INCREMENT,
  `batch_id` VARCHAR(45) NULL DEFAULT NULL,
  `created_on` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_on` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `note` VARCHAR(45) NULL DEFAULT NULL,
  `task_type` INT NOT NULL,
  `task_status` INT NOT NULL,
  `scheduled_for` DATETIME NULL DEFAULT NULL,
  `source_ref` VARCHAR(45) NULL DEFAULT NULL,
  `source_id` VARCHAR(45) NULL DEFAULT NULL,
  `closure_ref` VARCHAR(45) NULL DEFAULT NULL,
  `closure_id` VARCHAR(45) NULL DEFAULT NULL,
  `closed_on` DATETIME NULL DEFAULT NULL,
  `activity_param01` VARCHAR(150) NULL DEFAULT NULL,
  `activity_param02` VARCHAR(150) NULL DEFAULT NULL,
  PRIMARY KEY (`task_id`),
  INDEX `fk_tasktype_idx` (`task_type` ASC) VISIBLE,
  INDEX `fk_taskstatus_idx` (`task_status` ASC) VISIBLE,
  CONSTRAINT `fk_taskstatus`
    FOREIGN KEY (`task_status`)
    REFERENCES `atm`.`task_status` (`status_id`),
  CONSTRAINT `fk_tasktype`
    FOREIGN KEY (`task_type`)
    REFERENCES `atm`.`task_type` (`type_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 79
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

USE `atm` ;

-- -----------------------------------------------------
-- Placeholder table for view `atm`.`vw_tasks_active`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `atm`.`vw_tasks_active` (`task_id` INT, `status_name` INT, `type_name` INT, `created_on` INT, `updated_on` INT, `note` INT, `scheduled_for` INT, `source_ref` INT, `source_id` INT, `closure_ref` INT, `closure_id` INT, `closed_on` INT, `status_id` INT, `batch_id` INT);

-- -----------------------------------------------------
-- Placeholder table for view `atm`.`vw_tasks_closed`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `atm`.`vw_tasks_closed` (`task_id` INT, `status_name` INT, `type_name` INT, `created_on` INT, `updated_on` INT, `note` INT, `scheduled_for` INT, `source_ref` INT, `source_id` INT, `closure_ref` INT, `closure_id` INT, `closed_on` INT, `status_id` INT, `batch_id` INT);

-- -----------------------------------------------------
-- Placeholder table for view `atm`.`vw_tasks_error`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `atm`.`vw_tasks_error` (`task_id` INT, `status_name` INT, `type_name` INT, `created_on` INT, `updated_on` INT, `note` INT, `scheduled_for` INT, `source_ref` INT, `source_id` INT, `closure_ref` INT, `closure_id` INT, `closed_on` INT, `status_id` INT, `batch_id` INT);

-- -----------------------------------------------------
-- Placeholder table for view `atm`.`vw_tasks_hold`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `atm`.`vw_tasks_hold` (`task_id` INT, `status_name` INT, `type_name` INT, `created_on` INT, `updated_on` INT, `note` INT, `scheduled_for` INT, `source_ref` INT, `source_id` INT, `closure_ref` INT, `closure_id` INT, `closed_on` INT, `status_id` INT, `batch_id` INT);

-- -----------------------------------------------------
-- View `atm`.`vw_tasks_active`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `atm`.`vw_tasks_active`;
USE `atm`;
CREATE  OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `atm`.`vw_tasks_active` AS select `q`.`task_id` AS `task_id`,`s`.`status_name` AS `status_name`,`t`.`type_name` AS `type_name`,`q`.`created_on` AS `created_on`,`q`.`updated_on` AS `updated_on`,`q`.`note` AS `note`,`q`.`scheduled_for` AS `scheduled_for`,`q`.`source_ref` AS `source_ref`,`q`.`source_id` AS `source_id`,`q`.`closure_ref` AS `closure_ref`,`q`.`closure_id` AS `closure_id`,`q`.`closed_on` AS `closed_on`,`s`.`status_id` AS `status_id`,`q`.`batch_id` AS `batch_id` from ((`atm`.`task_queue` `q` join `atm`.`task_status` `s` on((`q`.`task_status` = `s`.`status_id`))) join `atm`.`task_type` `t` on((`q`.`task_type` = `t`.`type_id`))) where (`s`.`is_open` = 1);

-- -----------------------------------------------------
-- View `atm`.`vw_tasks_closed`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `atm`.`vw_tasks_closed`;
USE `atm`;
CREATE  OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `atm`.`vw_tasks_closed` AS select `q`.`task_id` AS `task_id`,`s`.`status_name` AS `status_name`,`t`.`type_name` AS `type_name`,`q`.`created_on` AS `created_on`,`q`.`updated_on` AS `updated_on`,`q`.`note` AS `note`,`q`.`scheduled_for` AS `scheduled_for`,`q`.`source_ref` AS `source_ref`,`q`.`source_id` AS `source_id`,`q`.`closure_ref` AS `closure_ref`,`q`.`closure_id` AS `closure_id`,`q`.`closed_on` AS `closed_on`,`s`.`status_id` AS `status_id`,`q`.`batch_id` AS `batch_id` from ((`atm`.`task_queue` `q` join `atm`.`task_status` `s` on((`q`.`task_status` = `s`.`status_id`))) join `atm`.`task_type` `t` on((`q`.`task_type` = `t`.`type_id`))) where (`s`.`is_open` = 0);

-- -----------------------------------------------------
-- View `atm`.`vw_tasks_error`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `atm`.`vw_tasks_error`;
USE `atm`;
CREATE  OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `atm`.`vw_tasks_error` AS select `q`.`task_id` AS `task_id`,`s`.`status_name` AS `status_name`,`t`.`type_name` AS `type_name`,`q`.`created_on` AS `created_on`,`q`.`updated_on` AS `updated_on`,`q`.`note` AS `note`,`q`.`scheduled_for` AS `scheduled_for`,`q`.`source_ref` AS `source_ref`,`q`.`source_id` AS `source_id`,`q`.`closure_ref` AS `closure_ref`,`q`.`closure_id` AS `closure_id`,`q`.`closed_on` AS `closed_on`,`s`.`status_id` AS `status_id`,`q`.`batch_id` AS `batch_id` from ((`atm`.`task_queue` `q` join `atm`.`task_status` `s` on((`q`.`task_status` = `s`.`status_id`))) join `atm`.`task_type` `t` on((`q`.`task_type` = `t`.`type_id`))) where (`s`.`is_error` = 1);

-- -----------------------------------------------------
-- View `atm`.`vw_tasks_hold`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `atm`.`vw_tasks_hold`;
USE `atm`;
CREATE  OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `atm`.`vw_tasks_hold` AS select `q`.`task_id` AS `task_id`,`s`.`status_name` AS `status_name`,`t`.`type_name` AS `type_name`,`q`.`created_on` AS `created_on`,`q`.`updated_on` AS `updated_on`,`q`.`note` AS `note`,`q`.`scheduled_for` AS `scheduled_for`,`q`.`source_ref` AS `source_ref`,`q`.`source_id` AS `source_id`,`q`.`closure_ref` AS `closure_ref`,`q`.`closure_id` AS `closure_id`,`q`.`closed_on` AS `closed_on`,`s`.`status_id` AS `status_id`,`q`.`batch_id` AS `batch_id` from ((`atm`.`task_queue` `q` join `atm`.`task_status` `s` on((`q`.`task_status` = `s`.`status_id`))) join `atm`.`task_type` `t` on((`q`.`task_type` = `t`.`type_id`))) where (`s`.`is_hold` = 1);

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
