.echo on
.headers on

-- Name: mask-use.sql
-- Author: Charles Carter
-- Date: April 7, 2021
-- Purpose: Creates table for mask_use.csv data file
-- Database: covidproj.db

drop table if exists mask_use;

--COUNTYFP,NEVER,RARELY,SOMETIMES,FREQUENTLY,ALWAYS

create table mask_use (
    COUNTYFP integer,
    NEVER real,
    RARELY real,
    SOMETIMES real,
    FREQUENTLY real,
    ALWAYS real
);

.mode csv mask_use
.import --skip 1 mask-use-by-county.csv mask_use

--drop index if exists us_counties_fips_idx;
--create index if not exists us_counties_fips_idx on us_counties (fips);
--drop index if exists us_counties_state_idx;
--create index if not exists us_counties_state_idx on us_counties (fips);
--drop index if exists us_counties_county_idx;
--create index if not exists us_counties_county_idx on us_counties (fips);
