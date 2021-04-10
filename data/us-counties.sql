.echo on
.headers on

-- Name: us-counties.sql
-- Author: Charles Carter
-- Date: April 5, 2021
-- Purpose: Creates table for us_counties.csv data file
-- Database: covidproj.db

drop table if exists us_counties;

create table us_counties (
    date text,
    county text,
    state text,
    fips integer,
    cases integer,
    deaths integer
);

.mode csv us_counties
.import --skip 1 us-counties.csv us_counties

drop index if exists us_counties_fips_idx;
create index if not exists us_counties_fips_idx on us_counties (fips);
drop index if exists us_counties_state_idx;
create index if not exists us_counties_state_idx on us_counties (fips);
drop index if exists us_counties_county_idx;
create index if not exists us_counties_county_idx on us_counties (fips);
