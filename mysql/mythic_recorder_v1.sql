--
-- mysql -u recorder -pbogus mythic_recorder_v1 < mythic_recorder_v1.sql
--
CREATE SCHEMA IF NOT EXISTS `mythic_recorder_v1` DEFAULT CHARACTER SET utf8;
USE `mythic_recorder_v1`;

DROP TABLE IF EXISTS `mythic_recorder_v1`.`task_log`;
CREATE TABLE IF NOT EXISTS `mythic_recorder_v1`.`task_log` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `time_stamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `command` VARCHAR(128) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC))
ENGINE = InnoDB;

DROP TABLE IF EXISTS `mythic_recorder_v1`.`application_log`;
CREATE TABLE IF NOT EXISTS `mythic_recorder_v1`.`application_log` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `time_stamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `task_id` BIGINT UNSIGNED NOT NULL,
  `level` INT NOT NULL,
  `facility` VARCHAR(32) NOT NULL,
  `event` VARCHAR(128) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC))
ENGINE = InnoDB;

DROP TABLE IF EXISTS `mythic_recorder_v1`.`exchange`;
CREATE TABLE IF NOT EXISTS `mythic_recorder_v1`.`exchange` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `creation_task_id` BIGINT UNSIGNED NOT NULL,
  `update_task_id` BIGINT UNSIGNED NOT NULL,
  `symbol` VARCHAR(32) NOT NULL,
  `name` VARCHAR(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `symbol_UNIQUE` (`symbol` ASC))
ENGINE = InnoDB;

DROP TABLE IF EXISTS `mythic_recorder_v1`.`file_stat`;
CREATE TABLE IF NOT EXISTS `mythic_recorder_v1`.`file_stat` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `creation_task_id` BIGINT UNSIGNED NOT NULL,
  `update_task_id` BIGINT UNSIGNED NOT NULL,
  `normalized_name` VARCHAR(64) NOT NULL,
  `file_size` BIGINT UNSIGNED NOT NULL,
  `sha1_hash` VARCHAR(48) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `normalized_name_UNIQUE` (`normalized_name` ASC))
ENGINE = InnoDB;

DROP TABLE IF EXISTS `mythic_recorder_v1`.`load_log`;
CREATE TABLE IF NOT EXISTS `mythic_recorder_v1`.`load_log` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `creation_task_id` BIGINT UNSIGNED NOT NULL,
  `update_task_id` BIGINT UNSIGNED NOT NULL,
  `exchange` VARCHAR(16) NOT NULL,
  `file_name` VARCHAR(32) NOT NULL,
  `normalized_name` VARCHAR(64) NOT NULL,
  `duplicate_pop` INT NOT NULL,
  `fail_pop` INT NOT NULL,
  `update_pop` INT NOT NULL,
  `total_pop` INT NOT NULL,
  `fresh_pop` INT NOT NULL,
  `stub_pop` INT NOT NULL,
  `complete_flag` TINYINT(1) NOT NULL,
  `duration` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  INDEX `ndx1` (`complete_flag` ASC, `file_name` ASC))
ENGINE = InnoDB;

DROP TABLE IF EXISTS `mythic_recorder_v1`.`load_log_summary`;
CREATE TABLE IF NOT EXISTS `mythic_recorder_v1`.`load_log_summary` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `time_stamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `task_id` BIGINT UNSIGNED NOT NULL,
  `total_file_pop` INT NOT NULL,
  `fresh_file_pop` INT NOT NULL,
  `update_file_pop` INT NOT NULL,
  `directory_pop` INT NOT NULL,
  `duration` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC))
ENGINE = InnoDB;

DROP TABLE IF EXISTS `mythic_recorder_v1`.`name`;
CREATE TABLE IF NOT EXISTS `mythic_recorder_v1`.`name` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `creation_task_id` BIGINT UNSIGNED NOT NULL,
  `update_task_id` BIGINT UNSIGNED NOT NULL,
  `exchange_id` BIGINT NOT NULL,
  `symbol` VARCHAR(32) NOT NULL,
  `name` VARCHAR(128) NOT NULL,
  `active_flag` TINYINT(1) NOT NULL,
  `put_call_flag` TINYINT(1) NOT NULL,
  `root_symbol_id` BIGINT NOT NULL,
  `expiration` DATE NOT NULL,
  `strike` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  INDEX `ndx1` (`symbol` ASC, `exchange_id` ASC))
ENGINE = InnoDB;

DROP TABLE IF EXISTS `mythic_recorder_v1`.`price_intraday`;
CREATE TABLE IF NOT EXISTS `mythic_recorder_v1`.`price_intraday` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `task_id` BIGINT UNSIGNED NOT NULL,
  `name_id` BIGINT UNSIGNED NOT NULL,
  `date` DATETIME NOT NULL,
  `open_price` BIGINT NOT NULL,
  `high_price` BIGINT NOT NULL,
  `low_price` BIGINT NOT NULL,
  `close_price` BIGINT NOT NULL,
  `volume` BIGINT NOT NULL,
  `open_interest` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `ndx1` (`name_id` ASC, `date` ASC))
ENGINE = InnoDB;

DROP TABLE IF EXISTS `mythic_recorder_v1`.`price_session`;
CREATE TABLE IF NOT EXISTS `mythic_recorder_v1`.`price_session` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `task_id` BIGINT UNSIGNED NOT NULL,
  `name_id` BIGINT UNSIGNED NOT NULL,
  `date` DATE NOT NULL,
  `open_price` BIGINT NOT NULL,
  `high_price` BIGINT NOT NULL,
  `low_price` BIGINT NOT NULL,
  `close_price` BIGINT NOT NULL,
  `volume` BIGINT NOT NULL,
  `open_interest` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `ndx1` (`name_id` ASC, `date` ASC))
ENGINE = InnoDB;



